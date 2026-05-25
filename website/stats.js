import Plotly from "plotly.js-dist-min";

const green = "#6d7246",
  brown = "#7a5a37",
  sage = "#cdd0b3";
const cfg = { displayModeBar: false, responsive: true };
const baseLayout = (extra) => ({
  margin: { t: 4, b: 24, l: 28, r: 4 },
  paper_bgcolor: "rgba(0,0,0,0)",
  plot_bgcolor: "rgba(0,0,0,0)",
  font: { family: "Franklin Gothic, sans-serif", size: 10, color: brown },
  ...extra,
});

Plotly.newPlot(
  "chart-trees",
  [
    {
      x: ["2019", "2020", "2021", "2022", "2023", "2024"],
      y: [420, 1800, 3500, 6200, 9800, 12804],
      type: "scatter",
      mode: "lines+markers",
      fill: "tozeroy",
      line: { color: green, width: 2 },
      marker: { color: green, size: 5 },
      fillcolor: "rgba(109,114,70,0.15)",
    },
  ],
  baseLayout({ xaxis: { showgrid: false }, yaxis: { gridcolor: sage } }),
  cfg,
);

Plotly.newPlot(
  "chart-energy",
  [
    {
      x: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ],
      y: [12, 18, 34, 52, 68, 74, 71, 65, 48, 30, 16, 10],
      type: "bar",
      marker: { color: brown },
    },
  ],
  baseLayout({
    xaxis: { showgrid: false },
    yaxis: { gridcolor: sage },
    bargap: 0.3,
  }),
  cfg,
);

const hours = Array.from({ length: 24 }, (_, i) => i + "h");
Plotly.newPlot(
  "chart-climate",
  [
    {
      x: hours,
      y: [
        14, 13, 13, 12, 12, 13, 14, 16, 17, 18, 19, 20, 20, 21, 21, 20, 19, 18,
        17, 16, 16, 15, 15, 14,
      ],
      name: "Temp °C",
      type: "scatter",
      mode: "lines",
      line: { color: brown, width: 2 },
    },
    {
      x: hours,
      y: [
        72, 74, 75, 76, 75, 73, 70, 66, 63, 61, 60, 58, 57, 57, 58, 60, 62, 64,
        66, 68, 69, 70, 71, 72,
      ],
      name: "Humidity %",
      type: "scatter",
      mode: "lines",
      line: { color: green, width: 2 },
      yaxis: "y2",
    },
  ],
  baseLayout({
    xaxis: { showgrid: false },
    yaxis: { gridcolor: sage },
    yaxis2: { overlaying: "y", side: "right", showgrid: false },
    legend: { orientation: "h", x: 0, y: 1.2 },
  }),
  cfg,
);
