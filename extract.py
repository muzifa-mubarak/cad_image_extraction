from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import base64
import os
from dotenv import load_dotenv
from fastapi import FastAPI,File ,UploadFile
import pandas as pd 
from io import StringIO

load_dotenv()

app=FastAPI()


@app.post("/extract")
async def extract(file: UploadFile=File(...)):
    chat = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  
        google_api_key="your-api",  
        temperature=0.7
    )

    image_bytes= await file.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")


    prompt = """you are an expert OCR model assisting in extracting manufacturing and mechanical part data from technical engineering drawings or CAD blueprints.
    Your task is to analyse the individual image and extract all available dimensions and structured information relevant to a bill of materials (BOM). Focus only on the data present in the image, especially in annotations, parts lists, and labels.
    Return the output as a structured table with the following columns:

    Item No.
    Part Name
    Material
    Quantity
    Weight
    Dimensions (L x W x H in mm or as shown)
    Remarks (any special notes, tolerances, or process instructions)
    Guidelines:
    Carefully identify tabular data usually present in a parts list or title block.
    When dimensions are present, group them under Length, Width, and Height if separable, otherwise extract as-is.
    If any field is not available for a part, use N/A.
    Only include parts that are labeled or numbered clearly.
    Use exact wording and units from the image (e.g., "Mild Steel", "12mm", "kg", etc.).
    Do not convert the image into Markdown. Just return raw tabular data in plain text or JSON format.
    If there is a parts table (usually found in a corner or side of the drawing), prioritize extracting from there."""


    msg = HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/avif;base64,{image_base64}"}
    ])

    response = chat.invoke([msg])
    raw_text=response.content
    
    clean_text = raw_text.replace("```", "").strip()
    lines = [line for line in clean_text.splitlines() if not set(line.strip()) <= {"|", "-", " "}]
    clean_text = "\n".join(lines)

    # Convert markdown-like table into DataFrame
    df = pd.read_csv(StringIO(clean_text), sep="|", engine="python").dropna(axis=1, how="all")

    # Convert DataFrame to JSON
    structured_data = df.to_dict(orient="records")

    return {"extracted_data": structured_data}
