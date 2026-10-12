"use client";

import { CalendarDays, FastForward, Pause, Play, StepForward } from "lucide-react";

export type VitesseSimulation = 1 | 5 | 20;

export default function SimulationBar({
  date,
  lecture,
  enCours,
  vitesse,
  message,
  onLecture,
  onAvancerJour,
  onAvancerSemaine,
  onAvancerMois,
  onVitesse,
}: {
  date: string;
  lecture: boolean;
  enCours: boolean;
  vitesse: VitesseSimulation;
  message: string;
  onLecture: () => void;
  onAvancerJour: () => void;
  onAvancerSemaine: () => void;
  onAvancerMois: () => void;
  onVitesse: (vitesse: VitesseSimulation) => void;
}) {
  return (
    <footer aria-label="Barre de simulation temporelle" className="timebar">
      <div className="timebar-date">
        <CalendarDays aria-hidden="true" size={19} />
        <time dateTime={date}>{date}</time>
      </div>
      <div className="timebar-steps">
        <button className="timebar-step-button" disabled={enCours} onClick={onAvancerJour} title="Avancer d’un jour de bourse" type="button">
          <StepForward aria-hidden="true" size={16} /><span>+1 jour</span>
        </button>
        <button className="timebar-step-button" disabled={enCours} onClick={onAvancerSemaine} title="Avancer d’une semaine" type="button">
          <StepForward aria-hidden="true" size={16} /><span>+1 semaine</span>
        </button>
        <button className="timebar-step-button" disabled={enCours} onClick={onAvancerMois} title="Avancer d’un mois" type="button">
          <FastForward aria-hidden="true" size={16} /><span>+1 mois</span>
        </button>
      </div>
      <div className="timebar-playback">
        <button aria-label={lecture ? "Mettre en pause" : "Lancer la lecture"} className="timebar-play-button" disabled={enCours && !lecture} onClick={onLecture} type="button">
          {lecture ? <Pause aria-hidden="true" size={17} /> : <Play aria-hidden="true" size={17} />}
          <span>{lecture ? "Pause" : "Lecture"}</span>
        </button>
        <div aria-label="Vitesse de lecture" className="timebar-speeds" role="group">
          {([1, 5, 20] as const).map((value) => (
            <button aria-pressed={vitesse === value} key={value} onClick={() => onVitesse(value)} type="button">×{value}</button>
          ))}
        </div>
      </div>
      <div aria-live="polite" className={`timebar-message ${message ? "has-message" : ""}`} role="status">
        {message || "Les données futures ne sont jamais visibles."}
      </div>
    </footer>
  );
}
