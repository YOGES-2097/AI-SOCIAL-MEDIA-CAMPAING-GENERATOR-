import os
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def analyze_poster(image_bytes: bytes) -> str:
    """Takes an uploaded image and returns a detailed description for the copywriter."""
    
    # Initialize the Gemini Vision model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Convert the raw image bytes to base64 so the API can read it
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    
    # Construct the multimodal message
    message = HumanMessage(
        content=[
            {
                "type": "text", 
                "text": "Analyze this social media poster. Describe the product, the target audience, the mood, and any text visible. Be concise but highly descriptive so an AI copywriter can use this to write a matching caption."
            },
            {
                "type": "image_url", 
                "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
            }
        ]
    )
    
    try:
        response = llm.invoke([message])
        return response.content
    except Exception as e:
        print(f"Vision API Error: {e}")
        return "Failed to analyze the provided image."