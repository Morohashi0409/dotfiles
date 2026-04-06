import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { getDashboardTheme } from "./dashboard-tokens";
import { ChartCard, DashboardPage, MetricCard } from "./react-dashboard-starter";

type MonthlyRow = {
  month: string;
  applications: number;
  approved: number;
  target: number;
};

type CategoryRow = {
  label: string;
  value: number;
};

type ShareRow = {
  label: string;
  value: number;
};

const monthlyRows: MonthlyRow[] = [
  { month: "Apr", applications: 920, approved: 720, target: 1000 },
  { month: "May", applications: 980, approved: 760, target: 1000 },
  { month: "Jun", applications: 1040, approved: 810, target: 1000 },
  { month: "Jul", applications: 1120, approved: 880, target: 1000 },
  { month: "Aug", applications: 1090, approved: 845, target: 1000 },
  { month: "Sep", applications: 1180, approved: 910, target: 1000 },
];

const categoryRows: CategoryRow[] = [
  { label: "Tokyo", value: 298 },
  { label: "Osaka", value: 244 },
  { label: "Aichi", value: 198 },
  { label: "Fukuoka", value: 164 },
  { label: "Hokkaido", value: 149 },
];

const shareRows: ShareRow[] = [
  { label: "Online", value: 58 },
  { label: "Counter", value: 27 },
  { label: "Other", value: 15 },
];

export function DigitalAgencyRechartsDashboardStarter() {
  const theme = getDashboardTheme("blue");
  const palette = theme.series;

  return (
    <DashboardPage
      title="申請ダッシュボード"
      lead="提示型の行政ダッシュボードを想定した Recharts 用 starter。左上の概要、上部フィルタ、近接した凡例、控えめな配色を前提にしている。"
      theme="blue"
      filters={
        <>
          <span className="dashboard-chip">Year: 2026</span>
          <span className="dashboard-chip">Region: Nationwide</span>
          <span className="dashboard-chip">Channel: All</span>
        </>
      }
      metrics={
        <>
          <MetricCard label="申請件数" value="1,180" support="2026-09" delta="+8.3% vs prev month" />
          <MetricCard label="承認率" value="77.1%" support="as of 2026-09" delta="+1.4pt vs prev month" />
          <MetricCard label="平均処理日数" value="5.8日" support="target 6.0日以下" delta="-0.3日 vs target" />
          <MetricCard label="未処理件数" value="143" support="backlog" delta="-12.8% vs prev month" />
        </>
      }
      meta={{
        source: "申請処理システム集計",
        updatedAt: "2026-10-03 09:00 JST",
        asOf: "2026-09",
        note: "Starter data only. Replace with repo-local data fetch and labels.",
      }}
    >
      <ChartCard title="申請件数（月次推移）" subtitle="月次推移 / 件数">
        <div style={{ height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              accessibilityLayer
              data={monthlyRows}
              margin={{ top: 8, right: 12, left: 0, bottom: 0 }}
            >
              <CartesianGrid stroke={palette[3]} vertical={false} />
              <XAxis axisLine={false} dataKey="month" tickLine={false} />
              <YAxis axisLine={false} domain={[0, "dataMax"]} tickLine={false} width={48} />
              <Tooltip />
              <Legend align="left" verticalAlign="top" />
              <ReferenceLine
                ifOverflow="extendDomain"
                label="目標"
                stroke={theme.aux1}
                strokeDasharray="4 4"
                y={1000}
              />
              <Line
                activeDot={{ r: 5 }}
                dataKey="applications"
                dot={{ r: 3 }}
                name="申請件数"
                stroke={theme.accentStrong}
                strokeWidth={2}
                type="monotone"
              />
              <Line
                activeDot={{ r: 5 }}
                dataKey="approved"
                dot={{ r: 3 }}
                name="承認件数"
                stroke={theme.accent}
                strokeWidth={2}
                type="monotone"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>

      <ChartCard title="地域別の処理件数" subtitle="数量比較 / 件数">
        <div style={{ height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              accessibilityLayer
              data={categoryRows}
              layout="vertical"
              margin={{ top: 8, right: 24, left: 12, bottom: 0 }}
            >
              <CartesianGrid stroke={palette[3]} horizontal={false} />
              <XAxis axisLine={false} domain={[0, "dataMax"]} tickLine={false} type="number" />
              <YAxis axisLine={false} dataKey="label" tickLine={false} type="category" width={72} />
              <Tooltip cursor={{ fill: palette[4] }} />
              <Legend align="left" verticalAlign="top" />
              <Bar dataKey="value" fill={theme.accent} name="処理件数" radius={[0, 6, 6, 0]}>
                <LabelList dataKey="value" position="right" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>

      <ChartCard
        title="受付チャネル構成比"
        subtitle="構成比 / 全体が明確な場合のみドーナツを使用"
        footer="カテゴリが増える場合は ranked bar に戻す。"
      >
        <div style={{ height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart accessibilityLayer margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
              <Tooltip />
              <Legend align="left" layout="vertical" verticalAlign="middle" />
              <Pie
                cx="34%"
                cy="50%"
                data={shareRows}
                dataKey="value"
                innerRadius={64}
                label
                labelLine={false}
                nameKey="label"
                outerRadius={104}
              >
                {shareRows.map((entry, index) => (
                  <Cell key={entry.label} fill={palette[index]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>
    </DashboardPage>
  );
}
