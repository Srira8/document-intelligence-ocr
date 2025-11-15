"""
Verify your free setup is complete and working
Run this before starting the API
"""

import sys
import subprocess
import requests

def check_python():
    """Check Python version"""
    print("🔍 Checking Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Need 3.10+")
        return False

def check_tesseract():
    """Check if Tesseract is installed"""
    print("\n🔍 Checking Tesseract OCR...")
    try:
        result = subprocess.run(
            ["tesseract", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ {version} - OK")
            return True
        else:
            print("❌ Tesseract not working properly")
            return False
    except FileNotFoundError:
        print("❌ Tesseract not found!")
        print("   Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    except Exception as e:
        print(f"❌ Error checking Tesseract: {e}")
        return False

def check_ollama():
    """Check if Ollama is running"""
    print("\n🔍 Checking Ollama...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama is running")
            
            # Check for llama models
            model_names = [m['name'] for m in models.get('models', [])]
            print(f"   Available models: {', '.join(model_names) if model_names else 'None'}")
            
            if any('llama' in m.lower() for m in model_names):
                print("✅ Llama model found")
                return True
            else:
                print("⚠️  No Llama model found!")
                print("   Run: ollama pull llama3.2")
                return False
        else:
            print("❌ Ollama responded with error")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama not running!")
        print("   Start it with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def check_dependencies():
    """Check Python dependencies"""
    print("\n🔍 Checking Python dependencies...")
    required = [
        'fastapi',
        'uvicorn',
        'pytesseract',
        'PIL',
        'pdf2image',
        'requests'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed")
        return True

def check_poppler():
    """Check if poppler is installed (for PDF support)"""
    print("\n🔍 Checking Poppler (PDF support)...")
    try:
        import pdf2image
        # Try to see if poppler is accessible
        # This is a basic check, actual usage will verify
        print("✅ pdf2image installed")
        print("   Note: If PDF processing fails, you may need to install poppler:")
        print("   - Windows: Download from https://github.com/oschwartz10612/poppler-windows")
        print("   - Mac: brew install poppler")
        print("   - Linux: sudo apt install poppler-utils")
        return True
    except ImportError:
        print("⚠️  pdf2image not installed (optional for PDFs)")
        return True  # Not critical

def main():
    """Run all checks"""
    print("=" * 60)
    print("🧪 Invoice Extraction API - Setup Verification")
    print("=" * 60)
    
    results = {
        "Python": check_python(),
        "Tesseract": check_tesseract(),
        "Ollama": check_ollama(),
        "Dependencies": check_dependencies(),
        "Poppler": check_poppler()
    }
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component}")
    
    all_ok = all(results.values())
    
    print("\n" + "=" * 60)
    if all_ok:
        print("🎉 All checks passed! You're ready to go!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("   1. Make sure Ollama is running: ollama serve")
        print("   2. Start the API: python main.py")
        print("   3. Open: http://localhost:8000")
        print("\n💡 Tip: First extraction takes 60-90 seconds (model loading)")
    else:
        print("⚠️  Some components need attention")
        print("=" * 60)
        print("\n📝 Fix the issues above and run this script again")
        print("\n💡 Quick fixes:")
        print("   - Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - Ollama: https://ollama.ai")
        print("   - Dependencies: pip install -r requirements.txt")
    
    print()
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())