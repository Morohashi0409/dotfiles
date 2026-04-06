import { useEffect, useRef } from "react";

import * as echarts from "echarts/core";
import { BarChart, LineChart, PieChart } from "echarts/charts";
import { AriaComponent, DatasetComponent, GridComponent, LegendComponent, TooltipComponent } from "echarts/components";
import { LabelLayout } from "echarts/features";
import { SVGRenderer } from "echarts/renderers";

import { getDashboardTheme, type DashboardThemeName } from "./dashboard-tokens";
import { ChartCard, DashboardPage, MetricCard } from "./react-dashboard-starter";

echarts.use([
  LineChart,
  BarChart,
  PieChart,
  GridComponent,
  LegendComponent,
  TooltipComponent,
  DatasetComponent,
  AriaComponent,
  LabelLayout,
  SVGRenderer,
]);

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

type DashboardOption = Parameters<echarts.EChartsType["setOption"]>[0];

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

function buildBaseOption(themeName: DashboardThemeName) {
  const theme = getDashboardTheme(themeName);

  return {
    aria: { show: true },
    animationDuration: 250,
    color: theme.series.slice(0, 5),
    grid: {
      top: 36,
      right: 20,
      bottom: 20,
      left: 16,
      containLabel: true,
    },
    legend: {
      top: 0,
      left: 0,
      itemWidth: 12,
      itemHeight: 12,
      textStyle: {
        color: "#1A1A1A",
        fontFamily: "Noto Sans JP, system-ui, sans-serif",
        fontSize: 14,
      },
    },
    textStyle: {
      color: "#1A1A1A",
      fontFamily: "Noto Sans JP, system-ui, sans-serif",
    },
    tooltip: {
      backgroundColor: "#FFFFFF",
      borderColor: "#CCCCCC",
      borderWidth: 1,
      textStyle: {
        color: "#1A1A1A",
        fontFamily: "Noto Sans JP, system-ui, sans-serif",
      },
    },
  };
}

export function buildTrendLineOption(
  rows: MonthlyRow[],
  themeName: DashboardThemeName = "blue",
): DashboardOption {
  const theme = getDashboardTheme(themeName);
  const base = buildBaseOption(themeName);

  return {
    ...base,
    dataset: { source: rows },
    tooltip: {
      ...base.tooltip,
      trigger: "axis",
      axisPointer: { type: "line" },
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      axisLine: { show: false },
      axisTick: { show: false },
    },
    yAxis: {
      type: "value",
      min: 0,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: theme.series[3] } },
    },
    series: [
      {
        type: "line",
        name: "申請件数",
        encode: { x: "month", y: "applications" },
        symbol: "circle",
        symbolSize: 6,
        lineStyle: { width: 2 },
        emphasis: { scale: false },
      },
      {
        type: "line",
        name: "承認件数",
        encode: { x: "month", y: "approved" },
        symbol: "circle",
        symbolSize: 6,
        lineStyle: { width: 2 },
        emphasis: { scale: false },
      },
      {
        type: "line",
        name: "目標",
        encode: { x: "month", y: "target" },
        symbol: "none",
        lineStyle: {
          width: 2,
          color: theme.aux1,
          type: "dashed",
        },
        emphasis: { disabled: true },
      },
    ],
  };
}

export function buildCategoryBarOption(
  rows: CategoryRow[],
  themeName: DashboardThemeName = "blue",
): DashboardOption {
  const theme = getDashboardTheme(themeName);
  const base = buildBaseOption(themeName);

  return {
    ...base,
    dataset: { source: rows },
    tooltip: {
      ...base.tooltip,
      trigger: "axis",
      axisPointer: { type: "shadow" },
    },
    xAxis: {
      type: "value",
      min: 0,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: theme.series[3] } },
    },
    yAxis: {
      type: "category",
      axisLine: { show: false },
      axisTick: { show: false },
    },
    series: [
      {
        type: "bar",
        name: "処理件数",
        encode: { x: "value", y: "label" },
        itemStyle: {
          borderRadius: [0, 6, 6, 0],
        },
        label: {
          show: true,
          position: "right",
          color: "#1A1A1A",
        },
      },
    ],
  };
}

export function buildDonutOption(
  rows: ShareRow[],
  themeName: DashboardThemeName = "blue",
): DashboardOption {
  const base = buildBaseOption(themeName);

  return {
    ...base,
    tooltip: {
      ...base.tooltip,
      trigger: "item",
    },
    legend: {
      ...base.legend,
      orient: "vertical",
      right: 0,
      top: "middle",
    },
    series: [
      {
        type: "pie",
        name: "受付チャネル",
        radius: ["50%", "72%"],
        center: ["34%", "50%"],
        avoidLabelOverlap: true,
        label: {
          show: true,
          formatter: "{d}%",
        },
        labelLine: { show: false },
        data: rows.map((row) => ({ name: row.label, value: row.value })),
      },
    ],
  };
}

export function EChartCanvas({
  option,
  height = 320,
  renderer = "svg",
}: {
  option: DashboardOption;
  height?: number;
  renderer?: "canvas" | "svg";
}) {
  const elementRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<echarts.EChartsType | null>(null);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) {
      return;
    }

    const chart = echarts.init(element, undefined, { renderer });
    chartRef.current = chart;

    const handleResize = () => {
      chart.resize();
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.dispose();
      chartRef.current = null;
    };
  }, [renderer]);

  useEffect(() => {
    chartRef.current?.setOption(option, true);
  }, [option]);

  return <div ref={elementRef} style={{ width: "100%", height }} />;
}

export function DigitalAgencyEChartsDashboardStarter() {
  return (
    <DashboardPage
      title="申請ダッシュボード"
      lead="提示型の行政ダッシュボードを想定した ECharts 用 starter。dataset、SVG renderer、aria、静かな tooltip/legend を前提にしている。"
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
        <EChartCanvas option={buildTrendLineOption(monthlyRows)} />
      </ChartCard>

      <ChartCard title="地域別の処理件数" subtitle="数量比較 / 件数">
        <EChartCanvas option={buildCategoryBarOption(categoryRows)} />
      </ChartCard>

      <ChartCard
        title="受付チャネル構成比"
        subtitle="構成比 / 全体が明確な場合のみドーナツを使用"
        footer="カテゴリが増える場合は ranked bar に戻す。"
      >
        <EChartCanvas option={buildDonutOption(shareRows)} />
      </ChartCard>
    </DashboardPage>
  );
}
