from models import EmailState
from langgraph.graph import StateGraph, START, END
from agents import (
    duplicate_checker,
    router,
    intent_identifier,
    intent_clasifier,
    fields_extractor
)
graph = StateGraph(EmailState)
graph.add_node("duplicate_checker", duplicate_checker)
graph.add_node("intent_identifier", intent_identifier)
graph.add_node("intent_classifier", intent_clasifier)
graph.add_node("fields_extractor", fields_extractor)

graph.add_edge(START, "duplicate_checker")
graph.add_conditional_edges("duplicate_checker", router, {True: END, False: "intent_identifier"})
graph.add_edge("intent_identifier", "intent_classifier")
graph.add_edge("intent_classifier", "fields_extractor")
graph.add_edge("fields_extractor", END)
compiled_graph = graph.compile()


def agentic_email_triage(email_content: str):
    state = EmailState(email_content=email_content)
    result = compiled_graph.invoke(state)
    print(result)
    return {
        "email_intent": result["email_intent"],
        "is_duplicate": result["is_duplicate"],
        "dup_reason": result["dup_reason"],
        "classification_result": result["classification_result"],
        "extracted_fields": result["extracted_fields"]
    }