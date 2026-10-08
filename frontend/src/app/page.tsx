import PriceChart from "@/components/PriceChart";

const nav = [
  "Tableau de bord", "Marchés", "Trading", "Portefeuille", "Risque",
  "Analyse et backtesting", "IA et prévisions", "Stress testing", "Formation", "Administration",
];

const kpis = [
  { l: "Valeur du portefeuille", v: "1 248 560 $", s: "+248 560 $ depuis le départ", up: true },
  { l: "P&L du jour", v: "+22 840 $", s: "+1,86 %", up: true },
  { l: "Capital disponible", v: "612 300 $", s: "49 % du portefeuille" },
  { l: "VaR 95 % (1 jour)", v: "31 450 $", s: "2,5 % du portefeuille" },
];

const positions = [
  ["CL=F", "Pétrole WTI", "Achat", "5", "76,10", "78,42", "+11 600 $"],
  ["GC=F", "Or", "Achat", "2", "2 318,20", "2 341,60", "+4 680 $"],
  ["NG=F", "Gaz naturel", "Vente", "3", "3,02", "2,86", "+4 800 $"],
  ["ZW=F", "Blé", "Achat", "4", "6,10", "5,92", "-3 600 $"],
];

const matieres = [
  ["Pétrole WTI", "CL=F", "78,42", "+1,12 %"],
  ["Pétrole Brent", "BZ=F", "82,15", "+0,94 %"],
  ["Gaz naturel", "NG=F", "2,86", "-2,31 %"],
  ["Or", "GC=F", "2 341,60", "+0,38 %"],
  ["Argent", "SI=F", "28,14", "+0,71 %"],
  ["Cuivre", "HG=F", "4,52", "-0,45 %"],
  ["Blé", "ZW=F", "5,92", "-1,08 %"],
  ["Café", "KC=F", "2,31", "+1,62 %"],
];

const shap = [
  ["Stocks de pétrole (EIA)", 0.31],
  ["Indice du dollar", -0.18],
  ["Volatilité sur 30 jours", 0.12],
  ["Sentiment des actualités", 0.09],
] as const;

const asks = [["78,51", 14], ["78,50", 9], ["78,49", 22], ["78,48", 7], ["78,47", 18]] as const;
const bids = [["78,42", 20], ["78,41", 11], ["78,40", 25], ["78,39", 8], ["78,38", 16]] as const;

const signe = (s: string) => (s.startsWith("-") ? "text-red-700" : "text-green-700");

function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <section className={`rounded-xl border border-slate-200 bg-white p-4 ${className}`}>
      {children}
    </section>
  );
}

function Champ({ label, valeur }: { label: string; valeur: string }) {
  return (
    <label className="text-xs text-slate-500">
      {label}
      <input
        defaultValue={valeur}
        className="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900"
      />
    </label>
  );
}

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
          <input
            placeholder="Rechercher un actif : WTI, or, blé"
            className="flex-1 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm"
          />
          <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-800">
            Simulation en direct
          </span>
          <span className="rounded-full border border-slate-200 px-3 py-1 text-xs">
            <b>Compte démo</b> · Rôle : Trader
          </span>
        </header>

        <main className="space-y-4 p-6">
          <div>
            <h1 className="text-2xl font-semibold">Tableau de bord</h1>
            <p className="text-sm text-slate-500">
              Portefeuille virtuel, matières premières. Capital initial : 1 000 000 $
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {kpis.map((k) => (
              <Card key={k.l}>
                <p className="text-xs text-slate-500">{k.l}</p>
                <p className="mt-1 font-mono text-2xl font-semibold">{k.v}</p>
                <p className={`text-xs ${k.up ? "text-green-700" : "text-slate-500"}`}>{k.s}</p>
              </Card>
            ))}
          </div>

          <div className="grid gap-4 xl:grid-cols-[1fr_320px]">
            <Card>
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold">Pétrole WTI <span className="text-xs font-normal text-slate-500">CL=F</span></p>
                  <p className="font-mono text-2xl">78,42 <span className="text-sm text-green-700">+0,87 (+1,12 %)</span></p>
                </div>
                <div className="flex gap-1 text-xs">
                  {["1S", "1M", "3M", "1A"].map((p) => (
                    <button key={p} className={`rounded-lg border px-3 py-2 ${p === "3M" ? "bg-[#0f1f3d] text-white" : "border-slate-200"}`}>{p}</button>
                  ))}
                </div>
              </div>
              <div className="my-3 flex gap-2 text-xs">
                {["SMA 20", "EMA", "RSI", "MACD", "Bollinger"].map((i) => (
                  <button key={i} className={`rounded-full border px-3 py-1 ${i === "SMA 20" ? "border-blue-200 bg-blue-50 text-blue-700" : "border-slate-200"}`}>{i}</button>
                ))}
              </div>
              <PriceChart />
              <p className="mt-2 text-xs text-slate-500">Bougies journalières · Moyenne mobile 20 (SMA)</p>
            </Card>

            <Card className="space-y-3">
              <div>
                <h2 className="font-semibold">Nouvel ordre</h2>
                <p className="text-xs text-slate-500">CL=F, Pétrole WTI. Dernier cours : 78,42</p>
              </div>
              <div className="grid grid-cols-2 gap-2 text-sm font-medium">
                <button className="rounded-lg bg-green-700 py-2 text-white">Achat</button>
                <button className="rounded-lg border border-slate-200 py-2 text-red-700">Vente</button>
              </div>
              <label className="block text-xs text-slate-500">
                Type d&apos;ordre
                <select className="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-900">
                  <option>Au marché</option>
                  <option>Limite</option>
                </select>
              </label>
              <div className="grid grid-cols-2 gap-2">
                <Champ label="Quantité (contrats)" valeur="5" />
                <Champ label="Prix limite" valeur="78,42" />
                <Champ label="Stop-loss" valeur="75,90" />
                <Champ label="Take-profit" valeur="83,00" />
              </div>
              <dl className="space-y-1 rounded-lg bg-slate-50 p-3 text-xs text-slate-500">
                {[["Valeur estimée", "392 100 $"], ["Frais estimés", "24,50 $"], ["Glissement estimé", "0,03 %"], ["Exposition après ordre", "31 % (limite 40 %)"]].map(([a, b]) => (
                  <div key={a} className="flex justify-between"><dt>{a}</dt><dd className="font-mono text-slate-900">{b}</dd></div>
                ))}
              </dl>
              <p className="rounded-lg bg-green-50 p-3 text-xs text-green-800">
                Évaluation du risque avant transaction : ordre accepté.
              </p>
              <button className="w-full rounded-lg bg-green-700 py-3 text-sm font-semibold text-white">Acheter 5 CL=F</button>
            </Card>
          </div>

          <div className="grid gap-4 xl:grid-cols-[1fr_320px]">
            <Card>
              <div className="mb-3 flex items-center justify-between">
                <h2 className="font-semibold">Positions</h2>
                <div className="flex gap-1 text-xs">
                  <button className="rounded-full bg-[#0f1f3d] px-3 py-1 text-white">Ouvertes</button>
                  <button className="rounded-full border border-slate-200 px-3 py-1">Fermées</button>
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="text-left text-xs text-slate-500">
                    <tr><th>Actif</th><th>Sens</th><th>Qté</th><th>Entrée</th><th>Dernier</th><th className="text-right">P&amp;L latent</th></tr>
                  </thead>
                  <tbody>
                    {positions.map((p) => (
                      <tr key={p[0]} className="border-t border-slate-100">
                        <td className="py-2"><b>{p[0]}</b> <span className="text-slate-500">{p[1]}</span></td>
                        <td>{p[2]}</td><td>{p[3]}</td>
                        <td className="font-mono">{p[4]}</td><td className="font-mono">{p[5]}</td>
                        <td className={`text-right font-mono font-semibold ${signe(p[6])}`}>{p[6]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>

            <Card>
              <h2 className="mb-2 font-semibold">Matières premières</h2>
              <table className="w-full text-sm">
                <thead className="text-left text-xs text-slate-500"><tr><th>Actif</th><th className="text-right">Dernier</th><th className="text-right">Variation</th></tr></thead>
                <tbody>
                  {matieres.map((m) => (
                    <tr key={m[1]} className="border-t border-slate-100">
                      <td className="py-1.5"><b>{m[0]}</b> <span className="text-xs text-slate-500">{m[1]}</span></td>
                      <td className="text-right font-mono">{m[2]}</td>
                      <td className={`text-right font-mono font-semibold ${signe(m[3])}`}>{m[3]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          </div>

          <div className="grid gap-4 lg:grid-cols-3">
            <Card className="space-y-3">
              <div><h2 className="font-semibold">Résultats IA</h2><p className="text-xs text-slate-500">CL=F, horizon 5 jours</p></div>
              <div>
                <div className="flex justify-between text-sm"><span>Tendance prévue : <b>haussière</b></span><b>68 %</b></div>
                <div className="my-1 h-2 rounded bg-slate-100"><div className="h-2 w-[68%] rounded bg-blue-600" /></div>
                <p className="text-xs text-slate-500">Indice de confiance du modèle</p>
              </div>
              <div>
                <div className="flex justify-between text-sm"><span>Sentiment des actualités (FinBERT)</span><b className="text-green-700">+0,42</b></div>
                <div className="my-1 h-2 rounded bg-slate-100"><div className="h-2 w-[71%] rounded bg-blue-600" /></div>
                <p className="text-xs text-slate-500">Échelle de -1 (négatif) à +1 (positif)</p>
              </div>
              <p className="rounded-lg bg-slate-50 p-3 text-xs">Détection d&apos;anomalies : aucune anomalie sur les 30 dernières séances.</p>
            </Card>

            <Card className="space-y-3">
              <div><h2 className="font-semibold">Pourquoi cette prévision ?</h2><p className="text-xs text-slate-500">Contribution des variables (SHAP)</p></div>
              {shap.map(([nom, v]) => (
                <div key={nom}>
                  <div className="flex justify-between text-sm"><span>{nom}</span><b className={v > 0 ? "text-green-700" : "text-red-700"}>{v > 0 ? "+" : ""}{v.toFixed(2).replace(".", ",")}</b></div>
                  <div className="mt-1 h-2 rounded bg-slate-100"><div className={`h-2 rounded ${v > 0 ? "bg-blue-600" : "bg-orange-700"}`} style={{ width: `${Math.abs(v) * 280}%`, maxWidth: "100%" }} /></div>
                </div>
              ))}
              <p className="text-xs text-slate-500">Bleu : pousse le cours à la hausse (+) · Orange : à la baisse (-)</p>
            </Card>

            <Card>
              <h2 className="mb-2 font-semibold">Carnet d&apos;ordres <span className="text-xs font-normal text-slate-500">CL=F</span></h2>
              <div className="flex justify-between text-xs text-slate-500"><span>Prix</span><span>Volume</span></div>
              {asks.map(([p, v]) => (
                <div key={p} className="relative flex justify-between py-0.5 font-mono text-sm">
                  <div className="absolute inset-y-0 right-0 bg-red-100" style={{ width: `${v * 3}%` }} />
                  <span className="relative font-semibold text-red-700">{p}</span><span className="relative">{v}</span>
                </div>
              ))}
              <p className="my-1 flex justify-between border-y border-slate-100 py-1 text-xs text-slate-500"><span>Écart (spread)</span><span className="font-mono">0,05</span></p>
              {bids.map(([p, v]) => (
                <div key={p} className="relative flex justify-between py-0.5 font-mono text-sm">
                  <div className="absolute inset-y-0 right-0 bg-green-100" style={{ width: `${v * 3}%` }} />
                  <span className="relative font-semibold text-green-700">{p}</span><span className="relative">{v}</span>
                </div>
              ))}
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}