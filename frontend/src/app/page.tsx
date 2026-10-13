"use client";

import GraphiqueOr from "@/components/Or/GraphiqueOr";
import StatsOr from "@/components/Or/StatsOr";
import Connexion from "@/components/Connexion";
import CommandPalette, { type NavigationPage, type PageId } from "@/components/CommandPalette";
import DashboardMetrics from "@/components/DashboardMetrics";
import Formation from "@/components/Formation";
import MarketSelector, { type Marche } from "@/components/MarketSelector";
import MarketTicker, { type CoursActif } from "@/components/MarketTicker";
import MarketPanel from "@/components/MarketPanel";
import Portefeuille from "@/components/Portefeuille";
import SimulationBar, { type VitesseSimulation } from "@/components/SimulationBar";
import Trading from "@/components/Trading";
import { apiJson, libelleActif } from "@/lib/api";
import {
  Activity,
  ArrowLeftRight,
  BrainCircuit,
  ChartCandlestick,
  ChartNoAxesCombined,
  GraduationCap,
  LayoutDashboard,
  Menu,
  Moon,
  PanelLeftClose,
  PanelLeftOpen,
  Repeat,
  Search,
  Settings,
  Shield,
  Sun,
  WalletCards,
  X,
} from "lucide-react";
import { useEffect, useEffectEvent, useMemo, useState } from "react";

type Utilisateur = { id: number; username: string; role: string; cash: number; sim_date: string };
type Theme = "dark" | "light";

const CLE_MARCHE = "market-simulator-marche";

const nav: NavigationPage[] = [
  { id: "dashboard", label: "Tableau de bord", Icon: LayoutDashboard, available: true },
  { id: "markets", label: "Marchés", Icon: ChartCandlestick, available: true, description: "Consulter les actifs et leurs cotations." },
  { id: "trading", label: "Trading", Icon: ArrowLeftRight, available: true },
  { id: "portefeuille", label: "Portefeuille", Icon: WalletCards, available: true },
  { id: "risk", label: "Risque", Icon: Shield, available: false, description: "Mesurer le risque et l’exposition du portefeuille." },
  { id: "analysis", label: "Analyse et backtesting", Icon: ChartNoAxesCombined, available: false, description: "Étudier des stratégies et leurs performances historiques." },
  { id: "ai", label: "IA et prévisions", Icon: BrainCircuit, available: false, description: "Explorer les prévisions et les analyses assistées par IA." },
  { id: "stress", label: "Stress testing", Icon: Activity, available: false, description: "Évaluer le portefeuille dans des scénarios de marché extrêmes." },
  { id: "training", label: "Formation", Icon: GraduationCap, available: true, description: "Apprendre les marchés et progresser du niveau débutant au niveau expert." },
  { id: "admin", label: "Administration", Icon: Settings, available: false, description: "Gérer les comptes et les paramètres de la plateforme." },
];

function lireThemeEnregistre(): Theme {
  if (typeof window === "undefined") return "dark";
  try {
    return localStorage.getItem("market-simulator-theme") === "light" ? "light" : "dark";
  } catch {
    return "dark";
  }
}

function formaterNombre(value: number): string {
  return value.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export default function Dashboard() {
  // Le marché choisi détermine la liste des actifs affichés partout dans l'application.
  const [marche, setMarche] = useState<Marche | null>(null);
  const [marchePrete, setMarchePrete] = useState(false);
  const actifs = useMemo(() => marche?.actifs ?? [], [marche]);
  const [symbole, setSymbole] = useState("");
  // Les résultats asynchrones sont rangés avec la date simulée qui les a produits : un résultat d'une autre date n'est jamais affiché.
  const [coursCharges, setCoursCharges] = useState<{ date: string; cours: Record<string, CoursActif | null> } | null>(null);
  const [alerteWti, setAlerteWti] = useState<{ date: string; prixNonPositif: boolean } | null>(null);
  const [erreurActifs, setErreurActifs] = useState(false);
  const [token, setToken] = useState("");
  const [utilisateur, setUtilisateur] = useState<Utilisateur | null>(null);
  const [sessionPrete, setSessionPrete] = useState(false);
  const [vue, setVue] = useState<PageId>("dashboard");
  const [rafraichissement, setRafraichissement] = useState(0);
  const [theme, setTheme] = useState<Theme>(lireThemeEnregistre);
  const [railReplie, setRailReplie] = useState(false);
  const [menuMobileOuvert, setMenuMobileOuvert] = useState(false);
  const [paletteOuverte, setPaletteOuverte] = useState(false);
  const [lecture, setLecture] = useState(false);
  const [vitesse, setVitesse] = useState<VitesseSimulation>(1);
  const [avancementEnCours, setAvancementEnCours] = useState(false);
  const [messageTemps, setMessageTemps] = useState("");
  const dateSimulation = utilisateur?.sim_date;

  // Restaure le marché choisi lors d'une précédente visite (et recale la date simulée si besoin).
  useEffect(() => {
    if (!token) return;
    const controller = new AbortController();
    const idEnregistre = localStorage.getItem(CLE_MARCHE);
    if (!idEnregistre) {
      setMarchePrete(true);
      return;
    }
    apiJson<Marche[]>("/api/marches", { signal: controller.signal }, token)
      .then(async (liste) => {
        const trouve = liste.find((item) => item.id === idEnregistre && item.disponible);
        if (!trouve) {
          localStorage.removeItem(CLE_MARCHE);
          return;
        }
        const reponse = await apiJson<{ sim_date: string }>(
          `/api/marches/${encodeURIComponent(trouve.id)}/choisir`,
          { method: "POST", signal: controller.signal },
          token,
        );
        if (controller.signal.aborted) return;
        setMarche(trouve);
        setSymbole(trouve.actifs[0].symbole);
        setUtilisateur((courant) => (courant ? { ...courant, sim_date: reponse.sim_date } : courant));
      })
      .catch(() => {
        if (!controller.signal.aborted) {
          localStorage.removeItem(CLE_MARCHE);
          setErreurActifs(true);
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setMarchePrete(true);
      });
    return () => controller.abort();
  }, [token]);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  useEffect(() => {
    if (!dateSimulation || actifs.length === 0) return;
    const controller = new AbortController();
    Promise.all(actifs.map(async (actif) => {
      const query = new URLSearchParams({ jusqua: dateSimulation });
      try {
        const quote = await apiJson<CoursActif>(
          `/api/resume/${encodeURIComponent(actif.symbole)}?${query}`,
          { signal: controller.signal },
        );
        return [actif.symbole, quote] as const;
      } catch {
        return [actif.symbole, null] as const;
      }
    })).then((entries) => {
      if (!controller.signal.aborted) setCoursCharges({ date: dateSimulation, cours: Object.fromEntries(entries) });
    });
    return () => controller.abort();
  }, [actifs, dateSimulation]);
  const coursAJour = coursCharges !== null && coursCharges.date === dateSimulation;
  const cours = coursAJour ? coursCharges.cours : {};
  const chargementCours = actifs.length === 0 || (Boolean(dateSimulation) && !coursAJour);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.code === "KeyK") {
        event.preventDefault();
        setPaletteOuverte((open) => !open);
      }
      if (event.key === "Escape") {
        setPaletteOuverte(false);
        setMenuMobileOuvert(false);
      }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    const storedToken = localStorage.getItem("market-simulator-token");
    const verification = storedToken
      ? apiJson<Utilisateur>("/api/moi", { signal: controller.signal }, storedToken)
        .then((currentUser) => {
          if (controller.signal.aborted) return;
          setToken(storedToken);
          setUtilisateur(currentUser);
        })
        .catch(() => {
          localStorage.removeItem("market-simulator-token");
        })
      : Promise.resolve();

    verification
      .finally(() => {
        if (!controller.signal.aborted) setSessionPrete(true);
      });
    return () => controller.abort();
  }, []);

  async function connecter(newToken: string) {
    const currentUser = await apiJson<Utilisateur>("/api/moi", {}, newToken);
    localStorage.setItem("market-simulator-token", newToken);
    setToken(newToken);
    setUtilisateur(currentUser);
    setSessionPrete(true);
  }

  function deconnecter() {
    localStorage.removeItem("market-simulator-token");
    localStorage.removeItem(CLE_MARCHE);
    setToken("");
    setUtilisateur(null);
    setMarche(null);
    setMarchePrete(false);
    setSymbole("");
    setCoursCharges(null);
    setVue("dashboard");
    setLecture(false);
  }

  function choisirMarche(nouveau: Marche, simDate: string) {
    localStorage.setItem(CLE_MARCHE, nouveau.id);
    setMarche(nouveau);
    setSymbole(nouveau.actifs[0].symbole);
    setCoursCharges(null);
    setUtilisateur((courant) => (courant ? { ...courant, sim_date: simDate } : courant));
    setVue("dashboard");
    setErreurActifs(false);
  }

  function changerMarche() {
    localStorage.removeItem(CLE_MARCHE);
    setMarche(null);
    setSymbole("");
    setCoursCharges(null);
    setLecture(false);
    setVue("dashboard");
    setMenuMobileOuvert(false);
  }

  async function actualiserCompte() {
    setRafraichissement((current) => current + 1);
    if (!token) return;
    try {
      setUtilisateur(await apiJson<Utilisateur>("/api/moi", {}, token));
    } catch {
      deconnecter();
    }
  }

  async function lireCompteCourant() {
    if (!token) return null;
    const current = await apiJson<Utilisateur>("/api/moi", {}, token);
    setUtilisateur(current);
    return current;
  }

  async function avancerProchaineSeance(): Promise<boolean> {
    if (!token || actifs.length === 0 || avancementEnCours) return false;
    setAvancementEnCours(true);
    setMessageTemps("");
    try {
      for (let jourCalendaire = 0; jourCalendaire < 10; jourCalendaire += 1) {
        const avance = await apiJson<{ sim_date: string }>("/api/simulation/avancer", {
          method: "POST",
          body: JSON.stringify({ jours: 1 }),
        }, token);
        const dateAtteinte = avance.sim_date;
        const requetes = await Promise.all(actifs.map(async (item) => {
          const query = new URLSearchParams({ jours: "1", jusqua: dateAtteinte });
          try {
            const bougies = await apiJson<{ time: string }[]>(
              `/api/prix/${encodeURIComponent(item.symbole)}?${query}`,
            );
            return bougies.some((bougie) => bougie.time === dateAtteinte);
          } catch {
            return false;
          }
        }));
        if (requetes.some(Boolean)) {
          await lireCompteCourant();
          setRafraichissement((current) => current + 1);
          return true;
        }
      }
      await lireCompteCourant();
      setMessageTemps("Aucune séance n’a été trouvée dans les dix prochains jours.");
      setLecture(false);
      return false;
    } catch (cause) {
      try {
        await lireCompteCourant();
      } catch {
        deconnecter();
      }
      const detail = cause instanceof Error ? cause.message : "Avancement impossible.";
      if (detail.toLocaleLowerCase("fr").includes("fin des données")) {
        setMessageTemps("Fin de l’historique des cotations atteinte.");
      } else {
        setMessageTemps(detail);
      }
      setLecture(false);
      return false;
    } finally {
      setAvancementEnCours(false);
    }
  }

  const avancerEtape = useEffectEvent(() => avancerProchaineSeance());

  useEffect(() => {
    if (!lecture) return;
    let annule = false;
    let timer: number | undefined;
    const tick = async () => {
      const continuer = await avancerEtape();
      if (!annule && continuer) {
        timer = window.setTimeout(tick, Math.max(50, 1000 / vitesse));
      }
    };
    timer = window.setTimeout(tick, 0);
    return () => {
      annule = true;
      if (timer !== undefined) window.clearTimeout(timer);
    };
  }, [lecture, vitesse]);

  async function avancerPeriode(jours: 7 | 30) {
    if (!token || avancementEnCours) return;
    setLecture(false);
    setAvancementEnCours(true);
    setMessageTemps("");
    try {
      await apiJson("/api/simulation/avancer", {
        method: "POST",
        body: JSON.stringify({ jours }),
      }, token);
      await lireCompteCourant();
      setRafraichissement((current) => current + 1);
    } catch (cause) {
      try {
        await lireCompteCourant();
      } catch {
        deconnecter();
      }
      const detail = cause instanceof Error ? cause.message : "Avancement impossible.";
      setMessageTemps(detail.toLocaleLowerCase("fr").includes("fin des données")
        ? "Fin de l’historique des cotations atteinte."
        : detail);
    } finally {
      setAvancementEnCours(false);
    }
  }

  function basculerTheme() {
    const nextTheme = theme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
    try {
      localStorage.setItem("market-simulator-theme", nextTheme);
    } catch {
      // Le thème reste actif pour cette session si le stockage est indisponible.
    }
  }

  function choisirActif(nextSymbole: string) {
    setSymbole(nextSymbole);
    setVue("dashboard");
    setMenuMobileOuvert(false);
  }

  function choisirPage(nextPage: PageId) {
    setVue(nextPage);
    setMenuMobileOuvert(false);
  }

  const actif = actifs.find((item) => item.symbole === symbole);
  const pageActive = nav.find((item) => item.id === vue);

  const surveillerWti = vue === "dashboard" && symbole === "CL=F" && Boolean(dateSimulation);
  useEffect(() => {
    if (!surveillerWti || !dateSimulation) return;
    const controller = new AbortController();
    const query = new URLSearchParams({ jours: "1", jusqua: dateSimulation });
    apiJson<{ low: number; close: number }[]>(`/api/prix/CL%3DF?${query}`, { signal: controller.signal })
      .then((candles) => {
        if (!controller.signal.aborted) setAlerteWti({ date: dateSimulation, prixNonPositif: candles.some((candle) => candle.low <= 0 || candle.close <= 0) });
      })
      .catch(() => {
        if (!controller.signal.aborted) setAlerteWti({ date: dateSimulation, prixNonPositif: false });
      });
    return () => controller.abort();
  }, [surveillerWti, dateSimulation]);
  const prixNonPositif = surveillerWti && alerteWti?.date === dateSimulation && alerteWti?.prixNonPositif === true;

  if (!sessionPrete) {
    return <main className="auth-page"><p className="loading-state">Vérification de la session…</p></main>;
  }

  if (!token || !utilisateur) {
    return <Connexion onConnected={connecter} theme={theme} onToggleTheme={basculerTheme} />;
  }

  if (!marchePrete) {
    return <main className="auth-page"><p className="loading-state">Chargement de votre marché…</p></main>;
  }

  if (!marche) {
    return (
      <main className="auth-page">
        <div>
          <MarketSelector token={token} onChoose={choisirMarche} />
          <div className="mt-4 text-center">
            <button className="text-button logout-button" onClick={deconnecter} type="button">Déconnexion</button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <div className="app-shell" data-active-asset={symbole} data-rail-collapsed={railReplie}>
      {menuMobileOuvert && <button aria-label="Fermer le menu" className="mobile-menu-backdrop" onClick={() => setMenuMobileOuvert(false)} type="button" />}
      <aside className={`app-rail ${menuMobileOuvert ? "is-mobile-open" : ""}`}>
        <div className="rail-brand-row">
          <div aria-hidden="true" className="brand-mark"><ChartCandlestick size={21} /></div>
          <div className="rail-brand-copy"><span className="rail-brand-title">Salle de marché</span><span className="rail-brand-subtitle">Simulateur</span></div>
          <button aria-label={railReplie ? "Déplier le rail" : "Replier le rail"} className="icon-button rail-collapse-button" onClick={() => setRailReplie((value) => !value)} title={railReplie ? "Déplier le rail" : "Replier le rail"} type="button">
            {railReplie ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
          </button>
          <button aria-label="Fermer le menu" className="icon-button mobile-close-button" onClick={() => setMenuMobileOuvert(false)} type="button"><X size={18} /></button>
        </div>
        <nav aria-label="Navigation principale" className="rail-navigation">
          {nav.map(({ id, label, Icon }) => (
            <button aria-current={vue === id ? "page" : undefined} className="rail-nav-item" key={id} onClick={() => choisirPage(id)} title={railReplie ? label : undefined} type="button">
              <Icon aria-hidden="true" size={19} strokeWidth={1.8} />
              <span className="rail-nav-label">{label}</span>
            </button>
          ))}
          <button className="rail-nav-item" onClick={changerMarche} title={railReplie ? "Changer de marché" : undefined} type="button">
            <Repeat aria-hidden="true" size={19} strokeWidth={1.8} />
            <span className="rail-nav-label">Changer de marché</span>
          </button>
        </nav>
        <div className="rail-bottom"><span className="rail-bottom-dot" />{marche.nom}</div>
      </aside>

      <div className="app-main">
        <header className="app-topbar">
          <button aria-expanded={menuMobileOuvert} aria-label="Ouvrir la navigation" className="icon-button mobile-menu-button" onClick={() => setMenuMobileOuvert(true)} type="button"><Menu size={19} /></button>
          <div className="topbar-asset">
            <label htmlFor="actif">Actif</label>
            <select id="actif" value={symbole} onChange={(event) => choisirActif(event.target.value)} disabled={actifs.length === 0}>
              {actifs.length === 0 && <option value="">{erreurActifs ? "API indisponible" : "Chargement…"}</option>}
              {actifs.map((item) => <option key={item.symbole} value={item.symbole}>{libelleActif(item.symbole, item.nom)}</option>)}
            </select>
          </div>
          <button aria-keyshortcuts="Control+K" className="command-trigger" onClick={() => setPaletteOuverte(true)} type="button">
            <Search aria-hidden="true" size={16} /><span>Rechercher</span><kbd>Ctrl K</kbd>
          </button>
          <div className="topbar-spacer" />
          <button aria-label={theme === "dark" ? "Activer le thème clair" : "Activer le thème sombre"} className="icon-button theme-toggle" onClick={basculerTheme} title={theme === "dark" ? "Thème clair" : "Thème sombre"} type="button">
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>
          <div className="topbar-user"><span className="user-avatar">{utilisateur.username.slice(0, 1).toLocaleUpperCase("fr")}</span><span className="user-identity"><b>{utilisateur.username}</b><small>{utilisateur.role}</small></span></div>
          <button className="text-button logout-button" onClick={deconnecter} type="button">Déconnexion</button>
        </header>

        {erreurActifs && <div className="global-error" role="alert">Impossible de charger les actifs. Vérifie que l’API est disponible, puis recharge la page.</div>}
        <MarketTicker actifs={actifs} cours={cours} symboleActif={symbole} dateSimulation={utilisateur.sim_date} chargement={chargementCours} onSelect={choisirActif} />

        <main aria-busy={avancementEnCours} className="app-content">
          {vue === "dashboard" && <>
            <div className="page-heading"><h1>Tableau de bord</h1><p>{actif ? `Marché : ${actif.nom}` : marche.nom}</p></div>
            {actif ? <>
              <DashboardMetrics token={token} symbole={actif.symbole} quote={cours[actif.symbole] ?? null} simDate={utilisateur.sim_date} rafraichissement={rafraichissement} />
              {prixNonPositif && <p className="market-warning" role="alert">Prix négatif : trading suspendu pour le WTI à cette date.</p>}
              <div className="dashboard-layout">
                <div className="dashboard-primary">
                  <StatsOr key={`stats-${actif.symbole}-${utilisateur.sim_date}`} symbole={actif.symbole} jusqua={utilisateur.sim_date} />
                  <GraphiqueOr key={`graphique-${actif.symbole}`} symbole={actif.symbole} nom={actif.nom} jusqua={utilisateur.sim_date} theme={theme} />
                </div>
                <MarketPanel actifs={actifs} cours={cours} symboleActif={actif.symbole} dateSimulation={utilisateur.sim_date} chargement={chargementCours} onSelect={choisirActif} />
              </div>
            </> : <p className="loading-state" role="status">Chargement des actifs…</p>}
          </>}
          {vue === "markets" && <section className="page-section">
            <div className="page-heading"><h1>Marchés</h1><p>{marche.nom} · cotations disponibles au {utilisateur.sim_date}.</p></div>
            <div className="market-list">
              {actifs.map((item) => {
                const quote = cours[item.symbole];
                const direction = quote ? quote.variation > 0 ? "positive" : quote.variation < 0 ? "negative" : "neutral" : "neutral";
                const prefix = quote ? quote.variation > 0 ? "▲ +" : quote.variation < 0 ? "▼ −" : "– " : "";
                return <button className="market-list-row" data-selected={symbole === item.symbole} key={item.symbole} onClick={() => choisirActif(item.symbole)} type="button">
                  <span><b>{libelleActif(item.symbole, item.nom)}</b><small>{item.symbole}</small></span>
                  <span className="market-list-price">{quote ? formaterNombre(quote.dernier) : "—"}</span>
                  <span className={`direction-${direction}`}>{quote ? `${prefix}${formaterNombre(Math.abs(quote.variation_pct))} %` : "Cotation indisponible"}</span>
                </button>;
              })}
            </div>
          </section>}
          {vue === "trading" && <Trading key={marche.id} token={token} actifs={actifs} symboleInitial={symbole || actifs[0]?.symbole || "GC=F"} simDate={utilisateur.sim_date} onTrade={actualiserCompte} />}
          {vue === "portefeuille" && <Portefeuille token={token} rafraichissement={rafraichissement} />}
          {vue === "training" && <Formation key={utilisateur.id} token={token} />}
          {pageActive && !pageActive.available && <section className="empty-page">
            <div aria-hidden="true" className="empty-page-icon"><pageActive.Icon size={25} strokeWidth={1.6} /></div>
            <h1>{pageActive.label}</h1>
            <p>{pageActive.description}</p>
            <span>Disponible dans un prochain sprint</span>
          </section>}
        </main>
      </div>
      <SimulationBar
        date={utilisateur.sim_date}
        lecture={lecture}
        enCours={avancementEnCours}
        vitesse={vitesse}
        message={messageTemps}
        onLecture={() => { setMessageTemps(""); setLecture((current) => !current); }}
        onAvancerJour={() => { setLecture(false); void avancerProchaineSeance(); }}
        onAvancerSemaine={() => void avancerPeriode(7)}
        onAvancerMois={() => void avancerPeriode(30)}
        onVitesse={setVitesse}
      />
      <CommandPalette actifs={actifs} onChooseAsset={choisirActif} onChoosePage={choisirPage} onClose={() => setPaletteOuverte(false)} open={paletteOuverte} pages={nav} />
    </div>
  );
}