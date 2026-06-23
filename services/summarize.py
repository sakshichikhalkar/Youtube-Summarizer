import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))




def get_summary(transcript_text: str, summary_type: str = "medium") -> dict:
    """
    Takes transcript text and returns AI generated summary.
    """
    
    prompts = {
        "short": "Summarize this in exactly 3 bullet points. Be very concise.",
        "medium": "Summarize this in 5 clear bullet points.",
        "detailed": "Summarize this in a detailed paragraph covering all key points."
     }
    
       
    instruction = prompts.get(summary_type, prompts["medium"])
    
    full_prompt = f"{instruction}\n\nTranscript: {transcript_text}"
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )
    
    summary_text = response.choices[0].message.content
    
    return {
        "success": True,
        "summary": summary_text,
        "summary_type": summary_type
    }
