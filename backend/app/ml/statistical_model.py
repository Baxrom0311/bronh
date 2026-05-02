from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from app.ml.features import FEATURE_NAMES


def split_samples(samples: list[dict[str, str]], train_ratio: float = 0.8, seed: int = 42) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    shuffled = list(samples)
    random.Random(seed).shuffle(shuffled)
    train_size = max(1, int(len(shuffled) * train_ratio))
    return shuffled[:train_size], shuffled[train_size:]


def split_samples_by_ids(
    samples: list[dict[str, str]],
    train_ids: Iterable[str],
    test_ids: Iterable[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    sample_map = {sample["sample_id"]: sample for sample in samples}
    train_samples = [sample_map[sample_id] for sample_id in train_ids if sample_id in sample_map]
    test_samples = [sample_map[sample_id] for sample_id in test_ids if sample_id in sample_map]
    return train_samples, test_samples


def train_naive_bayes(samples: list[dict[str, str]]) -> dict[str, Any]:
    labels = sorted({sample["label"] for sample in samples})
    label_counts = {label: 0 for label in labels}
    feature_value_counts = {
        feature: {label: defaultdict(int) for label in labels}
        for feature in FEATURE_NAMES
    }
    feature_vocab = {feature: set() for feature in FEATURE_NAMES}

    for sample in samples:
        label = sample["label"]
        label_counts[label] += 1
        for feature in FEATURE_NAMES:
            value = sample[feature]
            feature_value_counts[feature][label][value] += 1
            feature_vocab[feature].add(value)

    serializable_counts = {
        feature: {
            label: dict(values)
            for label, values in per_label.items()
        }
        for feature, per_label in feature_value_counts.items()
    }
    serializable_vocab = {
        feature: sorted(values)
        for feature, values in feature_vocab.items()
    }

    return {
        "model_type": "categorical_naive_bayes",
        "version": 1,
        "feature_names": list(FEATURE_NAMES),
        "labels": labels,
        "label_counts": label_counts,
        "feature_value_counts": serializable_counts,
        "feature_vocab": serializable_vocab,
        "sample_count": len(samples),
    }


def _log_prior(label_counts: dict[str, int], labels: list[str], label: str) -> float:
    total_count = sum(label_counts.values())
    return math.log((label_counts[label] + 1) / (total_count + len(labels)))


def _log_likelihood(artifact: dict[str, Any], label: str, feature: str, value: str) -> float:
    label_count = artifact["label_counts"][label]
    vocab = artifact["feature_vocab"][feature]
    vocab_size = len(vocab) + 1
    value_counts = artifact["feature_value_counts"][feature][label]
    count = value_counts.get(value, 0)
    return math.log((count + 1) / (label_count + vocab_size))


def predict_probabilities(artifact: dict[str, Any], feature_vector: dict[str, str]) -> list[tuple[str, float]]:
    label_counts: dict[str, int] = artifact["label_counts"]
    labels: list[str] = artifact["labels"]
    scores: dict[str, float] = {}

    for label in labels:
        score = _log_prior(label_counts, labels, label)
        for feature in artifact["feature_names"]:
            value = feature_vector.get(feature, "unknown")
            score += _log_likelihood(artifact, label, feature, value)
        scores[label] = score

    max_score = max(scores.values())
    exp_scores = {label: math.exp(score - max_score) for label, score in scores.items()}
    total_exp = sum(exp_scores.values()) or 1.0

    ranked = sorted(
        ((label, value / total_exp) for label, value in exp_scores.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked


def explain_prediction(
    artifact: dict[str, Any],
    feature_vector: dict[str, str],
    top_n: int = 5,
) -> dict[str, Any]:
    ranked = predict_probabilities(artifact, feature_vector)
    predicted_label, predicted_confidence = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None
    runner_up_label = runner_up[0] if runner_up is not None else None
    runner_up_confidence = runner_up[1] if runner_up is not None else None
    labels: list[str] = artifact["labels"]
    label_counts: dict[str, int] = artifact["label_counts"]

    supporting_features: list[dict[str, Any]] = []
    counter_features: list[dict[str, Any]] = []
    for feature in artifact["feature_names"]:
        value = feature_vector.get(feature, "unknown")
        predicted_support = _log_likelihood(artifact, predicted_label, feature, value)
        runner_up_support = (
            _log_likelihood(artifact, runner_up_label, feature, value)
            if runner_up_label is not None
            else predicted_support
        )
        support_score = round(predicted_support - runner_up_support, 3)
        feature_result = {
            "feature": feature,
            "value": value,
            "support_score": support_score,
            "predicted_support": round(predicted_support, 3),
            "runner_up_support": round(runner_up_support, 3),
        }
        if support_score >= 0:
            supporting_features.append(feature_result)
        else:
            counter_features.append(feature_result)

    supporting_features.sort(key=lambda item: item["support_score"], reverse=True)
    counter_features.sort(key=lambda item: item["support_score"])

    prior_delta = None
    if runner_up_label is not None:
        prior_delta = round(
            _log_prior(label_counts, labels, predicted_label)
            - _log_prior(label_counts, labels, runner_up_label),
            3,
        )

    return {
        "predicted_label": predicted_label,
        "predicted_confidence": round(predicted_confidence, 3),
        "runner_up_label": runner_up_label,
        "runner_up_confidence": round(runner_up_confidence, 3) if runner_up_confidence is not None else None,
        "prior_delta_vs_runner_up": prior_delta,
        "top_supporting_features": supporting_features[:top_n],
        "top_counter_features": counter_features[:top_n],
    }


def evaluate_artifact(artifact: dict[str, Any], samples: list[dict[str, str]]) -> dict[str, Any]:
    if not samples:
        return {
            "accuracy": 1.0,
            "tested_samples": 0,
            "per_label_accuracy": {},
            "confusion_matrix": {},
        }

    correct = 0
    per_label_total: dict[str, int] = defaultdict(int)
    per_label_correct: dict[str, int] = defaultdict(int)
    confusion_matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for sample in samples:
        expected = sample["label"]
        features = {feature: sample[feature] for feature in FEATURE_NAMES}
        predicted = predict_probabilities(artifact, features)[0][0]
        per_label_total[expected] += 1
        confusion_matrix[expected][predicted] += 1
        if predicted == expected:
            correct += 1
            per_label_correct[expected] += 1

    return {
        "accuracy": round(correct / len(samples), 3),
        "tested_samples": len(samples),
        "per_label_accuracy": {
            label: round(per_label_correct[label] / total, 3)
            for label, total in sorted(per_label_total.items())
        },
        "confusion_matrix": {
            label: dict(sorted(predictions.items()))
            for label, predictions in sorted(confusion_matrix.items())
        },
    }


def cross_validate_naive_bayes(
    samples: list[dict[str, str]],
    folds: int = 5,
    seed: int = 42,
) -> dict[str, Any]:
    if not samples:
        return {
            "folds": 0,
            "samples": 0,
            "mean_accuracy": 1.0,
            "overall_accuracy": 1.0,
            "fold_results": [],
            "per_label_accuracy": {},
            "confusion_matrix": {},
        }

    if len(samples) == 1:
        label = samples[0]["label"]
        return {
            "folds": 1,
            "samples": 1,
            "mean_accuracy": 1.0,
            "overall_accuracy": 1.0,
            "fold_results": [
                {
                    "fold": 1,
                    "train_samples": 1,
                    "test_samples": 1,
                    "accuracy": 1.0,
                }
            ],
            "per_label_accuracy": {label: 1.0},
            "confusion_matrix": {label: {label: 1}},
        }

    fold_count = max(2, min(folds, len(samples)))
    partitions: list[list[dict[str, str]]] = [[] for _ in range(fold_count)]
    samples_by_label: dict[str, list[dict[str, str]]] = defaultdict(list)
    for sample in samples:
        samples_by_label[sample["label"]].append(sample)

    randomizer = random.Random(seed)
    for label_index, label in enumerate(sorted(samples_by_label)):
        label_samples = samples_by_label[label]
        randomizer.shuffle(label_samples)
        start_offset = label_index % fold_count
        for index, sample in enumerate(label_samples):
            partitions[(start_offset + index) % fold_count].append(sample)

    partitions = [partition for partition in partitions if partition]
    if len(partitions) < 2:
        artifact = train_naive_bayes(samples)
        metrics = evaluate_artifact(artifact, samples)
        return {
            "folds": 1,
            "samples": len(samples),
            "mean_accuracy": metrics["accuracy"],
            "overall_accuracy": metrics["accuracy"],
            "fold_results": [
                {
                    "fold": 1,
                    "train_samples": len(samples),
                    "test_samples": len(samples),
                    "accuracy": metrics["accuracy"],
                }
            ],
            "per_label_accuracy": metrics["per_label_accuracy"],
            "confusion_matrix": metrics["confusion_matrix"],
        }

    fold_results: list[dict[str, Any]] = []
    total_correct = 0
    total_tested = 0
    per_label_total: dict[str, int] = defaultdict(int)
    per_label_correct: dict[str, int] = defaultdict(int)
    confusion_matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for fold_index, test_samples in enumerate(partitions, start=1):
        train_samples = [
            sample
            for partition_index, partition in enumerate(partitions, start=1)
            if partition_index != fold_index
            for sample in partition
        ]
        if not train_samples or not test_samples:
            continue

        artifact = train_naive_bayes(train_samples)
        metrics = evaluate_artifact(artifact, test_samples)
        fold_results.append(
            {
                "fold": fold_index,
                "train_samples": len(train_samples),
                "test_samples": len(test_samples),
                "accuracy": metrics["accuracy"],
            }
        )

        for expected_label, predicted_counts in metrics["confusion_matrix"].items():
            label_total = 0
            for predicted_label, count in predicted_counts.items():
                confusion_matrix[expected_label][predicted_label] += count
                label_total += count
                if expected_label == predicted_label:
                    total_correct += count
                    per_label_correct[expected_label] += count
            total_tested += label_total
            per_label_total[expected_label] += label_total

    mean_accuracy = sum(result["accuracy"] for result in fold_results) / len(fold_results)
    overall_accuracy = total_correct / total_tested if total_tested else 1.0
    return {
        "folds": fold_count,
        "samples": len(samples),
        "mean_accuracy": round(mean_accuracy, 3),
        "overall_accuracy": round(overall_accuracy, 3),
        "fold_results": fold_results,
        "per_label_accuracy": {
            label: round(per_label_correct[label] / total, 3)
            for label, total in sorted(per_label_total.items())
        },
        "confusion_matrix": {
            label: dict(sorted(predictions.items()))
            for label, predictions in sorted(confusion_matrix.items())
        },
    }


def save_artifact(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, indent=2, ensure_ascii=True), encoding="utf-8")


def load_artifact(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
