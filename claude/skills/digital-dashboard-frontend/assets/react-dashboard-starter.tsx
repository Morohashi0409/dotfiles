import type { PropsWithChildren, ReactNode } from "react";

import type { DashboardThemeName } from "./dashboard-tokens";

export type DashboardMeta = {
  source: string;
  updatedAt: string;
  asOf?: string;
  note?: string;
};

type DashboardPageProps = PropsWithChildren<{
  title: string;
  lead?: string;
  theme?: DashboardThemeName;
  filters?: ReactNode;
  metrics?: ReactNode;
  meta?: DashboardMeta;
}>;

export function DashboardPage({
  title,
  lead,
  theme = "blue",
  filters,
  metrics,
  meta,
  children,
}: DashboardPageProps) {
  return (
    <section className="dashboard-page" data-dashboard-theme={theme}>
      <div className="dashboard-shell">
        <header className="dashboard-header">
          <h1 className="dashboard-title">{title}</h1>
          {lead ? <p className="dashboard-lead">{lead}</p> : null}
        </header>
        {filters ? <div className="dashboard-filter-bar">{filters}</div> : null}
        {metrics ? <div className="dashboard-metric-grid">{metrics}</div> : null}
        <div className="dashboard-chart-grid">{children}</div>
        {meta ? <DashboardMetaBlock meta={meta} /> : null}
      </div>
    </section>
  );
}

export function MetricCard({
  label,
  value,
  support,
  delta,
}: {
  label: string;
  value: ReactNode;
  support?: ReactNode;
  delta?: ReactNode;
}) {
  return (
    <article className="dashboard-metric-card">
      <div className="dashboard-metric-label">{label}</div>
      <div className="dashboard-metric-value">{value}</div>
      {support ? <div className="dashboard-metric-support">{support}</div> : null}
      {delta ? <div className="dashboard-metric-delta">{delta}</div> : null}
    </article>
  );
}

export function ChartCard({
  title,
  subtitle,
  children,
  footer,
}: PropsWithChildren<{
  title: string;
  subtitle?: string;
  footer?: ReactNode;
}>) {
  return (
    <article className="dashboard-chart-card">
      <div className="dashboard-card-heading">
        <h2 className="dashboard-card-title">{title}</h2>
        {subtitle ? <p className="dashboard-card-subtitle">{subtitle}</p> : null}
      </div>
      {children}
      {footer ? <div className="dashboard-metric-support">{footer}</div> : null}
    </article>
  );
}

export function DashboardMetaBlock({ meta }: { meta: DashboardMeta }) {
  return (
    <dl className="dashboard-meta">
      <div>
        <strong>Source:</strong> {meta.source}
      </div>
      <div>
        <strong>Updated:</strong> {meta.updatedAt}
      </div>
      {meta.asOf ? (
        <div>
          <strong>As of:</strong> {meta.asOf}
        </div>
      ) : null}
      {meta.note ? (
        <div>
          <strong>Note:</strong> {meta.note}
        </div>
      ) : null}
    </dl>
  );
}
