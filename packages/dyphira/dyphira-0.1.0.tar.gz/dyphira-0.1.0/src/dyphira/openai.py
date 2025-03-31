import requests

class OpenAI:
  def __init__(self, api_key):
    self.api_key = api_key
    self.base_url = "https://novus-server-v3.fly.dev/api/v1/proxy/openai"
    # self.base_url = "http://localhost:8000/api/v1/proxy/openai"
    self.headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {self.api_key}"
    }

  def _request(self, method, endpoint, json=None, data=None, files=None, params=None):
    """Helper method to make requests to the API"""
    url = f"{self.base_url}/{endpoint}"
    headers = self.headers.copy()
    
    if files:
      # Don't set Content-Type for multipart/form-data
      headers.pop("Content-Type", None)
    
    response = requests.request(
      method=method,
      url=url,
      headers=headers,
      json=json,
      data=data,
      files=files,
      params=params
    )
    
    try:
        return response.json()
    except:
        # Handle case where response is not valid JSON
        return {"error": f"Failed to decode JSON response. Status code: {response.status_code}", "text": response.text}

  # Chat and Completions
  def responses(self, model, prompt, temperature=1.0, max_tokens=100, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    """Generate responses from the OpenAI API via Dyphira."""
    return self._request(
      "POST",
      "responses",
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
    
  def chat_completions(self, model, messages, temperature=1.0, max_tokens=100, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, tools=None, tool_choice=None):
    """Create a chat completion using the OpenAI API via Dyphira."""
    payload = {
      "model": model,
      "messages": messages,
      "temperature": temperature,
      "max_tokens": max_tokens,
      "top_p": top_p,
      "frequency_penalty": frequency_penalty,
      "presence_penalty": presence_penalty
    }
    
    if tools:
      payload["tools"] = tools
    if tool_choice:
      payload["tool_choice"] = tool_choice
      
    return self._request("POST", "chat/completions", json=payload)

  def completions(self, model, prompt, temperature=1.0, max_tokens=100, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    """Create a completion using the OpenAI API via Dyphira."""
    return self._request(
      "POST",
      "completions",
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

  # Images
  def images_generations(self, prompt, model="dall-e-3", n=1, size="1024x1024", quality="standard"):
    """Generate images using DALL-E models."""
    return self._request(
      "POST",
      "images/generations",
      json={
        "prompt": prompt,
        "model": model,
        "n": n,
        "size": size,
        "quality": quality
      }
    )
  
  def images_edits(self, image, mask=None, prompt="", n=1, size="1024x1024"):
    """Edit images using DALL-E 2."""
    files = {"image": open(image, "rb")}
    if mask:
      files["mask"] = open(mask, "rb")
    
    data = {
      "prompt": prompt,
      "n": n,
      "size": size
    }
    
    return self._request("POST", "images/edits", files=files, data=data)
  
  def images_variations(self, image, n=1, size="1024x1024"):
    """Create variations of an image using DALL-E 2."""
    files = {"image": open(image, "rb")}
    data = {
      "n": n,
      "size": size
    }
    
    return self._request("POST", "images/variations", files=files, data=data)

  # Embeddings
  def embeddings(self, model, input):
    """Create embeddings for text."""
    return self._request(
      "POST",
      "embeddings",
      json={
        "model": model,
        "input": input
      }
    )

  # Audio
  def audio_transcriptions(self, file, model="whisper-1", language=None, prompt=None):
    """Transcribe audio to text."""
    files = {"file": open(file, "rb")}
    data = {"model": model}
    
    if language:
      data["language"] = language
    if prompt:
      data["prompt"] = prompt
      
    return self._request("POST", "audio/transcriptions", files=files, data=data)
  
  def audio_translations(self, file, model="whisper-1", prompt=None):
    """Translate audio to English text."""
    files = {"file": open(file, "rb")}
    data = {"model": model}
    
    if prompt:
      data["prompt"] = prompt
      
    return self._request("POST", "audio/translations", files=files, data=data)
  
  def audio_speech(self, model, input, voice, response_format="mp3", speed=1.0):
    """Generate speech from text."""
    return self._request(
      "POST",
      "audio/speech",
      json={
        "model": model,
        "input": input,
        "voice": voice,
        "response_format": response_format,
        "speed": speed
      }
    )

  # Files
  def files_list(self):
    """List files that have been uploaded."""
    return self._request("GET", "files")
  
  def files_upload(self, file, purpose):
    """Upload a file for use with other endpoints."""
    files = {"file": open(file, "rb")}
    data = {"purpose": purpose}
    
    return self._request("POST", "files", files=files, data=data)
  
  def files_delete(self, file_id):
    """Delete a file."""
    return self._request("DELETE", f"files/{file_id}")
  
  def files_retrieve(self, file_id):
    """Retrieve information about a file."""
    return self._request("GET", f"files/{file_id}")
  
  def files_content(self, file_id):
    """Retrieve the contents of a file."""
    return self._request("GET", f"files/{file_id}/content")

  # Fine-tuning
  def fine_tuning_jobs_create(self, training_file, model, validation_file=None, hyperparameters=None):
    """Create a fine-tuning job."""
    payload = {
      "training_file": training_file,
      "model": model
    }
    
    if validation_file:
      payload["validation_file"] = validation_file
    if hyperparameters:
      payload["hyperparameters"] = hyperparameters
      
    return self._request("POST", "fine_tuning/jobs", json=payload)
  
  def fine_tuning_jobs_list(self, limit=20):
    """List fine-tuning jobs."""
    return self._request("GET", "fine_tuning/jobs", params={"limit": limit})
  
  def fine_tuning_jobs_retrieve(self, fine_tuning_id):
    """Retrieve a fine-tuning job."""
    return self._request("GET", f"fine_tuning/jobs/{fine_tuning_id}")
  
  def fine_tuning_jobs_cancel(self, fine_tuning_id):
    """Cancel a fine-tuning job."""
    return self._request("POST", f"fine_tuning/jobs/{fine_tuning_id}/cancel")
  
  def fine_tuning_jobs_events(self, fine_tuning_id, limit=20):
    """List events for a fine-tuning job."""
    return self._request("GET", f"fine_tuning/jobs/{fine_tuning_id}/events", params={"limit": limit})

  # Moderations
  def moderations(self, input, model="text-moderation-latest"):
    """Check if content complies with OpenAI's usage policies."""
    return self._request(
      "POST",
      "moderations",
      json={
        "input": input,
        "model": model
      }
    )

  # Assistants API
  def assistants_create(self, model, name=None, description=None, instructions=None, tools=None):
    """Create an assistant."""
    payload = {"model": model}
    
    if name:
      payload["name"] = name
    if description:
      payload["description"] = description
    if instructions:
      payload["instructions"] = instructions
    if tools:
      payload["tools"] = tools
      
    return self._request("POST", "assistants", json=payload)
  
  def assistants_retrieve(self, assistant_id):
    """Retrieve an assistant."""
    return self._request("GET", f"assistants/{assistant_id}")
  
  def assistants_modify(self, assistant_id, model=None, name=None, description=None, instructions=None, tools=None):
    """Modify an assistant."""
    payload = {}
    
    if model:
      payload["model"] = model
    if name:
      payload["name"] = name
    if description:
      payload["description"] = description
    if instructions:
      payload["instructions"] = instructions
    if tools:
      payload["tools"] = tools
      
    return self._request("POST", f"assistants/{assistant_id}", json=payload)
  
  def assistants_delete(self, assistant_id):
    """Delete an assistant."""
    return self._request("DELETE", f"assistants/{assistant_id}")
  
  def assistants_list(self, limit=20):
    """List assistants."""
    return self._request("GET", "assistants", params={"limit": limit})
