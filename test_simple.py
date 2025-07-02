"""
Simple API Connection Test

This script tests basic connectivity to the MOSDAC AI Bot API
without requiring the full setup.
"""

import requests
import time

def test_api_connection():
    """Test if the API server is running and responding"""
    api_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing MOSDAC AI Bot API Connection")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("1. Testing server connectivity...")
    try:
        response = requests.get(f"{api_url}/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running and accessible")
        else:
            print(f"   ❌ Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is not running or not accessible")
        print("   💡 Start the server with: python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ Server is not responding (timeout)")
        return False
    
    # Test 2: Check API health
    print("2. Testing API health...")
    try:
        response = requests.get(f"{api_url}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ API is healthy")
        else:
            print(f"   ⚠️  API responded with status code: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  API health check failed: {e}")
    
    # Test 3: Test simple query
    print("3. Testing query endpoint...")
    try:
        test_query = {
            "query": "What is MOSDAC?"
        }
        
        response = requests.post(
            f"{api_url}/query",
            json=test_query,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Query endpoint is working")
            print(f"   📝 Response preview: {result.get('answer', 'No answer')[:100]}...")
        else:
            print(f"   ❌ Query failed with status code: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Query timed out (this might indicate missing API key or vector store)")
        return False
    except Exception as e:
        print(f"   ❌ Query failed: {e}")
        return False
    
    print("\n🎉 All tests passed! The API is working correctly.")
    return True

if __name__ == "__main__":
    success = test_api_connection()
    
    if not success:
        print("\n🔧 Troubleshooting Tips:")
        print("- Make sure the backend server is running")
        print("- Check that your .env file has a valid GOOGLE_API_KEY")
        print("- Ensure the vector store exists (run data_ingestion.py)")
        print("- Try running the full setup with run.bat or run_in_venv.bat")
    
    input("\nPress Enter to exit...")
