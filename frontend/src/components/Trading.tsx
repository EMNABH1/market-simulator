"use client";

import { useEffect, useState, type FormEvent } from "react";
import { apiJson, libelleActif } from "@/lib/api";

type Actif = { symbole: string; nom: string };
type Bougie = { time: string; close: number };
type Ordre = { id: number; asset: string; side: "ACHAT" | "VENTE"; quantity: number; price: number; sim_date: string };

const nombre = (value: number) => value.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const quantiteTexte = (value: number) => value.toLocaleString("fr-FR", { maximumFractionDigits: 8 });

export default function Trading({
  token,
  actifs,
  symboleInitial,
  simDate,
  onTrade,
}: {
  token: string;
  actifs: Actif[];
  symboleInitial: string;
  simDate: string;
  onTrade: () => void;
}) {
  const [symbole, setSymbole] = useState(symboleInitial);
  const [sens, setSens] = useState<"ACHAT" | "VENTE">("ACHAT");
  const [quantite, setQuantite] = useState(1);
  const [prix, setPrix] = useState<number | null>(null);
  const [ordres, setOrdres] = useState<Ordre[]>([]);
  const [erreur, setErreur] = useState("");
  const [resultat, setResultat] = useState("");
  const [envoi, setEnvoi] = useState(false);

  useEffect(() => {
    let annule = false;
    const query = new URLSearchParams({ jours: "1", jusqua: simDate });
    Promise.all([
      apiJson<Bougie[]>(`/api/prix/${encodeURIComponent(symbole)}?${query}`),
      apiJson<Ordre[]>("/api/ordres", {}, token),
    ])
      .then(([bougies, historique]) => {
        if (annule) return;
        setPrix(bougies.length ? bougies[bougies.length - 1].close : null);
        setOrdres(historique.slice().reverse());
      })
      .catch((cause: unknown) => {
        if (!annule) setErreur(cause instanceof Error ? cause.message : "Chargement impossible.");
      });
    return () => { annule = true; };
  }, [symbole, simDate, token]);

  async function passerOrdre(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErreur("");
    setResultat("");
    setEnvoi(true);
    try {
      const response = await apiJson<{ message: string }>("/api/ordres", {
        method: "POST",
        body: JSON.stringify({ symbole, sens, quantite }),
      }, token);
      setResultat(response.message);
      const historique = await apiJson<Ordre[]>("/api/ordres", {}, token);
      setOrdres(historique.slice().reverse());
      onTrade();
    } catch (cause) {
      setErreur(cause instanceof Error ? cause.message : "Ordre refusé.");
    } finally {
      setEnvoi(false);
    }
  }

  const montant = prix === null ? null : prix * quantite;

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold">Trading</h1>
        <p className="text-secondary">Ordres exécutés au cours connu le {simDate}.</p>
      </div>
      <section className="trade-ticket">
        <form className="space-y-4" onSubmit={passerOrdre}>
          <label className="block text-sm font-medium">
            Actif
            <select value={symbole} onChange={(event) => setSymbole(event.target.value)}>
              {actifs.map((actif) => <option key={actif.symbole} value={actif.symbole}>{libelleActif(actif.symbole, actif.nom)}</option>)}
            </select>
          </label>
          <fieldset>
            <legend className="mb-1.5 text-sm font-medium">Sens de l’ordre</legend>
            <div className="side-toggle">
              {(["ACHAT", "VENTE"] as const).map((option) => (
                <button key={option} type="button" aria-pressed={sens === option} onClick={() => setSens(option)} className={`segmented-button ${sens === option ? option === "ACHAT" ? "trade-side-buy" : "trade-side-sell" : ""}`}>
                  {option}
                </button>
              ))}
            </div>
          </fieldset>
          <label className="block text-sm font-medium">
            Quantité
            <input type="number" min="0" step="any" required value={quantite} onChange={(event) => setQuantite(Math.max(0, Number(event.target.value)))} />
          </label>
          <div className="estimate-row">
            <span className="text-secondary">Cours connu · Montant estimé</span>
            <span className="text-right font-mono font-semibold">
              {prix === null ? "Cours indisponible" : `${nombre(prix)} USD · ${nombre(montant ?? 0)} USD`}
            </span>
          </div>
          {prix !== null && prix <= 0 && <p className="inline-warning">Cours nul ou négatif à cette date : l’ordre sera refusé.</p>}
          {erreur && <p role="alert" className="inline-error">{erreur}</p>}
          {resultat && <p role="status" className="inline-success">{resultat}</p>}
          <button type="submit" disabled={envoi || prix === null || quantite <= 0} className="primary-button">
            {envoi ? "Exécution…" : sens === "ACHAT" ? "Confirmer l’achat" : "Confirmer la vente"}
          </button>
        </form>
      </section>

      <section>
        <h2 className="panel-heading">Ordres récents</h2>
        {ordres.length === 0 ? <p className="text-secondary">Aucun ordre pour le moment.</p> : (
          <div className="table-wrap">
            <table className="data-table">
              <thead><tr><th>Date simulée</th><th>Actif</th><th>Sens</th><th className="numeric">Quantité</th><th className="numeric">Cours</th></tr></thead>
              <tbody>{ordres.map((ordre) => <tr key={ordre.id}><td>{ordre.sim_date}</td><td>{ordre.asset}</td><td className={ordre.side === "ACHAT" ? "trade-direction-positive" : "trade-direction-negative"}>{ordre.side}</td><td className="numeric">{quantiteTexte(ordre.quantity)}</td><td className="numeric">{nombre(ordre.price)} USD</td></tr>)}</tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}