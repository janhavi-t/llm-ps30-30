# LessonCraft AI – Problem Statement 30

## Problem
School teachers need structured lesson plans. This application accepts a topic and grade and uses a Gemini LLM to generate a 40-minute lesson plan with objectives, materials, timed activities, assessment, differentiation and homework.

## Stack
Python, Google Gemini API (`google-genai`), Gradio, python-dotenv.

## Run locally
1. Install Python 3.10+.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Put your Gemini API key in `.env` as `GEMINI_API_KEY=...`.
5. Run `python app.py`.

Keep `.env` private. It is excluded by `.gitignore`.

## Google Colab
If you run the application in Google Colab, install the packages from `requirements.txt` and provide your API key through a hidden input prompt or Colab Secrets. Do not paste the key into a public code cell.

## Testing
Test with at least five topic/grade combinations. Confirm the generated activity timings total 40 minutes, content suits the grade, and the Markdown download opens correctly. Record actual results and screenshots; do not claim tests that were not performed.
