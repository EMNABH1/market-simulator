"use client";

import { useEffect, useState } from "react";

type Stats = {
  dernier: number; haut_1an: number; bas_1an: number;
  var_1m_pct: number | null; var_1an_pct: number | null; vol_20j_pct: number | null;
  premiere_date: string; derniere_date: string; nb_jours: number;
};

const fr = (n: number, d = 2) =>
  n.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });
const signe = (n: number | null) => n === null ? "text-neutral" : n >= 0 ? "text-positive" : "text-negative";
const variation = (n: number | null) => n === null ? "N/D" : `${n >= 0 ? "+" : "−"}${fr(Math.abs(n))} %`;

export default function StatsOr({ symbole, jusqua }: { symbole: string; jusqua: string }) {
  const cle = `${symbole}|${jusqua}`;
  const [resultat, setResultat] = useState<{ cle: string; stats: Stats | null; erreur: boolean } | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    const query = new URLSearchParams({ jusqua });

    fetch(`http://127.0.0.1:8000/api/stats/${encodeURIComponent(symbole)}?${query}`, {
      signal: controller.signal,
    })
      .then((r) => {
        if (!r.ok) throw new Error(`Erreur API ${r.status}`);
        return r.json();
      })
      .then((stats: Stats) => setResultat({ cle, stats, erreur: false }))
      .catch(() => {
        if (!controller.signal.aborted) setResultat({ cle, stats: null, erreur: true });
      });

    return () => controller.abort();
  }, [cle, symbole, jusqua]);

  const courant = resultat?.cle === cle ? resultat : null;
  const s = courant?.stats ?? null;
  const erreur = courant?.erreur ?? false;

  if (erreur) return <p className="error-state">Impossible de charger les statistiques. Vérifie que le backend est lancé.</p>;
  if (!s) return <p className="loading-state">Chargement des statistiques…</p>;

  const cartes = [
    { l: "Dernier cours (USD)", v: fr(s.dernier), c: "" },
    { l: "Plus haut sur 1 an", v: fr(s.haut_1an), c: "" },
    { l: "Plus bas sur 1 an", v: fr(s.bas_1an), c: "" },
    { l: "Variation sur 1 mois", v: variation(s.var_1m_pct), c: signe(s.var_1m_pct) },
    { l: "Variation sur 1 an", v: variation(s.var_1an_pct), c: signe(s.var_1an_pct) },
    { l: "Volatilité (20 jours, par jour)", v: s.vol_20j_pct === null ? "N/D" : `${fr(s.vol_20j_pct)} %`, c: "" },
  ];

  return (
    <section aria-label="Statistiques du marché" className="stats-block stats-block-compact">
      <div className="stat-grid stat-grid-compact">
        {cartes.map((k) => (
          <section key={k.l} className="stat-item">
            <p className="stat-label">{k.l}</p>
            <p className={`stat-value ${k.c}`}>{k.v}</p>
          </section>
        ))}
      </div>
      <p className="data-caption">{s.nb_jours} séances · du {s.premiere_date} au {s.derniere_date}</p>
    </section>
  );
}