import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load variables from the .env file
load_dotenv()

print("--- Gemini API Test Script ---")

# 1. Check if the key is loaded from .env
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY was not found in the environment.")
    print("Please check your .env file.")
else:
    print("API Key found in environment.")
    # For security, let's only print the first and last few characters
    print(f"Key starts with: {api_key[:4]}... ends with: {api_key[-4:]}")

# 2. Try to initialize and make a simple call to the model
try:
    print("\nInitializing Gemini model...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    print("Model initialized successfully.")

    print("\nSending a simple test prompt to Gemini...")
    response = llm.invoke("Hello, what is your name?")
    
    print("\nSUCCESS! Received a response from Gemini:")
    print("------------------------------------------")
    print(response.content)
    print("------------------------------------------")

except Exception as e:
    print("\n--- ERROR DURING API CALL ---")
    print("An exception occurred:")
    print(e)
    print("-----------------------------")