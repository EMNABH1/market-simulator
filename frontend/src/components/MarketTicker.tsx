"use client";

import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { libelleActif } from "@/lib/api";

export type Actif = { symbole: string; nom: string };
export type CoursActif = {
  dernier: number;
  variation: number;
  variation_pct: number;
  date: string;
};

function nombre(value: number): string {
  return value.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function variation(value: number): string {
  const prefix = value > 0 ? "+" : value < 0 ? "−" : "";
  return `${prefix}${nombre(Math.abs(value))} %`;
}

export default function MarketTicker({
  actifs,
  cours,
  symboleActif,
  dateSimulation,
  chargement,
  onSelect,
}: {
  actifs: Actif[];
  cours: Record<string, CoursActif | null>;
  symboleActif: string;
  dateSimulation: string;
  chargement: boolean;
  onSelect: (symbole: string) => void;
}) {
  const coursPrecedents = useRef<Record<string, number>>({});
  const [flashs, setFlashs] = useState<string[]>([]);

  useEffect(() => {
    if (chargement) return;
    const changes = actifs
      .filter((actif) => {
        const quote = cours[actif.symbole];
        return quote && coursPrecedents.current[actif.symbole] !== undefined && coursPrecedents.current[actif.symbole] !== quote.dernier;
      })
      .map((actif) => actif.symbole);
    coursPrecedents.current = Object.fromEntries(actifs.flatMap((actif) => {
      const quote = cours[actif.symbole];
      return quote ? [[actif.symbole, quote.dernier] as const] : [];
    }));
    if (!changes.length) return;
    setFlashs(changes);
    const timer = window.setTimeout(() => setFlashs([]), 400);
    return () => window.clearTimeout(timer);
  }, [actifs, chargement, cours]);

  return (
    <section className="market-ticker" aria-label={`Cotations à la date simulée du ${dateSimulation}`}>
      <div className="ticker-heading">
        <span>Cotations</span>
        <span className="ticker-date">Au {dateSimulation}</span>
      </div>
      <div className="ticker-track" aria-live="polite">
        {actifs.map((actif) => {
          const quote = cours[actif.symbole];
          const direction = quote?.variation === undefined ? "neutral" : quote.variation > 0 ? "positive" : quote.variation < 0 ? "negative" : "neutral";
          const DirectionIcon = direction === "positive" ? ArrowUpRight : direction === "negative" ? ArrowDownRight : Minus;
          return (
            <button
              className="ticker-item"
              data-selected={symboleActif === actif.symbole}
              key={actif.symbole}
              onClick={() => onSelect(actif.symbole)}
              type="button"
              aria-label={`${libelleActif(actif.symbole, actif.nom)}${quote ? `, ${nombre(quote.dernier)}, variation ${variation(quote.variation_pct)}` : chargement ? ", cotation en chargement" : ", cotation indisponible"}`}
            >
              <span className="ticker-name">{libelleActif(actif.symbole, actif.nom)}</span>
              <span className="ticker-quote">
                {quote ? <span data-flash={flashs.includes(actif.symbole)}>{nombre(quote.dernier)}</span> : "—"}
              </span>
              <span className={`ticker-change direction-${direction}`}>
                {quote ? <><DirectionIcon size={14} strokeWidth={2} aria-hidden="true" />{variation(quote.variation_pct)}</> : chargement ? "Chargement…" : "Cotation indisponible"}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
