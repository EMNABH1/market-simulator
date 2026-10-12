"use client";

import { useEffect, useState } from "react";
import { apiJson } from "@/lib/api";
import type { CoursActif } from "@/components/MarketTicker";

type Portefeuille = { liquidites: number; valeur_totale: number; sim_date: string };
type Ordre = { side: "ACHAT" | "VENTE"; quantity: number; price: number };

function nombre(value: number): string {
  return value.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function unite(symbole: string): string {
  if (symbole === "HG=F") return "USD/lb";
  if (symbole === "CL=F") return "USD/bbl";
  if (symbole === "GC=F" || symbole === "SI=F") return "USD/oz";
  return "USD";
}

export default function DashboardMetrics({
  token,
  symbole,
  quote,
  simDate,
  rafraichissement,
}: {
  token: string;
  symbole: string;
  quote: CoursActif | null;
  simDate: string;
  rafraichissement: number;
}) {
  const cle = `${token}|${simDate}|${rafraichissement}`;
  const [resultat, setResultat] = useState<{
    cle: string;
    portefeuille: Portefeuille | null;
    ordres: Ordre[] | null;
    erreur: string;
  } | null>(null);

  useEffect(() => {
    let annule = false;
    Promise.all([
      apiJson<Portefeuille>("/api/portefeuille", {}, token),
      apiJson<Ordre[]>("/api/ordres", {}, token),
    ])
      .then(([resume, historique]) => {
        if (!annule) setResultat({ cle, portefeuille: resume, ordres: historique, erreur: "" });
      })
      .catch((cause: unknown) => {
        if (!annule) {
          const erreur = cause instanceof Error ? cause.message : "Données du portefeuille indisponibles.";
          setResultat({ cle, portefeuille: null, ordres: null, erreur });
        }
      });
    return () => { annule = true; };
  }, [cle, token]);

  const courant = resultat?.cle === cle ? resultat : null;
  const portefeuille = courant?.portefeuille ?? null;
  const ordres = courant?.ordres ?? null;
  const erreur = courant?.erreur ?? "";

  if (erreur) {
    return <p className="error-state" role="alert">Impossible de charger la valeur du portefeuille et son historique d’ordres : {erreur}</p>;
  }

  const loading = !portefeuille || !ordres;
  const capitalInitial = loading ? null : portefeuille.liquidites + ordres.reduce(
    (total, ordre) => total + (ordre.side === "ACHAT" ? 1 : -1) * ordre.quantity * ordre.price,
    0,
  );
  const gain = loading || capitalInitial === null ? null : portefeuille.valeur_totale - capitalInitial;
  const direction = gain === null ? "neutral" : gain > 0 ? "positive" : gain < 0 ? "negative" : "neutral";

  return (
    <section aria-busy={loading} aria-label="Chiffres clés du portefeuille" className="dashboard-kpis">
      <div className="dashboard-kpi">
        <span>Valeur totale</span>
        <strong>{loading ? "—" : `${nombre(portefeuille.valeur_totale)} USD`}</strong>
      </div>
      <div className="dashboard-kpi">
        <span>Liquidités</span>
        <strong>{loading ? "—" : `${nombre(portefeuille.liquidites)} USD`}</strong>
      </div>
      <div className="dashboard-kpi">
        <span>Gain/perte depuis le début</span>
        {gain === null ? <strong>—</strong> : <strong className={`direction-${direction}`}>{gain > 0 ? "+" : gain < 0 ? "−" : ""}{nombre(Math.abs(gain))} USD</strong>}
      </div>
      <div className="dashboard-kpi">
        <span>Dernier prix · {unite(symbole)}</span>
        <strong>{quote ? nombre(quote.dernier) : loading ? "—" : "Indisponible"}</strong>
      </div>
    </section>
  );
}
