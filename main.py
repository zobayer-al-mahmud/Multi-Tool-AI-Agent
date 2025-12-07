import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from agents.db_agents import (
    query_heart_db,
    query_cancer_db,
    query_diabetes_db,
)
from agents.web_search_tool import run_medical_web_search


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.github.ai/inference",
)

# Use a standard model name supported by GitHub Models
MODEL = "gpt-4.1"


ASSISTANT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_heart_db",
            "description": "Query the heart disease SQLite database for statistics and insights.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Natural language question about the heart disease dataset",
                    }
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_cancer_db",
            "description": "Query the cancer SQLite database for statistics and insights.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Natural language question about the cancer dataset",
                    }
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_diabetes_db",
            "description": "Query the diabetes SQLite database for statistics and insights.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Natural language question about the diabetes dataset",
                    }
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_medical_web_search",
            "description": "Use web search to answer general medical questions (definitions, symptoms, treatments, causes).",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Medical question that requires general knowledge or up-to-date information",
                    }
                },
                "required": ["question"],
            },
        },
    },
]


def execute_tool(name, args):
    """Execute the tool and return the string output."""
    try:
        if name == "query_heart_db":
            return query_heart_db(args["question"])
        elif name == "query_cancer_db":
            return query_cancer_db(args["question"])
        elif name == "query_diabetes_db":
            return query_diabetes_db(args["question"])
        elif name == "run_medical_web_search":
            return run_medical_web_search(args["question"])
        else:
            return f"Error: Unknown tool '{name}'"
    except Exception as e:
        return f"Error executing tool '{name}': {str(e)}"


def main():
    print("\n🔥 Multi-Tool Medical Assistant (OpenAI SDK Chat Completions) Ready!")
    print("Type 'exit' to quit.\n")

    # Initialize conversation history with system instructions
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful medical assistant. "
                "Use the database tools for statistical or dataset-specific questions. "
                "Use the web search tool for definitions, symptoms, causes, and treatments."
            ),
        }
    ]

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower().strip() == "exit":
                break

            messages.append({"role": "user", "content": user_input})

            # Inner loop to handle tool calls (ReAct pattern)
            while True:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=ASSISTANT_TOOLS,
                    tool_choice="auto",
                )

                response_message = response.choices[0].message
                messages.append(response_message)

                tool_calls = response_message.tool_calls

                if tool_calls:
                    # If the model wants to call tools, execute them and feed back the results
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"   > Calling tool: {function_name}...")
                        
                        tool_output = execute_tool(function_name, function_args)
                        
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": str(tool_output),
                            }
                        )
                    # Loop continues to let the model generate a response based on tool outputs
                else:
                    # No tool calls, just a final response
                    print(f"\nAI: {response_message.content}\n")
                    break

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            # Optional: remove the last user message if it caused a crash to allow continuation
            if messages and messages[-1]["role"] == "user":
                messages.pop()


if __name__ == "__main__":
    main()
