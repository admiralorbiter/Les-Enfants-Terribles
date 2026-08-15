"""Local heuristic perturbation engine providing offline deterministic cognitive probes."""

from __future__ import annotations

import uuid
from typing import Optional
from let.models.entities import AnalysisData, Episode, PerturbationItem

DOMAIN_HEURISTIC_PROBES: dict[str, dict[str, list[str]]] = {
    "movie": {
        "explore": [
            "What was the single most arresting visual shot or silence, and what did it convey that dialogue could not?",
            "How did the secondary characters reflect or distort the protagonist's core dilemma?",
        ],
        "challenge": [
            "Did the emotional resolution feel genuinely earned by the character's choices, or imposed by narrative convenience?",
            "What unexamined thematic assumption is the director taking for granted throughout the film?",
        ],
        "understand": [
            "What was the primary visual or acoustic mechanism the film used to establish tension without explicit exposition?",
            "At what exact turning point did your emotional engagement crystallize, and what triggered it?",
        ],
        "improve": [
            "What scene could be cut entirely to make the pacing and thematic focus significantly sharper?",
            "How could the narrative have handled its climax without defaulting to familiar genre conventions?",
        ],
        "surprise": [
            "What if the primary antagonist's perspective is actually the most coherent ethical position in the story?",
            "What unnoticed background detail completely alters the meaning of the ending?",
        ],
        "decide": [
            "What is the critical discriminating criterion: is this film primarily an aesthetic formal exercise or a character study?",
            "What would be the definitive test case to recommend this film to someone with different aesthetic priors?",
        ],
        "capture": [
            "What is the core emotional residue that remains with you right now?",
            "What specific visual image from the film will you still remember in a month?",
        ],
    },
    "piano": {
        "explore": [
            "How does the harmonic tension in the B-section modulate your natural dynamic shaping?",
            "What expressive possibilities open up if you exaggerate the dynamic contrast between voices?",
        ],
        "challenge": [
            "Was that rubato an intentional interpretive choice or an unconscious slowdown caused by technical difficulty?",
            "Are you relying on pedal to mask uneven finger legato in the transition bars?",
        ],
        "understand": [
            "Where in your body (wrist, forearm, shoulder, breath) did physical tension first originate before the phrase broke?",
            "What is the precise mechanical bottleneck: thumb-under rotation, fifth finger stability, or rhythmic subdivision?",
        ],
        "improve": [
            "What tempo reduction (e.g. -15 BPM with dotted rhythms) will completely eliminate tension in the difficult transition?",
            "Which exact 2-measure fragment requires isolated slow-practice before tomorrow's run-through?",
        ],
        "surprise": [
            "What happens to your tone quality if you play the melody with absolute zero arm weight and pure finger articulation?",
            "What if you practice the entire piece strictly non-legato to expose hidden rhythmic timing gaps?",
        ],
        "decide": [
            "Which fingering option creates the most reliable mechanical consistency under performance pressure?",
            "Should tomorrow's session prioritize tempo stabilization or expressive voicing of inner lines?",
        ],
        "capture": [
            "What was the single most satisfying tactile or acoustic moment during this practice run?",
            "What is the one phrase you want to calibrate first next time?",
        ],
    },
    "cod": {
        "explore": [
            "How did your route selection influence where the opposing team was forced to funnel?",
            "What unexploited line of sight or timing window did you notice in that match?",
        ],
        "challenge": [
            "Did you lose that gunfight due to mechanical aim, or because your pre-aim and positioning were compromised 3 seconds earlier?",
            "Were you actively controlling the map rotation, or merely reacting to enemy engagements?",
        ],
        "understand": [
            "What specific in-game trigger caused your decision-making to shift from patient flow to reckless chasing?",
            "How did your team's spawn distribution change right before the objective was overwhelmed?",
        ],
        "improve": [
            "What single positioning habit (e.g. ego-challenging while low health) should you eliminate in the next game?",
            "How can you adjust your centering to require smaller micro-adjustments upon corner checks?",
        ],
        "surprise": [
            "What if taking the slower, non-standard flank route completely neutralizes their anchor player?",
            "What happens if you play the next match with primary focus on audio cues and zero mini-map reliance?",
        ],
        "decide": [
            "Is the bottleneck in your performance current input calibration or tactical tempo management?",
            "Which loadout adjustment definitively addresses your most frequent death scenario?",
        ],
        "capture": [
            "What was the pivotal play or flow state moment of this session?",
            "What is the key takeaway to apply in your next match?",
        ],
    },
    "research": {
        "explore": [
            "What adjacent disciplinary lens (e.g. cybernetics, biology, economics) offers an illuminating metaphor for this mechanism?",
            "What unexpected secondary effect would follow if this hypothesis is completely correct?",
        ],
        "challenge": [
            "What specific, observable piece of evidence would conclusively falsify this hypothesis?",
            "What unstated prior assumption are you treating as an axiom that might actually be contingent?",
        ],
        "understand": [
            "What is the fundamental causal mechanism linking the inputs to the observed outcome?",
            "Why has this problem remained unsolved despite standard approaches?",
        ],
        "improve": [
            "What is the simplest, lowest-cost probe that could validate or kill this thesis this week?",
            "How can you state this claim with half the words and double the precision?",
        ],
        "surprise": [
            "What if the exact inverse of your primary thesis explains the empirical data just as well?",
            "What if this is not a technical problem at all, but a measurement artifact?",
        ],
        "decide": [
            "What is the single discriminating test that cleanly differentiates Hypothesis A from Hypothesis B?",
            "What evidence threshold is required before committing engineering resources to this direction?",
        ],
        "capture": [
            "What is the core intuition or insight you must preserve before it fades?",
            "What is the one question that remains open?",
        ],
    },
    "programming": {
        "explore": [
            "How does this design simplify downstream consumer code vs. internal implementation complexity?",
            "What future extension becomes trivial with this abstraction boundary?",
        ],
        "challenge": [
            "Is this abstraction genuinely isolating complexity, or merely scattering state across multiple call sites?",
            "Where is the hidden single point of failure or concurrency bottleneck in this architecture?",
        ],
        "understand": [
            "What is the fundamental invariant that this component must guarantee under all failure modes?",
            "Why did the previous design break down under real-world usage?",
        ],
        "improve": [
            "What is the smallest vertical slice that demonstrates value before building the full platform?",
            "How can we eliminate two intermediate layers and make data flow straightforwardly?",
        ],
        "surprise": [
            "What if we deleted this subsystem entirely and solved the problem with deterministic plain files?",
            "What happens if we make all operations strictly immutable and replayable?",
        ],
        "decide": [
            "What is the critical trade-off between operational friction and developer ergonomics here?",
            "Should we ship this minimal probe now or refine the boundary further?",
        ],
        "capture": [
            "What architectural realization did you reach during this coding session?",
            "What is the next bounded task to resume cleanly?",
        ],
    },
    "general": {
        "explore": [
            "What broader pattern or life theme does this spontaneous observation connect to?",
            "Where else in your routines have you observed a similar dynamic?",
        ],
        "challenge": [
            "What is the strongest counter-argument against your current conclusion?",
            "Are you interpreting this situation based on present evidence or past precedent?",
        ],
        "understand": [
            "What was the primary causal trigger that led to this outcome?",
            "What did this experience reveal about your tacit preferences?",
        ],
        "improve": [
            "What is the single smallest action you can take to test this realization?",
            "How can you remove one point of friction in this routine tomorrow?",
        ],
        "surprise": [
            "What if the conventional wisdom about this situation is completely backwards?",
            "What unexpected angle would an outside observer immediately notice?",
        ],
        "decide": [
            "What is the key decision point, and what is the cost of deferring it?",
            "What is the discriminating test that resolves your hesitation?",
        ],
        "capture": [
            "What is the core thought you want to preserve from this moment?",
            "What feeling or realization was most vivid?",
        ],
    },
}


def generate_local_perturbations(episode: Episode, transcript_text: Optional[str] = None) -> list[PerturbationItem]:
    """Generate deterministic domain/mode tuned cognitive questions without external API dependency."""
    domain_map = DOMAIN_HEURISTIC_PROBES.get(episode.domain, DOMAIN_HEURISTIC_PROBES["general"])
    mode_questions = domain_map.get(episode.mode, domain_map.get("capture", []))

    if not mode_questions:
        mode_questions = [
            f"What was the most surprising realization during this {episode.domain} reflection?",
            f"What specific action or experiment will you test next?",
        ]

    items: list[PerturbationItem] = []
    for i, q in enumerate(mode_questions[:2]):
        items.append(
            PerturbationItem(
                id=f"pert_loc_{uuid.uuid4().hex[:8]}",
                question_text=q,
            )
        )
    return items


def create_local_heuristic_analysis(episode: Episode, transcript_text: Optional[str] = None) -> AnalysisData:
    """Construct an instant offline AnalysisData packet populated with local heuristic probes."""
    items = generate_local_perturbations(episode, transcript_text)
    synthesis = (
        f"Spontaneous {episode.domain.upper()} observation captured in {episode.mode.upper()} mode. "
        "Local heuristic cognitive probes generated offline."
    )
    return AnalysisData(
        synthesis_text=synthesis,
        perturbations=[item.question_text for item in items],
        items=items,
        provider="Local Heuristic Engine",
        raw_response="",
    )
