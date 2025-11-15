

# **📄 Invoice Extraction API — 100% Free Version**

An AI-powered REST API that extracts structured data from invoices and receipts using **Tesseract OCR** and **Ollama (Llama 3.2)** — completely free and fully local.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

# Images

![alt text](image-1.png)
![alt text](image.png)

---

## ✨ Features

* 🆓 **100% free** — No API keys or credits
* 🚀 **FastAPI backend**
* 🎨 **Simple Web UI**
* 📊 **Structured JSON output**
* 📁 **Supports PDF, PNG, JPG**
* 🔒 **Fully local & privacy-safe**
* 📦 **Docker-ready**
* 📖 **Interactive API docs at `/docs`**

---

## 🎯 What It Extracts

### Vendor Info

* Company name
* Address
* Phone

### Invoice Details

* Invoice number
* Invoice date
* Due date

### Financial Data

* Subtotal
* Tax
* Total
* Currency

### Line Items

* Description
* Quantity
* Unit price
* Line total

---

## 🚀 Quick Start

### Prerequisites

* Python 3.10+
* Tesseract OCR
* Ollama + Llama 3.2

---

## Installation

### 1️⃣ Install Tesseract

**Mac**

```bash
brew install tesseract
```

**Linux**

```bash
sudo apt install tesseract-ocr poppler-utils
```

**Windows**
Download from UB Mannheim build and add to PATH.

---

### 2️⃣ Install Ollama + Model

```bash
ollama pull llama3.2
ollama serve
```

---

### 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Verify Setup

```bash
python verify_setup.py
```

---

## ▶️ Run API Server

```bash
python main.py
```

Open: **[http://localhost:8000](http://localhost:8000)**

---

## 📖 Usage

### Web UI

1. Open `http://localhost:8000`
2. Upload an invoice
3. Receive extracted JSON

---

## API Endpoint (No API Key Needed)

**POST** `/api/v1/extract/invoice`

```bash
curl -X POST "http://localhost:8000/api/v1/extract/invoice" \
  -F "file=@invoice.pdf"
```

### Example Response

```json
{
  "status": "success",
  "confidence": 0.92,
  "processing_time_ms": 24153,
  "data": {
    "vendor_name": "ACME Corporation",
    "total": 20072.5,
    "currency": "USD"
  }
}
```

---

## Python Client Example

```python
import requests

files = {"file": open("invoice.pdf", "rb")}
response = requests.post("http://localhost:8000/api/v1/extract/invoice", files=files)

print(response.json())
```

---

## 🧪 Testing

Generate a sample invoice:

```bash
python generate_sample_invoice.py
```

Generate multiple:

```bash
python generate_test_suite.py
```

Run tests:

```bash
python test_api.py sample_invoice.pdf
```

---

## 📊 Performance

| Metric        | Value         |
| ------------- | ------------- |
| First request | 60–90 seconds |
| Subsequent    | 30–45 seconds |
| Accuracy      | 75–85%        |

---

## 🏗️ Architecture

```
User → FastAPI → Tesseract OCR → Ollama (Llama 3.2) → JSON Output
```

---

## 📁 Project Structure

```
invoice-extraction-api/
├── main.py
├── requirements.txt
├── verify_setup.py
├── generate_sample_invoice.py
├── generate_test_suite.py
├── test_api.py
├── test_invoices/
└── sample_invoice.pdf
```

---

## ⚙️ Configuration

Optional `.env`:

```bash
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
HOST=0.0.0.0
PORT=8000
```

---

## 🔧 Troubleshooting

### Tesseract not found

Reinstall via brew/apt or add Windows PATH.

### Ollama not running

```bash
ollama serve
```

### PDF processing fails

Install poppler:

```bash
brew install poppler
```

---

## 🚀 Production Deployment

Optional upgrade for faster performance (3–5 seconds):

* Azure Document Intelligence
* OpenAI GPT-4

Deployment options:

* Google Cloud Run
* DigitalOcean
* Azure App Service
* AWS ECS

---

## 📈 Roadmap

* [x] Invoice extraction
* [x] Web UI
* [x] Docker support
* [ ] Batch processing
* [ ] Database integration
* [ ] Export to CSV/Excel
* [ ] Multi-language support
* [ ] Admin dashboard

---

## 🤝 Contributing

1. Fork
2. Create a new branch
3. Commit changes
4. Open PR

---

## 📄 License

MIT License

---

## 👤 Author

**Sriram Krishna**
GitHub: [https://github.com/Srira8](https://github.com/Srira8)
Email: [sriramvk2908@gmail.com](mailto:sriramvk2908@gmail.com)

---

## ⭐ Support

If this project helped you, please give it a ⭐!

---



Just tell me!
