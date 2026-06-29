import { createFileRoute } from "@tanstack/react-router";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { toast } from "sonner";
import { RefreshCw } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { AuthGate } from "@/components/AuthGate";
import { GlassCard } from "@/components/GlassCard";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { adminApi, getApiErrorMessage } from "@/lib/api";

export const Route = createFileRoute("/app/admin/ml")({
  component: () => (
    <AuthGate roles={["admin"]}>
      <MLPage />
    </AuthGate>
  ),
});

interface EvalReport {
  overall_accuracy: number;
  mean_accuracy: number;
  folds: number;
  samples: number;
  per_label_accuracy: Record<string, number>;
  confusion_matrix: Record<string, Record<string, number>>;
  fold_results?: Array<{ fold: number; accuracy: number }>;
}

interface FeatureSignal {
  feature: string;
  value: string;
  lift_ratio: number;
  support_score: number;
}

interface ExplainReport {
  per_label: Record<
    string,
    {
      sample_count: number;
      prior_probability: number;
      top_feature_signals: FeatureSignal[];
    }
  >;
}

const CHART_COLORS = [
  "oklch(0.62 0.16 215)",
  "oklch(0.7 0.14 175)",
  "oklch(0.68 0.15 155)",
  "oklch(0.78 0.15 75)",
  "oklch(0.62 0.22 25)",
  "oklch(0.74 0.15 280)",
  "oklch(0.65 0.18 340)",
];

function MLPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { data: meta, isLoading } = useQuery<Record<string, unknown>>({
    queryKey: ["admin", "ml", "metadata"],
    queryFn: adminApi.modelMeta,
  });

  const retrainMutation = useMutation({
    mutationFn: adminApi.retrain,
    onSuccess: () => {
      toast.success("OK");
      queryClient.invalidateQueries({ queryKey: ["admin", "ml", "metadata"] });
    },
    onError: (err: unknown) => {
      toast.error(getApiErrorMessage(err, t("common.errorOccurred")));
    },
  });

  const evalReport = meta?.evaluation_report as EvalReport | undefined;
  const explainReport = meta?.explainability_report as ExplainReport | undefined;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{t("admin.ml")}</h1>
        <Button
          onClick={() => retrainMutation.mutate()}
          disabled={retrainMutation.isPending}
          className="rounded-full"
        >
          <RefreshCw className={`size-4 mr-1 ${retrainMutation.isPending ? "animate-spin" : ""}`} />{" "}
          {t("admin.retrain")}
        </Button>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          <GlassCard>
            <Skeleton className="h-32 w-full" />
          </GlassCard>
          <GlassCard>
            <Skeleton className="h-64 w-full" />
          </GlassCard>
        </div>
      ) : (
        <Tabs defaultValue="metrics">
          <TabsList className="rounded-xl bg-background/60 backdrop-blur">
            <TabsTrigger value="metrics" className="rounded-lg">
              {t("admin.overallAccuracy")}
            </TabsTrigger>
            <TabsTrigger value="features" className="rounded-lg">
              {t("admin.featureImportance")}
            </TabsTrigger>
            <TabsTrigger value="raw" className="rounded-lg">
              {t("admin.rawData")}
            </TabsTrigger>
          </TabsList>

          <TabsContent value="metrics" className="space-y-4 mt-4">
            {evalReport ? (
              <>
                {/* Overall accuracy */}
                <div className="grid gap-4 sm:grid-cols-3">
                  <GlassCard>
                    <div className="text-xs uppercase tracking-wider text-muted-foreground">
                      {t("admin.overallAccuracy")}
                    </div>
                    <div className="text-4xl font-bold mt-2 text-gradient">
                      {(evalReport.overall_accuracy * 100).toFixed(1)}%
                    </div>
                    <div className="mt-3 h-2 rounded-full bg-muted overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-1000"
                        style={{
                          width: `${evalReport.overall_accuracy * 100}%`,
                          background: "var(--gradient-primary)",
                        }}
                      />
                    </div>
                  </GlassCard>
                  <GlassCard>
                    <div className="text-xs uppercase tracking-wider text-muted-foreground">
                      Cross-validation folds
                    </div>
                    <div className="text-4xl font-bold mt-2">{evalReport.folds}</div>
                  </GlassCard>
                  <GlassCard>
                    <div className="text-xs uppercase tracking-wider text-muted-foreground">
                      {t("admin.totalRecords")}
                    </div>
                    <div className="text-4xl font-bold mt-2">{evalReport.samples}</div>
                  </GlassCard>
                </div>

                {/* Per-class accuracy */}
                <GlassCard>
                  <h3 className="font-semibold mb-4">{t("admin.perClassMetrics")}</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-border/50">
                          <th className="text-left py-2 px-3 text-muted-foreground font-medium">
                            {t("diagnosis.predicted")}
                          </th>
                          <th className="text-right py-2 px-3 text-muted-foreground font-medium">
                            {t("admin.accuracy")}
                          </th>
                          <th className="text-left py-2 px-3 text-muted-foreground font-medium w-1/3">
                            &nbsp;
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(evalReport.per_label_accuracy).map(([label, acc], i) => (
                          <tr key={label} className="border-b border-border/30">
                            <td className="py-2.5 px-3 font-medium">{label}</td>
                            <td className="py-2.5 px-3 text-right tabular-nums font-bold">
                              {(acc * 100).toFixed(1)}%
                            </td>
                            <td className="py-2.5 px-3">
                              <div className="h-2 rounded-full bg-muted overflow-hidden">
                                <div
                                  className="h-full rounded-full transition-all duration-700"
                                  style={{
                                    width: `${acc * 100}%`,
                                    backgroundColor: CHART_COLORS[i % CHART_COLORS.length],
                                  }}
                                />
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </GlassCard>

                {/* Confusion matrix */}
                <GlassCard>
                  <h3 className="font-semibold mb-4">{t("admin.confusionMatrix")}</h3>
                  <ConfusionMatrix matrix={evalReport.confusion_matrix} />
                </GlassCard>
              </>
            ) : (
              <GlassCard>
                <p className="text-center text-sm text-muted-foreground py-8">
                  {t("common.empty")}
                </p>
              </GlassCard>
            )}
          </TabsContent>

          <TabsContent value="features" className="space-y-4 mt-4">
            {explainReport ? (
              Object.entries(explainReport.per_label).map(([label, data]) => (
                <GlassCard key={label}>
                  <h3 className="font-semibold mb-1">{label}</h3>
                  <p className="text-xs text-muted-foreground mb-4">
                    Prior: {(data.prior_probability * 100).toFixed(1)}% · {t("admin.support")}:{" "}
                    {data.sample_count}
                  </p>
                  <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={data.top_feature_signals.map((s) => ({
                          name: `${s.feature}=${s.value}`,
                          lift: Number(s.lift_ratio.toFixed(1)),
                        }))}
                        layout="vertical"
                        margin={{ top: 0, right: 20, left: 0, bottom: 0 }}
                      >
                        <XAxis
                          type="number"
                          tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
                          axisLine={false}
                          tickLine={false}
                        />
                        <YAxis
                          type="category"
                          dataKey="name"
                          width={160}
                          tick={{ fontSize: 11, fill: "var(--muted-foreground)" }}
                          axisLine={false}
                          tickLine={false}
                        />
                        <Tooltip
                          contentStyle={{
                            background: "var(--glass-bg)",
                            backdropFilter: "blur(16px)",
                            border: "1px solid var(--glass-border)",
                            borderRadius: "12px",
                            fontSize: "12px",
                          }}
                          formatter={(v: number) => [`${v}x`, "Lift"]}
                        />
                        <Bar dataKey="lift" radius={[0, 6, 6, 0]}>
                          {data.top_feature_signals.map((_, i) => (
                            <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </GlassCard>
              ))
            ) : (
              <GlassCard>
                <p className="text-center text-sm text-muted-foreground py-8">
                  {t("common.empty")}
                </p>
              </GlassCard>
            )}
          </TabsContent>

          <TabsContent value="raw" className="mt-4">
            <GlassCard>
              <h3 className="font-semibold mb-2">{t("admin.modelMeta")}</h3>
              <pre className="text-xs whitespace-pre-wrap break-words bg-background/40 rounded-xl p-3 max-h-[60vh] overflow-auto">
                {JSON.stringify(meta, null, 2)}
              </pre>
            </GlassCard>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}

function ConfusionMatrix({ matrix }: { matrix: Record<string, Record<string, number>> }) {
  const labels = Object.keys(matrix);
  const maxVal = Math.max(...labels.flatMap((r) => labels.map((c) => matrix[r]?.[c] ?? 0)));

  return (
    <div className="overflow-x-auto">
      <table className="text-xs">
        <thead>
          <tr>
            <th className="py-1 px-2 text-muted-foreground" />
            {labels.map((l) => (
              <th
                key={l}
                className="py-1 px-2 text-muted-foreground font-medium text-center max-w-20 truncate"
                title={l}
              >
                {l.length > 12 ? l.slice(0, 10) + "…" : l}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {labels.map((actual) => (
            <tr key={actual}>
              <td
                className="py-1 px-2 font-medium text-muted-foreground text-right max-w-28 truncate"
                title={actual}
              >
                {actual.length > 15 ? actual.slice(0, 13) + "…" : actual}
              </td>
              {labels.map((predicted) => {
                const val = matrix[actual]?.[predicted] ?? 0;
                const intensity = maxVal > 0 ? val / maxVal : 0;
                const isDiag = actual === predicted;
                return (
                  <td
                    key={predicted}
                    className="py-1 px-2 text-center font-mono tabular-nums rounded"
                    style={{
                      backgroundColor: isDiag
                        ? `oklch(0.68 0.15 155 / ${0.15 + intensity * 0.6})`
                        : val > 0
                          ? `oklch(0.62 0.22 25 / ${0.15 + intensity * 0.5})`
                          : "transparent",
                    }}
                  >
                    {val || "·"}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
