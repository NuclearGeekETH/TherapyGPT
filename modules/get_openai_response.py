import openai
import os
from datetime import date

key = os.getenv("OPENAI_API_KEY")

openai.api_key = key

def chat_response(message, history, model, system):

    history.insert(0, {"role": "system", "content": f"{system} Current Date: {date.today()}"})
    history.append({"role": "user", "content": message})
    
    print(f"system: {system}")
    print(f"message: {message}")
    print(f"history: {history}")

    try:
        # Request completion with streaming enabled
        completion = openai.chat.completions.create(
            model=model,
            messages=history,
            stream=True
        )

        # Stream Response
        partial_message = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Ensure content is not None
                partial_message += chunk.choices[0].delta.content
                yield partial_message

    except Exception as e:
        # Handle API error: retry, log, or notify
        yield f"OpenAI API returned an API Error: {e}"

