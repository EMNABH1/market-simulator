"use client";

import { useEffect, useState } from "react";

type Stats = {
  dernier: number; haut_1an: number; bas_1an: number;
  var_1m_pct: number; var_1an_pct: number; vol_20j_pct: number;
  premiere_date: string; derniere_date: string; nb_jours: number;
};

const fr = (n: number, d = 2) =>
  n.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });
const signe = (n: number) => (n >= 0 ? "text-green-700" : "text-red-700");

export default function StatsOr() {
  const [s, setS] = useState<Stats | null>(null);
  const [erreur, setErreur] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/stats/GC=F")
      .then((r) => r.json())
      .then(setS)
      .catch(() => setErreur(true));
  }, []);

  if (erreur) return <p className="text-sm text-red-700">Backend injoignable.</p>;
  if (!s) return <p className="text-sm text-slate-500">Chargement…</p>;

  const cartes = [
    { l: "Dernier cours (USD)", v: fr(s.dernier), c: "" },
    { l: "Plus haut sur 1 an", v: fr(s.haut_1an), c: "" },
    { l: "Plus bas sur 1 an", v: fr(s.bas_1an), c: "" },
    { l: "Variation sur 1 mois", v: `${fr(s.var_1m_pct)} %`, c: signe(s.var_1m_pct) },
    { l: "Variation sur 1 an", v: `${fr(s.var_1an_pct)} %`, c: signe(s.var_1an_pct) },
    { l: "Volatilité (20 jours, par jour)", v: `${fr(s.vol_20j_pct)} %`, c: "" },
  ];

  return (
    <div className="space-y-2">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-6">
        {cartes.map((k) => (
          <section key={k.l} className="rounded-xl border border-slate-200 bg-white p-4">
            <p className="text-xs text-slate-500">{k.l}</p>
            <p className={`mt-1 font-mono text-xl font-semibold ${k.c}`}>{k.v}</p>
          </section>
        ))}
      </div>
      <p className="text-xs text-slate-500">
        Données : {s.nb_jours} séances, du {s.premiere_date} au {s.derniere_date}
      </p>
    </div>
  );
}