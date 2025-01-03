import os

from crewai import Agent, Task, Crew
from composio_crewai import ComposioToolSet, App
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

toolset = ComposioToolSet()

connection = toolset.initiate_connection(
    app=App.NEON, connected_account_params={"neon_api_key": os.getenv("NEON_API_KEY")}
)

tools = toolset.get_tools(actions=["NEON_GET_CURRENT_USER_DETAILS"])

# Define agent
crewai_agent = Agent(
    role="Sample Agent",
    goal="""You are an AI agent that is responsible for taking actions based on the tools you have""",
    backstory=(
        "You are AI agent that is responsible for taking actions based on the tools you have"
    ),
    verbose=True,
    tools=tools,
    llm="gpt-4",
)

task = Task(
    description="list me my neon current user details",
    agent=crewai_agent,
    expected_output="",
)

my_crew = Crew(agents=[crewai_agent], tasks=[task])

result = my_crew.kickoff()
print(result)
