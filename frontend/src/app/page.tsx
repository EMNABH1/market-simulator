import GraphiqueOr from "@/components/Or/GraphiqueOr";
import StatsOr from "@/components/StatsOr";

const nav = [
  "Tableau de bord", "Marchés", "Trading", "Portefeuille", "Risque",
  "Analyse et backtesting", "IA et prévisions", "Stress testing", "Formation", "Administration",
];

export default function Dashboard() {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <aside className="hidden w-60 shrink-0 bg-[#0f1f3d] p-3 text-slate-300 md:block">
        <div className="mb-4 px-2 py-3">
          <p className="font-semibold text-white">Salle de marché</p>
          <p className="text-xs">Simulateur</p>
        </div>
        <nav className="flex flex-col gap-1 text-sm">
          {nav.map((n, i) => (
            <a
              key={n}
              href="#"
              className={`rounded-lg px-3 py-2 ${i === 0 ? "bg-[#1d3159] text-white" : "hover:bg-[#162a4f]"}`}
            >
              {n}
            </a>
          ))}
        </nav>
      </aside>

      <div className="min-w-0 flex-1">
        <header className="flex items-center gap-3 border-b border-slate-200 bg-white px-6 py-3">
          <span className="flex-1 text-sm text-slate-500">Matière suivie : Or (GC=F)</span>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs">
            Données de clôture journalière
          </span>
          <span className="rounded-full border border-slate-200 px-3 py-1 text-xs">
            <b>Compte démo</b> · Rôle : Trader
          </span>
        </header>

        <main className="space-y-4 p-6">
          <div>
            <h1 className="text-2xl font-semibold">Tableau de bord</h1>
            <p className="text-sm text-slate-500">Marché de l&apos;or</p>
          </div>
          <StatsOr />
          <GraphiqueOr />
        </main>
      </div>
    </div>
  );
}