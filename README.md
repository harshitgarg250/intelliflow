# 🚀 IntelliFlow - AI Agent Management Platform

A full-stack web application for orchestrating multi-agent workflows with real-time monitoring and task management.

## Features

✨ **Agent Management**
- Create and manage AI agents with custom roles and skills
- Configure LLM models and tools for each agent
- Real-time agent status tracking

📋 **Task Management**
- Assign tasks to agents
- Priority-based task execution
- Task status and history tracking

🔄 **Workflow Orchestration**
- Design multi-agent workflows
- Sequential task execution
- Cross-agent data passing

📊 **Real-time Dashboard**
- Live execution monitoring
- Performance metrics and analytics
- Detailed execution logs

🔐 **Authentication**
- Secure JWT-based authentication
- User account management
- Password security with bcrypt

## Tech Stack

**Backend**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- JWT (Authentication)

**Frontend**
- React 18 (UI Framework)
- TypeScript (Type safety)
- Tailwind CSS (Styling)
- Zustand (State management)

**Deployment**
- Docker & Docker Compose
- PostgreSQL 15
- Redis (Caching)

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/intelliflow.git
   cd intelliflow
```

2. **Start Docker services**
```bash
   docker-compose up -d
```

3. **Install backend dependencies**
```bash
   cd backend
   pip install -r requirements.txt
```

4. **Run the backend**
```bash
   python app/main.py
```

   Backend will be available at: http://localhost:8000
   API Docs: http://localhost:8000/api/docs

5. **Setup frontend**
```bash
   cd ../frontend
   npm install
   npm run dev
```

   Frontend will be available at: http://localhost:5173

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Agents (Coming soon)
- `GET /api/agents/` - List all agents
- `POST /api/agents/` - Create agent
- `GET /api/agents/{id}` - Get agent details
- `PUT /api/agents/{id}` - Update agent
- `DELETE /api/agents/{id}` - Delete agent

### Tasks (Coming soon)
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task
- `PUT /api/tasks/{id}` - Update task

### Workflows (Coming soon)
- `GET /api/workflows/` - List workflows
- `POST /api/workflows/` - Create workflow
- `POST /api/workflows/{id}/execute` - Execute workflow

## Project Structure
intelliflow/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ └── routes/
│ │ │ └── auth.py
│ │ ├── models/
│ │ │ ├── user.py
│ │ │ ├── agent.py
│ │ │ └── task.py
│ │ ├── schemas/
│ │ │ ├── user.py
│ │ │ └── agent.py
│ │ ├── core/
│ │ │ └── security.py
│ │ ├── main.py
│ │ └── database.py
│ ├── requirements.txt
│ └── .env
├── frontend/
│ ├── src/
│ ├── package.json
│ └── vite.config.ts
├── docker-compose.yml
└── README.md
## Development

### Testing the API

1. **Health check**
```bash
   curl http://localhost:8000/api/health
```

2. **Register user**
```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "TestPass123!"
     }'
```

3. **Login**
```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "TestPass123!"
     }'
```

## Database

PostgreSQL is used for data persistence. Database schema includes:
- Users (authentication)
- Agents (AI agent definitions)
- Tasks (work assignments)
- Workflows (orchestration)
- Executions (run history)
- Logs (detailed tracking)

## Contributing

1. Create a feature branch
2. Make your changes
3. Write clear commit messages
4. Push to your fork
5. Create a Pull Request

## License

MIT License

## Author

Harshit Garg (harshitgarg250)

## Project Timeline

- **Day 1**: Backend setup ✅
- **Day 2**: Agent & Task APIs
- **Day 3**: Workflow execution
- **Day 4**: React Frontend
- **Day 5**: Polish & Deployment

## Support

For issues and questions, open an issue on GitHub.

---

Built with ❤️ as a portfolio project demonstrating full-stack development skills.
