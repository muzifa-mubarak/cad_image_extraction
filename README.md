# CAD Image Extraction API
This project provides a **FastAPI-based service** for extracting manufacturing and mechanical part data from **CAD images / engineering drawings** using **AI (Gemini 2.5 Flash)**.  
It performs OCR-like extraction and returns structured information such as **parts list, dimensions, materials, and annotations**.

---

## 🚀 Features
- Upload a **CAD image** via API  
- Uses **Google Gemini 2.5 Flash** model for AI-powered extraction  
- Returns structured data in **JSON format** (Bill of Materials style)  
- Built with **FastAPI** for easy deployment and testing  

---

## ⚡ Installation & Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cad_image_extraction.git
   cd cad_image_extraction
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the FastAPI server:
   ```bash
   uvicorn extract:app --reload
4. Open in browser or Postman:
   ```bash
   http://127.0.0.1:8000/docs

   
   



 

