# main.py
import os
import base64
import json
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# Optional: Load environment variables if running locally
# from dotenv import load_dotenv
# load_dotenv()

app = FastAPI(
    title="TDS Virtual TA API",
    description="API for answering student questions based on TDS course content and Discourse posts.",
    version="0.1.0"
)

# --- Pydantic Models for Request and Response ---

class Link(BaseModel):
    url: str
    text: str

class ApiResponse(BaseModel):
    answer: str
    links: List[Link] = Field(default_factory=list) # Default to an empty list if no links

class StudentQuestion(BaseModel):
    question: str
    image: Optional[str] = Field(None, description="Optional base64 encoded image attachment")

# --- API Endpoint ---

@app.post("/api/", response_model=ApiResponse)
async def handle_question(student_query: StudentQuestion):
    """
    Accepts a student question and an optional base64 image,
    and returns an answer with relevant links.
    """
    question = student_query.question
    image_base64 = student_query.image

    if not question:
        raise HTTPException(status_code=400, detail="'question' field is required.")

    # --- Placeholder for your core logic ---
    # This is where you will integrate your RAG (Retrieval Augmented Generation) pipeline:
    #
    # 1. Image Processing (if image_base64 is provided):
    #    - Decode the base64 image.
    #    - If using an OCR library (e.g., PyTesseract), extract text from the image.
    #    - If using a multimodal LLM (e.g., GPT-4o), pass the image_base64 directly.
    #    - Combine extracted image text (if any) with the 'question' for better context.
    #
    # 2. Data Retrieval (RAG - Retrieval Augmented Generation):
    #    - Embed the 'question' (and any image-derived text) using an embedding model.
    #    - Query your vector database (containing embeddings of scraped course content and Discourse posts)
    #      to retrieve the most relevant document chunks.
    #
    # 3. LLM Interaction:
    #    - Construct a detailed prompt for your chosen LLM (e.g., OpenAI GPT-3.5-turbo, GPT-4o-mini).
    #    - The prompt should include:
    #        - The student's original 'question'.
    #        - The retrieved relevant document chunks as context.
    #        - Instructions for the LLM on how to answer (e.g., "Answer concisely based ONLY on provided context.", "Provide relevant URLs and descriptive text.").
    #    - Send the prompt to the LLM API.
    #
    # 4. Parse LLM Response:
    #    - Extract the generated 'answer' text.
    #    - Extract any 'links' the LLM generates (you might need to instruct the LLM to output links in a specific format or use function calling).
    #      A robust way would be to have the LLM output JSON, or use regex to find URLs and then manually map them to text if the LLM provides context.
    #
    # --- Dummy Response for now (Replace with your actual logic) ---
    print(f"Received question: {question}")
    if image_base64:
        print(f"Received image (first 50 chars of base64): {image_base64[:50]}...")
        # Example of how you might decode and save/process an image
        # try:
        #     image_data = base64.b64decode(image_base64)
        #     # Example: Save image to a temp file for processing or pass to a library
        #     # with open("temp_image.png", "wb") as f:
        #     #     f.write(image_data)
        #     # Run OCR or vision model here
        # except Exception as e:
        #     print(f"Error decoding image: {e}")
        #     # Handle error or inform user

    # This is the example response provided in the problem description
    if "gpt-4o-mini" in question.lower() and "gpt3.5 turbo" in question.lower():
        answer = "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question."
        links = [
            {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4", "text": "Use the model that’s mentioned in the question."},
            {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3", "text": "My understanding is that you just have to use a tokenizer, similar to what Prof. Anand used, to get the number of tokens and multiply that by the given rate."}
        ]
    else:
        answer = f"Thank you for your question: '{question}'. I'm currently processing it based on the available course content and Discourse posts. Please note that the full AI logic is under development."
        if image_base64:
            answer += " I also received an image, which will be considered in the analysis."
        links = [
            {"url": "https://discourse.onlinedegree.iitm.ac.in/", "text": "Visit the TDS Discourse Forum"},
            {"url": "https://onlinedegree.iitm.ac.in/course/tools-in-data-science", "text": "TDS Course Page"}
        ]

    return ApiResponse(answer=answer, links=links)

# --- Health Check Endpoint (Good for deployment platforms like Render) ---
@app.get("/")
async def read_root():
    """
    Health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "message": "TDS Virtual TA API is running!"}
