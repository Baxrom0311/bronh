import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { Users, Stethoscope, BrainCircuit, CheckCircle2, ClipboardList } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { AuthGate } from "@/components/AuthGate";
import { GlassCard } from "@/components/GlassCard";
import { Skeleton } from "@/components/ui/skeleton";
import { adminApi, type AdminStats } from "@/lib/api";

export const Route = createFileRoute("/app/admin/")({
  component: () => (
    <AuthGate roles={["admin"]}>
      <AdminStatsPage />
    </AuthGate>
  ),
});

const ROLE_COLORS: Record<string, string> = {
  admin: "oklch(0.62 0.22 25)",
  doctor: "oklch(0.62 0.16 215)",
  patient: "oklch(0.7 0.14 175)",
};

function AdminStatsPage() {
  const { t } = useTranslation();
  const { data: stats } = useQuery<AdminStats>({
    queryKey: ["admin", "stats"],
    queryFn: adminApi.stats,
  });

  if (!stats)
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {[...Array(5)].map((_, i) => (
            <GlassCard key={i}>
              <Skeleton className="h-3 w-20 mb-2" />
              <Skeleton className="h-8 w-12" />
            </GlassCard>
          ))}
        </div>
      </div>
    );

  const tiles = [
    {
      label: t("admin.totalUsers"),
      value: stats.total_users,
      icon: Users,
      color: "from-sky-400 to-blue-500",
    },
    {
      label: t("admin.totalPatients"),
      value: stats.total_patients,
      icon: Stethoscope,
      color: "from-teal-400 to-emerald-500",
    },
    {
      label: t("admin.totalRecords"),
      value: stats.total_symptom_records,
      icon: ClipboardList,
      color: "from-amber-400 to-orange-500",
    },
    {
      label: t("admin.totalDiagnoses"),
      value: stats.total_diagnoses,
      icon: BrainCircuit,
      color: "from-violet-400 to-fuchsia-500",
    },
    {
      label: t("admin.confirmed"),
      value: stats.confirmed_diagnoses,
      icon: CheckCircle2,
      color: "from-emerald-400 to-green-500",
    },
  ];

  const roleData = Object.entries(stats.users_by_role).map(([role, count]) => ({
    name: t(`roles.${role}`, { defaultValue: role }),
    value: count,
    color: ROLE_COLORS[role] || "oklch(0.68 0.15 155)",
  }));

  const confirmRate =
    stats.total_diagnoses > 0
      ? Math.round((stats.confirmed_diagnoses / stats.total_diagnoses) * 100)
      : 0;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">{t("admin.stats")}</h1>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {tiles.map((tile) => (
          <GlassCard key={tile.label}>
            <div className="flex items-start justify-between">
              <div>
                <div className="text-xs uppercase tracking-wider text-muted-foreground">
                  {tile.label}
                </div>
                <div className="text-3xl font-bold mt-2">{tile.value}</div>
              </div>
              <div
                className={`size-10 rounded-2xl bg-gradient-to-br ${tile.color} flex items-center justify-center shadow-lg`}
              >
                <tile.icon className="size-4 text-white" />
              </div>
            </div>
          </GlassCard>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <GlassCard>
          <h3 className="font-semibold mb-3">{t("admin.byRole")}</h3>
          {roleData.length > 0 ? (
            <div className="flex items-center gap-6">
              <div className="h-48 w-48 shrink-0">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={roleData}
                      cx="50%"
                      cy="50%"
                      innerRadius={35}
                      outerRadius={70}
                      paddingAngle={3}
                      dataKey="value"
                    >
                      {roleData.map((d, i) => (
                        <Cell key={i} fill={d.color} />
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
              <div className="space-y-3">
                {roleData.map((d) => (
                  <div key={d.name} className="flex items-center gap-2">
                    <div className="size-3 rounded-full" style={{ background: d.color }} />
                    <span className="text-sm">{d.name}</span>
                    <span className="text-sm font-bold ml-auto">{d.value}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">{t("common.empty")}</p>
          )}
        </GlassCard>

        <GlassCard>
          <h3 className="font-semibold mb-3">{t("admin.confirmationRate")}</h3>
          <div className="flex items-center justify-center py-6">
            <div className="relative size-36">
              <svg viewBox="0 0 100 100" className="size-full -rotate-90">
                <circle cx="50" cy="50" r="42" fill="none" stroke="var(--muted)" strokeWidth="8" />
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  fill="none"
                  stroke="var(--primary)"
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={`${confirmRate * 2.64} 264`}
                  className="transition-all duration-1000"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl font-bold">{confirmRate}%</span>
              </div>
            </div>
          </div>
          <p className="text-center text-sm text-muted-foreground">
            {stats.confirmed_diagnoses} / {stats.total_diagnoses}
          </p>
        </GlassCard>
      </div>
    </div>
  );
}
