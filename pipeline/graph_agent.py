from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from pipeline.image import analyze_poster
from pipeline.chains import generate_platform_content
from pipeline.vector_store import retrieve_guidelines 

# 1. Update State to include brand_rules and image_description
class CampaignState(TypedDict):
    prompt: str
    platform: str
    image_bytes: Optional[bytes]
    image_description: Optional[str]
    brand_rules: Optional[str] 
    final_campaign: Optional[str]

# 2. Add a new Node to fetch memory
def fetch_memory_node(state: CampaignState):
    """Searches ChromaDB for relevant brand rules before writing."""
    print("Searching ChromaDB for brand guidelines...")
    rules = retrieve_guidelines(state["prompt"])
    return {"brand_rules": rules}

def process_image_node(state: CampaignState):
    if state.get("image_bytes"):
        print(" Analyzing uploaded poster...")
        description = analyze_poster(state["image_bytes"])
        return {"image_description": description}
    return {"image_description": "No visual context provided."}

def generate_text_node(state: CampaignState):
    print(f" Generating campaign for {state['platform']}...")
    content = generate_platform_content(
        state["prompt"], 
        state["platform"], 
        state["image_description"],
        state["brand_rules"] 
    )
    return {"final_campaign": content}

# 3. Build the Graph
workflow = StateGraph(CampaignState)

workflow.add_node("fetch_memory", fetch_memory_node)
workflow.add_node("analyze_image", process_image_node)
workflow.add_node("generate_content", generate_text_node)

# Flow: Fetch Memory -> Analyze Image -> Generate Text -> End
workflow.set_entry_point("fetch_memory")
workflow.add_edge("fetch_memory", "analyze_image")
workflow.add_edge("analyze_image", "generate_content")
workflow.add_edge("generate_content", END)

app = workflow.compile()

def run_campaign_agent(prompt: str, platform: str, image_bytes: Optional[bytes] = None) -> str:
    initial_state = {
        "prompt": prompt, 
        "platform": platform, 
        "image_bytes": image_bytes
    }
    result = app.invoke(initial_state)
    return result["final_campaign"]