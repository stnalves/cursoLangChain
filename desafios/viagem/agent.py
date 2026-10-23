import os
from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# ==========================================
# 1. Definição de Esquemas (Contrato de Saída)
# ==========================================
class ActivityModel(BaseModel):
    day: int = Field(description="Travel day number (e.g., 1, 2, 3)")
    activity: str = Field(description="Detailed description of the daily activity")

class ExtractedInfo(BaseModel):
    destination: str = Field(description="City of destination")
    duration_days: int = Field(description="Number of days of the trip")
    interests: List[str] = Field(description="List of user interests")

class ItineraryModel(BaseModel):
    activities: List[ActivityModel] = Field(description="List with at least 1 activity per day")

# ==========================================
# 2. Estado do Grafo
# ==========================================
class AgentState(TypedDict):
    request: str
    status: str
    destination: Optional[str]
    duration_days: Optional[int]
    interests: List[str]
    activities: List[dict]

# ==========================================
# 3. Nós do LangGraph
# ==========================================
def extract_info_node(state: AgentState):
    """Extrai informações principais do pedido original."""
    llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)
    structured_llm = llm.with_structured_output(ExtractedInfo)
    
    prompt = f"Analyze the following travel request and extract the destination city, duration in days, and a list of interests: {state['request']}"
    result = structured_llm.invoke(prompt)
    
    # Se falhar a extração, garantimos que levante exceção
    if not result:
        raise ValueError("O LLM não conseguiu extrair as informações no formato estruturado.")
        
    return {
        "destination": result.destination,
        "duration_days": result.duration_days,
        "interests": result.interests
    }

def generate_itinerary_node(state: AgentState):
    """Gera o roteiro estruturado em formato JSON."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    structured_llm = llm.with_structured_output(ItineraryModel)
    
    # Previne erros caso interests venha nulo do LLM
    interests_list = state.get('interests') or []
    interests_str = ", ".join(interests_list)
    
    prompt = (
        f"Create a travel itinerary for a {state['duration_days']}-day trip "
        f"to {state['destination']}. The user is interested in: {interests_str}. "
        "Provide EXACTLY one or more activities organized by day, starting from day 1 to "
        f"day {state['duration_days']}."
    )
    
    result = structured_llm.invoke(prompt)
    
    if not result:
        raise ValueError("O LLM não conseguiu gerar o roteiro estruturado.")
        
    activities_dict = [{"day": act.day, "activity": act.activity} for act in result.activities]
    
    return {
        "activities": activities_dict,
        "status": "success"
    }

# ==========================================
# 4. Construção do Grafo
# ==========================================
def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("extract_info", extract_info_node)
    workflow.add_node("generate_itinerary", generate_itinerary_node)
    
    workflow.add_edge(START, "extract_info")
    workflow.add_edge("extract_info", "generate_itinerary")
    workflow.add_edge("generate_itinerary", END)
    
    return workflow.compile()

# ==========================================
# 5. Ponto de Entrada do Agente
# ==========================================
def agent(user_request: str) -> dict:
    if not user_request or not user_request.strip():
        return {
            "status": "failure",
            "destination": None,
            "duration_days": None,
            "interests": [],
            "activities": []
        }

    initial_state = {
        "request": user_request,
        "status": "failure",
        "destination": None,
        "duration_days": None,
        "interests": [],
        "activities": []
    }

    try:
        graph = build_graph()
        final_state = graph.invoke(initial_state)
        
        return {
            "status": final_state.get("status", "failure"),
            "destination": final_state.get("destination"),
            "duration_days": final_state.get("duration_days"),
            "interests": final_state.get("interests", []),
            "activities": final_state.get("activities", [])
        }
    except Exception as e:
        # AGORA IMPRIME O ERRO NO TERMINAL PARA DEPURARMOS SE AINDA FALHAR
        print(f"\n[ERRO NA EXECUÇÃO DO AGENTE]: {type(e).__name__} -> {str(e)}\n")
        return {
            "status": "failure",
            "destination": None,
            "duration_days": None,
            "interests": [],
            "activities": []
        }