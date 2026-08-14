"""Mission Brief Markdown prompt generator for external AI bridge."""

from __future__ import annotations

from typing import Optional
from let.models.entities import Episode, TranscriptData

DOMAIN_PROMPTS = {
    "movie": "Analyze this film reflection. Pay attention to cinematography, pacing, narrative themes, emotional resonance, and directorial choices.",
    "piano": "Analyze this piano practice reflection. Focus on tempo stability, motor mechanics, difficult transitions, fingering choices, and self-calibration.",
    "cod": "Analyze this gaming reflection. Focus on tactical decisions, positioning, map awareness, spawn control, tilt management, and flow state.",
    "research": "Analyze this research hypothesis. Focus on epistemic grounding, falsifiability, key mechanisms, and unexamined prior assumptions.",
    "programming": "Analyze this programming reflection. Focus on architectural trade-offs, agent delegation boundaries, resumption context, and debt.",
    "general": "Analyze this spontaneous reflection. Focus on core thesis, clarity of thought, and underlying motivations.",
}

MODE_PROMPTS = {
    "capture": "Preserve the core observation with clean synthesis; provide 1 light observational follow-up.",
    "explore": "Identify adjacent connections, subtle patterns, and unexplored implications.",
    "challenge": "Probe unexamined assumptions, detect vague conclusions, and propose counter-hypotheses.",
    "understand": "Isolate the primary causal mechanism. Why did this work or fail?",
    "improve": "Highlight discrepancies between intent and execution; focus on actionable calibration.",
    "surprise": "Offer an unexpected, counter-intuitive angle or unconventional lens.",
    "decide": "Distill the critical trade-off and outline the discriminating experiment.",
}


def generate_mission_brief(
    episode: Episode,
    transcript: Optional[TranscriptData] = None,
    transcript_text: Optional[str] = None,
) -> str:
    """Construct a bounded Mission Brief Markdown packet."""
    text = ""
    if transcript and transcript.text:
        text = transcript.text.strip()
    elif transcript_text:
        text = transcript_text.strip()
    else:
        text = "[No transcript available for this episode yet.]"

    domain_guidance = DOMAIN_PROMPTS.get(episode.domain, DOMAIN_PROMPTS["general"])
    mode_guidance = MODE_PROMPTS.get(episode.mode, MODE_PROMPTS["capture"])

    brief = f"""# MISSION BRIEF — Les Enfants Terribles
**Episode:** {episode.title}
**ID:** `{episode.id}`
**Domain:** `{episode.domain.upper()}` | **Declared Mode:** `{episode.mode.upper()}`

---

## 1. Lived Evidence (Verbatim Spoken Transcript)
> \"{text}\"

---

## 2. Mission Directives for AI Partner
You are the personal cognitive reflection partner for Jonathan in the *Les Enfants Terribles* environment.
- **Domain Guidance:** {domain_guidance}
- **Mode Objective ({episode.mode}):** {mode_guidance}
- **Tone Rules:** Avoid generic cheerleading, sycophancy, filler introductions, and buzzwords. Be incisive, precise, and respectful of the original voice.

---

## 3. Required Output Format
Please structure your exact response using these two markdown headers:

### Polished Synthesis
(Transform Jonathan's spoken stream-of-consciousness into a clean, eloquent, and well-organized synthesis or review note. Maintain his authentic voice, terminology, and key insights. Make it ready to copy directly into notes or a review publication.)

### Liquid Perturbations
1. (First high-leverage question or challenge tailored to his declared mode.)
2. (Optional second question or counter-intuitive perspective.)
"""
    return brief
