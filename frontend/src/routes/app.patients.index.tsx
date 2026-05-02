import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { useEffect } from "react";
import { Plus, User as UserIcon } from "lucide-react";
import { GlassCard } from "@/components/GlassCard";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-store";
import { patientsApi, type Patient } from "@/lib/api";

export const Route = createFileRoute("/app/patients/")({
  component: PatientsList,
});

function PatientsList() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const navigate = useNavigate();
  const isPatient = user?.role === "patient";
  const { data: patients, isLoading } = useQuery<Patient[]>({
    queryKey: ["patients"],
    queryFn: patientsApi.list,
  });

  // Patient role: auto-redirect to their profile or to create one
  useEffect(() => {
    if (!isPatient || isLoading || !patients) return;
    if (patients.length > 0) {
      navigate({ to: "/app/patients/$id", params: { id: patients[0].id }, replace: true });
    } else {
      navigate({ to: "/app/patients/new", replace: true });
    }
  }, [isPatient, isLoading, patients, navigate]);

  // Patient sees loading while redirecting
  if (isPatient) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <GlassCard><Skeleton className="h-32 w-full" /></GlassCard>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{t("patients.title")}</h1>
          <p className="text-sm text-muted-foreground">{patients?.length ?? 0}</p>
        </div>
        <Button asChild className="rounded-full">
          <Link to="/app/patients/new">
            <Plus className="size-4 mr-1" /> {t("patients.new")}
          </Link>
        </Button>
      </div>

      {isLoading ? (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <GlassCard key={i}>
              <div className="flex items-center gap-3">
                <Skeleton className="size-11 rounded-2xl" />
                <div className="space-y-2 flex-1">
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-3 w-1/2" />
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      ) : !patients || patients.length === 0 ? (
        <GlassCard>
          <p className="text-center text-sm text-muted-foreground py-8">{t("common.empty")}</p>
        </GlassCard>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {patients.map((p) => (
            <Link key={p.id} to="/app/patients/$id" params={{ id: p.id }}>
              <GlassCard className="hover:-translate-y-0.5 cursor-pointer">
                <div className="flex items-center gap-3">
                  <div className="size-11 rounded-2xl bg-primary/15 text-primary flex items-center justify-center">
                    <UserIcon className="size-5" />
                  </div>
                  <div className="min-w-0">
                    <div className="font-medium truncate">{p.full_name}</div>
                    <div className="text-xs text-muted-foreground">
                      {p.gender === "male" ? t("patients.male") : t("patients.female")} ·{" "}
                      {p.date_of_birth}
                    </div>
                  </div>
                </div>
              </GlassCard>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
