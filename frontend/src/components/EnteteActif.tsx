"use client";

import { useEffect, useState } from "react";
import { libelleActif } from "@/lib/api";

type Resume = { dernier: number; variation: number; variation_pct: number; date: string };

const fr = (n: number, d = 2) =>
  n.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });

export default function EnteteActif({ symbole, nom, jusqua }: { symbole: string; nom: string; jusqua: string }) {
  const cle = `${symbole}|${jusqua}`;
  const [resultat, setResultat] = useState<{ cle: string; resume: Resume | null } | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    const query = new URLSearchParams({ jusqua });

    fetch(`http://127.0.0.1:8000/api/resume/${encodeURIComponent(symbole)}?${query}`, {
      signal: controller.signal,
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Erreur API ${res.status}`);
        return res.json();
      })
      .then((resume: Resume) => setResultat({ cle, resume }))
      .catch(() => {
        if (!controller.signal.aborted) setResultat({ cle, resume: null });
      });

    return () => controller.abort();
  }, [cle, symbole, jusqua]);

  const r = resultat?.cle === cle ? resultat.resume : null;

  const hausse = (r?.variation ?? 0) >= 0;
  return (
    <div>
      <p className="font-semibold">
        {libelleActif(symbole, nom)}
      </p>
      {r ? (
        <p className="font-mono text-2xl">
          {fr(r.dernier)}{" "}
          <span className={`text-sm ${hausse ? "text-positive" : "text-negative"}`}>
            {hausse ? "+" : "−"}{fr(Math.abs(r.variation))} ({hausse ? "+" : "−"}{fr(Math.abs(r.variation_pct))} %)
          </span>
        </p>
      ) : (
        <p className="loading-state">Chargement du cours…</p>
      )}
    </div>
  );
}