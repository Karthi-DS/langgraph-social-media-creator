from langgraph.graph import StateGraph, END
from nodes import day_planner, content_generator, formatter, saver
from typing import TypedDict, Any

class ContentState(TypedDict):
    theme: str
    days: int
    topics: list[str]
    content_plan: list[dict]
    df: Any

def build_graph():
    graph = StateGraph(ContentState)
    
    graph.add_node("planner", day_planner.plan_days)
    graph.add_node("generator", content_generator.generate_content)
    graph.add_node("formatter", formatter.format_output)
    graph.add_node("saver", saver.save_csv)
    
    graph.set_entry_point("planner")
    graph.add_edge("planner", "generator")
    graph.add_edge("generator", "formatter")
    graph.add_edge("formatter", "saver")
    graph.add_edge("saver", END)
    
    return graph.compile()