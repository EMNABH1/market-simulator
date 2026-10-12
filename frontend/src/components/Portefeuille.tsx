"use client";

import { useEffect, useState } from "react";
import { apiJson } from "@/lib/api";

type Position = {
  Actif: string;
  "Quantité": number;
  "Coût moyen": number;
  "Prix actuel": number;
  Valeur: number;
  "Gain/perte ($)": number;
  "Gain/perte (%)": number;
};
type PortefeuilleData = {
  sim_date: string;
  liquidites: number;
  positions: Position[];
  valeur_positions: number;
  valeur_totale: number;
};

const nombre = (value: number) => value.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export default function Portefeuille({ token, rafraichissement }: { token: string; rafraichissement: number }) {
  const [data, setData] = useState<PortefeuilleData | null>(null);
  const [erreur, setErreur] = useState("");

  useEffect(() => {
    let annule = false;
    apiJson<PortefeuilleData>("/api/portefeuille", {}, token)
      .then((resultat) => { if (!annule) setData(resultat); })
      .catch((cause: unknown) => { if (!annule) setErreur(cause instanceof Error ? cause.message : "Portefeuille indisponible."); });
    return () => { annule = true; };
  }, [token, rafraichissement]);

  if (erreur) return <p role="alert" className="error-state">{erreur}</p>;
  if (!data) return <p role="status" className="loading-state">Chargement du portefeuille…</p>;

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold">Portefeuille</h1>
        <p className="text-secondary">Valorisation au {data.sim_date}.</p>
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        {[{ label: "Liquidités", value: data.liquidites }, { label: "Valeur des positions", value: data.valeur_positions }, { label: "Valeur totale", value: data.valeur_totale }].map((metric) => (
          <section key={metric.label} className="stat-item">
            <p className="stat-label">{metric.label}</p>
            <p className="stat-value">{nombre(metric.value)} USD</p>
          </section>
        ))}
      </div>
      <section>
        <h2 className="panel-heading">Positions ouvertes</h2>
        {data.positions.length === 0 ? <p className="text-secondary">Aucune position ouverte.</p> : (
          <div className="table-wrap">
            <table className="data-table">
              <thead><tr><th>Actif</th><th className="numeric">Quantité</th><th className="numeric">Coût moyen</th><th className="numeric">Prix simulé</th><th className="numeric">Valeur</th><th className="numeric">Gain/perte</th><th className="numeric">%</th></tr></thead>
              <tbody>{data.positions.map((position) => {
                const positif = position["Gain/perte ($)"] >= 0;
                return <tr key={position.Actif}><td>{position.Actif}</td><td className="numeric">{position["Quantité"]}</td><td className="numeric">{nombre(position["Coût moyen"])}</td><td className="numeric">{nombre(position["Prix actuel"])}</td><td className="numeric">{nombre(position.Valeur)}</td><td className={`numeric ${positif ? "text-positive" : "text-negative"}`}>{positif ? "+" : "−"}{nombre(Math.abs(position["Gain/perte ($)"]))}</td><td className={`numeric ${positif ? "text-positive" : "text-negative"}`}>{positif ? "+" : "−"}{nombre(Math.abs(position["Gain/perte (%)"]))} %</td></tr>;
              })}</tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}