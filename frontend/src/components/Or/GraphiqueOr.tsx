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

export default function GraphiqueOr() {
  const [jours, setJours] = useState(90);
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4">
      <div className="flex items-start justify-between">
        <EnteteActif symbole="GC=F" nom="Or" />
        <div className="flex gap-1 text-xs">
          {PERIODES.map((p) => (
            <button
              key={p.label}
              onClick={() => setJours(p.jours)}
              className={`rounded-lg border px-3 py-2 ${
                jours === p.jours ? "bg-[#0f1f3d] text-white" : "border-slate-200"
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>
      <div className="mt-3">
        <PriceChart symbole="GC=F" jours={jours} />
      </div>
      <p className="mt-2 text-xs text-slate-500">
        Bougies journalières · Moyenne mobile 20 jours (SMA) · Source : Yahoo Finance (GC=F)
      </p>
    </section>
  );
}