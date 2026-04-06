export type DashboardThemeName =
  | "blue"
  | "light-blue"
  | "cyan"
  | "green"
  | "orange"
  | "red"
  | "solid-gray";

export type DashboardTheme = {
  readonly name: DashboardThemeName;
  readonly series: readonly string[];
  readonly accentStrong: string;
  readonly accent: string;
  readonly accentSoft: string;
  readonly accentSurface: string;
  readonly aux1: string;
  readonly aux2: string;
  readonly canvas: string;
};

export const dashboardThemes: Record<DashboardThemeName, DashboardTheme> = {
  blue: {
    name: "blue",
    series: ["#0017C1", "#3460FB", "#7096F8", "#C5D7FB", "#E8F1FE", "#FE3939", "#FFBBBB", "#F8F8FB"],
    accentStrong: "#0017C1",
    accent: "#3460FB",
    accentSoft: "#C5D7FB",
    accentSurface: "#E8F1FE",
    aux1: "#FE3939",
    aux2: "#FFBBBB",
    canvas: "#F8F8FB",
  },
  "light-blue": {
    name: "light-blue",
    series: ["#0055AD", "#008BF2", "#57B8FF", "#C0E4FF", "#F0F9FF", "#FE3939", "#FFBBBB", "#F8F8FB"],
    accentStrong: "#0055AD",
    accent: "#008BF2",
    accentSoft: "#C0E4FF",
    accentSurface: "#F0F9FF",
    aux1: "#FE3939",
    aux2: "#FFBBBB",
    canvas: "#F8F8FB",
  },
  cyan: {
    name: "cyan",
    series: ["#006F83", "#00A3BF", "#2BC8E4", "#99F2FF", "#E9F7F9", "#666666", "#CCCCCC", "#F8F8FB"],
    accentStrong: "#006F83",
    accent: "#00A3BF",
    accentSoft: "#99F2FF",
    accentSurface: "#E9F7F9",
    aux1: "#666666",
    aux2: "#CCCCCC",
    canvas: "#F8F8FB",
  },
  green: {
    name: "green",
    series: ["#115A36", "#259D63", "#51B883", "#9BD4B5", "#E6F5EC", "#666666", "#CCCCCC", "#F8F8FB"],
    accentStrong: "#115A36",
    accent: "#259D63",
    accentSoft: "#9BD4B5",
    accentSurface: "#E6F5EC",
    aux1: "#666666",
    aux2: "#CCCCCC",
    canvas: "#F8F8FB",
  },
  orange: {
    name: "orange",
    series: ["#AC3E00", "#FB5B01", "#FF8D44", "#FFC199", "#FFEEE2", "#666666", "#CCCCCC", "#F8F8FB"],
    accentStrong: "#AC3E00",
    accent: "#FB5B01",
    accentSoft: "#FFC199",
    accentSurface: "#FFEEE2",
    aux1: "#666666",
    aux2: "#CCCCCC",
    canvas: "#F8F8FB",
  },
  red: {
    name: "red",
    series: ["#CE0000", "#FE3939", "#FF7171", "#FFBBBB", "#FDEEEE", "#666666", "#CCCCCC", "#F8F8FB"],
    accentStrong: "#CE0000",
    accent: "#FE3939",
    accentSoft: "#FFBBBB",
    accentSurface: "#FDEEEE",
    aux1: "#666666",
    aux2: "#CCCCCC",
    canvas: "#F8F8FB",
  },
  "solid-gray": {
    name: "solid-gray",
    series: ["#4D4D4D", "#767676", "#999999", "#CCCCCC", "#F2F2F2", "#3460FB", "#FE3939", "#F8F8FB"],
    accentStrong: "#4D4D4D",
    accent: "#767676",
    accentSoft: "#CCCCCC",
    accentSurface: "#F2F2F2",
    aux1: "#3460FB",
    aux2: "#FE3939",
    canvas: "#F8F8FB",
  },
};

export const dashboardLayout = {
  maxWidth: 1440,
  columns: 12,
  mobileBreakpoint: 768,
  space1: 8,
  space2: 16,
  space3: 24,
  space4: 32,
  space6: 64,
  cardRadius: 12,
} as const;

export const dashboardTypography = {
  metricValue: { fontSize: 32, lineHeight: 1.5, fontWeight: 700 },
  sectionTitle: { fontSize: 24, lineHeight: 1.5, fontWeight: 700 },
  cardTitle: { fontSize: 16, lineHeight: 1.7, fontWeight: 700 },
  body: { fontSize: 16, lineHeight: 1.7, fontWeight: 400 },
  denseLabel: { fontSize: 14, lineHeight: 1.3, fontWeight: 400 },
  meta: { fontSize: 14, lineHeight: 1.5, fontWeight: 400 },
} as const;

export const dashboardMetaFields = ["source", "updatedAt", "asOf", "note"] as const;

export function getDashboardTheme(themeName: DashboardThemeName = "blue"): DashboardTheme {
  return dashboardThemes[themeName];
}

export function getPrimarySeriesPalette(themeName: DashboardThemeName = "blue"): readonly string[] {
  return dashboardThemes[themeName].series.slice(0, 5);
}

export function getComparisonSeriesPalette(themeName: DashboardThemeName = "blue"): readonly string[] {
  const theme = dashboardThemes[themeName];
  return [theme.series[0], theme.series[1], theme.series[2], theme.aux1, theme.aux2];
}
