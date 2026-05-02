import { createFileRoute, useParams } from "@tanstack/react-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import { toast } from "sonner";
import { CheckCircle2, AlertTriangle, Lightbulb, ShieldCheck, Download } from "lucide-react";
import { GlassCard } from "@/components/GlassCard";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useAuth } from "@/lib/auth-store";
import { diagnosesApi, getApiErrorMessage, type Diagnosis } from "@/lib/api";

export const Route = createFileRoute("/app/diagnoses/$id")({
  component: DiagnosisDetail,
});

function riskBadgeClass(level: string) {
  const l = level.toLowerCase();
  if (l.includes("high") || l.includes("crit"))
    return "bg-destructive/15 text-destructive border-destructive/25";
  if (l.includes("med") || l.includes("mod"))
    return "bg-warning/15 text-warning-foreground border-warning/25";
  return "bg-success/15 text-success-foreground border-success/25";
}

async function downloadPdf(d: Diagnosis) {
  const { jsPDF } = await import("jspdf");
  const doc = new jsPDF();
  const margin = 20;
  let y = margin;

  doc.setFontSize(18);
  doc.text("Respiratory CDSS — Diagnosis Report", margin, y);
  y += 12;

  doc.setFontSize(10);
  doc.setTextColor(120);
  doc.text(`Date: ${new Date(d.created_at).toLocaleString()}`, margin, y);
  y += 8;
  doc.text(`ID: ${d.id}`, margin, y);
  y += 12;

  doc.setTextColor(0);
  doc.setFontSize(14);
  doc.text("Predicted Condition", margin, y);
  y += 8;
  doc.setFontSize(12);
  doc.text(d.predicted_condition, margin, y);
  y += 10;

  doc.setFontSize(10);
  doc.text(`Confidence: ${(d.confidence_score * 100).toFixed(1)}%`, margin, y);
  y += 6;
  doc.text(`Risk Level: ${d.risk_level}`, margin, y);
  y += 6;
  doc.text(`Urgency: ${d.urgency_level}`, margin, y);
  y += 10;

  if (d.summary) {
    doc.setFontSize(14);
    doc.text("Summary", margin, y);
    y += 8;
    doc.setFontSize(10);
    const lines = doc.splitTextToSize(d.summary, 170);
    doc.text(lines, margin, y);
    y += lines.length * 5 + 6;
  }

  if (d.top_predictions?.length > 0) {
    doc.setFontSize(14);
    doc.text("Top Predictions", margin, y);
    y += 8;
    doc.setFontSize(10);
    for (const p of d.top_predictions) {
      const conf = (Number(p.confidence) * 100).toFixed(1);
      doc.text(`  ${p.disease}: ${conf}%`, margin, y);
      y += 6;
    }
    y += 4;
  }

  if (d.rule_engine_alerts?.length > 0) {
    doc.setFontSize(14);
    doc.text("Alerts", margin, y);
    y += 8;
    doc.setFontSize(10);
    for (const a of d.rule_engine_alerts) {
      const aLines = doc.splitTextToSize(`! ${a}`, 170);
      doc.text(aLines, margin, y);
      y += aLines.length * 5 + 2;
    }
    y += 4;
  }

  if (d.recommendations?.length > 0) {
    if (y > 250) { doc.addPage(); y = margin; }
    doc.setFontSize(14);
    doc.text("Recommendations", margin, y);
    y += 8;
    doc.setFontSize(10);
    for (const r of d.recommendations) {
      const rLines = doc.splitTextToSize(`- ${r}`, 170);
      doc.text(rLines, margin, y);
      y += rLines.length * 5 + 2;
    }
  }

  if (d.is_confirmed && d.confirmed_condition) {
    if (y > 250) { doc.addPage(); y = margin; }
    y += 6;
    doc.setFontSize(14);
    doc.text("Confirmed Diagnosis", margin, y);
    y += 8;
    doc.setFontSize(10);
    doc.text(d.confirmed_condition, margin, y);
    if (d.doctor_notes) {
      y += 6;
      const nLines = doc.splitTextToSize(`Notes: ${d.doctor_notes}`, 170);
      doc.text(nLines, margin, y);
    }
  }

  doc.save(`diagnosis-${d.id.slice(0, 8)}.pdf`);
}

function DiagnosisDetail() {
  const { t } = useTranslation();
  const { id } = useParams({ from: "/app/diagnoses/$id" });
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const { data: d } = useQuery<Diagnosis>({
    queryKey: ["diagnoses", id],
    queryFn: () => diagnosesApi.get(id),
  });
  const [confirmedCondition, setConfirmedCondition] = useState("");
  const [notes, setNotes] = useState("");
  const [confirming, setConfirming] = useState(false);
  const [initialized, setInitialized] = useState(false);

  if (d && !initialized) {
    setConfirmedCondition(d.confirmed_condition || d.predicted_condition);
    setNotes(d.doctor_notes || "");
    setInitialized(true);
  }

  async function confirm() {
    setConfirming(true);
    try {
      await diagnosesApi.confirm(id, {
        confirmed_condition: confirmedCondition,
        doctor_notes: notes,
      });
      queryClient.invalidateQueries({ queryKey: ["diagnoses", id] });
      toast.success(t("diagnosis.confirmed"));
    } catch (err: unknown) {
      toast.error(getApiErrorMessage(err, t("common.errorOccurred")));
    } finally {
      setConfirming(false);
    }
  }

  if (!d)
    return (
      <div className="max-w-4xl mx-auto space-y-4">
        <div className="space-y-2">
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-9 w-64" />
        </div>
        <div className="grid gap-3 sm:grid-cols-3">
          {[...Array(3)].map((_, i) => (
            <GlassCard key={i}>
              <Skeleton className="h-3 w-20 mb-2" />
              <Skeleton className="h-7 w-16" />
              <Skeleton className="h-2 w-full mt-3 rounded-full" />
            </GlassCard>
          ))}
        </div>
        <GlassCard>
          <Skeleton className="h-4 w-32 mb-3" />
          <Skeleton className="h-16 w-full" />
        </GlassCard>
      </div>
    );

  const canConfirm = user && (user.role === "doctor" || user.role === "admin");
  const confidencePct = d.confidence_score * 100;

  return (
    <div className="max-w-4xl mx-auto space-y-4">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <p className="text-xs uppercase tracking-wider text-muted-foreground">
            {t("diagnosis.predicted")}
          </p>
          <h1 className="text-3xl font-bold text-gradient">{d.predicted_condition}</h1>
        </div>
        <div className="flex items-center gap-2">
          {d.is_confirmed && (
            <span className="inline-flex items-center gap-1 text-xs px-3 py-1 rounded-full bg-success/20 text-success-foreground">
              <CheckCircle2 className="size-4" /> {t("diagnosis.confirmed")}
            </span>
          )}
          <Button
            variant="outline"
            size="sm"
            className="rounded-full"
            onClick={() => downloadPdf(d)}
          >
            <Download className="size-4 mr-1" />
            {t("diagnosis.downloadPdf")}
          </Button>
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        <GlassCard>
          <div className="text-xs uppercase tracking-wider text-muted-foreground">
            {t("diagnosis.confidence")}
          </div>
          <div className="text-2xl font-bold mt-1">{confidencePct.toFixed(1)}%</div>
          <div className="mt-2 h-2 rounded-full bg-muted overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-1000"
              style={{ width: `${confidencePct}%`, background: "var(--gradient-primary)" }}
            />
          </div>
        </GlassCard>
        <GlassCard>
          <div className="text-xs uppercase tracking-wider text-muted-foreground">
            {t("diagnosis.risk")}
          </div>
          <div className="flex items-center gap-2 mt-1">
            <div className="text-2xl font-bold capitalize">{d.risk_level}</div>
            <span className={`text-[10px] px-2 py-0.5 rounded-full border ${riskBadgeClass(d.risk_level)}`}>
              {d.risk_level}
            </span>
          </div>
        </GlassCard>
        <GlassCard>
          <div className="text-xs uppercase tracking-wider text-muted-foreground">
            {t("diagnosis.urgency")}
          </div>
          <div className="text-2xl font-bold mt-1 capitalize">{d.urgency_level}</div>
        </GlassCard>
      </div>

      {d.summary && (
        <GlassCard>
          <h3 className="font-semibold mb-2">{t("diagnosis.summary")}</h3>
          <p className="text-sm leading-relaxed">{d.summary}</p>
        </GlassCard>
      )}

      {d.top_predictions?.length > 0 && (
        <GlassCard>
          <h3 className="font-semibold mb-3">{t("diagnosis.top")}</h3>
          <ul className="space-y-2">
            {d.top_predictions.map((p, i) => {
              const cond = p.disease;
              const score = Math.max(0, Math.min(1, Number(p.confidence) || 0));
              return (
                <li key={i} className="flex items-center gap-3">
                  <div className="text-sm w-32 truncate">{cond}</div>
                  <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-700"
                      style={{ width: `${score * 100}%`, background: "var(--gradient-primary)" }}
                    />
                  </div>
                  <div className="text-xs tabular-nums w-12 text-right">
                    {(score * 100).toFixed(1)}%
                  </div>
                </li>
              );
            })}
          </ul>
        </GlassCard>
      )}

      {d.rule_engine_alerts?.length > 0 && (
        <GlassCard>
          <h3 className="font-semibold mb-2 flex items-center gap-2">
            <AlertTriangle className="size-4 text-warning" /> {t("diagnosis.alerts")}
          </h3>
          <ul className="space-y-1.5">
            {d.rule_engine_alerts.map((a, i) => (
              <li
                key={i}
                className="text-sm rounded-xl bg-warning/10 px-3 py-2 border border-warning/20"
              >
                {a}
              </li>
            ))}
          </ul>
        </GlassCard>
      )}

      {d.recommendations?.length > 0 && (
        <GlassCard>
          <h3 className="font-semibold mb-2 flex items-center gap-2">
            <Lightbulb className="size-4 text-secondary" /> {t("diagnosis.recommendations")}
          </h3>
          <ul className="space-y-1.5">
            {d.recommendations.map((r, i) => (
              <li
                key={i}
                className="text-sm rounded-xl bg-secondary/10 px-3 py-2 border border-secondary/20"
              >
                {r}
              </li>
            ))}
          </ul>
        </GlassCard>
      )}

      {canConfirm && !d.is_confirmed && (
        <GlassCard>
          <h3 className="font-semibold mb-3 flex items-center gap-2">
            <ShieldCheck className="size-4 text-primary" /> {t("diagnosis.confirmCta")}
          </h3>
          <div className="space-y-3">
            <div className="space-y-1.5">
              <Label>{t("diagnosis.confirmedCondition")}</Label>
              <Input
                value={confirmedCondition}
                onChange={(e) => setConfirmedCondition(e.target.value)}
                className="rounded-xl bg-background/40"
              />
            </div>
            <div className="space-y-1.5">
              <Label>{t("diagnosis.doctorNotes")}</Label>
              <Textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="rounded-xl bg-background/40"
              />
            </div>
            <Button onClick={confirm} disabled={confirming} className="rounded-full">
              {confirming ? t("common.loading") : t("common.confirm")}
            </Button>
          </div>
        </GlassCard>
      )}

      {d.is_confirmed && d.confirmed_condition && (
        <GlassCard>
          <div className="text-xs uppercase tracking-wider text-muted-foreground">
            {t("diagnosis.confirmedCondition")}
          </div>
          <div className="font-semibold mt-1">{d.confirmed_condition}</div>
          {d.doctor_notes && <p className="text-sm text-muted-foreground mt-2">{d.doctor_notes}</p>}
        </GlassCard>
      )}
    </div>
  );
}
