import pandas as pd
import pytest

from app import moteur


@pytest.fixture
def compte(tmp_path, monkeypatch):
    monkeypatch.setattr(moteur, "DB_PATH", tmp_path / "test_simulateur.db")
    moteur.init_db()
    ok, _ = moteur.creer_compte("trader-test", "secret123", "2025-01-01")
    assert ok
    user_id = moteur.authentifier("trader-test", "secret123")
    assert user_id is not None
    return user_id


def test_achat_debite_les_liquidites_et_cree_ordre(compte):
    ok, _ = moteur.passer_ordre(compte, "GC=F", "ACHAT", 2, 50.0, "2025-01-01")

    assert ok
    assert moteur.obtenir_utilisateur(compte)["cash"] == pytest.approx(99_900.0)
    ordres = moteur.lire_ordres(compte)
    assert len(ordres) == 1
    assert ordres.iloc[0]["side"] == "ACHAT"


def test_vente_credite_les_liquidites_et_reduit_position(compte):
    moteur.passer_ordre(compte, "GC=F", "ACHAT", 2, 50.0, "2025-01-01")

    ok, _ = moteur.passer_ordre(compte, "GC=F", "VENTE", 1, 60.0, "2025-01-02")

    assert ok
    assert moteur.obtenir_utilisateur(compte)["cash"] == pytest.approx(99_960.0)
    positions = moteur.positions(moteur.lire_ordres(compte))
    assert positions["GC=F"] == (1, 50.0)


def test_fonds_insuffisants_refusent_achat(compte):
    ok, message = moteur.passer_ordre(compte, "GC=F", "ACHAT", 2_001, 50.0, "2025-01-01")

    assert not ok
    assert "Fonds insuffisants" in message
    assert moteur.obtenir_utilisateur(compte)["cash"] == pytest.approx(100_000.0)
    assert moteur.lire_ordres(compte).empty


def test_vente_a_decouvert_refusee(compte):
    ok, message = moteur.passer_ordre(compte, "GC=F", "VENTE", 1, 50.0, "2025-01-01")

    assert not ok
    assert "ne détenez" in message
    assert moteur.lire_ordres(compte).empty


def test_prix_negatif_refuse(compte):
    ok, message = moteur.passer_ordre(compte, "CL=F", "ACHAT", 1, -37.63, "2020-04-20")

    assert not ok
    assert "nul ou négatif" in message
    assert moteur.obtenir_utilisateur(compte)["cash"] == pytest.approx(100_000.0)


def test_charger_actifs_lit_colonne_close_depuis_mapping(tmp_path, monkeypatch):
    dossier = tmp_path / "Or" / "processed"
    dossier.mkdir(parents=True)
    pd.DataFrame(
        {"date": ["2025-01-01", "2025-01-02"], "Close": [10.0, 11.0]}
    ).to_csv(dossier / "or_propre.csv", index=False)
    monkeypatch.setattr(moteur, "FICHIERS", {"GC=F": "processed/or_propre.csv"})

    actifs = moteur.charger_actifs(tmp_path)

    assert list(actifs) == ["GC=F"]
    assert actifs["GC=F"].tolist() == [10.0, 11.0]


def test_prix_a_date_ne_retourne_pas_de_donnee_future():
    serie = pd.Series(
        [10.0, 20.0],
        index=pd.to_datetime(["2025-01-01", "2025-01-03"]),
    )

    assert moteur.prix_a_date(serie, "2025-01-02") == 10.0
    assert moteur.prix_a_date(serie, "2024-12-31") is None