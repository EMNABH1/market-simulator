"use client";

import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";
import { useEffect, useRef } from "react";
import { createChart, LineSeries, type IChartApi, type Time } from "lightweight-charts";
import { apiJson, libelleActif } from "@/lib/api";
import type { Actif, CoursActif } from "@/components/MarketTicker";

type Point = { time: Time; close: number };
type PrixApi = { time: string; close: number };

function nombre(value: number): string {
  return value.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function Sparkline({ symbole, jusqua }: { symbole: string; jusqua: string }) {
  const host = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let chart: IChartApi | null = null;
    let annule = false;
    const query = new URLSearchParams({ jours: "30", jusqua });
    apiJson<PrixApi[]>(`/api/prix/${encodeURIComponent(symbole)}?${query}`)
      .then((data) => {
        if (annule || !host.current || data.length === 0) return;
        const styles = getComputedStyle(host.current);
        chart = createChart(host.current, {
          width: host.current.clientWidth,
          height: 38,
          layout: { background: { color: "transparent" }, textColor: styles.getPropertyValue("--text-secondary").trim() },
          grid: { vertLines: { visible: false }, horzLines: { visible: false } },
          rightPriceScale: { visible: false },
          leftPriceScale: { visible: false },
          timeScale: { visible: false, borderVisible: false },
          crosshair: { vertLine: { visible: false }, horzLine: { visible: false } },
          handleScroll: false,
          handleScale: false,
        });
        const line = chart.addSeries(LineSeries, {
          color: styles.getPropertyValue("--market-accent").trim(),
          lineWidth: 1,
          priceLineVisible: false,
          lastValueVisible: false,
        });
        const points: Point[] = data.map((item) => ({ time: item.time as Time, close: item.close }));
        line.setData(points.map((item) => ({ time: item.time, value: item.close })));
        chart.timeScale().fitContent();
      })
      .catch(() => undefined);

    return () => {
      annule = true;
      chart?.remove();
    };
  }, [symbole, jusqua]);

  return <div aria-hidden="true" className="market-sparkline" data-asset={symbole} ref={host} />;
}

export default function MarketPanel({
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
  return (
    <aside aria-label="Marchés" className="market-panel">
      <header className="market-panel-heading">
        <h2>Marchés</h2>
        <span>Au {dateSimulation}</span>
      </header>
      <div aria-busy={chargement} className="market-watchlist">
        {actifs.map((actif) => {
          const quote = cours[actif.symbole];
          const direction = quote ? quote.variation > 0 ? "positive" : quote.variation < 0 ? "negative" : "neutral" : "neutral";
          const DirectionIcon = direction === "positive" ? ArrowUpRight : direction === "negative" ? ArrowDownRight : Minus;
          return (
            <div
              aria-current={symboleActif === actif.symbole ? "true" : undefined}
              aria-label={`${libelleActif(actif.symbole, actif.nom)}${quote ? `, prix ${nombre(quote.dernier)}, variation ${nombre(Math.abs(quote.variation_pct))} pour cent` : ", cotation indisponible"}`}
              className="market-watch-item"
              data-asset={actif.symbole}
              key={actif.symbole}
              onClick={() => onSelect(actif.symbole)}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  onSelect(actif.symbole);
                }
              }}
              role="button"
              tabIndex={0}
            >
              <div className="market-watch-head">
                <span className="market-watch-name">{libelleActif(actif.symbole, actif.nom)}</span>
                <span className="market-watch-symbol">{actif.symbole}</span>
              </div>
              <div className="market-watch-quote">
                <strong>{quote ? nombre(quote.dernier) : "—"}</strong>
                <span className={`direction-${direction}`}>
                  {quote ? <><DirectionIcon aria-hidden="true" size={13} />{quote.variation > 0 ? "+" : quote.variation < 0 ? "−" : ""}{nombre(Math.abs(quote.variation_pct))} %</> : chargement ? "Chargement…" : "Indisponible"}
                </span>
              </div>
              <Sparkline symbole={actif.symbole} jusqua={dateSimulation} />
            </div>
          );
        })}
      </div>
    </aside>
  );
}
