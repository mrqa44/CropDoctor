# AgriLens - Your AI Plant Doctor

## Inspiration
In Pakistan, agriculture is the backbone of the economy, yet small farmers and home gardeners often struggle to identify crop diseases early. Without access to professional agronomists, many rely on guesswork, leading to massive crop losses, misuse of pesticides, and food insecurity. We were inspired to bridge this gap by bringing an expert "Plant Doctor" to every farmer's pocket, entirely for free, to empower local communities with actionable, safe agricultural advice.

## What it does
AgriLens is a mobile-optimized web application that allows users to snap a photo or upload an image of a sick plant leaf. Within seconds, our AI analyzes the image and provides:
1. A diagnosis of the disease and its severity.
2. Step-by-step treatment plans, prioritizing organic and low-cost natural remedies first.
3. Safe chemical treatment suggestions with strong guardrails (always deferring to product labels for dosages).
4. Text-to-Speech (TTS) readout of the diagnosis in English or Urdu, ensuring accessibility for farmers with low literacy.
5. Local weather data to advise on safe spraying conditions.
6. A downloadable offline text report to share with local experts or agriculture shops.

## How we built it
We designed AgriLens to be as lightweight and accessible as possible, keeping in mind that our target users might have low-end smartphones and slow internet connections.
* **Frontend**: We used **Streamlit** to build a responsive, mobile-friendly interface without writing complex JavaScript.
* **Backend & AI**: The core intelligence is powered by **Google's Gemini 3.1 Pro vision models**. We use `google-genai` alongside `Pydantic` to enforce structured JSON outputs, ensuring the AI consistently returns safe, predictable, and accurately categorized advice.
* **Processing & Utilities**: We integrated the **Pillow** library to compress and resize images locally before sending them to the API, drastically reducing data usage. **gTTS (Google Text-to-Speech)** handles the audio translation and readout in English and Urdu.
* **Deployment**: The application is containerized and hosted on Streamlit Community Cloud for free, zero-friction access.

## Challenges we ran into
1. **Handling Edge Cases**: The AI initially tried to diagnose images that weren't even plants! We implemented strict guardrails and prompt engineering so the model explicitly rejects non-plant images or blurry photos.
2. **Safety and Liability**: Suggesting exact chemical dosages is extremely dangerous. We had to fine-tune our system prompts to guarantee that the AI never provides exact pesticide measurements, but rather advises the user to consult local experts and follow the manufacturer's label.
3. **Data Constraints**: Uploading high-res images from rural areas is slow. We solved this by implementing an automatic image compression pipeline before the API call.

## Accomplishments that we're proud of
* Successfully integrating **bilingual Text-to-Speech (Urdu & English)**, making the tool genuinely useful for non-readers in our community.
* Engineering a prompt and Pydantic schema combination that reliably forces a powerful LLM to return safe, organic-first advice every single time.
* Delivering a fully functional, end-to-end AI product in a single hackathon weekend.

## What we learned
We learned that building AI for the real world isn't just about the model—it's about constraints. Thinking about bandwidth limits, literacy barriers, and safety guardrails was just as important as the actual AI implementation.

## What's next for AgriLens
* **Regional Disease Database**: Tailoring diagnoses to track common diseases by district/province.
* **Offline Mode**: Implementing lightweight caching or on-device models for areas with zero connectivity.
* **More Languages**: Adding support for regional languages like Sindhi, Pashto, and Punjabi.
* **Expert Connect**: A feature to link farmers directly to nearby agriculture extension offices via WhatsApp.
