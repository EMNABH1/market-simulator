import pandas as pd
from fastapi.testclient import TestClient

from app import formation, main, moteur


def _reponses_correctes(questions):
    return [question["reponse"] for question in questions]


def _creer_utilisateur(client, nom):
    inscription = client.post(
        "/api/auth/inscription",
        json={"username": nom, "password": "secret123"},
    )
    assert inscription.status_code == 201
    connexion = client.post(
        "/api/auth/connexion",
        json={"username": nom, "password": "secret123"},
    )
    assert connexion.status_code == 200
    return {"Authorization": f"Bearer {connexion.json()['access_token']}"}


def test_catalogue_propose_cours_detaille_et_quiz_de_dix_questions():
    assert len(formation.NIVEAUX) == 4
    assert sum(len(niveau["cours"]) for niveau in formation.NIVEAUX) == 12
    for niveau in formation.NIVEAUX:
        assert len(niveau["quiz"]) == 10
        assert len({question["reponse"] for question in niveau["quiz"]}) > 1
        for cours in niveau["cours"]:
            assert len(cours["objectifs"]) == 3
            assert len(cours["sections"]) == 5
            assert len(cours["quiz"]) == 10
            assert cours["reflexe"]
            assert len({question["reponse"] for question in cours["quiz"]}) > 1
            assert formation.noter(
                cours["quiz"], _reponses_correctes(cours["quiz"])
            ) == 10


def test_cours_sequentiels_et_quiz_par_utilisateur(tmp_path, monkeypatch):
    monkeypatch.setattr(moteur, "DB_PATH", tmp_path / "formation.db")
    serie = pd.Series([10.0, 20.0], index=pd.to_datetime(["2025-01-01", "2026-01-01"]))
    monkeypatch.setattr(moteur, "charger_actifs", lambda: {"GC=F": serie})

    with TestClient(main.app) as client:
        headers = _creer_utilisateur(client, "formation-test")
        initial = client.get("/api/formation", headers=headers).json()
        debutant = initial["niveaux"][0]
        assert debutant["id"] == "debutant"
        assert debutant["cours"][0]["disponible"] is True
        assert debutant["cours"][1]["disponible"] is False
        cours_initial = client.get("/api/formation/cours/debutant-1", headers=headers).json()
        assert len(cours_initial["objectifs"]) == 3
        assert len(cours_initial["sections"]) == 5
        assert cours_initial["reflexe"]
        assert len(cours_initial["quiz"]) == 0
        assert client.get("/api/formation/cours/debutant-2", headers=headers).status_code == 403
        assert client.post(
            "/api/formation/cours/debutant-1/quiz",
            headers=headers,
            json={"reponses": [0] * 10},
        ).status_code == 403

        etudie = client.post("/api/formation/cours/debutant-1/etudier", headers=headers)
        assert etudie.status_code == 200
        quiz = client.get("/api/formation/cours/debutant-1", headers=headers).json()["quiz"]
        assert len({question["question"] for question in quiz}) == 10
        assert all("reponse" not in question for question in quiz)
        assert len({
            question["reponse"]
            for question in formation.COURS_PAR_ID["debutant-1"][1]["quiz"]
        }) > 1
        assert client.post(
            "/api/formation/cours/debutant-1/quiz",
            headers=headers,
            json={"reponses": [0] * 5},
        ).status_code == 422
        mauvaises = [(question["reponse"] + 1) % 4 for question in formation.COURS_PAR_ID["debutant-1"][1]["quiz"]]
        echec = client.post(
            "/api/formation/cours/debutant-1/quiz",
            headers=headers,
            json={"reponses": mauvaises},
        )
        assert echec.status_code == 200
        assert echec.json()["score"] == 0
        assert echec.json()["reussi"] is False
        correction = echec.json()["correction"]
        assert len(correction) == 10
        premiere_question = formation.COURS_PAR_ID["debutant-1"][1]["quiz"][0]
        assert correction[0] == {
            "question": premiere_question["question"],
            "reponse_utilisateur": premiere_question["options"][mauvaises[0]],
            "bonne_reponse": premiere_question["options"][premiere_question["reponse"]],
            "correcte": False,
        }
        assert client.get("/api/formation/cours/debutant-2", headers=headers).status_code == 403
        assert len(quiz) == 10

        reponses_partielles = _reponses_correctes(
            formation.COURS_PAR_ID["debutant-1"][1]["quiz"]
        )
        reponses_partielles[5:] = [
            (reponse + 1) % 4 for reponse in reponses_partielles[5:]
        ]
        reussite = client.post(
            "/api/formation/cours/debutant-1/quiz",
            headers=headers,
            json={"reponses": reponses_partielles},
        )
        assert reussite.json()["score"] == 5
        assert reussite.json()["reussi"] is True
        assert sum(item["correcte"] for item in reussite.json()["correction"]) == 5
        assert client.get("/api/formation/cours/debutant-2", headers=headers).status_code == 200

        autre_utilisateur = _creer_utilisateur(client, "formation-autre")
        autre_etat = client.get("/api/formation", headers=autre_utilisateur).json()
        assert autre_etat["niveaux"][0]["cours"][0]["reussi"] is False


def test_validation_niveau_requiert_cours_et_quiz_reussi(tmp_path, monkeypatch):
    monkeypatch.setattr(moteur, "DB_PATH", tmp_path / "formation-niveaux.db")
    serie = pd.Series([10.0, 20.0], index=pd.to_datetime(["2025-01-01", "2026-01-01"]))
    monkeypatch.setattr(moteur, "charger_actifs", lambda: {"GC=F": serie})

    with TestClient(main.app) as client:
        headers = _creer_utilisateur(client, "formation-niveau")
        assert client.get(
            "/api/formation/niveaux/debutant/quiz", headers=headers
        ).status_code == 403

        for cours in formation.NIVEAUX[0]["cours"]:
            client.post(f"/api/formation/cours/{cours['id']}/etudier", headers=headers)
            resultat = client.post(
                f"/api/formation/cours/{cours['id']}/quiz",
                headers=headers,
                json={"reponses": _reponses_correctes(cours["quiz"])},
            )
            assert resultat.status_code == 200
            assert resultat.json()["reussi"] is True

        quiz = client.get("/api/formation/niveaux/debutant/quiz", headers=headers)
        assert quiz.status_code == 200
        assert len(quiz.json()["quiz"]) == 10
        assert all("reponse" not in question for question in quiz.json()["quiz"])
        mauvaise_reponse = [
            (question["reponse"] + 1) % 4
            for question in formation.NIVEAUX[0]["quiz"]
        ]
        echec = client.post(
            "/api/formation/niveaux/debutant/quiz",
            headers=headers,
            json={"reponses": mauvaise_reponse},
        )
        assert echec.json()["reussi"] is False
        assert len(echec.json()["correction"]) == 10
        assert client.get("/api/formation/cours/intermediaire-1", headers=headers).status_code == 403

        reussite = client.post(
            "/api/formation/niveaux/debutant/quiz",
            headers=headers,
            json={"reponses": _reponses_correctes(formation.NIVEAUX[0]["quiz"])},
        )
        assert reussite.json()["score"] == 10
        assert reussite.json()["reussi"] is True
        assert all(item["correcte"] for item in reussite.json()["correction"])
        etat = client.get("/api/formation", headers=headers).json()
        assert etat["niveau_actif"] == "intermediaire"
        assert etat["niveaux"][1]["cours"][0]["disponible"] is True
