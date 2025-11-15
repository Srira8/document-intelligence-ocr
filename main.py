"""
Invoice/Receipt Extraction API - 100% FREE VERSION
Using Tesseract OCR + Ollama (Local LLM)
No API keys or payment required!
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import time
from datetime import datetime
import tempfile
from pathlib import Path

# Tesseract for OCR
import pytesseract
from PIL import Image
import pdf2image

# Ollama for LLM
import requests

app = FastAPI(
    title="Invoice Extraction API (Free Version)",
    description="Extract structured data from invoices using Tesseract + Ollama - 100% free!",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
API_KEY = os.getenv("API_KEY", "dev-key-12345")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Check Tesseract installation
try:
    pytesseract.get_tesseract_version()
    TESSERACT_AVAILABLE = True
except:
    TESSERACT_AVAILABLE = False
    print("⚠️ Tesseract not found. Install: https://github.com/UB-Mannheim/tesseract/wiki")

# Check Ollama availability
try:
    response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
    OLLAMA_AVAILABLE = response.status_code == 200
except:
    OLLAMA_AVAILABLE = False
    print("⚠️ Ollama not running. Install from: https://ollama.ai")


# Models
class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None


class InvoiceData(BaseModel):
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    vendor_phone: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = "USD"
    line_items: List[LineItem] = []


class ExtractionResponse(BaseModel):
    status: str
    confidence: float
    data: InvoiceData
    processing_time_ms: int
    ocr_text_preview: Optional[str] = None


# Helper: Verify API key
def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


# Helper: Extract text using Tesseract
async def extract_text_tesseract(file_bytes: bytes, filename: str) -> str:
    """Extract text from document using Tesseract OCR"""
    if not TESSERACT_AVAILABLE:
        raise HTTPException(status_code=500, detail="Tesseract OCR not installed")
    
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        
        text_content = ""
        
        # Handle PDF
        if filename.lower().endswith('.pdf'):
            # Convert PDF to images
            images = pdf2image.convert_from_path(tmp_path)
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image)
                text_content += f"\n--- Page {i+1} ---\n{page_text}"
        else:
            # Handle images directly
            image = Image.open(tmp_path)
            text_content = pytesseract.image_to_string(image)
        
        # Cleanup
        os.unlink(tmp_path)
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="No text found in document")
        
        return text_content
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR error: {str(e)}")


# Helper: Parse with Ollama
async def parse_with_ollama(text: str) -> InvoiceData:
    """Parse extracted text into structured data using Ollama"""
    if not OLLAMA_AVAILABLE:
        raise HTTPException(status_code=500, detail="Ollama not running. Start with: ollama serve")
    
    prompt = f"""You are an expert at extracting structured data from invoices and receipts.

Extract the following information from this invoice/receipt text and return ONLY a valid JSON object.

Required JSON format:
{{
  "vendor_name": "company name or null",
  "vendor_address": "full address or null",
  "vendor_phone": "phone number or null",
  "invoice_number": "invoice/receipt number or null",
  "invoice_date": "date in YYYY-MM-DD format or null",
  "due_date": "due date in YYYY-MM-DD format or null",
  "subtotal": amount as number or null,
  "tax": tax amount as number or null,
  "total": total amount as number or null,
  "currency": "currency code (USD, EUR, etc.) or USD",
  "line_items": [
    {{
      "description": "item description",
      "quantity": quantity as number or null,
      "unit_price": price as number or null,
      "total": line total as number or null
    }}
  ]
}}

CRITICAL RULES:
1. Return ONLY the JSON object, no other text
2. Use null for missing fields (not "null" string)
3. Convert all dates to YYYY-MM-DD format
4. Extract all numbers as floats (no currency symbols)
5. Include all line items found
6. Do not add markdown code blocks or any other text

Invoice/Receipt Text:
{text}

JSON:"""
    
    try:
        # Call Ollama API
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 2000
                }
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Ollama error: {response.text}")
        
        result = response.json()
        json_str = result.get("response", "").strip()
        
        # Clean up response
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.startswith("```"):
            json_str = json_str[3:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        json_str = json_str.strip()
        
        # Parse JSON
        data_dict = json.loads(json_str)
        return InvoiceData(**data_dict)
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {str(e)}")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=500, detail="Ollama timeout - try again")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")


# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve test UI"""
    tesseract_status = "✅ Ready" if TESSERACT_AVAILABLE else "❌ Not Installed"
    ollama_status = "✅ Ready" if OLLAMA_AVAILABLE else "❌ Not Running"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice Extraction API - Free Version</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 50px auto; padding: 20px; }}
            h1 {{ color: #333; }}
            .status {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .status-item {{ margin: 5px 0; }}
            .container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
            .section {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
            input[type="file"] {{ margin: 10px 0; }}
            button {{ background: #007bff; color: white; padding: 10px 20px; border: none; 
                     border-radius: 5px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background: #0056b3; }}
            button:disabled {{ background: #ccc; cursor: not-allowed; }}
            .result {{ background: white; padding: 15px; border-radius: 5px; margin-top: 20px; 
                     white-space: pre-wrap; font-family: monospace; font-size: 12px; max-height: 600px; overflow-y: auto; }}
            .loading {{ color: #007bff; }}
            .error {{ color: #dc3545; }}
            .success {{ color: #28a745; }}
            label {{ display: block; margin: 10px 0 5px; font-weight: bold; }}
            input[type="text"] {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
            .badge {{ display: inline-block; padding: 4px 8px; border-radius: 3px; font-size: 12px; }}
            .badge-success {{ background: #28a745; color: white; }}
            .badge-danger {{ background: #dc3545; color: white; }}
        </style>
    </head>
    <body>
        <h1>📄 Invoice/Receipt Extraction API</h1>
        <p><strong>100% Free Version</strong> - Uses Tesseract OCR + Ollama (Local LLM)</p>
        
        <div class="status">
            <h3>System Status:</h3>
            <div class="status-item">Tesseract OCR: <span class="badge badge-{'success' if TESSERACT_AVAILABLE else 'danger'}">{tesseract_status}</span></div>
            <div class="status-item">Ollama LLM: <span class="badge badge-{'success' if OLLAMA_AVAILABLE else 'danger'}">{ollama_status}</span></div>
        </div>
        
        <div class="container">
            <div class="section">
                <h2>Upload Document</h2>
                <label>API Key:</label>
                <input type="text" id="apiKey" value="dev-key-12345" placeholder="Enter API key">
                
                <label>Select Invoice/Receipt:</label>
                <input type="file" id="fileInput" accept=".pdf,.png,.jpg,.jpeg">
                
                <button onclick="extractInvoice()" id="extractBtn">Extract Data</button>
                
                <div id="status"></div>
            </div>
            
            <div class="section">
                <h2>Setup Instructions</h2>
                <p><strong>If components are not ready:</strong></p>
                
                <p><strong>1. Install Tesseract:</strong></p>
                <ul>
                    <li>Windows: <a href="https://github.com/UB-Mannheim/tesseract/wiki" target="_blank">Download installer</a></li>
                    <li>Mac: <code>brew install tesseract</code></li>
                    <li>Linux: <code>sudo apt install tesseract-ocr</code></li>
                </ul>
                
                <p><strong>2. Install Ollama:</strong></p>
                <ul>
                    <li>Download: <a href="https://ollama.ai" target="_blank">ollama.ai</a></li>
                    <li>Run: <code>ollama pull llama3.2</code></li>
                    <li>Start: <code>ollama serve</code></li>
                </ul>
                
                <p><a href="/docs" target="_blank">View API Docs →</a></p>
            </div>
        </div>
        
        <div class="section" style="margin-top: 30px;">
            <h2>Extraction Result</h2>
            <div id="result" class="result">Results will appear here...</div>
        </div>
        
        <script>
            async function extractInvoice() {{
                const fileInput = document.getElementById('fileInput');
                const apiKey = document.getElementById('apiKey').value;
                const statusDiv = document.getElementById('status');
                const resultDiv = document.getElementById('result');
                const btn = document.getElementById('extractBtn');
                
                if (!fileInput.files[0]) {{
                    alert('Please select a file');
                    return;
                }}
                
                btn.disabled = true;
                statusDiv.innerHTML = '<p class="loading">⏳ Processing document... (This may take 30-60 seconds with local LLM)</p>';
                resultDiv.textContent = 'Processing...';
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                try {{
                    const startTime = Date.now();
                    const response = await fetch('/api/v1/extract/invoice', {{
                        method: 'POST',
                        headers: {{
                            'X-API-Key': apiKey
                        }},
                        body: formData
                    }});
                    
                    const data = await response.json();
                    const timeTaken = Date.now() - startTime;
                    
                    if (response.ok) {{
                        statusDiv.innerHTML = `<p class="success">✅ Success! Processed in ${{timeTaken}}ms</p>`;
                        resultDiv.textContent = JSON.stringify(data, null, 2);
                    }} else {{
                        statusDiv.innerHTML = `<p class="error">❌ Error: ${{data.detail}}</p>`;
                        resultDiv.textContent = JSON.stringify(data, null, 2);
                    }}
                }} catch (error) {{
                    statusDiv.innerHTML = `<p class="error">❌ Error: ${{error.message}}</p>`;
                    resultDiv.textContent = error.message;
                }} finally {{
                    btn.disabled = false;
                }}
            }}
        </script>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "tesseract_available": TESSERACT_AVAILABLE,
        "ollama_available": OLLAMA_AVAILABLE,
        "ollama_model": OLLAMA_MODEL,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/extract/invoice", response_model=ExtractionResponse)
async def extract_invoice(
    file: UploadFile = File(...),
    api_key: str = Header(None, alias="X-API-Key")
):
    """
    Extract structured data from invoice/receipt (FREE VERSION)
    
    - **file**: Invoice/receipt file (PDF, PNG, JPG)
    - **X-API-Key**: API key for authentication
    """
    verify_api_key(api_key)
    
    start_time = time.time()
    
    # Validate file type
    allowed_types = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed_types}")
    
    try:
        # Read file
        file_bytes = await file.read()
        
        # Step 1: Extract text using Tesseract
        extracted_text = await extract_text_tesseract(file_bytes, file.filename)
        
        # Step 2: Parse with Ollama
        invoice_data = await parse_with_ollama(extracted_text)
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        # Calculate confidence
        total_fields = 11
        filled_fields = sum([
            invoice_data.vendor_name is not None,
            invoice_data.invoice_number is not None,
            invoice_data.invoice_date is not None,
            invoice_data.total is not None,
            invoice_data.subtotal is not None,
            invoice_data.tax is not None,
            len(invoice_data.line_items) > 0,
            invoice_data.vendor_address is not None,
            invoice_data.vendor_phone is not None,
            invoice_data.due_date is not None,
            invoice_data.currency is not None,
        ])
        confidence = round(filled_fields / total_fields, 2)
        
        return ExtractionResponse(
            status="success",
            confidence=confidence,
            data=invoice_data,
            processing_time_ms=processing_time,
            ocr_text_preview=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    # Check dependencies on startup
    if not TESSERACT_AVAILABLE:
        print("\n⚠️  WARNING: Tesseract not found!")
        print("   Install from: https://github.com/UB-Mannheim/tesseract/wiki\n")
    
    if not OLLAMA_AVAILABLE:
        print("\n⚠️  WARNING: Ollama not running!")
        print("   1. Install from: https://ollama.ai")
        print("   2. Run: ollama pull llama3.2")
        print("   3. Start: ollama serve\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)