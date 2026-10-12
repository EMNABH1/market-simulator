import pandas as pd
from fastapi.testclient import TestClient

from app import main, moteur


def test_flux_authentifie_et_prix_a_date(tmp_path, monkeypatch):
    monkeypatch.setattr(moteur, "DB_PATH", tmp_path / "api_test.db")
    serie = pd.Series(
        [10.0, 20.0, 500.0],
        index=pd.to_datetime(["2025-01-01", "2026-01-01", "2026-01-03"]),
    )
    monkeypatch.setattr(moteur, "charger_actifs", lambda: {"GC=F": serie})

    with TestClient(main.app) as client:
        inscription = client.post(
            "/api/auth/inscription",
            json={"username": "api-trader", "password": "secret123"},
        )
        assert inscription.status_code == 201

        with moteur.connexion() as conn:
            user = conn.execute("SELECT salt, password_hash FROM users").fetchone()
        assert user["password_hash"] != "secret123"
        assert len(user["salt"]) == 32

        connexion = client.post(
            "/api/auth/connexion",
            json={"username": "api-trader", "password": "secret123"},
        )
        assert connexion.status_code == 200
        jeton = connexion.json()["access_token"]
        headers = {"Authorization": f"Bearer {jeton}"}

        moi = client.get("/api/moi", headers=headers)
        assert moi.status_code == 200
        assert moi.json()["username"] == "api-trader"

        ordre = client.post(
            "/api/ordres",
            headers=headers,
            json={"symbole": "GC=F", "sens": "ACHAT", "quantite": 1},
        )
        assert ordre.status_code == 201
        assert ordre.json()["sim_date"] == "2026-01-01"
        assert ordre.json()["prix"] == 20.0

        avance = client.post(
            "/api/simulation/avancer", headers=headers, json={"jours": 1}
        )
        assert avance.status_code == 200
        assert avance.json()["sim_date"] == "2026-01-02"

        invalide = client.post(
            "/api/simulation/avancer", headers=headers, json={"jours": 2}
        )
        assert invalide.status_code == 422

        ordres = client.get("/api/ordres", headers=headers)
        assert ordres.status_code == 200
        assert len(ordres.json()) == 1

        portefeuille = client.get("/api/portefeuille", headers=headers)
        assert portefeuille.status_code == 200
        assert portefeuille.json()["positions"][0]["Prix actuel"] == 20.0

        assert client.get("/api/moi").status_code == 401


def test_resume_et_stats_avec_une_seule_seance(tmp_path, monkeypatch):
    monkeypatch.setattr(moteur, "DB_PATH", tmp_path / "historique_court.db")
    df = pd.DataFrame(
        {"Open": [10.0], "High": [12.0], "Low": [9.0], "Close": [11.0], "Volume": [100]},
        index=pd.to_datetime(["2025-01-01"]),
    )
    monkeypatch.setattr(main, "charger", lambda _symbole: df)

    with TestClient(main.app) as client:
        resume = client.get("/api/resume/GC=F?jusqua=2025-01-01")
        stats = client.get("/api/stats/GC=F?jusqua=2025-01-01")

    assert resume.status_code == 200
    assert resume.json()["variation"] == 0
    assert stats.status_code == 200
    assert stats.json()["var_1m_pct"] is None
    assert stats.json()["var_1an_pct"] is None
    assert stats.json()["vol_20j_pct"] is None