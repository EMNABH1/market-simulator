"""
Moteur du simulateur de salle de marche : donnees, comptes, ordres, portefeuille.

Aucun code d'interface ici : ce module se teste seul et sera reutilise par les
autres modules (risque, backtesting, IA...).
"""
import hashlib
import hmac
import os
import secrets
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = ROOT_DIR / "backend" / "simulateur.db"
CAPITAL_INITIAL = 100_000.0
FICHIERS = {
    "GC=F": "MatieresPremieres/Or/processed/or_propre.csv",
    "CL=F": "MatieresPremieres/processed/petrole_propre.csv",
    "SI=F": "MatieresPremieres/processed/argent_propre.csv",
    "HG=F": "MatieresPremieres/Cuivre/processed/cuivre_propre.csv",
    "BTC-USD": "Crypto/processed/bitcoin_propre.csv",
    "ETH-USD": "Crypto/processed/ethereum_propre.csv",
    "SOL-USD": "Crypto/processed/solana_propre.csv",
    "DOGE-USD": "Crypto/processed/dogecoin_propre.csv",
}

# Un marche = un groupe d'actifs. Le cash reste unique par utilisateur.
MARCHES = {
    "matieres": {
        "nom": "Matières premières",
        "description": "Or, pétrole, argent, cuivre. Séances en semaine.",
        "actifs": ["GC=F", "CL=F", "SI=F", "HG=F"],
    },
    "crypto": {
        "nom": "Cryptomonnaies",
        "description": "Bitcoin, Ethereum, Solana, Dogecoin. Marché ouvert 7j/7.",
        "actifs": ["BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD"],
    },
}


# ----------------------------------------------------------------- donnees
def chemin_actif(symbole, dossier=None):
    """Résout le CSV nettoyé configuré, avec repli sur data/<actif>/processed."""
    dossier = Path(dossier) if dossier else DATA_DIR
    relatif = FICHIERS.get(symbole)
    if relatif is None:
        return None
    chemin = dossier / relatif
    if chemin.is_file():
        return chemin
    correspondances = sorted(dossier.glob(f"*/processed/{Path(relatif).name}"))
    return correspondances[0] if correspondances else chemin


def charger_actifs(dossier=None, marche=None):
    """Lit les clôtures des actifs configurés (ou d'un seul marché) depuis leurs CSV nettoyés."""
    dossier = Path(dossier) if dossier else DATA_DIR
    symboles = MARCHES[marche]["actifs"] if marche else FICHIERS
    actifs = {}
    for symbole in symboles:
        f = chemin_actif(symbole, dossier)
        try:
            if f is None or not f.is_file():
                continue
            df = pd.read_csv(f, parse_dates=["date"], index_col="date")
        except (ValueError, KeyError):
            continue
        colonne_cloture = next((col for col in df.columns if col.lower() == "close"), None)
        if colonne_cloture:
            s = df[colonne_cloture].dropna().sort_index()
            if len(s):
                actifs[symbole] = s
    return actifs


def date_fin(actifs):
    return max(s.index[-1] for s in actifs.values())


def date_debut(actifs):
    """Date de depart : un an apres le debut des donnees (pour avoir de l'historique)."""
    debut = max(s.index[0] for s in actifs.values()) + pd.Timedelta(days=365)
    return min(debut, date_fin(actifs))


def prix_a_date(serie, date):
    """Dernier prix connu a cette date (jamais de donnees du futur)."""
    s = serie.loc[:date]
    return float(s.iloc[-1]) if len(s) else None


# ------------------------------------------------------------ base de donnees
def connexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(connexion()) as conn, conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'trader',
                cash REAL NOT NULL,
                sim_date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                asset TEXT NOT NULL,
                side TEXT NOT NULL CHECK(side IN ('ACHAT','VENTE')),
                quantity REAL NOT NULL CHECK(quantity > 0),
                price REAL NOT NULL,
                sim_date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions(
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS formation_cours(
                user_id INTEGER NOT NULL REFERENCES users(id),
                cours_id TEXT NOT NULL,
                etudie INTEGER NOT NULL DEFAULT 0,
                meilleur_score INTEGER,
                reussi INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY(user_id, cours_id)
            );
            CREATE TABLE IF NOT EXISTS formation_niveaux(
                user_id INTEGER NOT NULL REFERENCES users(id),
                niveau_id TEXT NOT NULL,
                meilleur_score INTEGER,
                reussi INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY(user_id, niveau_id)
            );
            """
        )


def progression_formation(user_id):
    with closing(connexion()) as conn:
        cours = conn.execute(
            "SELECT cours_id, etudie, meilleur_score, reussi FROM formation_cours WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        niveaux = conn.execute(
            "SELECT niveau_id, meilleur_score, reussi FROM formation_niveaux WHERE user_id = ?",
            (user_id,),
        ).fetchall()
    return (
        {row["cours_id"]: dict(row) for row in cours},
        {row["niveau_id"]: dict(row) for row in niveaux},
    )


def marquer_cours_etudie(user_id, cours_id):
    with closing(connexion()) as conn, conn:
        conn.execute(
            """
            INSERT INTO formation_cours(user_id, cours_id, etudie)
            VALUES(?, ?, 1)
            ON CONFLICT(user_id, cours_id) DO UPDATE SET etudie = 1
            """,
            (user_id, cours_id),
        )


def enregistrer_score_cours(user_id, cours_id, score, seuil):
    reussi = int(score >= seuil)
    with closing(connexion()) as conn, conn:
        conn.execute(
            """
            INSERT INTO formation_cours(user_id, cours_id, etudie, meilleur_score, reussi)
            VALUES(?, ?, 1, ?, ?)
            ON CONFLICT(user_id, cours_id) DO UPDATE SET
                meilleur_score = MAX(COALESCE(meilleur_score, 0), excluded.meilleur_score),
                reussi = MAX(reussi, excluded.reussi)
            """,
            (user_id, cours_id, score, reussi),
        )
    return bool(reussi)


def enregistrer_score_niveau(user_id, niveau_id, score, seuil):
    reussi = int(score >= seuil)
    with closing(connexion()) as conn, conn:
        conn.execute(
            """
            INSERT INTO formation_niveaux(user_id, niveau_id, meilleur_score, reussi)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(user_id, niveau_id) DO UPDATE SET
                meilleur_score = MAX(meilleur_score, excluded.meilleur_score),
                reussi = MAX(reussi, excluded.reussi)
            """,
            (user_id, niveau_id, score, reussi),
        )
    return bool(reussi)


# ----------------------------------------------------------------- comptes
def _hacher(mot_de_passe, sel=None):
    sel = sel or os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode("utf-8"), sel, 200_000)
    return sel.hex(), h.hex()


def creer_compte(nom, mot_de_passe, date_depart):
    nom = nom.strip()
    if len(nom) < 3:
        return False, "Le nom d'utilisateur doit contenir au moins 3 caractères."
    if len(mot_de_passe) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères."
    sel, h = _hacher(mot_de_passe)
    try:
        with closing(connexion()) as conn, conn:
            conn.execute(
                "INSERT INTO users(username, salt, password_hash, cash, sim_date) VALUES(?,?,?,?,?)",
                (nom, sel, h, CAPITAL_INITIAL, str(date_depart)[:10]),
            )
    except sqlite3.IntegrityError:
        return False, "Ce nom d'utilisateur est déjà pris."
    return True, f"Compte créé : vous avez {CAPITAL_INITIAL:,.0f} $ virtuels."


def authentifier(nom, mot_de_passe):
    """Renvoie l'id de l'utilisateur, ou None si les identifiants sont faux."""
    with closing(connexion()) as conn:
        ligne = conn.execute("SELECT * FROM users WHERE username = ?", (nom.strip(),)).fetchone()
    if ligne is None:
        return None
    _, h = _hacher(mot_de_passe, bytes.fromhex(ligne["salt"]))
    return ligne["id"] if hmac.compare_digest(h, ligne["password_hash"]) else None


def creer_jeton(user_id):
    """Crée un jeton opaque et ne conserve que son empreinte en base."""
    jeton = secrets.token_urlsafe(32)
    empreinte = hashlib.sha256(jeton.encode("utf-8")).hexdigest()
    with closing(connexion()) as conn, conn:
        conn.execute("INSERT INTO sessions(token_hash, user_id) VALUES(?,?)", (empreinte, user_id))
    return jeton


def utilisateur_du_jeton(jeton):
    empreinte = hashlib.sha256(jeton.encode("utf-8")).hexdigest()
    with closing(connexion()) as conn:
        ligne = conn.execute("SELECT user_id FROM sessions WHERE token_hash = ?", (empreinte,)).fetchone()
    return ligne["user_id"] if ligne else None


def obtenir_utilisateur(user_id):
    with closing(connexion()) as conn:
        ligne = conn.execute(
            "SELECT id, username, role, cash, sim_date FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    utilisateur = dict(ligne) if ligne else None
    if utilisateur is not None:
        utilisateur["sim_date"] = str(utilisateur["sim_date"])[:10]
    return utilisateur


def definir_date(user_id, date):
    with closing(connexion()) as conn, conn:
        conn.execute("UPDATE users SET sim_date = ? WHERE id = ?", (str(date)[:10], user_id))


# ------------------------------------------------------------------ ordres
def lire_ordres(user_id):
    with closing(connexion()) as conn:
        return pd.read_sql_query(
            "SELECT id, asset, side, quantity, price, sim_date FROM orders WHERE user_id = ? ORDER BY id",
            conn,
            params=(user_id,),
        )


def positions(ordres):
    """{actif: (quantite, cout_moyen)} pour les positions encore ouvertes."""
    pos = {}
    for o in ordres.itertuples():
        q, moyen = pos.get(o.asset, (0, 0.0))
        if o.side == "ACHAT":
            moyen = (q * moyen + o.quantity * o.price) / (q + o.quantity)
            q += o.quantity
        else:
            q -= o.quantity
        pos[o.asset] = (q, moyen)
    return {a: v for a, v in pos.items() if v[0] > 1e-9}


def passer_ordre(user_id, actif, sens, quantite, prix, date_sim):
    """Execute un ordre au prix du marche. Renvoie (ok, message)."""
    if prix is None or prix <= 0:
        return False, "Prix non valide à cette date (nul ou négatif) : ordre refusé."
    if sens not in ("ACHAT", "VENTE"):
        return False, "Sens de l'ordre inconnu."
    quantite = round(float(quantite), 8)
    if quantite <= 0:
        return False, "La quantité doit être un nombre positif."
    montant = quantite * prix

    with closing(connexion()) as conn, conn:
        ligne = conn.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()
        if ligne is None:
            return False, "Utilisateur introuvable."
        cash = ligne["cash"]
        if sens == "ACHAT":
            if montant > cash + 1e-9:
                return False, f"Fonds insuffisants : il faut {montant:,.2f} $ et vous avez {cash:,.2f} $."
            nouveau_cash = cash - montant
        else:
            ordres = pd.read_sql_query(
                "SELECT asset, side, quantity, price FROM orders WHERE user_id = ? ORDER BY id",
                conn,
                params=(user_id,),
            )
            detenu = positions(ordres).get(actif, (0, 0.0))[0]
            if quantite > detenu + 1e-9:
                return False, f"Vous ne détenez que {detenu:g} unité(s) de {actif}."
            nouveau_cash = cash + montant
        conn.execute("UPDATE users SET cash = ? WHERE id = ?", (nouveau_cash, user_id))
        conn.execute(
            "INSERT INTO orders(user_id, asset, side, quantity, price, sim_date) VALUES(?,?,?,?,?,?)",
            (user_id, actif, sens, quantite, prix, str(date_sim)[:10]),
        )
    verbe = "Achat exécuté" if sens == "ACHAT" else "Vente exécutée"
    return True, f"{verbe} : {quantite:g} × {actif} à {prix:,.2f} $ (total {montant:,.2f} $)."


# --------------------------------------------------------------- portefeuille
def tableau_positions(pos, actifs, date):
    """Tableau des positions ouvertes avec valeur et gain/perte."""
    lignes = []
    for actif, (q, moyen) in pos.items():
        prix = prix_a_date(actifs[actif], date) if actif in actifs else None
        if prix is None:
            prix = moyen
        valeur = q * prix
        gain = valeur - q * moyen
        lignes.append(
            {
                "Actif": actif,
                "Quantité": q,
                "Coût moyen": round(moyen, 2),
                "Prix actuel": round(prix, 2),
                "Valeur": round(valeur, 2),
                "Gain/perte ($)": round(gain, 2),
                "Gain/perte (%)": round(100 * gain / (q * moyen), 2) if moyen else 0.0,
            }
        )
    colonnes = ["Actif", "Quantité", "Coût moyen", "Prix actuel", "Valeur", "Gain/perte ($)", "Gain/perte (%)"]
    return pd.DataFrame(lignes, columns=colonnes)