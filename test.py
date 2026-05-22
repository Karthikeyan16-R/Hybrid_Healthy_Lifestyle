"""
Simple script to debug API key loading
Save this as test_api.py and run it
"""
import os
from pathlib import Path

print("=" * 70)
print("🔍 API Key Debug Script")
print("=" * 70)
print()

# Step 1: Check current directory
print("📁 Current Directory:")
print(f"   {Path.cwd()}")
print()

# Step 2: Check if .env exists
env_path = Path.cwd() / ".env"
print("📄 .env File:")
print(f"   Path: {env_path}")
print(f"   Exists: {env_path.exists()}")
print()

if env_path.exists():
    print("📝 Reading .env file directly:")
    with open(env_path, 'r') as f:
        content = f.read()
        print("-" * 70)
        # Show content but hide key value
        for line in content.split('\n'):
            if 'GOOGLE_API_KEY' in line and '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key_name = parts[0].strip()
                    key_value = parts[1].strip()
                    print(f"{key_name}={key_value[:10]}...{key_value[-5:]} (length: {len(key_value)})")
                else:
                    print(line)
            else:
                print(line)
        print("-" * 70)
    print()

# Step 3: Try loading with dotenv
print("📦 Testing dotenv:")
try:
    from dotenv import load_dotenv
    print("   ✅ dotenv imported successfully")
    
    # Load from specific path
    result = load_dotenv(env_path)
    print(f"   Load result: {result}")
    print()
    
except ImportError:
    print("   ❌ dotenv not installed!")
    print("   Run: pip install python-dotenv")
    exit(1)

# Step 4: Check environment variable
print("🔑 Environment Variable Check:")
api_key = os.getenv("GOOGLE_API_KEY")
print(f"   Found: {api_key is not None}")

if api_key:
    print(f"   Length: {len(api_key)}")
    print(f"   Starts with 'AIza': {api_key.startswith('AIza')}")
    print(f"   Has spaces: {' ' in api_key}")
    print(f"   Preview: {api_key[:15]}...{api_key[-5:]}")
    
    # Check for common issues
    if ' ' in api_key:
        print("   ⚠️ WARNING: API key contains spaces!")
    if api_key.startswith(' ') or api_key.endswith(' '):
        print("   ⚠️ WARNING: API key has leading/trailing spaces!")
else:
    print("   ❌ NOT FOUND")
    print()
    print("🔧 Trying alternative methods:")
    
    # Try reading directly
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if 'GOOGLE_API_KEY' in line and '=' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        direct_key = parts[1].strip()
                        print(f"   Found in file: {direct_key[:15]}...{direct_key[-5:]}")
                        print(f"   But not in os.getenv() - dotenv issue!")

print()

# Step 5: Test API connection
if api_key and len(api_key) > 30:
    print("🧪 Testing API Connection:")
    try:
        from google import genai
        print("   ✅ google-genai imported")
        
        client = genai.Client(api_key=api_key)
        print("   ✅ Client created")
        
        # Try to list models
        print("   🔄 Fetching models...")
        models = list(client.models.list())
        print(f"   ✅ SUCCESS! Found {len(models)} models")
        
        if models:
            print()
            print("   📋 Available models:")
            for model in models[:3]:
                print(f"      - {model.name}")
        
    except Exception as e:
        print(f"   ❌ API Error: {type(e).__name__}")
        print(f"   Message: {str(e)[:200]}")
        
        error_str = str(e)
        if "API key not valid" in error_str or "authentication" in error_str.lower():
            print()
            print("   💡 Your API key might be invalid or revoked")
            print("   Create a new one at: https://aistudio.google.com/app/apikey")
        elif "429" in error_str:
            print()
            print("   💡 Quota exceeded - wait a few minutes or create a new project")
        elif "404" in error_str:
            print()
            print("   💡 Models not found - check API access permissions")

print()
print("=" * 70)
print("✅ Debug Complete")
print("=" * 70)