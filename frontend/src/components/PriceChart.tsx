"use client";

import { useEffect, useRef, useState } from "react";
import {
  createChart,
  CandlestickSeries,
  HistogramSeries,
  LineSeries,
  type IChartApi,
  type MouseEventParams,
  type Time,
} from "lightweight-charts";

type Bougie = { time: string; open: number; high: number; low: number; close: number; volume: number };
type DetailBougie = Omit<Bougie, "time"> & { time: Time; dateLabel: string };

const API = "http://127.0.0.1:8000";
const HAUTEUR_SECOURS = 420;

// Garde uniquement des bougies complètes, finies, non postérieures à la date simulée, triées et sans doublon de date.
// Les prix négatifs restent valides (WTI du 2020-04-20).
function bougiesValides(brut: unknown, jusqua: string): Bougie[] {
  if (!Array.isArray(brut)) return [];
  const parDate = new Map<string, Bougie>();
  for (const item of brut) {
    if (typeof item !== "object" || item === null) continue;
    const { time, open, high, low, close, volume } = item as Record<string, unknown>;
    if (typeof time !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(time) || time > jusqua) continue;
    if (![open, high, low, close].every((v) => typeof v === "number" && Number.isFinite(v))) continue;
    parDate.set(time, {
      time,
      open: open as number,
      high: high as number,
      low: low as number,
      close: close as number,
      volume: typeof volume === "number" && Number.isFinite(volume) && volume >= 0 ? volume : 0,
    });
  }
  return [...parDate.values()].sort((a, b) => (a.time < b.time ? -1 : a.time > b.time ? 1 : 0));
}

function sma(data: Bougie[], p: number) {
  return data
    .map((d, i) =>
      i < p - 1
        ? null
        : {
            time: d.time,
            value: data.slice(i - p + 1, i + 1).reduce((s, x) => s + x.close, 0) / p,
          }
    )
    .filter((x): x is { time: string; value: number } => x !== null);
}

export default function PriceChart({
  symbole = "GC=F",
  jours = 90,
  jusqua,
  theme,
}: {
  symbole?: string;
  jours?: number;
  jusqua: string;
  theme: "dark" | "light";
}) {
  const ref = useRef<HTMLDivElement>(null);
  const cle = `${symbole}|${jours}|${jusqua}`;
  // État rangé avec la requête qui l'a produit : changer d'actif, de période ou de date l'invalide sans remise à zéro.
  const [etat, setEtat] = useState<{ cle: string; erreur: string | null; vide: boolean } | null>(null);
  const [survol, setSurvol] = useState<{ cle: string; detail: DetailBougie | null } | null>(null);
  const erreur = etat?.cle === cle ? etat.erreur : null;
  const vide = etat?.cle === cle && etat.vide;
  const detail = survol?.cle === cle ? survol.detail : null;

  useEffect(() => {
    let chart: IChartApi | null = null;
    const controller = new AbortController();
    // La hauteur vient du CSS (.chart-canvas) ; la valeur de secours évite un graphique de 0 px si le style manque.
    const dimensions = (el: HTMLElement) => ({
      width: Math.max(el.clientWidth, 1),
      height: el.clientHeight > 0 ? el.clientHeight : HAUTEUR_SECOURS,
    });
    const resizeObserver = new ResizeObserver(() => {
      if (!chart || !ref.current) return;
      const { width, height } = dimensions(ref.current);
      chart.resize(width, height);
    });
    const query = new URLSearchParams({ jours: String(jours), jusqua });
    const setDetail = (valeur: DetailBougie | null) => setSurvol({ cle, detail: valeur });

    fetch(`${API}/api/prix/${encodeURIComponent(symbole)}?${query}`, { signal: controller.signal })
      .then((r) => {
        if (!r.ok) throw new Error(`Erreur API ${r.status}`);
        return r.json();
      })
      .then((brut: unknown) => {
        if (controller.signal.aborted || !ref.current) return;
        const bougies = bougiesValides(brut, jusqua);
        if (bougies.length === 0) {
          setEtat({ cle, erreur: null, vide: true });
          return;
        }
        const styles = getComputedStyle(ref.current);
        const jeton = (nom: string) => styles.getPropertyValue(nom).trim();
        chart = createChart(ref.current, {
          ...dimensions(ref.current),
          layout: { textColor: jeton("--text-secondary"), background: { color: jeton("--panel") } },
          grid: { vertLines: { visible: false }, horzLines: { color: jeton("--line") } },
          rightPriceScale: { borderVisible: false, scaleMargins: { top: 0.08, bottom: 0.22 } },
          timeScale: { borderVisible: false },
        });
        const candles = chart.addSeries(CandlestickSeries, {
          upColor: jeton("--positive"),
          downColor: jeton("--negative"),
          borderVisible: false,
          wickUpColor: jeton("--positive"),
          wickDownColor: jeton("--negative"),
        });
        candles.setData(bougies);
        const ligne = chart.addSeries(LineSeries, { color: jeton("--active-accent"), lineWidth: 2 });
        ligne.setData(sma(bougies, 20));
        const volume = chart.addSeries(HistogramSeries, {
          priceScaleId: "volume",
          priceFormat: { type: "volume" },
          priceLineVisible: false,
          lastValueVisible: false,
        });
        volume.setData(bougies.map((bougie) => ({
          time: bougie.time,
          value: bougie.volume,
          color: bougie.close >= bougie.open ? jeton("--positive") : jeton("--negative"),
        })));
        chart.priceScale("volume").applyOptions({ scaleMargins: { top: 0.82, bottom: 0 }, visible: false });

        const onCrosshair = (event: MouseEventParams<Time>) => {
          if (!event.time) {
            setDetail(null);
            return;
          }
          const candle = event.seriesData.get(candles);
          if (!candle || !("open" in candle)) {
            setDetail(null);
            return;
          }
          const volumePoint = event.seriesData.get(volume);
          setDetail({
            time: event.time,
            dateLabel: dateLabel(event.time),
            open: candle.open,
            high: candle.high,
            low: candle.low,
            close: candle.close,
            volume: volumePoint && "value" in volumePoint ? volumePoint.value : bougies.find((item) => item.time === event.time)?.volume ?? 0,
          });
        };
        chart.subscribeCrosshairMove(onCrosshair);
        chart.timeScale().fitContent();
        resizeObserver.observe(ref.current);
      })
      .catch(() => {
        if (!controller.signal.aborted) setEtat({ cle, erreur: "Impossible de charger les prix. Le backend est-il lancé ?", vide: false });
      });

    return () => {
      controller.abort();
      resizeObserver.disconnect();
      chart?.remove();
      chart = null;
    };
  }, [cle, symbole, jours, jusqua, theme]);

  if (erreur) return <p className="error-state">{erreur}</p>;
  if (vide) return <p className="loading-state">Aucune cotation disponible à cette date.</p>;
  return (
    <div className="chart-frame">
      {detail && <div aria-live="polite" className="chart-ohlcv-tooltip">
        <time>{detail.dateLabel}</time>
        <span>Ouverture <b>{detail.open.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b></span>
        <span>Haut <b>{detail.high.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b></span>
        <span>Bas <b>{detail.low.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b></span>
        <span>Clôture <b>{detail.close.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b></span>
        <span>Volume <b>{volumeCompact(detail.volume)}</b></span>
      </div>}
      <div ref={ref} className="chart-canvas" />
    </div>
  );
}

function volumeCompact(value: number): string {
  return new Intl.NumberFormat("fr-FR", { notation: "compact", maximumFractionDigits: 1 }).format(value);
}

function dateLabel(time: Time): string {
  if (typeof time === "string") return time;
  if (typeof time === "number") return new Date(time * 1000).toLocaleDateString("fr-FR");
  return `${time.year}-${String(time.month).padStart(2, "0")}-${String(time.day).padStart(2, "0")}`;
}