from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage

from llm_fallback import FallbackLLM
from agents.db_agents import get_heart_agent, get_cancer_agent, get_diabetes_agent
from agents.web_search_tool import get_medical_web_search_tool

load_dotenv()


def build_main_agent():

    fallback = FallbackLLM()
    # Use the ChatOpenAI instance directly
    llm = fallback.openai

    # Tools
    heart = get_heart_agent()
    cancer = get_cancer_agent()
    diabetes = get_diabetes_agent()
    web_search = get_medical_web_search_tool()

    tools = [
        Tool(
            name="HeartDiseaseDBTool",
            func=lambda q: heart.invoke({"input": q})["output"],
            description="Use for heart-disease dataset statistics."
        ),
        Tool(
            name="CancerDBTool",
            func=lambda q: cancer.invoke({"input": q})["output"],
            description="Use for cancer dataset analysis."
        ),
        Tool(
            name="DiabetesDBTool",
            func=lambda q: diabetes.invoke({"input": q})["output"],
            description="Use for diabetes dataset analysis."
        ),
        Tool(
            name="MedicalWebSearchTool",
            func=lambda q: web_search.run(q),
            description="Use for medical definitions, symptoms, causes, treatments."
        ),
    ]

    # Create the agent using LangGraph
    system_message = "You are a helpful medical assistant with access to multiple tools. Use them to answer questions about heart disease, cancer, diabetes, and general medical information."
    
    agent_executor = create_react_agent(llm, tools, prompt=system_message)

    return agent_executor


def main():
    agent = build_main_agent()

    print("\n🔥 Multi-Tool Medical Agent with Fallback LLM Ready!")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        # LangGraph agent expects a dictionary with "messages"
        result = agent.invoke({"messages": [("user", query)]})
        
        # The result contains the full state, we want the last message content
        last_message = result["messages"][-1]
        print("\nAI:", last_message.content, "\n")



if __name__ == "__main__":
    main()
