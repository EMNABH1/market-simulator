"use client";

import { useState, type FormEvent } from "react";
import { Moon, Sun } from "lucide-react";
import { apiJson } from "@/lib/api";

type AuthResponse = { access_token: string; token_type: string };

export default function Connexion({ onConnected, theme, onToggleTheme }: { onConnected: (token: string) => Promise<void>; theme: "dark" | "light"; onToggleTheme: () => void }) {
  const [mode, setMode] = useState<"connexion" | "inscription">("connexion");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [erreur, setErreur] = useState("");
  const [chargement, setChargement] = useState(false);

  async function soumettre(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErreur("");
    setChargement(true);
    try {
      if (mode === "inscription") {
        await apiJson("/api/auth/inscription", {
          method: "POST",
          body: JSON.stringify({ username, password }),
        });
      }
      const auth = await apiJson<AuthResponse>("/api/auth/connexion", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      await onConnected(auth.access_token);
    } catch (cause) {
      setErreur(cause instanceof Error ? cause.message : "Connexion impossible.");
    } finally {
      setChargement(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-panel">
        <div className="auth-panel-head">
          <div><p className="auth-brand">Salle de marché</p><h1>{mode === "connexion" ? "Connexion" : "Créer un compte"}</h1></div>
          <button aria-label={theme === "dark" ? "Activer le thème clair" : "Activer le thème sombre"} className="icon-button" onClick={onToggleTheme} type="button">
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
        <p>Accède à ton compte de simulation.</p>

        <div className="auth-tabs">
          {(["connexion", "inscription"] as const).map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => { setMode(option); setErreur(""); }}
              aria-pressed={mode === option}
              className="auth-tab"
            >
              {option}
            </button>
          ))}
        </div>

        <form className="auth-form" onSubmit={soumettre}>
          <label>
            Nom d’utilisateur
            <input
              autoComplete="username"
              required
              minLength={mode === "inscription" ? 3 : 1}
              maxLength={100}
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </label>
          <label>
            Mot de passe
            <input
              type="password"
              autoComplete={mode === "connexion" ? "current-password" : "new-password"}
              required
              minLength={mode === "inscription" ? 6 : 1}
              maxLength={1024}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </label>
          {erreur && <p role="alert" className="inline-error">{erreur}</p>}
          <button
            type="submit"
            disabled={chargement}
            className="primary-button auth-submit"
          >
            {chargement ? "Traitement…" : mode === "connexion" ? "Se connecter" : "Créer le compte"}
          </button>
        </form>
      </section>
    </main>
  );
}