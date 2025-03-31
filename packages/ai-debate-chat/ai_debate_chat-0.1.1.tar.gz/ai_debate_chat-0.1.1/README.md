# AI Debate Chat

A powerful Python package for creating AI-powered debate and chat applications with advanced knowledge retrieval capabilities.

## Installation

```bash
pip install ai-debate-chat
```

## Features

- **Flexible AI Models**: Support for multiple AI models including OpenAI, Claude, DeepSeek, local models, and G4F (GPT for Free)
- **Smart Information Retrieval**: Automatic research on debate topics using Wikipedia, Google, and DuckDuckGo
- **Vector Store Database**: Efficient storage and retrieval of debate knowledge using FAISS and embeddings
- **Conversational Memory**: Manages conversation history for contextual responses
- **Multi-Perspective Analysis**: Presents various viewpoints on complex topics
- **Interactive Mode**: Built-in interactive terminal interface for immediate use

## Quick Start

```python
from ai_debate_chat.debate_chat import AIDebateBot

# Initialize with OpenAI (requires API key)
bot = AIDebateBot(
    topic="Climate Change",
    model_choice="openai",
    api_key="your-api-key"
)

# Generate a response to a question
response = bot.generate_response("What are the main arguments for carbon taxes?")
print(response)

# Or use the interactive mode
bot.run_interactive()
```

## Advanced Usage

### Model Options

```python
# Use Claude AI
bot = AIDebateBot(topic="Artificial Intelligence Ethics", model_choice="claude", api_key="your-anthropic-key")

# Use a local model
bot = AIDebateBot(topic="Space Exploration", model_choice="local", local_model_path="path/to/your/model")

# Use G4F (GPT for Free)
bot = AIDebateBot(topic="Quantum Computing", model_choice="g4f")
```

### Custom Memory Management

```python
from langchain.memory import ConversationBufferMemory

# Create custom memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize bot with custom memory
bot = AIDebateBot(
    topic="Cryptocurrency",
    model_choice="openai",
    api_key="your-api-key",
    memory=memory,
    max_memory_items=15  # Control memory size
)

# Clear memory when needed
bot.clear_memory()
```

## ML Pipeline Details

The package includes a sophisticated machine learning pipeline that:

1. Collects information from multiple sources:
   - Wikipedia articles
   - Google search results
   - DuckDuckGo search results
2. Processes content:
   - Text cleaning and preprocessing
   - Removal of non-essential elements
   - Natural language processing with NLTK
3. Creates knowledge embeddings:
   - Document chunking for better retrieval
   - FAISS vector storage for efficient similarity search
   - HuggingFace embeddings for semantic understanding

## Requirements

- Python 3.10 or higher
- Key dependencies:
  - langchain-community
  - langchain-huggingface
  - langchain-text-splitters
  - faiss-cpu
  - transformers
  - g4f (optional)
  - sentence-transformers
  - torch
  - nltk
  - beautifulsoup4

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
