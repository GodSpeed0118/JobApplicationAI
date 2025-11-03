# test_tool_call.py
import os, json
from openai import OpenAI
from dotenv import load_dotenv
from tools.greenhouse_tools import search_jobs_tool

load_dotenv()

# ✅ Step 1: Initialize OpenAI client (not LlamaIndex)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Step 2: Define tool schema
function_schema = {
    "name": "search_greenhouse_jobs",
    "description": "Searches job listings on Greenhouse by company and keyword.",
    "parameters": {
        "type": "object",
        "properties": {
            "company": {
                "type": "string",
                "description": "The company name whose Greenhouse board will be searched."
            },
            "keyword": {
                "type": "string",
                "description": "The job title or role keyword to search for."
            }
        },
        "required": ["company", "keyword"]
    }
}

# ✅ Step 3: Your natural-language query
query = "Find software engineer jobs at Stripe."

# ✅ Step 4: Let GPT-4o infer which tool to call + its arguments
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful job search assistant."},
        {"role": "user", "content": query},
    ],
    tools=[{"type": "function", "function": function_schema}],
    tool_choice="auto",
)

# ✅ Step 5: Parse the model’s function call
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

print(f"🧠 LLM chose tool `{tool_call.function.name}` with args:")
print(json.dumps(args, indent=2))

# ✅ Step 6: Call your tool dynamically
result = search_jobs_tool.fn(**args)
print("\n📄 Tool Output:")
print(result)
