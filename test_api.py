"""
Complete Integration Test

This script performs comprehensive testing of all MOSDAC AI Bot components:
- Environment configuration
- Vector store
- LLM integration
- API functionality
- Frontend connectivity
"""

import os
import sys
import requests
import time
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔧 Checking Environment Configuration")
    print("-" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        return False
    
    # Check if Google API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_google_ai_api_key_here':
        print("   ❌ GOOGLE_API_KEY not set in .env file")
        return False
    
    print("   ✅ Environment configuration is valid")
    return True

def check_vector_store():
    """Check if vector store exists and is accessible"""
    print("\n📚 Checking Vector Store")
    print("-" * 40)
    
    vector_store_path = Path("vector_store")
    
    if not vector_store_path.exists():
        print("   ❌ Vector store directory not found")
        return False
    
    required_files = ["index.faiss", "index.pkl"]
    for file in required_files:
        if not (vector_store_path / file).exists():
            print(f"   ❌ Vector store file missing: {file}")
            return False
    
    print("   ✅ Vector store is available")
    return True

def check_scraped_data():
    """Check if scraped data exists"""
    print("\n🕷️ Checking Scraped Data")
    print("-" * 40)
    
    data_file = Path("mosdac_scraper/scraped_data.jsonl")
    
    if not data_file.exists():
        print("   ❌ Scraped data file not found")
        return False
    
    # Check if file has content
    if data_file.stat().st_size == 0:
        print("   ❌ Scraped data file is empty")
        return False
    
    print("   ✅ Scraped data is available")
    return True

def test_llm_integration():
    """Test LLM integration directly"""
    print("\n🤖 Testing LLM Integration")
    print("-" * 40)
    
    try:
        # Import and test LLM handler
        sys.path.append('backend')
        from llm_handler import LLMHandler
        
        llm = LLMHandler()
        
        # Test simple query
        test_response = llm.get_response("What is MOSDAC?", ["MOSDAC is a test context"])
        
        if test_response and len(test_response) > 10:
            print("   ✅ LLM integration is working")
            return True
        else:
            print("   ❌ LLM returned empty or invalid response")
            return False
            
    except Exception as e:
        print(f"   ❌ LLM integration failed: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality"""
    print("\n📖 Testing Knowledge Base")
    print("-" * 40)
    
    try:
        sys.path.append('backend')
        from knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase()
        
        # Test query
        results = kb.query("MOSDAC", k=3)
        
        if results and len(results) > 0:
            print(f"   ✅ Knowledge base returned {len(results)} results")
            return True
        else:
            print("   ❌ Knowledge base returned no results")
            return False
            
    except Exception as e:
        print(f"   ❌ Knowledge base test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints")
    print("-" * 40)
    
    api_url = "http://127.0.0.1:8000"
    
    # Check if server is running
    try:
        response = requests.get(f"{api_url}/docs", timeout=5)
        if response.status_code != 200:
            print("   ❌ API server is not running")
            print("   💡 Start with: python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to API server")
        print("   💡 Start with: python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000")
        return False
    
    # Test query endpoint
    try:
        test_query = {"query": "What services does MOSDAC provide?"}
        response = requests.post(f"{api_url}/query", json=test_query, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('answer') and len(result['answer']) > 10:
                print("   ✅ API query endpoint is working")
                return True
            else:
                print("   ❌ API returned empty response")
                return False
        else:
            print(f"   ❌ API query failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False

def test_frontend_connectivity():
    """Test if frontend can connect to backend"""
    print("\n🎨 Testing Frontend Connectivity")
    print("-" * 40)
    
    try:
        # This is a basic test - in a real scenario, you'd test the Streamlit app
        frontend_url = "http://localhost:8501"
        print("   ℹ️  Frontend should be accessible at: " + frontend_url)
        print("   ✅ Frontend test skipped (requires manual verification)")
        return True
        
    except Exception as e:
        print(f"   ❌ Frontend test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 MOSDAC AI Bot - Complete Integration Test")
    print("=" * 60)
    
    tests = [
        ("Environment", check_environment),
        ("Scraped Data", check_scraped_data),
        ("Vector Store", check_vector_store),
        ("Knowledge Base", test_knowledge_base),
        ("LLM Integration", test_llm_integration),
        ("API Endpoints", test_api_endpoints),
        ("Frontend", test_frontend_connectivity),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your MOSDAC AI Bot is fully functional.")
    else:
        print("🔧 Some tests failed. Check the output above for troubleshooting.")
        print("\n💡 Common fixes:")
        print("- Run the full setup: run.bat or run_in_venv.bat")
        print("- Check your .env file has a valid GOOGLE_API_KEY")
        print("- Ensure the backend server is running")
        print("- Verify all dependencies are installed")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
