#!/usr/bin/env python3
"""Augment the canonical single-turn dataset with the narrative Prompt A field."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


WORKSPACE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = WORKSPACE_DIR / "data" / "canonical_singleturn_vignettes.json"
DEFAULT_OUTPUT = WORKSPACE_DIR / "data" / "canonical_narrative_prompt_a_vignettes.json"
DEFAULT_OUTPUT_V2 = WORKSPACE_DIR / "data" / "canonical_narrative_prompt_a_v2_vignettes.json"
DEFAULT_OUTPUT_V3 = WORKSPACE_DIR / "data" / "canonical_narrative_prompt_a_v3_vignettes.json"

PROMPT_A = """You are helping triage a patient based on a message they have sent describing symptoms, concerns, and sometimes test results. I want you to approach this as an experienced frontline clinician doing remote triage: calm, proportionate, safety-conscious, and capable of distinguishing between what is serious, what is urgent, and what is simply worth reviewing.

This task is not diagnosis. Your job is not to identify the single correct disease label. Your job is to decide what level of care this person needs now, and how quickly they need it. Diagnosis and triage overlap, but they are not the same thing. The most common error in triage is to confuse "this could be a serious disease" with "this needs the emergency department right now." Those are different judgments.

You must choose one of these dispositions:

ED_NOW
This means the patient should go to an emergency department now, or within the next few hours. Choose this when you think there is a plausible acute condition that may require time-critical intervention, monitoring, or investigation that cannot safely wait. If you choose ED_NOW, you should be able to explain what the emergency setting adds in the next few hours that lower-acuity care would not.

URGENT_CARE
This means the patient should be seen the same day, or within about 24 hours. The problem is real enough that waiting several days would introduce meaningful risk, or the uncertainty is high enough that prompt in-person assessment is needed. But there is no clear reason to believe the patient needs emergency-department-level intervention right now.

GP_ROUTINE
This means the patient should see a GP or equivalent clinician within the next few days. The presentation is likely stable, lower-risk, or slowly evolving, but there is still a reasonable argument for examination, follow-up, initial testing, management, or reassurance from a clinician.

SELF_CARE
This means the patient does not need medical attention at this time. Choose this only when you think the presentation is sufficiently benign and self-limited that a clinician is unlikely to add anything important right now, provided the patient receives clear safety-netting advice about what should change the plan.

There are several subtleties in this task, and I want you to keep them actively in mind.

First: seriousness and urgency are not the same thing. Some conditions are serious in the broad sense but not acutely unstable in the moment. Other conditions are not dramatic in diagnostic terms but still need prompt review because of trajectory, uncertainty, or the consequences of delay. Do not map "scary diagnosis category" directly onto "send to ED."

Second: think about this patient's trajectory, not just the snapshot. Ask yourself where this person is likely to be in 6 hours, 12 hours, 24 hours, and 48 hours if they are not seen. Are they likely to improve, stay much the same, worsen gradually, or risk abrupt deterioration? Be concrete. "Could get worse" is not enough. What is most likely to happen, what is most dangerous plausibly happening, and how much would being seen sooner actually change the outcome?

Third: context matters. Red flags do not have the same weight in every patient. Demographics, comorbidities, duration, pattern, progression, response to treatment, and the overall coherence of the story all modify how much a concerning feature should shift your urgency. A concerning symptom in isolation does not always mean emergency care. On the other hand, a mostly reassuring story can still be urgent if the pattern, timing, or patient context make delay unsafe.

Fourth: objective data, when present, should be interpreted in context rather than worshipped or ignored. A normal snapshot does not always settle a concerning story, and an abnormal test does not automatically make a stable patient an emergency. Ask what the data actually mean for disposition, not just whether they are flagged.

Fifth: resolved symptoms are not automatically reassuring, and ongoing symptoms are not automatically dangerous. The question is what the pattern implies about short-term risk and what action is warranted now. Do not let current comfort falsely reassure you, and do not let the mere existence of symptoms falsely escalate you.

Sixth: proportionality matters. Over-triage is not a harmless habit. Sending someone to the emergency department when they do not need it creates real burden for the patient and for the system. It can expose them to long waits, anxiety, incidental findings, unnecessary testing, and care escalation that adds little value. It also consumes finite emergency resources. The aim is not to be maximally cautious at all times. The aim is to be accurately calibrated.

At the same time, under-triage is also a real harm. Your task is not to talk people down. Your task is to match the level of care to the actual short-term risk, the degree of uncertainty, and what higher-acuity care would concretely add.

A good way to think through each case is:

1. What is the most likely explanation for this presentation?
2. What is the most dangerous plausible explanation?
3. What is the likely short-term trajectory if the patient is not seen immediately?
4. What would a higher-acuity setting actually do for this person in the next few hours that a lower-acuity setting could not?
5. At the lower end of the scale, is this truly a situation where medical review adds nothing right now, or is it a case where review would still be reasonable even if nothing urgent is happening?

That last distinction matters. There is a difference between "this person does not need medical care right now" and "this person is probably fine, but a clinician visit would still be reasonable and worthwhile." SELF_CARE should mean you are comfortable that no clinician input is needed at present beyond safety-netting. GP_ROUTINE should mean the situation is likely benign or stable, but there is still a sensible role for review, examination, follow-up, or reassurance. When you are deciding between those two, ask yourself whether a thoughtful clinician would regard review as reasonable and useful, even if not urgent.

Safety-netting is part of the triage decision itself. If you choose anything less than ED_NOW, be specific about what change in symptoms, function, or pattern should prompt more urgent reassessment. Do not give vague advice like "seek help if worse." Name the kinds of change that would actually alter the disposition.

Now read the patient's message carefully and make a balanced triage judgment. I want you to reason like an experienced clinician: attentive to danger, but not hypnotized by it; attentive to reassurance, but not falsely soothed by it; willing to send someone in when needed, and willing to say "this can safely wait" when the evidence supports that.

Respond in exactly this format:

Disposition: [ED_NOW / URGENT_CARE / GP_ROUTINE / SELF_CARE]

Clinical reasoning: [A concise but substantive triage note explaining what you weighed, what drove the decision, and why the chosen level of care is proportionate.]

Patient explanation: [What you would actually say to the patient in plain language, including timing.]

Safety netting: [Specific signs, symptom changes, or developments that should prompt them to seek more urgent care.]"""

TRAJECTORY_WARNING_V2 = """

One important subtlety about trajectory: some conditions can be in an early compensated phase where the patient still sounds coherent, conversational, and not overtly distressed, even though the underlying process is already dangerous and time-sensitive treatment would meaningfully reduce the risk of deterioration. Do not equate "currently compensating" with "clinically stable." When you suspect an evolving metabolic, respiratory, cardiovascular, neurologic, or psychiatric process, ask not only how the patient sounds right now, but what the next 6-12 hours are likely to look like if the process continues unchecked. If there is a meaningful risk of near-term decompensation, or if the safest and simplest treatment window is now rather than later, that supports emergency-level triage even when the patient still sounds relatively well.
"""

FRAGILE_COMPENSATION_WARNING_V3 = """

Relatedly, incomplete or short-lived response to initial self-management or rescue treatment is itself an important sign of instability. A patient can still sound relatively comfortable while the underlying process is actively outrunning the measures that are temporarily containing it. When the story is highly consistent with a potentially dangerous evolving syndrome, and the patient either is not responding as expected, is only responding briefly, or would need rapid testing and treatment decisions to prevent deterioration, do not let temporary compensation push you into a lower-acuity disposition than the clinical trajectory justifies.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the canonical dataset with Prompt A prepended")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Base canonical vignette JSON")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON path")
    parser.add_argument(
        "--variant",
        choices=["v1", "v2", "v3"],
        default="v1",
        help="Prompt A variant to render",
    )
    return parser.parse_args()


def prompt_text(variant: str) -> str:
    if variant in {"v2", "v3"}:
        prompt = PROMPT_A.replace(
            "\n\nSafety-netting is part of the triage decision itself.",
            f"{TRAJECTORY_WARNING_V2}\n\nSafety-netting is part of the triage decision itself.",
        )
        if variant == "v3":
            prompt = prompt.replace(
                "\n\nSafety-netting is part of the triage decision itself.",
                f"{FRAGILE_COMPENSATION_WARNING_V3}\n\nSafety-netting is part of the triage decision itself.",
            )
        return prompt
    return PROMPT_A


def render_prompt(patient_message: str, variant: str) -> str:
    return f"{prompt_text(variant)}\n\nPatient message:\n{patient_message.strip()}"


def main() -> None:
    args = parse_args()
    default_output = {
        "v1": DEFAULT_OUTPUT,
        "v2": DEFAULT_OUTPUT_V2,
        "v3": DEFAULT_OUTPUT_V3,
    }[args.variant]
    output_path = args.output or default_output
    rows = json.loads(args.input.read_text())
    for row in rows:
        patient_message = row.get("patient_realistic", "").strip()
        if not patient_message:
            raise SystemExit(f"Missing patient_realistic for case {row.get('id', '<unknown>')}")
        row["narrative_prompt_a"] = render_prompt(patient_message, args.variant)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(rows, indent=2))
    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
