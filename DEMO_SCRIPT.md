# AgriLens — Demo Video Script (2–3 minutes)
# Record with OBS, Loom, or your phone screen recorder.

## ==============================
## SECTION 1: THE PROBLEM (0:00 – 0:30)
## ==============================

# [Show a simple title slide or the AgriLens logo]

NARRATION:
"In Pakistan, over 40% of the population depends on agriculture.
But small farmers and home gardeners face a massive problem —
when their crops get sick, they can't identify what's wrong.

They don't have access to agronomists.
They guess, they use the wrong pesticide, and they lose their harvest.

What if every farmer had a plant doctor — right in their pocket?"

# [Transition to live demo]


## ==============================
## SECTION 2: LIVE DEMO (0:30 – 2:00)
## ==============================

# [Open the AgriLens app in your browser — use your phone for extra impact]

NARRATION:
"This is AgriLens. It works on any smartphone browser — no app install needed."

# STEP 1: Show the clean UI
"The interface is simple. Two options: take a photo with your camera,
or upload an existing image."

# STEP 2: Select settings
"On the side, the farmer picks their crop — say, Wheat —
and chooses their language. We support Urdu for local farmers."

# [Select 'Wheat (گندم)' and 'Urdu' from the dropdowns]

# STEP 3: Upload or capture a photo
"Let me upload a photo of a diseased wheat leaf..."

# [Upload a sample image of a sick leaf]

# STEP 4: Click Analyze
"One tap on 'Analyze Plant'... and within seconds..."

# [Click the Analyze button, wait for the spinner]

# STEP 5: Show the results
"AgriLens identifies the disease, shows confidence level and severity,
and gives treatment steps — organic options first, then chemical with safety warnings.

Notice: it never tells the farmer an exact chemical dosage.
It always says 'follow the product label'. Safety is built in."

# STEP 6: Show Listen button
"For farmers who struggle with reading, there's a Listen button —
the entire diagnosis is read out loud in Urdu."

# [Click play on the audio player]

# STEP 7: Show Download Report
"And they can download the full report as a text file
to take to a local agriculture shop or expert."

# [Click the Download Report button]

# STEP 8: Show safety guardrail
"If someone uploads a blurry photo or something that's not a plant,
AgriLens doesn't guess — it politely asks for a better photo."

# [Optionally upload a blurry or non-plant image to demonstrate]


## ==============================
## SECTION 3: HOW IT WORKS + WHAT'S NEXT (2:00 – 2:30)
## ==============================

# [Show the Architecture diagram from the README, or a simple slide]

NARRATION:
"Under the hood, AgriLens compresses the image to save bandwidth,
sends it to Google's Gemini AI with a carefully engineered prompt,
and gets back structured JSON — validated with Pydantic —
so the results are always consistent and safe.

It's built with Python and Streamlit, deployed for free
on Streamlit Community Cloud. No paid services. Fully open source."

# [Show the GitHub repo briefly]

"In the future, we want to add a regional disease database,
support for more Pakistani languages like Sindhi and Punjabi,
and an offline mode for areas with no internet.

AgriLens — because every farmer deserves a plant doctor in their pocket.
Thank you."

# [End with the AgriLens logo and GitHub link on screen]
