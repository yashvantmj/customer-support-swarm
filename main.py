# Multi-Agent Customer Support Swarm – Works instantly on Replit
# Paste this entire file into main.py and hit Run

import os
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, VERBOSE

# Ensure API key is set for the SDKs that expect it from environment variables
os.environ.setdefault("GROQ_API_KEY", GROQ_API_KEY)

# Install (Replit does this automatically on first run)
# Just keep this line at the top
# pip install crewai==1.6.1 crewai-tools==1.6.1 langchain-groq==0.1.3

from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM as CrewLLM
from crewai.tools import BaseTool
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import Type

# Support a test mode where an offline Dummy LLM is used to avoid external API calls
if os.getenv("TEST_MODE", "0") in ("1", "true", "True"):
    class DummyLLM(CrewLLM):
        def __init__(self, model: str | None = None, temperature: float = 0.2, **kwargs):
            # Don't forward is_litellm to super().__init__ (it's handled in __new__)
            super().__init__(model=model or "dummy", temperature=temperature, **kwargs)
        def call(self, *args, **kwargs):
            return "DUMMY RESPONSE"
        async def acall(self, *args, **kwargs):
            return "DUMMY RESPONSE"
    # Use a dummy model name so crewai doesn't attempt to import a native provider
    # Set is_litellm=True so the LLM base class doesn't attempt to load native providers
    llm = DummyLLM(model="dummy", temperature=TEMPERATURE, is_litellm=True)
else:
    llm = ChatGroq(model=MODEL_NAME, temperature=TEMPERATURE)

# ——— Tools ———
class PolicyQuery(BaseModel):
    topic: str = Field(..., description="Policy topic")

class PolicyTool(BaseTool):
    name: str = "Policy Lookup"
    description: str = "Company policies and pricing"
    args_schema: Type[BaseModel] = PolicyQuery
    def _run(self, topic: str) -> str:
        policies = {"refund": "Full refund within 7 days", "cancel": "Cancel anytime", "pricing": "Basic $19 → Pro $49 → Enterprise custom"}
        return policies.get(topic.lower(), "Escalate to human")

class EscalateQuery(BaseModel):
    ticket_id: str = Field(..., description="Ticket ID")

class EscalateTool(BaseTool):
    name: str = "Escalate to Human"
    description: str = "Escalates urgent tickets"
    args_schema: Type[BaseModel] = EscalateQuery
    def _run(self, ticket_id: str) -> str:
        return f"ESCALATED {ticket_id} to human support"

# ——— Agents ———
triage   = Agent(role="Triage",    goal="Classify urgency & category",   backstory="Ex-support lead", tools=[PolicyTool()], llm=llm, verbose=VERBOSE)
research = Agent(role="Research",  goal="Find exact policy",             backstory="Walking KB",      tools=[PolicyTool()], llm=llm, verbose=VERBOSE)
writer   = Agent(role="Writer",    goal="Empathetic reply <120 words",   backstory="CX writer",       tools=[],             llm=llm, verbose=VERBOSE)
guardian = Agent(role="Guardian",  goal="Check tone & compliance",       backstory="Compliance pro",  tools=[PolicyTool()], llm=llm, verbose=VERBOSE)
closer   = Agent(role="Closer",    goal="Finalize or escalate",          backstory="Process nerd",    tools=[EscalateTool()], llm=llm, verbose=VERBOSE)

# ——— Swarm ———
def run_support_swarm(query: str, id: str = "T001"):
    # Build tasks sequentially so contexts can reference earlier tasks
    t1 = Task(description=f"Classify: {query}", expected_output="Category + urgency", agent=triage)
    t2 = Task(description="Research policy", expected_output="Key facts", agent=research, context=[t1])
    t3 = Task(description="Draft reply", expected_output="Kind message", agent=writer, context=[t1, t2])
    t4 = Task(description="Review tone/compliance", expected_output="Approved reply", agent=guardian, context=[t1, t2, t3])
    t5 = Task(description="Finalize/escalate", expected_output="Customer message", agent=closer, context=[t1, t2, t3, t4])
    tasks = [t1, t2, t3, t4, t5]
    crew = Crew(agents=[triage,research,writer,guardian,closer], tasks=tasks, process=Process.sequential, verbose=VERBOSE)
    result = crew.kickoff()
    print(f"\n{id} RESOLVED:\n{result}\n" + "—"*70)
    return result

# ——— Demo tickets ———
print("MULTI-AGENT SUPPORT SWARM – LIVE ON REPLIT\n" + "="*70)
tickets = [
    "Charged but never used the product – full refund?",
    "How do I cancel my subscription?",
    "App keeps crashing on iPhone 16 – urgent!",
    "What’s the price difference between Pro and Enterprise?",
    "Someone logged in from Russia – lock my account now!!"
]

for i, msg in enumerate(tickets, 1):
    run_support_swarm(msg, f"T{i:03d}")