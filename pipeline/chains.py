import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# --- ADDED brand_rules to the function arguments ---
def generate_platform_content(prompt: str, platform: str, image_description: str = "No image provided.", brand_rules: str = "") -> str:
    """Generates the final social media post tailored to the specific platform."""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # --- ADDED the "Strict Brand Guidelines" section to the template ---
    template = """
    You are an expert social media marketer and copywriter for Spark AI.
    Your task is to create a highly engaging campaign tailored specifically for {platform}.
    
    User's Request / Campaign Topic: 
    {prompt}
    
    Visual Context (Description of the uploaded poster/image):
    {image_description}
    
    Strict Brand Guidelines (YOU MUST FOLLOW THESE):
    {brand_rules}
    
    Instructions:
    1. Write the perfect post for {platform}. 
    2. Adapt the tone to fit the platform.
    3. Include emojis and relevant hashtags.
    4. Ensure no Brand Guidelines are violated!
    
    Final Campaign Text:
    """
    
    prompt_template = PromptTemplate(
        input_variables=["platform", "prompt", "image_description", "brand_rules"],
        template=template
    )
    
    chain = prompt_template | llm
    
    try:
        response = chain.invoke({
            "platform": platform,
            "prompt": prompt,
            "image_description": image_description,
            "brand_rules": brand_rules # Pass it into the chain
        })
        return response.content
    except Exception as e:
        print(f"Generation API Error: {e}")
        return "Failed to generate campaign content."