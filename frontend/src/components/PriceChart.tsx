"use client";

import { useEffect, useRef, useState } from "react";
import {
  createChart,
  CandlestickSeries,
  LineSeries,
  type IChartApi,
  type Time,
} from "lightweight-charts";

type Bougie = { time: Time; open: number; high: number; low: number; close: number };

const API = "http://127.0.0.1:8000";

function sma(data: Bougie[], p: number) {
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

export default function PriceChart({
  symbole = "GC=F",
  jours = 90,
}: {
  symbole?: string;
  jours?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [erreur, setErreur] = useState<string | null>(null);

  useEffect(() => {
    let chart: IChartApi | null = null;
    let annule = false;
    const onResize = () => chart?.applyOptions({ width: ref.current?.clientWidth });

    fetch(`${API}/api/prix/${encodeURIComponent(symbole)}?jours=${jours}`)
      .then((r) => {
        if (!r.ok) throw new Error(`Erreur API ${r.status}`);
        return r.json();
      })
      .then((bougies: Bougie[]) => {
        if (annule || !ref.current) return;
        chart = createChart(ref.current, {
          height: 300,
          layout: { textColor: "#64748b", background: { color: "#ffffff" } },
          grid: { vertLines: { visible: false }, horzLines: { color: "#eef2f7" } },
          rightPriceScale: { borderVisible: false },
          timeScale: { borderVisible: false },
        });
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
        window.addEventListener("resize", onResize);
      })
      .catch(() => setErreur("Impossible de charger les prix. Le backend est-il lancé ?"));

    return () => {
      annule = true;
      window.removeEventListener("resize", onResize);
      chart?.remove();
    };
  }, [symbole, jours]);

  if (erreur) return <p className="py-10 text-center text-sm text-red-700">{erreur}</p>;
  return <div ref={ref} className="w-full" />;
}