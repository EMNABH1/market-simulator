"use client";

import { useEffect, useState } from "react";

type Resume = { dernier: number; variation: number; variation_pct: number; date: string };

const fr = (n: number, d = 2) =>
  n.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });

export default function EnteteActif({ symbole, nom }: { symbole: string; nom: string }) {
  const [r, setR] = useState<Resume | null>(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/resume/${encodeURIComponent(symbole)}`)
      .then((res) => res.json())
      .then(setR)
      .catch(() => setR(null));
  }, [symbole]);

  const hausse = (r?.variation ?? 0) >= 0;
  return (
    <div>
      <p className="font-semibold">
        {nom} <span className="text-xs font-normal text-slate-500">{symbole}</span>
      </p>
      {r ? (
        <p className="font-mono text-2xl">
          {fr(r.dernier)}{" "}
          <span className={`text-sm ${hausse ? "text-green-700" : "text-red-700"}`}>
            {hausse ? "+" : ""}{fr(r.variation)} ({hausse ? "+" : ""}{fr(r.variation_pct)} %)
          </span>
        </p>
      ) : (
        <p className="text-sm text-slate-500">Chargement…</p>
      )}
    </div>
  );
}