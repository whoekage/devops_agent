# DevOps Automation Project

An automation project for DevOps processes using LLM-based agents. Currently focused on local LLM deployment using Ollama.

## Features

- 🤖 LLM Integration for intelligent automation (using Ollama)
- 📨 Notifications support via Telegram and Slack
- 🔄 Asynchronous task processing
- 📝 Logging and monitoring

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) for local LLM

## Installation

1. Install Ollama:
```bash
# For macOS or Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

2. Clone the repository:
```bash
git clone git@github.com:whoekage/devops_agent.git
cd devops_agent
```

3. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
# or
.\venv\Scripts\activate  # For Windows
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Copy the example configuration file and set it up:
```bash
cp config.yaml.example config.yaml
```

6. Edit `config.yaml` and specify the required parameters:
- Ollama model configuration
- Telegram and Slack tokens
- Other parameters as needed

## Running

1. Start Ollama and pull the required model:
```bash
# Start Ollama service
ollama serve

# In another terminal, pull the model (e.g., mistral)
ollama pull mistral
```

2. Activate virtual environment (if not already activated):
```bash
source venv/bin/activate  # For Linux/MacOS
# or
.\venv\Scripts\activate  # For Windows
```

3. Run the main application:
```bash
python main.py
```

## Project Structure

```
.
├── agents/             # Agents for various tasks
│   └── k8s_agent.py   # Kubernetes management agent
├── core/              # Application core
│   ├── llm.py         # LLM integration
│   ├── database.py    # Database operations
│   └── notifications.py # Notification system
├── workers/           # Worker processes
│   ├── llm_worker.py  # LLM task processor
│   └── notification_worker.py # Notification processor
├── utils/             # Utility functions
│   └── logger.py      # Logging
├── config.yaml        # Application configuration
├── main.py           # Application entry point
└── requirements.txt   # Project dependencies
```

## Configuration

Main settings are stored in `config.yaml`. Configuration example:

```yaml
llm:
  type: "ollama"
  model: "mistral"
  host: "http://localhost:11434"
  temperature: 0.7
  max_tokens: 2000

notifications:
  telegram:
    token: your_telegram_token
    chat_id: your_chat_id
  slack:
    token: your_slack_token
    channel: #notifications

database:
  path: history.db
```

## Development

To contribute to development:

1. Create a fork of the repository
2. Create a branch for new functionality
3. Make changes and create a pull request

## TODO

- [ ] Implement core notification functionality:
  - [ ] Add Telegram bot commands and interactions
  - [ ] Implement Slack app integration and slash commands
  - [ ] Add message templates and formatting
  - [ ] Implement notification priorities and rules
- [ ] Add support for multiple LLM providers (OpenAI, Anthropic)
- [ ] Implement model switching functionality
- [ ] Add Kubernetes integration
- [ ] Create comprehensive test suite
- [ ] Add metrics collection and monitoring
- [ ] Implement rate limiting and queue management
- [ ] Add support for more notification channels (Discord, Email)
- [ ] Create web interface for management
- [ ] Add documentation for API endpoints
- [ ] Implement backup and restore functionality
- [ ] Add support for custom agent development
- [ ] Create examples and use cases
- [ ] Add CI/CD pipeline configuration

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) file for details. 