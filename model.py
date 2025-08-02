from openai import OpenAI

# Replace this with your actual Groq API key
GROQ_API_KEY = "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"

# Create and return OpenAI-compatible Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def get_groq_reply(messages, model="llama3-8b-8192"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=0.7,  # Controls randomness (lower = more deterministic)
            max_tokens=500    # Limit response length
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"❌ Error: {str(e)}"