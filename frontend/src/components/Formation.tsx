"use client";

import { useCallback, useEffect, useState } from "react";
import { ArrowLeft, ArrowRight, Check, Lock, RotateCcw } from "lucide-react";
import { apiJson } from "@/lib/api";

type Question = { question: string; options: string[] };
type Cours = {
  id: string;
  titre: string;
  resume: string;
  etudie: boolean;
  score: number | null;
  reussi: boolean;
  disponible: boolean;
};
type Niveau = {
  id: string;
  nom: string;
  description: string;
  cours: Cours[];
  quiz_disponible: boolean;
  quiz_score: number | null;
  quiz_reussi: boolean;
};
type EtatFormation = {
  seuil_reussite: number;
  note_maximale: number;
  niveau_actif: string | null;
  cours_actuel: string | null;
  niveaux: Niveau[];
};
type Lecon = {
  id: string;
  titre: string;
  niveau: string;
  resume: string;
  objectifs: string[];
  sections: { titre: string; texte: string }[];
  reflexe: string;
  etudie: boolean;
  score: number | null;
  reussi: boolean;
  quiz: Question[];
};
type QuizNiveau = { niveau_id: string; nom: string; quiz: Question[] };
type ResultatQuiz = {
  score: number;
  note_maximale: number;
  seuil_reussite: number;
  reussi: boolean;
  correction: { question: string; reponse_utilisateur: string; bonne_reponse: string; correcte: boolean }[];
};

export default function Formation({ token }: { token: string }) {
  const [etat, setEtat] = useState<EtatFormation | null>(null);
  const [lecon, setLecon] = useState<Lecon | null>(null);
  const [quizNiveau, setQuizNiveau] = useState<QuizNiveau | null>(null);
  const [reponses, setReponses] = useState<number[]>([]);
  const [resultat, setResultat] = useState<ResultatQuiz | null>(null);
  const [erreur, setErreur] = useState("");
  const [chargement, setChargement] = useState(true);
  const [envoi, setEnvoi] = useState(false);
  const [coursSelectionne, setCoursSelectionne] = useState("");
  const [sectionIndex, setSectionIndex] = useState(0);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [quizDemarre, setQuizDemarre] = useState(false);

  const chargerEtat = useCallback(async () => {
    const data = await apiJson<EtatFormation>("/api/formation", {}, token);
    setEtat(data);
    return data;
  }, [token]);

  const chargerCours = useCallback(async (coursId: string) => {
    const data = await apiJson<Lecon>(`/api/formation/cours/${encodeURIComponent(coursId)}`, {}, token);
    setCoursSelectionne(coursId);
    setLecon(data);
    setSectionIndex(0);
    setQuizNiveau(null);
    setQuizDemarre(false);
    setQuestionIndex(0);
    setReponses([]);
    setResultat(null);
  }, [token]);

  useEffect(() => {
    let annule = false;
    apiJson<EtatFormation>("/api/formation", {}, token)
      .then((data) => {
        if (annule) return;
        setEtat(data);
        if (!data.cours_actuel) return;
        return apiJson<Lecon>(`/api/formation/cours/${encodeURIComponent(data.cours_actuel)}`, {}, token)
          .then((cours) => {
            if (annule) return;
            setCoursSelectionne(cours.id);
            setLecon(cours);
          });
      })
      .catch((cause: unknown) => {
        if (!annule) setErreur(cause instanceof Error ? cause.message : "La formation est indisponible.");
      })
      .finally(() => {
        if (!annule) setChargement(false);
      });
    return () => { annule = true; };
  }, [token]);

  async function actualiserApresAction() {
    const data = await chargerEtat();
    if (coursSelectionne) {
      const coursExiste = data.niveaux.some((niveau) => niveau.cours.some((cours) => cours.id === coursSelectionne && cours.disponible));
      if (coursExiste) {
        await chargerCours(coursSelectionne);
        return;
      }
    }
    if (data.cours_actuel) await chargerCours(data.cours_actuel);
    else {
      setLecon(null);
      setQuizNiveau(null);
    }
  }

  async function marquerEtudie() {
    if (!lecon) return;
    setEnvoi(true);
    setErreur("");
    try {
      await apiJson(`/api/formation/cours/${encodeURIComponent(lecon.id)}/etudier`, {
        method: "POST",
      }, token);
      await actualiserApresAction();
    } catch (cause: unknown) {
      setErreur(cause instanceof Error ? cause.message : "Impossible d’enregistrer le cours.");
    } finally {
      setEnvoi(false);
    }
  }

  async function ouvrirQuizNiveau(niveau: Niveau) {
    setEnvoi(true);
    setErreur("");
    try {
      const data = await apiJson<QuizNiveau>(`/api/formation/niveaux/${encodeURIComponent(niveau.id)}/quiz`, {}, token);
      setQuizNiveau(data);
      setLecon(null);
      setCoursSelectionne("");
      setQuizDemarre(true);
      setReponses([]);
      setQuestionIndex(0);
      setResultat(null);
    } catch (cause: unknown) {
      setErreur(cause instanceof Error ? cause.message : "Impossible de charger le quiz.");
    } finally {
      setEnvoi(false);
    }
  }

  async function soumettreQuiz(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if ((!lecon && !quizNiveau) || !reponsesCompletes) return;
    setEnvoi(true);
    setErreur("");
    try {
      const path = lecon
        ? `/api/formation/cours/${encodeURIComponent(lecon.id)}/quiz`
        : `/api/formation/niveaux/${encodeURIComponent(quizNiveau!.niveau_id)}/quiz`;
      const score = await apiJson<ResultatQuiz>(path, {
        method: "POST",
        body: JSON.stringify({ reponses }),
      }, token);
      setResultat(score);
      await chargerEtat();
    } catch (cause: unknown) {
      setErreur(cause instanceof Error ? cause.message : "Impossible d’enregistrer le résultat du quiz.");
    } finally {
      setEnvoi(false);
    }
  }

  if (chargement) return <p className="loading-state" role="status">Chargement de la formation…</p>;
  if (erreur && !etat) return <p className="error-state" role="alert">{erreur}</p>;
  if (!etat) return null;

  const niveauActif = etat.niveaux.find((niveau) => niveau.id === etat.niveau_actif);
  const progression = etat.niveaux.flatMap((niveau) => niveau.cours).filter((cours) => cours.reussi).length;
  const totalCours = etat.niveaux.reduce((total, niveau) => total + niveau.cours.length, 0);
  const questions = quizDemarre ? lecon?.quiz ?? quizNiveau?.quiz ?? [] : [];
  const titreQuiz = lecon ? `Quiz · ${lecon.titre}` : quizNiveau ? `Évaluation · ${quizNiveau.nom}` : "";
  const reponsesCompletes = questions.length > 0 && reponses.length === questions.length && Array.from(
    { length: questions.length },
    (_, index) => Number.isInteger(reponses[index]),
  ).every(Boolean);

  return (
    <section className="training-page">
      <div className="page-heading">
        <h1>Formation</h1>
        <p>Progressez des bases à l’expertise. Chaque leçon et chaque niveau se débloquent après validation.</p>
      </div>
      <div aria-label="Progression de la formation" className="training-progress">
        <div className="training-progress-copy">
          <strong>{progression} / {totalCours} cours validés</strong>
          <span>{niveauActif ? `Niveau en cours : ${niveauActif.nom}` : "Parcours terminé"}</span>
        </div>
        <progress max={totalCours} value={progression} />
        <div aria-label="Étapes du parcours" className="training-step-list">
          {etat.niveaux.map((niveau, index) => (
            <span className={`training-step ${niveau.quiz_reussi ? "is-done" : niveau.id === etat.niveau_actif ? "is-active" : ""}`} key={niveau.id}>
              <span>{niveau.quiz_reussi ? <Check size={14} /> : index + 1}</span>{niveau.nom}
            </span>
          ))}
        </div>
      </div>

      <div className="training-layout">
        <nav aria-label="Cours par niveau" className="training-curriculum">
          {etat.niveaux.map((niveau, index) => {
            const niveauVerrouille = index > 0 && !etat.niveaux[index - 1].quiz_reussi;
            return (
              <section className="training-level" key={niveau.id}>
                <div className="training-level-heading">
                  <div><span className="training-level-number">Niveau {index + 1}</span><h2>{niveau.nom}</h2></div>
                  {niveau.quiz_reussi ? <span className="training-badge is-done"><Check size={13} /> Validé · {niveau.quiz_score}/10</span> : niveauVerrouille ? <span className="training-badge"><Lock size={13} /> Verrouillé</span> : null}
                </div>
                <p>{niveau.description}</p>
                <ol className="training-course-list">
                  {niveau.cours.map((cours) => (
                    <li key={cours.id}>
                      <button
                        aria-current={coursSelectionne === cours.id ? "true" : undefined}
                        className="training-course-button"
                        disabled={!cours.disponible || envoi}
                        onClick={() => {
                          setErreur("");
                          void chargerCours(cours.id).catch((cause: unknown) => setErreur(cause instanceof Error ? cause.message : "Impossible de charger le cours."));
                        }}
                        type="button"
                      >
                        <span className={`training-course-status ${cours.reussi ? "is-done" : ""}`}>{cours.reussi ? <Check size={14} /> : cours.disponible ? `${niveau.cours.indexOf(cours) + 1}` : <Lock size={13} />}</span>
                        <span className="training-course-copy"><strong>{cours.titre}</strong><small>{cours.resume}</small></span>
                        {cours.score !== null && <span className="training-course-score">{cours.score}/10</span>}
                      </button>
                    </li>
                  ))}
                </ol>
                {niveau.quiz_disponible && (
                  <button className="training-level-quiz-button" disabled={envoi} onClick={() => void ouvrirQuizNiveau(niveau)} type="button">
                    Passer le quiz de niveau
                  </button>
                )}
                {niveau.quiz_score !== null && !niveau.quiz_reussi && <p className="training-level-result">Dernier meilleur résultat : {niveau.quiz_score}/10 · minimum {etat.seuil_reussite}/10 pour débloquer le niveau suivant.</p>}
              </section>
            );
          })}
        </nav>

        <div className="training-content">
          {erreur && <p className="error-state" role="alert">{erreur}</p>}
          {lecon && (
            <article aria-labelledby="training-lesson-title" className="training-lesson panel-surface">
              <span className="training-eyebrow">{lecon.niveau} · Leçon</span>
              <h2 id="training-lesson-title">{lecon.titre}</h2>
              <p className="training-lesson-summary">{lecon.resume}</p>
              <section className="training-objectives">
                <h3>À la fin de cette leçon, vous pourrez :</h3>
                <ul>{lecon.objectifs.map((objectif) => <li key={objectif}>{objectif}</li>)}</ul>
              </section>
              <div aria-label={`Étape ${sectionIndex + 1} sur ${lecon.sections.length}`} className="training-reading-progress">
                <span>Étape {sectionIndex + 1} sur {lecon.sections.length}</span>
                <progress max={lecon.sections.length} value={sectionIndex + 1} />
              </div>
              <div className="training-lesson-sections">
                <section aria-live="polite" className="training-reading-card" key={lecon.sections[sectionIndex].titre}>
                  <span className="training-section-number">PARTIE {sectionIndex + 1}</span>
                  <h3>{lecon.sections[sectionIndex].titre}</h3>
                  <p>{lecon.sections[sectionIndex].texte}</p>
                </section>
              </div>
              <aside className="training-trader-principle">
                <strong>Réflexe du trader</strong>
                <p>{lecon.reflexe}</p>
              </aside>
              <div className="training-reading-controls">
                <button className="training-secondary-button" disabled={sectionIndex === 0} onClick={() => setSectionIndex((index) => Math.max(0, index - 1))} type="button"><ArrowLeft size={17} /> Partie précédente</button>
                {sectionIndex < lecon.sections.length - 1 ? (
                  <button className="primary-button" onClick={() => setSectionIndex((index) => Math.min(lecon.sections.length - 1, index + 1))} type="button">Continuer la leçon <ArrowRight size={17} /></button>
                ) : !lecon.etudie ? (
                  <button className="primary-button" disabled={envoi} onClick={() => void marquerEtudie()} type="button">{envoi ? "Enregistrement…" : "Terminer et marquer comme étudié"} <Check size={17} /></button>
                ) : null}
              </div>
              {lecon.etudie && !lecon.reussi && !quizDemarre && <div className="training-next-step">
                <p>Leçon terminée. Répondez aux 10 questions et obtenez au moins {etat.seuil_reussite}/10 pour débloquer le cours suivant.</p>
                <button className="primary-button" onClick={() => { setQuizDemarre(true); setReponses([]); setResultat(null); }} type="button">Commencer le quiz <ArrowRight size={17} /></button>
              </div>}
              {lecon.reussi && <p className="training-success" role="status"><Check size={16} /> Cours validé · meilleur score : {lecon.score}/10</p>}
            </article>
          )}

          {questions.length > 0 && (
            <form className="training-quiz panel-surface" onSubmit={(event) => void soumettreQuiz(event)}>
              <div className="training-quiz-heading"><div><span className="training-eyebrow">Évaluation</span><h2>{titreQuiz}</h2></div></div>
              <p className="training-quiz-intro">10 questions · 1 point par bonne réponse · réussite à partir de {etat.seuil_reussite}/10. Choisissez une réponse à chaque question.</p>
              <div className="training-quiz-progress">
                <div><strong>Question {questionIndex + 1} sur {questions.length}</strong><span>{reponses.filter(Number.isInteger).length} réponse(s) choisie(s)</span></div>
                <progress max={questions.length} value={questionIndex + 1} />
              </div>
              <nav aria-label="Choisir une question" className="training-question-nav">
                {questions.map((_, index) => (
                  <button
                    aria-current={questionIndex === index ? "step" : undefined}
                    aria-label={`Question ${index + 1}${Number.isInteger(reponses[index]) ? ", réponse choisie" : ", sans réponse"}`}
                    className={Number.isInteger(reponses[index]) ? "is-answered" : ""}
                    key={index}
                    onClick={() => setQuestionIndex(index)}
                    type="button"
                  >{index + 1}</button>
                ))}
              </nav>
              {questions[questionIndex] && <fieldset className="training-question" key={`${questions[questionIndex].question}-${questionIndex}`}>
                <legend>{questionIndex + 1}. {questions[questionIndex].question}</legend>
                {questions[questionIndex].options.map((option, optionIndex) => (
                  <label className="training-answer" key={option}>
                    <input
                      checked={reponses[questionIndex] === optionIndex}
                      disabled={Boolean(resultat)}
                      name={`question-${questionIndex}`}
                      onChange={() => setReponses((current) => {
                        const next = [...current];
                        next[questionIndex] = optionIndex;
                        return next;
                      })}
                      type="radio"
                      value={optionIndex}
                    />
                    <span>{option}</span>
                  </label>
                ))}
              </fieldset>}
              <div className="training-quiz-navigation">
                <button className="training-secondary-button" disabled={questionIndex === 0} onClick={() => setQuestionIndex((index) => Math.max(0, index - 1))} type="button"><ArrowLeft size={17} /> Précédente</button>
                {questionIndex < questions.length - 1 && <button className="training-secondary-button" onClick={() => setQuestionIndex((index) => Math.min(questions.length - 1, index + 1))} type="button">Suivante <ArrowRight size={17} /></button>}
              </div>
              {resultat && <section aria-live="polite" className={`training-result-card ${resultat.reussi ? "is-passed" : "is-failed"}`}>
                <h3>{resultat.reussi ? "Quiz réussi" : "Quiz à retenter"} · {resultat.score}/{resultat.note_maximale}</h3>
                <p>{resultat.reussi
                  ? "Bravo, votre résultat valide cette étape. Prenez le temps de lire les corrections avant de continuer."
                  : `Il faut au moins ${resultat.seuil_reussite}/${resultat.note_maximale} pour valider cette étape. Relisez les corrections puis réessayez.`}</p>
                <ol className="training-corrections">
                  {resultat.correction.map((item, index) => (
                    <li className={item.correcte ? "is-correct" : "is-incorrect"} key={`${index}-${item.question}`}>
                      <strong>{index + 1}. {item.question}</strong>
                      <span>Votre réponse : {item.reponse_utilisateur}</span>
                      {!item.correcte && <span>Bonne réponse : {item.bonne_reponse}</span>}
                    </li>
                  ))}
                </ol>
              </section>}
              <div className="training-quiz-submit-row">
                {resultat && !resultat.reussi && <button className="training-secondary-button" onClick={() => { setResultat(null); setReponses([]); setQuestionIndex(0); }} type="button"><RotateCcw size={16} /> Réessayer le quiz</button>}
                {!resultat && <>
                  <span>{reponsesCompletes ? "Toutes les questions ont une réponse." : "Répondez à toutes les questions pour terminer."}</span>
                  {questionIndex === questions.length - 1 && <button className="primary-button" disabled={envoi || !reponsesCompletes} type="submit">{envoi ? "Correction…" : "Terminer le quiz"}</button>}
                </>}
                {resultat?.reussi && etat.cours_actuel && <button className="primary-button" onClick={() => void chargerCours(etat.cours_actuel!)} type="button">Continuer vers le cours suivant <ArrowRight size={17} /></button>}
              </div>
            </form>
          )}

          {!lecon && !quizNiveau && !erreur && (
            <section className="training-complete panel-surface">
              <div className="training-course-status is-done"><Check size={14} /></div>
              <h2>Parcours terminé !</h2>
              <p>Vous avez validé tous les cours et les évaluations. Félicitations pour votre progression, du niveau débutant au niveau expert.</p>
            </section>
          )}
        </div>
      </div>
    </section>
  );
}
