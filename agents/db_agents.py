import os
import sys
from dotenv import load_dotenv

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

# Add parent directory to path to import llm_fallback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_fallback import FallbackLLM

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "databases")


def _make_sql_agent(db_file):
    db_path = os.path.join(DB_DIR, db_file)
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    fallback_llm = FallbackLLM()
    # Use the ChatOpenAI instance directly
    llm = fallback_llm.openai

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type="openai-tools",
        verbose=True
    )


def get_heart_agent():
    return _make_sql_agent("heart_disease.db")

def get_cancer_agent():
    return _make_sql_agent("cancer.db")

def get_diabetes_agent():
    return _make_sql_agent("diabetes.db")


