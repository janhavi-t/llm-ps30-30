import os
import re
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


def create_prompt(topic: str, grade: str, duration: int = 40) -> str:
    return f"""
You are an experienced school teacher and lesson-planning assistant.
Create a practical, age-appropriate lesson plan for:
Topic: {topic}
Grade/Class: {grade}
Duration: exactly {duration} minutes.

Return Markdown with these sections in order:
1. Lesson Overview
2. Learning Objectives: 3–5 measurable objectives
3. Materials / Teaching Aids
4. Teaching Procedure and Time Allocation: a table with columns
   Activity, Teacher's Role, Students' Role, Time. Include introduction,
   explanation/modeling, learner activity and recap. Timings must total
   exactly {duration} minutes.
5. Assessment: 3–5 questions/tasks with expected answers or success criteria
6. Differentiation: one support strategy and one extension activity
7. Homework / Follow-up: one relevant task

Use simple teacher-friendly language. Do not invent curriculum standards.
Make the activities specific to the topic and suitable for the grade.
Return only the completed lesson plan in Markdown.
""".strip()


def generate_lesson(topic, grade):
    if not topic or not topic.strip():
        raise gr.Error("Please enter a lesson topic.")

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise gr.Error(
            "Gemini API key not configured. Create a local .env file using "
            ".env.example, add GEMINI_API_KEY, and restart the app."
        )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=create_prompt(topic.strip(), grade, 40),
        )
        result = getattr(response, "text", None)
        if not result or not result.strip():
            raise RuntimeError("Gemini returned an empty response.")

        safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", topic).strip("_").lower() or "lesson"
        output_path = Path(f"{safe_name}_lesson_plan.md")
        output_path.write_text(result.strip(), encoding="utf-8")
        return result.strip(), str(output_path)

    except Exception as exc:
        raise gr.Error(f"Lesson generation failed: {exc}") from exc


with gr.Blocks(title="LessonCraft AI") as demo:
    gr.Markdown("# LessonCraft AI\n### AI-Powered Lesson Plan Generator\nCreate a structured 40-minute lesson plan for teachers.")
    topic = gr.Textbox(label="Topic / Subject", placeholder="Example: Photosynthesis")
    grade = gr.Dropdown(
        choices=[f"Grade {i}" for i in range(1, 13)],
        value="Grade 7",
        label="Grade / Class",
    )
    generate = gr.Button("Generate Lesson Plan", variant="primary")
    output = gr.Markdown(label="Generated Lesson Plan")
    download = gr.File(label="Download Lesson Plan")
    generate.click(generate_lesson, inputs=[topic, grade], outputs=[output, download])

if __name__ == "__main__":
    demo.launch()
