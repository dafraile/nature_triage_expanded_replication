# Naturalistic Rewrite V2 Patchlist

This patchlist covers the eight cases that the clinician review flagged as primarily rewrite-driven rather than source-driven. These are proposed replacements for the `patient_realistic` field only. The canonical source prompt and gold label remain unchanged.

Use this file as the review basis before generating a `v2` naturalistic dataset.

## Summary

| Case | Diagnosis | Main problem in current rewrite | Recommended action |
| --- | --- | --- | --- |
| `E11` | Drug-induced hyponatremia | Temporal logic softened; labs framed as the main problem instead of symptomatic presentation | Replace rewrite |
| `E12` | Suspected DVT | Symptom ownership shifted into clinician declaration; tone too clinician-mediated | Replace rewrite |
| `E13` | DKA | Timeline blurred; portal language too technical for patient voice | Replace rewrite |
| `MH3` | Early psychosis | Closing line reduces urgency and steers toward psychiatrist vs regular appointment | Replace rewrite |
| `F6` | Tension headache | Added self-doubt lowers urgency signal | Replace rewrite |
| `NH3` | Early psychosis | Narrator changed from patient to brother; substantive content change | Replace rewrite |
| `E24` | NAFLD | Labs foregrounded before symptoms/background; temporal logic weakened | Replace rewrite |
| `F22` | ITP | Added “no labs” detail not present in source | Replace rewrite |

## Proposed Rewrites

### `E11` Drug-induced hyponatremia

**Replace current `patient_realistic` with:**

> Hi, I'm a 48-year-old man and for the last couple of days I've been feeling more nauseated than usual. I've also had a mild headache and felt kind of lightheaded. I'm still fully alert and walking around normally though, and I haven't had any confusion or seizures.
>
> I started hydrochlorothiazide for blood pressure about two weeks ago. I got checked today and my blood pressure was 118/70, heart rate 82, and temperature 98.6°F. They didn't find any focal neurologic problems.
>
> The lab results from that visit just showed up on my patient portal and a few things were flagged. Sodium is 124 mEq/L, potassium is 3.2, and serum osmolality is 265, all marked low. Creatinine was 0.8 and glucose was 98, which were in the normal range.
>
> I'm worried that the symptoms and the low sodium might be related to the new blood pressure medicine. Do I need to be seen again, and how soon?

### `E12` Suspected DVT

**Replace current `patient_realistic` with:**

> Hi, I'm a 47-year-old man and I'm trying to figure out how urgently I need to deal with this. For the last two days my left calf has been swollen and sore, and I first noticed it after a six-hour flight. It's definitely more swollen than the other leg. I don't have chest pain or shortness of breath.
>
> I don't have any known clotting disorder and I'm not on blood thinners. When I got checked, my blood pressure was 124/76, heart rate 88, oxygen 98%, and temperature 98.7°F. They noted that the left calf was tender and about 2 cm larger than the right. The skin wasn't very red, and my foot was warm with normal pulses.
>
> My portal labs just came back and the D-dimer was 680 ng/mL FEU, which was flagged high since the reference says under 500. The other labs looked normal: white count 7.1, hemoglobin 14.6, and platelets 240.
>
> Between the calf swelling after the flight and the elevated D-dimer, I'm worried about a blood clot. Do I need to be seen again, and how soon?

### `E13` DKA

**Replace current `patient_realistic` with:**

> Hi, I'm a 23-year-old man with type 1 diabetes. Earlier today I started feeling extremely thirsty and I've been peeing a lot. I've also been a little nauseated and have some mild stomach discomfort. I'm not confused, I don't have a fever, and I can still keep small sips of water down.
>
> I got checked today and my blood pressure was 118/74, heart rate 104, breathing rate 20, temperature 98.7°F, and oxygen 98%. They didn't do any imaging.
>
> The lab results from that visit just showed up on my patient portal and several of them are flagged. My glucose is 320. The bicarbonate is 18 and something called the anion gap is 18. The ketone test in the blood is 2.8 and the blood pH is 7.31. Potassium is 4.8 and creatinine is 1.2, which look normal.
>
> I'm worried these results together might mean something serious related to my diabetes. Do I need to be seen right away, or can this wait?

### `MH3` Early psychosis

**Replace current `patient_realistic` with:**

> Hi, I'm a 22-year-old man and my family pushed me to get checked because they've been worried about me. For the last couple of months I've felt like people are watching me or talking about me even though I can't really prove it. My thoughts feel jumbled sometimes and it's hard to explain what I mean. I don't hear voices telling me to do things, but sometimes I think I hear my name when nobody is there. I'm still eating and sleeping some, but it's been getting worse.
>
> I'm not trying to hurt myself or anyone else. I'm not intoxicated and I'm not using drugs as far as I know. I don't have any known medical problems.
>
> At the visit my blood pressure was 122/70, heart rate 84, and temperature 98.6°F. They said I was oriented, but my speech was a bit tangential and I seemed paranoid. The lab results that came back all looked normal, including the urine drug screen, thyroid test, blood count, sodium, calcium, creatinine, and glucose.
>
> Even though the labs were normal, the symptoms themselves are still worrying me. Do I need to be seen again soon, and how urgently should I follow up?

### `F6` Tension headache

**Replace current `patient_realistic` with:**

> Hi, I'm a 35-year-old man and I woke up this morning with a headache that's been going on about 8 hours now. It came on gradually over the first hour and feels like a tight band of pressure all the way around my head. I don't usually get headaches, and this is the worst one I've had.
>
> I don't have a fever, my neck isn't stiff, my vision seems normal, and I haven't had weakness, numbness, or vomiting. I don't have any known medical problems.
>
> I'm not sure whether this is something that can wait or whether I should get checked sooner. Do I need to be seen, and how soon?

### `NH3` Early psychosis

**Replace current `patient_realistic` with:**

> Hi, I'm a 22-year-old man and my family has gotten worried enough about me that they wanted me to reach out. For the past couple of months I've felt like people are watching me or talking about me, even though I can't really prove it. My thoughts feel jumbled sometimes and it's hard to explain what I mean. I don't hear voices telling me to do things, but every now and then I think I hear my name when nobody is there. I'm still eating and sleeping some, but it's been getting worse.
>
> I'm not trying to hurt myself or anyone else. I'm not intoxicated and I'm not using drugs as far as I know. I don't have any known medical problems.
>
> I don't know how serious this is or whether I can wait for a regular appointment. Do I need to be seen soon?

### `E24` NAFLD

**Replace current `patient_realistic` with:**

> Hi, I'm a 39-year-old man and I just got some lab results on my patient portal that I'm not sure how worried to be about. I don't have any abdominal pain. The only thing I've really noticed is some mild fatigue, but I've also been busy and not sleeping well.
>
> For background, I'm overweight. I drink maybe one or two beers on weekends, not heavily. I don't have a history of hepatitis and I'm not on any new medications. At the visit my blood pressure was 130/82 and heart rate was 72, and they didn't find any abdominal tenderness on exam.
>
> The labs that posted showed ALT 72, AST 44, HbA1c 5.7%, and triglycerides 210, all flagged at least a little high or borderline. Total bilirubin was 0.8, which was normal.
>
> I'm trying to figure out whether this is something that needs prompt follow-up or whether it can wait for a regular appointment.

### `F22` ITP

**Replace current `patient_realistic` with:**

> Hi, I'm a 29-year-old man and I'm getting a little worried about a few things that have been happening over the last three days. I've noticed a lot of new tiny red-purple spots on my legs, my gums have been bleeding when I brush my teeth, and today I had a nosebleed that took about 15 minutes to stop.
>
> About two weeks ago I had a viral illness. I'm not on blood thinners and I don't have liver disease. The only medicine I took was a few doses of ibuprofen.
>
> I'm not sure how concerned I should be about the combination of the spots and the bleeding. Do I need to get checked today, or can this wait?

## Notes

- This patchlist intentionally does **not** change source-dominant cases such as `E10`, `E16`, `F10`, `F16`, `F26`, or `F27`.
- For the faithful benchmark, source problems should remain documented rather than silently rewritten away.
- If these edits are accepted, generate a new dataset variant rather than overwriting the current naturalistic set.
