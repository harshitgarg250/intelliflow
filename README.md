# 🚀 IntelliFlow - AI Agent Management Platform

A full-stack web application for orchestrating multi-agent workflows with real-time monitoring and task management.

## Features

✨ **Agent Management** - Create and manage AI agents with custom roles and skills
📋 **Task Management** - Assign tasks to agents with priority and status tracking
🔄 **Workflow Orchestration** - Design multi-agent workflows with sequential execution
📊 **Real-time Dashboard** - Live execution monitoring with performance metrics
🔐 **Authentication** - Secure JWT-based authentication with user management

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, PostgreSQL, JWT, Python 3.11+
**Frontend:** React 18, TypeScript, Tailwind CSS (Coming soon)
**Deployment:** Docker & Docker Compose

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/intelliflow.git
cd intelliflow

# Start Docker services
docker-compose up -d

# Install dependencies
cd backend
pip install -r requirements.txt

# Run backend
python app/main.py
```

Backend: http://localhost:8000
API Docs: http://localhost:8000/api/docs

## API Endpoints

### Auth
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Agents
- `GET /api/agents/` - List all agents
- `POST /api/agents/` - Create agent
- `GET /api/agents/{id}` - Get agent details
- `PUT /api/agents/{id}` - Update agent
- `DELETE /api/agents/{id}` - Delete agent

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Testing

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "harshit",
    "email": "harshit@example.com",
    "password": "HarshitPass123!"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "harshit@example.com",
    "password": "HarshitPass123!"
  }'

# Create Agent (replace TOKEN with access_token from login)
curl -X POST http://localhost:8000/api/agents/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "name": "Data Analyst",
    "role": "Senior Data Analyst",
    "goal": "Analyze data and provide insights",
    "backstory": "10 years of data science experience",
    "tools": ["python", "sql", "pandas"]
  }'

# List Agents
curl http://localhost:8000/api/agents/ \
  -H "Authorization: Bearer TOKEN"
```

## Project Status

✅ Day 1: Backend setup + Authentication
✅ Day 2: Agent & Task APIs
⏳ Day 3: Workflow Engine
⏳ Day 4: React Frontend
⏳ Day 5: Polish & Deployment

## License

MIT

## Author

Harshit Garg (harshitgarg250)

---

Built as a portfolio project demonstrating full-stack development skills.