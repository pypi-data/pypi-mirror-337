import requests

class OpenAI:
  def __init__(self, api_key):
    self.api_key = api_key

  def responses(self, model, prompt, temperature = 1.0, max_tokens = 100, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0):
    """
    This function is used to generate responses from the OpenAI API via Dyphira.
    """
    response = requests.post(
      "https://novus-server-v3.fly.dev/api/v1/proxy/openai/responses",
      headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.api_key}"
      },
      json={  
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
      }
    )
    return response.json()