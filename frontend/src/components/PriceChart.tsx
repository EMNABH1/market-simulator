"use client";

import { useEffect, useRef } from "react";
import {
  createChart,
  CandlestickSeries,
  LineSeries,
  type Time,
} from "lightweight-charts";

// Données fictives déterministes (à remplacer par l'API FastAPI)
function genererBougies(n: number) {
  let seed = 7;
  const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647) - 0.5;
  const out: { time: Time; open: number; high: number; low: number; close: number }[] = [];
  let prix = 80;
  const debut = new Date("2026-08-01");
  for (let i = 0; i < n; i++) {
    const open = prix;
    const close = open + rnd() * 3;
    const high = Math.max(open, close) + Math.abs(rnd()) * 1.2;
    const low = Math.min(open, close) - Math.abs(rnd()) * 1.2;
    const d = new Date(debut.getTime() + i * 86400000);
    out.push({ time: d.toISOString().slice(0, 10) as Time, open, high, low, close });
    prix = close;
  }
  return out;
}

function sma(data: ReturnType<typeof genererBougies>, p: number) {
  return data
    .map((d, i) =>
      i < p - 1
        ? null
        : {
            time: d.time,
            value: data.slice(i - p + 1, i + 1).reduce((s, x) => s + x.close, 0) / p,
          }
    )
    .filter((x): x is { time: Time; value: number } => x !== null);
}

export default function PriceChart() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      height: 300,
      layout: { textColor: "#64748b", background: { color: "#ffffff" } },
      grid: { vertLines: { visible: false }, horzLines: { color: "#eef2f7" } },
      rightPriceScale: { borderVisible: false },
      timeScale: { borderVisible: false },
    });
    const bougies = genererBougies(60);
    const candles = chart.addSeries(CandlestickSeries, {
      upColor: "#0f7a3e",
      downColor: "#b42318",
      borderVisible: false,
      wickUpColor: "#0f7a3e",
      wickDownColor: "#b42318",
    });
    candles.setData(bougies);
    const ligne = chart.addSeries(LineSeries, { color: "#2563eb", lineWidth: 2 });
    ligne.setData(sma(bougies, 20));
    chart.timeScale().fitContent();

    const onResize = () => chart.applyOptions({ width: ref.current?.clientWidth });
    window.addEventListener("resize", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      chart.remove();
    };
  }, []);

  return <div ref={ref} className="w-full" />;
}