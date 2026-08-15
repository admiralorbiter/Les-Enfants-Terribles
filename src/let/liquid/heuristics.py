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


from let.models.entities import AnalysisData, DomainConcept, Episode, PerturbationItem

DOMAIN_CONCEPTS_REGISTRY: dict[str, DomainConcept] = {
    # Piano
    "piano.tempo_rushing": DomainConcept(
        id="piano.tempo_rushing",
        domain="piano",
        term="Tempo / Rushing",
        icon="⏱️",
        definition="Subconscious rhythmic acceleration driven by motor tension or anticipation of upcoming difficult passages.",
        aliases=["speeding up", "rushing", "pulse compression"],
    ),
    "piano.tension_posture": DomainConcept(
        id="piano.tension_posture",
        domain="piano",
        term="Tension / Posture",
        icon="🦾",
        definition="Accumulation of muscular stiffness in wrist, forearm, or shoulders preventing natural arm-weight transfer.",
        aliases=["wrist lock", "arm strain", "stiffness"],
    ),
    "piano.memory_fingering": DomainConcept(
        id="piano.memory_fingering",
        domain="piano",
        term="Memory / Fingering",
        icon="🧠",
        definition="Consistent finger choreography across repetitions to ensure mechanical reliability under performance pressure.",
        aliases=["fingering consistency", "motor memory"],
    ),
    "piano.finger_articulation": DomainConcept(
        id="piano.finger_articulation",
        domain="piano",
        term="Finger Articulation & Legato",
        icon="🖐️",
        definition="Connecting melodic notes through independent finger articulation rather than relying on sustain pedal.",
        aliases=["finger legato", "clean articulation", "finger independence"],
    ),
    "piano.dynamics_voicing": DomainConcept(
        id="piano.dynamics_voicing",
        domain="piano",
        term="Dynamics / Voicing",
        icon="🎨",
        definition="Balancing the relative volume of polyphonic layers to project the melodic line over accompaniment.",
        aliases=["voicing", "balance", "dynamic contrast"],
    ),
    "piano.damper_pedal": DomainConcept(
        id="piano.damper_pedal",
        domain="piano",
        term="Damper Pedal Bleed",
        icon="🦶",
        definition="Holding sustain pedal across harmonic chord shifts, causing muddy acoustic resonance.",
        aliases=["pedal blur", "sustain bleed", "dirty pedal"],
    ),
    "piano.arm_weight": DomainConcept(
        id="piano.arm_weight",
        domain="piano",
        term="Arm-Weight Drop",
        icon="🎹",
        definition="Using natural arm gravity to generate deep tone without forearm or wrist strain.",
        aliases=["gravity drop", "relaxed weight"],
    ),
    "piano.rubato": DomainConcept(
        id="piano.rubato",
        domain="piano",
        term="Rubato",
        icon="🌊",
        definition="Expressive rhythmic elasticity that stretches and compresses time without losing the underlying pulse.",
        aliases=["tempo flexibility", "elastic pulse"],
    ),
    "piano.thumb_under": DomainConcept(
        id="piano.thumb_under",
        domain="piano",
        term="Thumb-Under Rotation",
        icon="🔄",
        definition="Pivoting the wrist and forearm smoothly to tuck the thumb during scale or arpeggio runs.",
        aliases=["thumb pivot", "arpeggio pass"],
    ),

    # Call of Duty
    "cod.centering": DomainConcept(
        id="cod.centering",
        domain="cod",
        term="Centering / Aim",
        icon="🎯",
        definition="Pre-aligning crosshairs at head/chest height where enemies will appear to minimize reaction micro-adjustments.",
        aliases=["crosshair placement", "pre-aim", "elevation tracking"],
    ),
    "cod.sprinting_pacing": DomainConcept(
        id="cod.sprinting_pacing",
        domain="cod",
        term="Sprinting / Pacing",
        icon="🏃",
        definition="Managing sprint-to-fire delays by transitioning to walking or pre-aiming before entering engagement zones.",
        aliases=["pacing", "sprint-out delay", "tactical sprint control"],
    ),
    "cod.rotation_timing": DomainConcept(
        id="cod.rotation_timing",
        domain="cod",
        term="Rotation Timing & Spawns",
        icon="🗺️",
        definition="Anticipating objective shifts early to secure favorable spawn anchors before enemies collapse.",
        aliases=["spawn rotation", "early rotation", "map control"],
    ),
    "cod.patience_tilt": DomainConcept(
        id="cod.patience_tilt",
        domain="cod",
        term="Patience / Tilt",
        icon="🧘",
        definition="Maintaining emotional composure and tactical discipline after losing consecutive gunfights.",
        aliases=["composure", "tilt control", "anti-panic"],
    ),
    "cod.cover_anchor": DomainConcept(
        id="cod.cover_anchor",
        domain="cod",
        term="Cover / Anchor",
        icon="🛡️",
        definition="Holding strategic perimeter points and maintaining hard shoulder cover without over-exposing hitbox.",
        aliases=["anchor positioning", "head glitch", "cover discipline"],
    ),
    "cod.ego_challenging": DomainConcept(
        id="cod.ego_challenging",
        domain="cod",
        term="Ego-Challenging",
        icon="⚔️",
        definition="Re-peeking or contesting gunfights at a positional, health, or weapon range disadvantage.",
        aliases=["re-peeking", "stubborn challenge", "over-challenging"],
    ),

    # Programming
    "programming.state_invariants": DomainConcept(
        id="programming.state_invariants",
        domain="programming",
        term="State Invariants",
        icon="🔒",
        definition="Structural conditions that must remain valid across all state transitions and async boundaries.",
        aliases=["data invariant", "system integrity", "consistency"],
    ),
    "programming.concurrency_race": DomainConcept(
        id="programming.concurrency_race",
        domain="programming",
        term="Concurrency / Race",
        icon="⚡",
        definition="Synchronizing asynchronous tasks and database operations to eliminate race conditions and deadlocks.",
        aliases=["race condition", "lease safety", "lock contention"],
    ),
    "programming.layer_boundary": DomainConcept(
        id="programming.layer_boundary",
        domain="programming",
        term="Layer Boundary",
        icon="🧩",
        definition="Preserving clean separation between presentation, business logic, and persistent storage layers.",
        aliases=["abstraction boundary", "separation of concerns"],
    ),
    "programming.edge_cases": DomainConcept(
        id="programming.edge_cases",
        domain="programming",
        term="Edge Cases",
        icon="🧪",
        definition="Anticipating zero-state, boundary condition, and crash recovery behaviors before implementation.",
        aliases=["boundary testing", "crash resilience", "fault tolerance"],
    ),
    "programming.productive_friction": DomainConcept(
        id="programming.productive_friction",
        domain="programming",
        term="Productive Friction",
        icon="🛠️",
        definition="Cognitive resistance that deepens reflection, learning, or comprehension without operational clerical burden.",
        aliases=["epistemic effort", "active recall"],
    ),

    # Research
    "research.falsification_test": DomainConcept(
        id="research.falsification_test",
        domain="research",
        term="Falsification Test",
        icon="🔬",
        definition="The specific, observable empirical evidence that would decisively disprove your working hypothesis.",
        aliases=["falsification threshold", "null hypothesis", "discriminating test"],
    ),
    "research.underlying_mechanism": DomainConcept(
        id="research.underlying_mechanism",
        domain="research",
        term="Underlying Mechanism",
        icon="📐",
        definition="The step-by-step physical or logical causal process that produces observed effects.",
        aliases=["causal mechanism", "first principles"],
    ),
    "research.causal_direction": DomainConcept(
        id="research.causal_direction",
        domain="research",
        term="Causal Direction",
        icon="🔍",
        definition="Distinguishing correlation from causation and determining whether intervention produces effect.",
        aliases=["causality", "epistemic separation"],
    ),
    "research.hidden_axiom": DomainConcept(
        id="research.hidden_axiom",
        domain="research",
        term="Hidden Axiom",
        icon="🧱",
        definition="An unstated foundational assumption being treated as fact that may actually be contingent.",
        aliases=["implicit assumption", "unexamined prior"],
    ),
    "research.adjacent_metaphor": DomainConcept(
        id="research.adjacent_metaphor",
        domain="research",
        term="Adjacent Metaphor",
        icon="💡",
        definition="Borrowing explanatory models from neighboring scientific disciplines to illuminate hidden structures.",
        aliases=["cross-domain transfer", "analogical reasoning"],
    ),

    # Movie
    "movie.visual_composition": DomainConcept(
        id="movie.visual_composition",
        domain="movie",
        term="Visual Composition",
        icon="🎬",
        definition="Analyzing scene framing, geometric alignment, lighting contrast, and spatial relationships.",
        aliases=["formalist framing", "cinematography", "blocking"],
    ),
    "movie.tone_silence": DomainConcept(
        id="movie.tone_silence",
        domain="movie",
        term="Tone & Silence",
        icon="🤫",
        definition="Using acoustic absence, pacing deceleration, and ambient resonance to generate dramatic weight.",
        aliases=["diegetic silence", "negative space"],
    ),
    "movie.character_choice": DomainConcept(
        id="movie.character_choice",
        domain="movie",
        term="Character Choice",
        icon="🎭",
        definition="Evaluating whether protagonist decisions emerge earned from psychological motives or plot contrivance.",
        aliases=["agency", "dramatic necessity"],
    ),
    "movie.acoustic_pacing": DomainConcept(
        id="movie.acoustic_pacing",
        domain="movie",
        term="Acoustic Pacing",
        icon="🎼",
        definition="The interplay between sound design, diegetic noise, and external score in modulating narrative rhythm.",
        aliases=["sound design", "diegetic sound"],
    ),
    "movie.thematic_premise": DomainConcept(
        id="movie.thematic_premise",
        domain="movie",
        term="Thematic Premise",
        icon="🏛️",
        definition="The underlying philosophical or ethical argument tested by the film's conflict.",
        aliases=["moral argument", "resonance drift"],
    ),

    # General
    "general.core_decision": DomainConcept(
        id="general.core_decision",
        domain="general",
        term="Core Decision",
        icon="🎯",
        definition="The pivotal fork in a workflow or habit where intentional choice replaces default drift.",
        aliases=["decision point", "commitment"],
    ),
    "general.point_of_friction": DomainConcept(
        id="general.point_of_friction",
        domain="general",
        term="Point of Friction",
        icon="⚡",
        definition="The exact juncture where resistance, confusion, or hesitation interrupts flow.",
        aliases=["operational bottleneck", "cognitive friction"],
    ),
    "general.tacit_assumption": DomainConcept(
        id="general.tacit_assumption",
        domain="general",
        term="Tacit Assumption",
        icon="🧭",
        definition="An automatic premise guiding action that has not been explicitly examined.",
        aliases=["unconscious bias", "default prior"],
    ),
    "general.recurring_pattern": DomainConcept(
        id="general.recurring_pattern",
        domain="general",
        term="Recurring Pattern",
        icon="🔁",
        definition="A behavioral or structural theme observed across multiple separate episodes.",
        aliases=["longitudinal pattern", "habitual cycle"],
    ),
    "general.surprising_insight": DomainConcept(
        id="general.surprising_insight",
        domain="general",
        term="Surprising Insight",
        icon="✨",
        definition="An unexpected realization that contradicts initial expectations or intuitive estimates.",
        aliases=["epistemic surprise", "calibration discrepancy"],
    ),
}


DOMAIN_CONCEPT_PALETTES: dict[str, list[str]] = {
    domain: [c.display_label for c in DOMAIN_CONCEPTS_REGISTRY.values() if c.domain == domain]
    for domain in ["piano", "cod", "programming", "research", "movie", "general"]
}

DOMAIN_CONCEPT_GLOSSARY: dict[str, dict[str, str]] = {
    domain: {c.term: c.definition for c in DOMAIN_CONCEPTS_REGISTRY.values() if c.domain == domain}
    for domain in ["piano", "cod", "programming", "research", "movie", "general"]
}


def get_concept_by_id(concept_id: str) -> Optional[DomainConcept]:
    """Retrieve a DomainConcept by its canonical stable ID."""
    return DOMAIN_CONCEPTS_REGISTRY.get(concept_id)


def get_domain_concepts(domain: str) -> list[dict[str, str]]:
    """Retrieve structured domain glossary concepts for tooltips and vocabulary discovery."""
    concepts = [c for c in DOMAIN_CONCEPTS_REGISTRY.values() if c.domain == domain]
    if not concepts:
        concepts = [c for c in DOMAIN_CONCEPTS_REGISTRY.values() if c.domain == "general"]
    return [
        {
            "id": c.id,
            "term": c.term,
            "definition": c.definition,
            "icon": c.icon or "",
            "display_label": c.display_label,
        }
        for c in concepts
    ]


def generate_local_perturbations(episode: Episode, transcript_text: Optional[str] = None) -> list[PerturbationItem]:
    """Generate intelligent domain-tuned cognitive questions using transcript cues and prediction discrepancies."""
    items: list[PerturbationItem] = []
    text_lower = (transcript_text or "").lower()

    # 1. Transcript-Aware Piano Probes
    if episode.domain == "piano" and text_lower:
        if any(w in text_lower for w in ["shift", "jump", "leap", "interval", "keys", "reach", "wide", "distance", "c or d", "first c", "second", "third", "movement"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="You noted friction during keyboard shifts across multi-key transitions. Did the hand make the jump using anticipatory eye movements (looking at target key first), or did the arm trajectory rely on blind muscle memory?"
                )
            )
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="During these lateral hand movements, was the inaccuracy driven by horizontal forearm displacement or missing tactile anchor points on surrounding black keys?"
                )
            )
        elif any(w in text_lower for w in ["tempo", "rush", "fast", "slow", "timing", "rhythm", "beat", "speed", "pulse"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="When the rhythm compressed, was the rushing caused by physical finger tension in the leading hand or by cognitive anticipation of upcoming chord transitions?"
                )
            )
        elif any(w in text_lower for w in ["tension", "tight", "wrist", "arm", "stiff", "lock", "forearm", "pain", "strain"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="Where in the movement sequence did physical tension accumulate, and did you release arm weight completely to the bottom of the keybed?"
                )
            )
        elif any(w in text_lower for w in ["pedal", "blur", "muddy", "bleed", "clean", "sustain"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="Was the sustain pedal cleared simultaneously with the key strike, or did harmonic resonance bleed across into the next bar?"
                )
            )

    # 2. Transcript-Aware COD Probes
    elif episode.domain == "cod" and text_lower:
        if any(w in text_lower for w in ["aim", "center", "crosshair", "recoil", "shoot", "corner", "gunfight", "kd"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="In those corner engagements, was your crosshair centered at target head-height before turning, or did you have to micro-adjust after sprint-out delay?"
                )
            )
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="When taking those gunfights, did you hold right-shoulder peeker advantage around cover or contest in open space?"
                )
            )
        elif any(w in text_lower for w in ["rotate", "spawn", "time", "hill", "point", "hardpoint", "anchor", "back"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="Did you rotate early to anchor favorable spawn control for your team, or did you overstay the contested zone and get collapsed on?"
                )
            )
        elif any(w in text_lower for w in ["challenge", "peek", "ego", "repeek", "push", "died", "dead"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="When you re-peeked that angle, did you have full health and positional advantage, or was it an ego-challenge while tagged?"
                )
            )

    # 3. Transcript-Aware Programming Probes
    elif episode.domain == "programming" and text_lower:
        if any(w in text_lower for w in ["state", "invariant", "race", "async", "lock", "transaction", "lease", "concurrency", "sqlite"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="What implicit state invariant was violated during this transition, and could the data structure or type system enforce it structurally?"
                )
            )
        elif any(w in text_lower for w in ["error", "bug", "crash", "edge case", "null", "none", "fail", "broken"]):
            items.append(
                PerturbationItem(
                    id=f"pert_cue_{uuid.uuid4().hex[:8]}",
                    question_text="What assumption about boundary conditions proved false, and is there a simpler architecture that eliminates this edge case entirely?"
                )
            )

    # 4. Calibration Prediction Probes
    if episode.prediction:
        pred = episode.prediction
        pred_text = pred.prediction_text.strip() if pred.prediction_text else ""
        has_real_prediction = bool(pred_text and pred_text != "(Spoken Voice Prediction)")
        concept_name = pred.target_concept or episode.domain.capitalize()
        confidence = pred.confidence.capitalize()

        if has_real_prediction:
            q_cal = (
                f"You predicted '{pred_text}' ({confidence} confidence on {concept_name}). "
                f"Did the actual outcome confirm this expectation, or did friction emerge elsewhere?"
            )
            items.insert(0, PerturbationItem(id=f"pert_cal_{uuid.uuid4().hex[:8]}", question_text=q_cal))
        elif pred.prediction_artifact_id or pred.target_concept_id or pred.target_concept:
            concept_obj = get_concept_by_id(pred.target_concept_id) if pred.target_concept_id else None
            if concept_obj and concept_obj.definition:
                q_cal = (
                    f"You set a pre-session focus on {concept_name} ({confidence} confidence): {concept_obj.definition} "
                    f"How closely did your execution align with this target mechanic?"
                )
            else:
                q_cal = (
                    f"You set a pre-session focus on {concept_name} ({confidence} confidence). "
                    f"Did the actual outcome confirm your intention, or did unexpected friction dominate?"
                )
            items.insert(0, PerturbationItem(id=f"pert_cal_{uuid.uuid4().hex[:8]}", question_text=q_cal))

    # If fewer than 2 items generated, fill with domain/mode heuristics
    if len(items) < 2:
        domain_map = DOMAIN_HEURISTIC_PROBES.get(episode.domain, DOMAIN_HEURISTIC_PROBES["general"])
        mode_questions = domain_map.get(episode.mode, domain_map.get("capture", []))
        for q in mode_questions:
            if len(items) >= 2:
                break
            if not any(it.question_text == q for it in items):
                items.append(PerturbationItem(id=f"pert_loc_{uuid.uuid4().hex[:8]}", question_text=q))

    return items[:2]


def create_local_heuristic_analysis(episode: Episode, transcript_text: Optional[str] = None) -> AnalysisData:
    """Construct an instant offline AnalysisData packet populated with local heuristic probes and vocabulary concepts."""
    items = generate_local_perturbations(episode, transcript_text)
    concepts_raw = get_domain_concepts(episode.domain)
    domain_concepts = [
        DomainConcept(
            id=c.get("id", ""),
            term=c["term"],
            definition=c["definition"],
            icon=c.get("icon"),
            domain=episode.domain,
        )
        for c in concepts_raw
    ]

    discrepancy_summary = None
    if episode.prediction:
        pred = episode.prediction
        discrepancy_summary = (
            f"Pre-Session Prediction: \"{pred.prediction_text}\" "
            f"[{pred.target_concept or 'General'}, {pred.confidence.upper()} Confidence]"
        )
        synthesis = (
            f"Calibration debrief for {episode.domain.upper()} in {episode.mode.upper()} mode. "
            f"Pre-prediction compared against lived session evidence."
        )
    else:
        synthesis = (
            f"Spontaneous {episode.domain.upper()} observation captured in {episode.mode.upper()} mode. "
            "Local heuristic cognitive probes generated offline."
        )

    return AnalysisData(
        synthesis_text=synthesis,
        perturbations=[item.question_text for item in items],
        items=items,
        prediction_discrepancy=discrepancy_summary,
        domain_concepts=domain_concepts,
        provider="Local Heuristic Engine",
        raw_response="",
    )

