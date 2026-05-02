import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { Users, User as UserIcon, Stethoscope, BrainCircuit, ShieldCheck, ArrowRight, ClipboardPlus, FileSearch } from "lucide-react";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { GlassCard } from "@/components/GlassCard";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuth } from "@/lib/auth-store";
import { cn } from "@/lib/utils";
import {
  adminApi,
  diagnosesApi,
  patientsApi,
  symptomsApi,
  type AdminStats,
  type Diagnosis,
  type Patient,
  type SymptomRecord,
} from "@/lib/api";

export const Route = createFileRoute("/app/")({
  component: Dashboard,
});

const CHART_COLORS = [
  "oklch(0.62 0.16 215)",
  "oklch(0.7 0.14 175)",
  "oklch(0.68 0.15 155)",
  "oklch(0.78 0.15 75)",
  "oklch(0.62 0.22 25)",
  "oklch(0.74 0.15 280)",
  "oklch(0.65 0.18 340)",
];

function groupBy<T>(arr: T[], keyFn: (item: T) => string) {
  const map: Record<string, number> = {};
  for (const item of arr) {
    const key = keyFn(item);
    map[key] = (map[key] || 0) + 1;
  }
  return Object.entries(map).map(([name, value]) => ({ name, value }));
}

function Dashboard() {
  const { t } = useTranslation();
  const { user } = useAuth();

  const { data: patients, isLoading: pLoading } = useQuery<Patient[]>({
    queryKey: ["patients"],
    queryFn: patientsApi.list,
  });
  const { data: symptoms, isLoading: sLoading } = useQuery<SymptomRecord[]>({
    queryKey: ["symptoms"],
    queryFn: symptomsApi.list,
  });
  const { data: diagnoses, isLoading: dLoading } = useQuery<Diagnosis[]>({
    queryKey: ["diagnoses"],
    queryFn: diagnosesApi.history,
  });
  const { data: adminStats } = useQuery<AdminStats>({
    queryKey: ["admin", "stats"],
    queryFn: adminApi.stats,
    enabled: user?.role === "admin",
  });

  const recent = diagnoses?.slice(0, 5) ?? [];
  const diseaseData = diagnoses ? groupBy(diagnoses, (d) => d.predicted_condition) : [];
  const riskData = diagnoses ? groupBy(diagnoses, (d) => d.risk_level) : [];

  const isPatient = user?.role === "patient";

  const tiles = isPatient
    ? [
        {
          label: t("nav.myProfile"),
          value: patients?.length ?? 0,
          icon: UserIcon,
          to: "/app/patients",
          color: "from-sky-400 to-blue-500",
          loading: pLoading,
        },
        {
          label: t("nav.mySymptoms"),
          value: symptoms?.length ?? 0,
          icon: Stethoscope,
          to: "/app/symptoms",
          color: "from-teal-400 to-emerald-500",
          loading: sLoading,
        },
        {
          label: t("nav.myHistory"),
          value: diagnoses?.length ?? 0,
          icon: BrainCircuit,
          to: "/app/diagnoses",
          color: "from-violet-400 to-fuchsia-500",
          loading: dLoading,
        },
      ]
    : [
        {
          label: t("nav.patients"),
          value: patients?.length ?? 0,
          icon: Users,
          to: "/app/patients",
          color: "from-sky-400 to-blue-500",
          loading: pLoading,
        },
        {
          label: t("symptoms.title"),
          value: symptoms?.length ?? 0,
          icon: Stethoscope,
          to: "/app/symptoms",
          color: "from-teal-400 to-emerald-500",
          loading: sLoading,
        },
        {
          label: t("diagnosis.history"),
          value: diagnoses?.length ?? 0,
          icon: BrainCircuit,
          to: "/app/diagnoses",
          color: "from-violet-400 to-fuchsia-500",
          loading: dLoading,
        },
      ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl lg:text-3xl font-bold">
          {t("auth.welcomeBack")},{" "}
          <span className="text-gradient">{user?.full_name?.split(" ")[0]}</span>
        </h1>
        <p className="text-muted-foreground text-sm mt-1">{t("app.tagline")}</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {tiles.map((tile) => (
          <Link key={tile.label} to={tile.to}>
            <GlassCard className="hover:-translate-y-0.5 cursor-pointer transition-transform">
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-xs uppercase tracking-wider text-muted-foreground">
                    {tile.label}
                  </div>
                  {tile.loading ? (
                    <Skeleton className="h-9 w-16 mt-2" />
                  ) : (
                    <div className="text-3xl font-bold mt-2">{tile.value}</div>
                  )}
                </div>
                <div
                  className={`size-11 rounded-2xl bg-gradient-to-br ${tile.color} flex items-center justify-center shadow-lg`}
                >
                  <tile.icon className="size-5 text-white" />
                </div>
              </div>
              <div className="mt-4 text-xs text-primary inline-flex items-center gap-1">
                {t("common.view")} <ArrowRight className="size-3" />
              </div>
            </GlassCard>
          </Link>
        ))}
      </div>

      {/* Patient onboarding steps */}
      {isPatient && !pLoading && !sLoading && !dLoading && (
        <GlassCard>
          <h2 className="font-semibold mb-4">{t("app.tagline")}</h2>
          <div className="grid gap-3 sm:grid-cols-3">
            <Link to="/app/patients/new">
              <div className={cn(
                "rounded-2xl border p-4 transition-all hover:-translate-y-0.5",
                (patients?.length ?? 0) > 0
                  ? "border-primary/30 bg-primary/5"
                  : "border-border/50 bg-background/40"
              )}>
                <div className={cn(
                  "size-10 rounded-xl flex items-center justify-center mb-3",
                  (patients?.length ?? 0) > 0 ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"
                )}>
                  <UserIcon className="size-5" />
                </div>
                <div className="font-medium text-sm">{t("dashboard.createProfile")}</div>
                <div className="text-xs text-muted-foreground mt-1">{t("dashboard.createProfileDesc")}</div>
                {(patients?.length ?? 0) > 0 && <div className="text-xs text-primary mt-2">&#10003;</div>}
              </div>
            </Link>
            <Link to="/app/symptoms/new">
              <div className={cn(
                "rounded-2xl border p-4 transition-all hover:-translate-y-0.5",
                (symptoms?.length ?? 0) > 0
                  ? "border-primary/30 bg-primary/5"
                  : "border-border/50 bg-background/40"
              )}>
                <div className={cn(
                  "size-10 rounded-xl flex items-center justify-center mb-3",
                  (symptoms?.length ?? 0) > 0 ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"
                )}>
                  <ClipboardPlus className="size-5" />
                </div>
                <div className="font-medium text-sm">{t("dashboard.addSymptoms")}</div>
                <div className="text-xs text-muted-foreground mt-1">{t("dashboard.addSymptomsDesc")}</div>
                {(symptoms?.length ?? 0) > 0 && <div className="text-xs text-primary mt-2">&#10003;</div>}
              </div>
            </Link>
            <Link to="/app/diagnoses">
              <div className={cn(
                "rounded-2xl border p-4 transition-all hover:-translate-y-0.5",
                (diagnoses?.length ?? 0) > 0
                  ? "border-primary/30 bg-primary/5"
                  : "border-border/50 bg-background/40"
              )}>
                <div className={cn(
                  "size-10 rounded-xl flex items-center justify-center mb-3",
                  (diagnoses?.length ?? 0) > 0 ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"
                )}>
                  <FileSearch className="size-5" />
                </div>
                <div className="font-medium text-sm">{t("dashboard.viewResults")}</div>
                <div className="text-xs text-muted-foreground mt-1">{t("dashboard.viewResultsDesc")}</div>
                {(diagnoses?.length ?? 0) > 0 && <div className="text-xs text-primary mt-2">&#10003;</div>}
              </div>
            </Link>
          </div>
        </GlassCard>
      )}

      {user?.role === "admin" && adminStats && (
        <GlassCard>
          <div className="flex items-center gap-2 mb-4">
            <ShieldCheck className="size-5 text-primary" />
            <h2 className="font-semibold">{t("admin.stats")}</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <Stat label={t("admin.totalUsers")} value={adminStats.total_users} />
            <Stat label={t("admin.totalPatients")} value={adminStats.total_patients} />
            <Stat label={t("admin.totalRecords")} value={adminStats.total_symptom_records} />
            <Stat label={t("admin.totalDiagnoses")} value={adminStats.total_diagnoses} />
            <Stat label={t("admin.confirmed")} value={adminStats.confirmed_diagnoses} />
          </div>
        </GlassCard>
      )}

      {/* Charts row */}
      {diagnoses && diagnoses.length > 0 && (
        <div className="grid gap-4 lg:grid-cols-2">
          <GlassCard>
            <h3 className="font-semibold mb-4">{t("dashboard.diseaseDistribution")}</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={diseaseData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={90}
                    paddingAngle={3}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    labelLine={false}
                  >
                    {diseaseData.map((_, i) => (
                      <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: "var(--glass-bg)",
                      backdropFilter: "blur(16px)",
                      border: "1px solid var(--glass-border)",
                      borderRadius: "12px",
                      fontSize: "12px",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>

          <GlassCard>
            <h3 className="font-semibold mb-4">{t("dashboard.riskDistribution")}</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={riskData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <XAxis
                    dataKey="name"
                    tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    allowDecimals={false}
                    tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
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
                  />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {riskData.map((_, i) => (
                      <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>
        </div>
      )}

      <GlassCard>
        <h2 className="font-semibold mb-4">{t("dashboard.recentDiagnoses")}</h2>
        {dLoading ? (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="flex items-center justify-between py-3">
                <div className="space-y-2">
                  <Skeleton className="h-4 w-32" />
                  <Skeleton className="h-3 w-48" />
                </div>
                <Skeleton className="h-4 w-12" />
              </div>
            ))}
          </div>
        ) : recent.length === 0 ? (
          <p className="text-sm text-muted-foreground py-8 text-center">{t("common.empty")}</p>
        ) : (
          <ul className="divide-y divide-border/50">
            {recent.map((d) => (
              <li key={d.id} className="py-3 flex items-center justify-between">
                <div>
                  <div className="font-medium">{d.predicted_condition}</div>
                  <div className="text-xs text-muted-foreground">
                    {(d.confidence_score * 100).toFixed(1)}% · {d.risk_level} · {d.urgency_level}
                  </div>
                </div>
                <Link
                  to="/app/diagnoses/$id"
                  params={{ id: d.id }}
                  className="text-xs text-primary hover:underline"
                >
                  {t("common.view")}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </GlassCard>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl bg-background/40 p-3">
      <div className="text-xs text-muted-foreground">{label}</div>
      <div className="text-xl font-bold mt-1">{value}</div>
    </div>
  );
}
