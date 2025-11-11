import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from tools.greenhouse_tools import search_jobs_tool, search_greenhouse_jobs
from dotenv import load_dotenv
load_dotenv()


async def main():
    agent = FunctionAgent(
        tools=[search_jobs_tool],
        llm=OpenAI(model="gpt-4o-mini"),
        system_prompt="You are a helpful assistant that searches job listings on Greenhouse by company and keyword ",
    )

    response = await agent.run("Find me engineering jobs from Stripe")

    print(str(response))


if __name__ == "__main__":
    asyncio.run(main())