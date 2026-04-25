import os
import base64
from io import BytesIO
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def analyze_poster(image_bytes: bytes) -> str:
    """Compresses the image using Pillow, then sends it to Gemini to save tokens."""
    # 1. Open the image from the raw Streamlit bytes
    img = Image.open(BytesIO(image_bytes))
    
    # 2. Convert to RGB (Required if the user uploads a transparent PNG)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    # 3. Resize the image (Max 1024x1024, maintains aspect ratio)
    img.thumbnail((1024, 1024))
    
    # 4. Save the compressed image back to temporary memory as a JPEG
    output_buffer = BytesIO()
    img.save(output_buffer, format="JPEG", quality=85)
    compressed_bytes = output_buffer.getvalue()
    # --------------------------------
    
    # Initialize the Gemini Vision model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Convert the COMPRESSED image bytes to base64
    image_b64 = base64.b64encode(compressed_bytes).decode("utf-8")
    
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
