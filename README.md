
# Multi‑Tool Medical AI Agent

A multi‑tool AI assistant that can:

- Query three structured medical datasets (Heart Disease, Cancer, Diabetes) via SQLite + Text‑to‑SQL
- Use web search for general medical knowledge (definitions, symptoms, treatments)
- Seamlessly route each question to the right tool using an LLM‑powered agent

Built with LangChain, LangGraph, OpenAI‑compatible GitHub Models, Gemini, and Tavily.

---

## 🧠 Project Overview

This project implements an **agentic AI system** that combines:

- **Structured data tools** (SQL agents over medical datasets)
- **Web search tool** (Tavily API)
- **LLM routing + reasoning** (GitHub Models via OpenAI client, with Gemini fallback)
- **Agent orchestration** (LangGraph `create_react_agent`)

The agent can answer:

- **Dataset questions**
  - “How many heart patients are older than 50?”
  - “What is the average glucose level in the diabetes dataset?”
  - “How many cancer patients are labeled malignant?”

- **General medical questions**
  - “What are early symptoms of heart disease?”
  - “How can diabetes be prevented?”
  - “What causes cancer?”

> This is **not** a RAG (Retrieval-Augmented Generation) system. It is a **multi-tool agent** combining Text‑to‑SQL with web search.

---

## 📂 Project Structure

```text
Multi-Tool AI Agent/
├─ agents/
│  ├─ db_agents.py           # SQL agents for each medical DB
│  └─ web_search_tool.py     # Tavily-based medical web search tool
├─ data/                     # Kaggle CSVs (not committed)
├─ databases/
│  ├─ heart_disease.db
│  ├─ cancer.db
│  └─ diabetes.db
├─ scripts/
│  └─ create_databases.py    # CSV → SQLite conversion
├─ llm_fallback.py           # GitHub Models + Gemini fallback LLM wrapper
├─ main.py                   # Main multi-tool agent entrypoint
├─ requirements.txt
├─ .env                      # Local secrets (ignored)
├─ .env.example              # Example environment variables
├─ .gitignore
├─ LICENSE
└─ README.md
```

---

## ✨ Features

### 1. Medical Dataset SQL Agents

Defined in `agents/db_agents.py`:

- Uses `SQLDatabase`, `SQLDatabaseToolkit`, and `create_sql_agent`.
- Connects to:
  - `databases/heart_disease.db` (table `heart_patients`)
  - `databases/cancer.db` (table `cancer_patients`)
  - `databases/diabetes.db` (table `diabetes_patients`)
- Exposes three agents:
  - `get_heart_agent()` → used as **HeartDiseaseDBTool**
  - `get_cancer_agent()` → used as **CancerDBTool**
  - `get_diabetes_agent()` → used as **DiabetesDBTool**

These agents let the LLM:

- Inspect table schemas
- Generate SQL queries
- Execute the queries
- Return results in natural language

### 2. Medical Web Search Tool

Defined in `agents/web_search_tool.py`:

- Uses `TavilySearchResults(max_results=3)` from LangChain community tools.
- Exposed as **MedicalWebSearchTool** in `main.py`.
- Intended for:
  - Definitions
  - Symptoms and causes
  - Treatments and lifestyle advice

### 3. Fallback LLM Strategy

Implemented in `llm_fallback.py` as `FallbackLLM`:

- **Primary LLM**: GitHub Models via the OpenAI-compatible client
  - Reads `GITHUB_TOKEN` from `.env`.
  - Uses an OpenAI-compatible endpoint (e.g. `https://models.github.ai/inference`).
- **Fallback LLM**: Google Gemini (`gemini-2.5-flash`)
  - Reads `GEMINI_API_KEY` from `.env`.

The `FallbackLLM`:

1. Tries to answer using GitHub Models.
2. If there is an error (e.g. API failure), it falls back to Gemini and returns that answer.

### 4. Main Agent Orchestration

Defined in `main.py`:

- Uses `create_react_agent` from `langgraph.prebuilt`.
- Uses the `ChatOpenAI` instance from `FallbackLLM` as the LLM.
- Registers four tools:
  - `HeartDiseaseDBTool`
  - `CancerDBTool`
  - `DiabetesDBTool`
  - `MedicalWebSearchTool`
- Adds a system instruction to guide routing:
  - Use DB tools for statistics / dataset queries.
  - Use web search for general medical knowledge.

The CLI loop:

- Prompts the user (`You: ...`).
- Sends the query as a message to the LangGraph agent.
- Prints the final AI answer extracted from the graph’s message list.

---

## 🛠️ Setup

### 1. Clone the Repository

```powershell
git clone <your-repo-url> "Multi-Tool AI Agent"
cd "Multi-Tool AI Agent"
```

### 2. Create & Activate Virtual Environment (Windows / PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```env
# GitHub Models (OpenAI-compatible)
GITHUB_TOKEN=ghp_your_github_token_here

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Tavily Web Search
TAVILY_API_KEY=tvly_your_tavily_api_key_here
```

> Never commit `.env` to Git.

---

## 🗄️ Preparing the Databases

### 1. Download Kaggle Datasets

Place the following CSVs into the `data/` folder:

- **Heart Disease Dataset**  
  https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset  
  Save as: `data/heart.csv`

- **Cancer Prediction Dataset**  
  https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset  
  Save as: `data/cancer.csv`

- **Diabetes Dataset**  
  https://www.kaggle.com/datasets/mathchi/diabetes-data-set  
  Save as: `data/diabetes.csv`

### 2. Convert CSVs → SQLite

Run the helper script:

```powershell
.\venv\Scripts\Activate.ps1
python .\scripts\create_databases.py
```

This will create:

- `databases/heart_disease.db` with table `heart_patients`
- `databases/cancer.db` with table `cancer_patients`
- `databases/diabetes.db` with table `diabetes_patients`

---

## ▶️ Running the Agent

With the virtual environment active and `.env` + databases ready:

```powershell
.\venv\Scripts\Activate.ps1
python .\main.py
```

You should see:

```text
🔥 Multi-Tool Medical Agent with Fallback LLM Ready!
Type 'exit' to quit.
You:
```

Now you can start chatting.

---

## 💬 Example Queries

### Dataset‑Focused (DB tools)

- Heart Disease:
  - “How many heart patients are older than 50?”
  - “What is the average cholesterol level in the heart disease dataset?”
- Diabetes:
  - “What is the average glucose level in the diabetes dataset?”
  - “How many diabetes patients are older than 60?”
- Cancer:
  - “How many cancer patients are labeled as malignant?”
  - “What is the average BMI for malignant cancer patients?”

### Web Knowledge (Tavily)

- “What are early symptoms of heart disease?”
- “How can diabetes be prevented?”
- “What causes cancer?”
- “What lifestyle changes reduce cardiovascular risk?”

---

## 🔍 How Tool Routing Works

The main agent uses:

- A **system message** describing when to use each tool.
- Clear tool descriptions in `main.py`.

The ReAct agent then:

1. Interprets the user query.
2. Selects the appropriate tool (`HeartDiseaseDBTool`, `CancerDBTool`, `DiabetesDBTool`, or `MedicalWebSearchTool`).
3. Executes one or more tool calls.
4. Produces a final natural language answer.

---

## ✅ Assignment Mapping

- **1. Convert CSVs to SQLite DBs**  
  Implemented in `scripts/create_databases.py` + `databases/`.

- **2. Build DB‑specific Agents (Tools)**  
  `HeartDiseaseDBTool`, `CancerDBTool`, `DiabetesDBTool` wired in `main.py` via `agents/db_agents.py`.

- **3. Add a Web Search Tool**  
  `MedicalWebSearchTool` implemented via Tavily in `agents/web_search_tool.py`.

- **4. Main AI Agent Logic**  
  `main.py` uses LangGraph `create_react_agent` + tools to route queries correctly.

---

## 📜 License

This project is licensed under the MIT License — see [`LICENSE`](./LICENSE) for details.

Built with LangChain, LangGraph, OpenAI (via GitHub Models), Gemini, and Tavily.

---

## 🧠 Project Overview

This project implements an **agentic AI system** that combines:

- **Structured data tools** (SQL agents over medical datasets)
- **Web search tool** (Tavily API)
- **LLM routing + reasoning** (GitHub Models via OpenAI client, with Gemini fallback)
- **Agent orchestration** (LangGraph `create_react_agent`)

The agent can answer:

- Dataset questions:  
  “How many heart patients are older than 50?”  
  “What is the average glucose level in the diabetes dataset?”  
  “How many cancer patients are labeled malignant?”

- General medical questions:  
  “What are early symptoms of heart disease?”  
  “How can diabetes be prevented?”  
  “What causes cancer?”

---

## 📂 Project Structure

Key files and folders:

- `main.py`  
  Entry point. Builds the **main multi‑tool agent** and runs the CLI loop.

- `llm_fallback.py`  
  Defines `FallbackLLM`:
  - Primary LLM: GitHub Models via OpenAI client (`ChatOpenAI` wrapper)
  - Fallback LLM: Google Gemini (`gemini-2.5-flash`)
  - Uses `GITHUB_TOKEN` and `GEMINI_API_KEY` from `.env`.

- `agents/`
  - `db_agents.py`  
    Creates SQL agents for each SQLite DB using:
    - `SQLDatabase`
    - `SQLDatabaseToolkit`
    - `create_sql_agent`
    - Tools:
      - `get_heart_agent()` → `heart_disease.db`
      - `get_cancer_agent()` → `cancer.db`
      - `get_diabetes_agent()` → `diabetes.db`
  - `web_search_tool.py`  
    Defines `get_medical_web_search_tool()` using `TavilySearchResults`.

- `scripts/`
  - `create_databases.py`  
    Converts CSVs into SQLite databases:
    - `data/heart.csv` → `databases/heart_disease.db` (table `heart_patients`)
    - `data/cancer.csv` → `databases/cancer.db` (table `cancer_patients`)
    - `data/diabetes.csv` → `databases/diabetes.db` (table `diabetes_patients`)

- `databases/`
  - `heart_disease.db`
  - `cancer.db`
  - `diabetes.db`

- `data/`
  - Expected CSVs (you download them from Kaggle):
    - `heart.csv`
    - `cancer.csv`
    - `diabetes.csv`

- `requirements.txt`  
  Python dependencies.

- `.env`  
  API keys and tokens (not committed).

---

## ✨ Features

### 1. Medical Dataset SQL Agents

For each dataset:

- Connects to a SQLite DB (`heart_disease.db`, `cancer.db`, `diabetes.db`)
- Uses LangChain’s `SQLDatabaseToolkit` + `create_sql_agent`
- Lets the LLM:
  - Inspect schema
  - Generate SQL queries
  - Execute them safely
  - Return a natural language explanation

Tools exposed in `main.py`:

- `HeartDiseaseDBTool`
- `CancerDBTool`
- `DiabetesDBTool`

### 2. Medical Web Search Tool

- Implemented in `agents/web_search_tool.py`
- Uses `TavilySearchResults(max_results=3)`
- Intended for:
  - Definitions (e.g., “What is diabetes?”)
  - Symptoms, causes, risk factors
  - Treatments and prevention

Tool in `main.py`:

- `MedicalWebSearchTool`

### 3. Fallback LLM Strategy

Defined in `llm_fallback.py`:

- Primary: GitHub Models via `ChatOpenAI`
  - Endpoint: `https://models.github.ai/inference`
  - Model: GitHub Models OpenAI‑compatible model (configured as `gpt-4o-mini` / `openai/gpt-4.1-mini`, depending on config)
- Fallback: Google Gemini
  - Model: `gemini-2.5-flash`
- Logic:
  - Try GitHub Models first
  - If it fails (API error, rate limit, etc.), automatically fallback to Gemini

### 4. Main Agent Orchestration (LangGraph ReAct Agent)

In `main.py`:

- Builds a **ReAct‑style agent** using:
  - `create_react_agent` from `langgraph.prebuilt`
  - The `FallbackLLM`’s `ChatOpenAI` instance as the LLM
  - The four tools (3 DB tools + web search tool)
- Uses a system prompt to instruct the agent:
  - Use DB tools for numeric/statistical queries
  - Use `MedicalWebSearchTool` for general medical knowledge

The CLI loop:

- Reads user input
- Sends it to the LangGraph agent via `agent.invoke({"messages": [("user", query)]})`
- Prints the final answer.

---

## 🛠️ Setup

### 1. Clone the Repository

```powershell
git clone <your-repo-url> "Multi-Tool AI Agent"
cd "Multi-Tool AI Agent"
```

### 2. Create & Activate Virtual Environment (Windows / PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root with:

```env
# GitHub Models (used via OpenAI client)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Tavily Web Search
TAVILY_API_KEY=tvly_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> Do **not** commit `.env` to version control.

---

## 🗄️ Preparing the Databases

### 1. Download the Datasets from Kaggle

Download and place the CSV files into the `data/` folder:

- Heart Disease Dataset  
  https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset  
  → save as `data/heart.csv`

- Cancer Prediction Dataset  
  https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset  
  → save as `data/cancer.csv`

- Diabetes Dataset  
  https://www.kaggle.com/datasets/mathchi/diabetes-data-set  
  → save as `data/diabetes.csv`

### 2. Run the Database Creation Script

```powershell
.\venv\Scripts\Activate.ps1
python .\scripts\create_databases.py
```

This will create:

- `databases/heart_disease.db` with table `heart_patients`
- `databases/cancer.db` with table `cancer_patients`
- `databases/diabetes.db` with table `diabetes_patients`

---

## ▶️ Running the Agent

With the virtual environment activated and `.env` configured:

```powershell
.\venv\Scripts\Activate.ps1
python .\main.py
```

You should see:

```text
🔥 Multi-Tool Medical Agent with Fallback LLM Ready!
Type 'exit' to quit.
You:
```

Now you can start asking questions.

---

## 💬 Example Queries

### Database‑Focused Questions (will use DB tools)

- Heart Disease:
  - “How many heart patients are older than 50?”
  - “What is the average cholesterol level in the heart disease dataset?”
- Diabetes:
  - “What is the average glucose level in the diabetes dataset?”
  - “How many diabetes patients are older than 60?”
- Cancer:
  - “How many cancer patients are labeled as malignant?”
  - “What is the average BMI for malignant cancer patients?”

### Web Knowledge Questions (will use Tavily)

- “What are early symptoms of heart disease?”
- “How can diabetes be prevented?”
- “What causes cancer?”
- “What lifestyle changes reduce cardiovascular risk?”

---

## 🔍 How the Routing Works

The main agent uses:

- A **system message** that explains:
  - Use DB tools for statistical/data questions.
  - Use the web search tool for definitions/symptoms/causes/treatments.
- Tool descriptions reinforce correct tool choice.

The ReAct agent then:

1. Interprets the user’s question.
2. Chooses the appropriate tool:
   - `HeartDiseaseDBTool`, `CancerDBTool`, `DiabetesDBTool`, or `MedicalWebSearchTool`.
3. Executes one or more tool calls.
4. Produces a final natural language answer.

---

## ⚠️ Notes & Limitations

- **Not a RAG agent:**  
  This project does **not** use vector stores or semantic document retrieval. It’s a **multi‑tool agent** combining:
  - Text‑to‑SQL over structured datasets
  - Web search for general knowledge
- **Python 3.14 warning:**  
  You may see Pydantic/LangChain warnings about Python 3.14; they are deprecation warnings but do not stop execution.
- **API costs:**  
  GitHub Models, Gemini, and Tavily may incur usage costs depending on your quota/plan.

