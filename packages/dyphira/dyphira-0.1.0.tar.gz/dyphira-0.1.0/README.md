# Dyphira Python

A Python package for interacting with OpenAI APIs via Dyphira proxy server.

## Installation

You can install the package via pip:

```bash
pip install dyphira
```

## Usage

### Basic Example

```python
from dyphira import OpenAI

# Initialize with your API key
client = OpenAI("your-api-key")

# Generate an image
response = client.images_generations("A cat with a hat.")
print(response)
```

### Available Features

The package provides access to the following OpenAI API endpoints:

- **Chat & Completions**: Generate text responses
- **Images**: Generate, edit, and create variations of images
- **Embeddings**: Create text embeddings
- **Audio**: Transcribe, translate, and generate speech
- **Files**: Upload, list, and manage files
- **Fine-tuning**: Create and manage fine-tuning jobs
- **Moderations**: Check content compliance
- **Assistants**: Create and manage AI assistants

## Documentation

### Chat Completions

```python
response = client.chat_completions(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

### Image Generation

```python
response = client.images_generations(
    prompt="A sunset over mountains",
    model="dall-e-3",
    size="1024x1024"
)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Links

- [GitHub Repository](https://github.com/DivinerX/dyphira-python)
- [Issue Tracker](https://github.com/DivinerX/dyphira-python/issues)
