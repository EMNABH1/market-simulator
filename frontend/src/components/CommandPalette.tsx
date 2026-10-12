"use client";

import { CandlestickChart, Command, Search, type LucideIcon } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { libelleActif } from "@/lib/api";
import type { Actif } from "@/components/MarketTicker";

export type PageId = "dashboard" | "markets" | "trading" | "portefeuille" | "risk" | "analysis" | "ai" | "stress" | "training" | "admin";
export type NavigationPage = { id: PageId; label: string; Icon: LucideIcon; available: boolean; description?: string };

type CommandItem =
  | { kind: "page"; id: PageId; label: string; Icon: LucideIcon; searchable: string }
  | { kind: "asset"; id: string; label: string; Icon: LucideIcon; searchable: string };

type ProprietesPalette = {
  pages: NavigationPage[];
  actifs: Actif[];
  onClose: () => void;
  onChoosePage: (page: PageId) => void;
  onChooseAsset: (symbole: string) => void;
};

// La palette n'est montée qu'ouverte : la recherche et la sélection repartent ainsi de zéro à chaque ouverture.
export default function CommandPalette({ open, ...proprietes }: ProprietesPalette & { open: boolean }) {
  if (!open) return null;
  return <PaletteOuverte {...proprietes} />;
}

function PaletteOuverte({ pages, actifs, onClose, onChoosePage, onChooseAsset }: ProprietesPalette) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const commands = useMemo<CommandItem[]>(() => [
    ...pages.map((page) => ({
      kind: "page" as const,
      id: page.id,
      label: page.label,
      Icon: page.Icon,
      searchable: `${page.label} ${page.description ?? ""}`.toLocaleLowerCase("fr"),
    })),
    ...actifs.map((actif) => ({
      kind: "asset" as const,
      id: actif.symbole,
      label: libelleActif(actif.symbole, actif.nom),
      Icon: CandlestickChart,
      searchable: `${actif.nom} ${actif.symbole}`.toLocaleLowerCase("fr"),
    })),
  ], [pages, actifs]);
  const filtered = commands.filter((item) => item.searchable.includes(query.trim().toLocaleLowerCase("fr")));

  const indexActif = Math.min(selected, Math.max(0, filtered.length - 1));

  useEffect(() => {
    const frame = requestAnimationFrame(() => inputRef.current?.focus());
    return () => cancelAnimationFrame(frame);
  }, []);

  function choisir(item: CommandItem) {
    if (item.kind === "page") onChoosePage(item.id);
    else onChooseAsset(item.id);
    onClose();
  }

  return (
    <div className="command-overlay" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section aria-label="Palette de commandes" aria-modal="true" className="command-palette" role="dialog">
        <div className="command-search-row">
          <Search aria-hidden="true" size={18} />
          <input
            ref={inputRef}
            aria-label="Rechercher une page ou un actif"
            onChange={(event) => { setQuery(event.target.value); setSelected(0); }}
            onKeyDown={(event) => {
              if (event.key === "Escape") { event.preventDefault(); onClose(); }
              if (event.key === "ArrowDown") { event.preventDefault(); setSelected(Math.min(indexActif + 1, filtered.length - 1)); }
              if (event.key === "ArrowUp") { event.preventDefault(); setSelected(Math.max(indexActif - 1, 0)); }
              if (event.key === "Enter" && filtered[indexActif]) { event.preventDefault(); choisir(filtered[indexActif]); }
            }}
            placeholder="Aller à une page ou changer d’actif…"
            value={query}
          />
          <kbd>Esc</kbd>
        </div>
        <p className="command-section-label">Pages et actifs</p>
        <div className="command-results">
          {filtered.length ? filtered.map((item, index) => {
            const Icon = item.Icon;
            return (
              <button
                aria-current={index === indexActif ? "true" : undefined}
                className="command-result"
                key={`${item.kind}-${item.id}`}
                onClick={() => choisir(item)}
                onMouseEnter={() => setSelected(index)}
                type="button"
              >
                <Icon aria-hidden="true" size={17} />
                <span>{item.label}</span>
                {item.kind === "asset" && <span className="command-kind">Actif</span>}
              </button>
            );
          }) : <p className="command-empty">Aucun résultat.</p>}
        </div>
        <footer className="command-footer"><Command aria-hidden="true" size={14} /> Ctrl K pour ouvrir</footer>
      </section>
    </div>
  );
}
