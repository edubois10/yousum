import requests
from config.settings import LLM_ENDPOINT

def generate_summary_with_custom_llm(transcript_text):
    """
    Calls your local LLM container at /v1/chat/completions
    which expects a 'messages' array with 'role' and 'content'.
    """
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes YouTube transcripts."
            },
            {
                "role": "user",
                "content": f"Summarize the following text:\n\n{transcript_text}"
            }
        ]
    }

    try:
        response = requests.post(LLM_ENDPOINT, json=payload, timeout=300)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"LLM request error: {str(e)}"

    data = response.json()
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    else:
        return "No summary returned from LLM."
