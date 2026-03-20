from langgraph.graph import StateGraph, END
from packages.core.graph.state import AgentState
from packages.agents.manager import manager_node
from packages.agents.researcher import researcher_node
from packages.agents.educator import educator_node

# Initialize the Graph
workflow = StateGraph(AgentState)

# Add our Nodes (The "Agents")
workflow.add_node("manager", manager_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("educator", educator_node)

# Set the Entry Point
workflow.set_entry_point("manager")

# Define the Routing Logic
def route_decision(state: AgentState):
    return state.get("next_step", "educator")

workflow.add_conditional_edges(
    "manager",
    route_decision,
    {
        "researcher": "researcher",
        "educator": "educator"
    }
)

# Connect the remaining paths
# After researching, the Educator MUST explain the results.
workflow.add_edge("researcher", "educator")
# After educating, the conversation loop ends (until you reply).
workflow.add_edge("educator", END)

# Compile the Application
scholar_os = workflow.compile()