"use client";

import { useEffect, useState } from "react";
import { apiJson } from "@/lib/api";
import type { Actif } from "@/components/MarketTicker";

export type Marche = {
  id: string;
  nom: string;
  description: string;
  disponible: boolean;
  actifs: Actif[];
};

export default function MarketSelector({
  token,
  onChoose,
}: {
  token: string;
  // simDate : date simulée après le choix (elle peut avoir avancé pour atteindre le début des données)
  onChoose: (marche: Marche, simDate: string) => void;
}) {
  const [marches, setMarches] = useState<Marche[] | null>(null);
  const [erreur, setErreur] = useState("");
  const [envoi, setEnvoi] = useState(false);

  useEffect(() => {
    let annule = false;
    apiJson<Marche[]>("/api/marches", {}, token)
      .then((data) => { if (!annule) setMarches(data); })
      .catch((cause: unknown) => {
        if (!annule) setErreur(cause instanceof Error ? cause.message : "Marchés indisponibles.");
      });
    return () => { annule = true; };
  }, [token]);

  async function choisir(marche: Marche) {
    setErreur("");
    setEnvoi(true);
    try {
      const reponse = await apiJson<{ marche: string; sim_date: string }>(
        `/api/marches/${encodeURIComponent(marche.id)}/choisir`,
        { method: "POST" },
        token,
      );
      onChoose(marche, reponse.sim_date);
    } catch (cause) {
      setErreur(cause instanceof Error ? cause.message : "Choix du marché impossible.");
    } finally {
      setEnvoi(false);
    }
  }

  if (!marches) {
    return erreur
      ? <p role="alert" className="error-state">{erreur}</p>
      : <p role="status" className="loading-state">Chargement des marchés…</p>;
  }

  return (
    <div className="mx-auto max-w-3xl space-y-5 p-6">
      <div>
        <h1 className="text-2xl font-semibold">Choisissez votre marché</h1>
        <p className="text-secondary">Votre solde est commun à tous les marchés.</p>
      </div>
      {erreur && <p role="alert" className="inline-error">{erreur}</p>}
      <div className="grid gap-4 sm:grid-cols-2">
        {marches.map((marche) => (
          <button
            key={marche.id}
            type="button"
            disabled={!marche.disponible || envoi}
            onClick={() => choisir(marche)}
            className="stat-item text-left disabled:opacity-50"
          >
            <p className="text-lg font-semibold">{marche.nom}</p>
            <p className="text-secondary">{marche.description}</p>
            <p className="mt-2 text-sm">
              {marche.disponible ? `${marche.actifs.length} actifs` : "Bientôt disponible"}
            </p>
          </button>
        ))}
      </div>
    </div>
  );
}