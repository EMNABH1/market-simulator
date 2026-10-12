"use client";

import { useState } from "react";
import EnteteActif from "../EnteteActif";
import PriceChart from "../PriceChart";
const PERIODES = [
  { label: "1M", jours: 30 },
  { label: "3M", jours: 90 },
  { label: "1A", jours: 365 },
  { label: "Max", jours: 4000 },
];

export default function GraphiqueOr({ symbole, nom, jusqua, theme }: { symbole: string; nom: string; jusqua: string; theme: "dark" | "light" }) {
  const [jours, setJours] = useState(90);
  return (
    <section className="chart-panel">
      <div className="flex items-start justify-between">
        <EnteteActif symbole={symbole} nom={nom} jusqua={jusqua} />
        <div className="flex gap-1 text-xs">
          {PERIODES.map((p) => (
            <button
              key={p.label}
              type="button"
              aria-pressed={jours === p.jours}
              onClick={() => setJours(p.jours)}
              className="period-button"
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>
      <div className="mt-3">
        <PriceChart symbole={symbole} jours={jours} jusqua={jusqua} theme={theme} />
      </div>
      <p className="data-caption">
        Bougies journalières · Moyenne mobile 20 jours (SMA) · Source : Yahoo Finance ({symbole})
      </p>
    </section>
  );
}