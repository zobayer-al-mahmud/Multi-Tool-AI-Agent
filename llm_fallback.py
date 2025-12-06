import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_openai import ChatOpenAI

# Load .env from the project root directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class FallbackLLM:
    def __init__(self):
        # OpenAI via GitHub Token (GitHub models)
        token = os.getenv("GITHUB_TOKEN")
        endpoint = "https://models.inference.ai.azure.com"
        model_name = "gpt-4o-mini"
        
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set. Please provide a valid token.")
        
        self.openai = ChatOpenAI(
            model_name=model_name,
            openai_api_key=token,
            openai_api_base=endpoint,
            temperature=0.5,
        )

        # Gemini fallback
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini = genai.GenerativeModel("gemini-2.5-flash")

    def run(self, prompt):
        """
        Try OpenAI → if fails, fallback to Gemini.
        """
        try:
            resp = self.openai.invoke(prompt)
            return resp.content
        
        except Exception as e:
            print("⚠️ OpenAI failed, switching to Gemini...", e)

            try:
                result = self.gemini.generate_content(prompt)
                return result.text
            except Exception as e2:
                return f"Both OpenAI and Gemini failed: {e2}"
