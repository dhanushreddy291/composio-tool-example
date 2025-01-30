import os

from crewai import Agent, Task, Crew
from composio_crewai import ComposioToolSet, App
from dotenv import load_dotenv

load_dotenv()

toolset = ComposioToolSet()

# To connect to Neon, either create a new connection or use an existing one configured in your Composio dashboard (Apps -> Integrations).
# You can comment out the connection creation if you have already created a connection in the dashboard.
connection = toolset.initiate_connection(
    app=App.NEON, connected_account_params={"api_key": os.getenv("NEON_API_KEY")}
)

tools = toolset.get_tools(actions=["NEON_GET_CURRENT_USER_INFORMATION"])

# Define agent
crewai_agent = Agent(
    role="Assistant",
    goal="""You are an AI agent that is responsible for taking actions based on the tools you have""",
    backstory=(
        "You are AI agent that is responsible for taking actions based on the tools you have"
    ),
    verbose=True,
    tools=tools,
    llm="gpt-4o-mini",
)

task = Task(
    description="List me my neon current user details",
    agent=crewai_agent,
    expected_output="All important details of the current user in a single sentence.",
)

my_crew = Crew(agents=[crewai_agent], tasks=[task])

result = my_crew.kickoff()
print(result)
