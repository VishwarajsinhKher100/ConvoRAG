# ConvoRAG – Stateful Multi-Turn Conversational AI Assistant

ConvoRAG is a ChatGPT-inspired conversational AI application that supports continuous multi-turn conversations and context-aware PDF-based Retrieval-Augmented Generation (RAG).

Built using React, FastAPI, LangGraph, Groq, PostgreSQL, and ChromaDB, it provides secure user authentication, persistent conversation history, session-isolated document retrieval, and seamless switching between previous conversations.

### Key Features
- Secure authentication using JWT and Argon2 password hashing.
- Multi-turn conversational AI powered by Groq and LangGraph.
- PDF-based Retrieval-Augmented Generation (RAG).
- Session-isolated document storage and semantic search using ChromaDB.
- Persistent chat history and conversation management using PostgreSQL.
- Structured JSON production logging and request correlation (`X-Request-ID`).
- Prometheus real-time monitoring and metrics telemetry endpoint (`/metrics`).
- Context-aware responses based on conversation history and uploaded documents.
- Interactive ChatGPT-inspired React interface.

A ChatGPT-inspired AI chatbot that supports continuous, multi-turn conversations between a user and a Large Language Model (LLM). Built with **React, FastAPI, LangGraph, Groq, and PostgreSQL**.

The chatbot maintains conversation history, user credentials, and secure session validation using a persistent PostgreSQL database, allowing users to sign up securely, log in with JSON Web Tokens (JWT), seamlessly switch between previous chat conversations via the sidebar, and perform Retrieval-Augmented Generation (RAG) by uploading and removing PDF documents.

## Tech Stack

- **Frontend:** React, Vite, CSS
- **Backend:** FastAPI, Python
- **Database & ORM:** PostgreSQL, SQLAlchemy, Chroma (Vector Store)
- **Observability & Monitoring:** Prometheus FastAPI Instrumentator, Python JSON Logger
- **LLM Orchestration:** LangGraph
- **LLM Integration:** LangChain Groq, HuggingFace Embeddings
- **LLM Provider:** Groq
- **Security:** PyJWT, Passlib (Argon2)

## Features

- Secure User Authentication with Argon2 password hashing and signed JWT access tokens (Sign In & Sign Up)
- FastAPI Dependency Injection middleware (`get_current_user`) for protected endpoints
- Production Observability: Structured JSON logging and automatic request ID tracing (`X-Request-ID`) via custom telemetry middleware
- Prometheus Metrics Integration: Real-time API monitoring via `/metrics` endpoint for tracking throughput, P95/P99 latency, and HTTP status codes
- Persistent PostgreSQL backend storage for user accounts, session metadata, and chat messages
- Vector database integration (Chroma) for document chunk storage and semantic search embeddings
- Session-isolated PDF document upload, context-aware RAG answering, and file deletion
- Collapsible sidebar with modern ChatGPT-inspired layout
- Sidebar-integrated **Recent Chats** history section to browse and switch between past conversations
- Sidebar **+ New chat** button and **Log out** functionality
- Multi-turn user and AI conversations
- Context-aware responses using previous messages and attached PDF context
- Backend-managed session creation and tracking bound to authenticated users
- Centralized API service layer with automatic authorization token injection
- Interactive message composer with file attachment preview and removal badges
- Loading indicator while the AI generates a response
- Error handling for failed API requests and database constraints
- FastAPI interactive API documentation

## Project Structure

```text
chatbot/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth_utils.py
│   ├── dependencies.py
│   ├── telemetry.py
│   ├── graph.py
│   ├── schemas.py
│   ├── rag_store.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── rag.py
│   └── .env
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Auth.jsx
    │   │   └── Auth.css
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   ├── App.css
    │   ├── index.css
    │   └── main.jsx
    ├── .env
    ├── package.json
    └── index.html
```

## Prerequisites

Install the following before running the project:

- Python 3.10 or later
- Node.js and npm
- PostgreSQL installed and running locally or via a cloud provider
- A Groq API key

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd chatbot
```

Replace `<your-repository-url>` with your repository URL.

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
uv sync
```

(Note: Ensure you install required RAG, observability, and security packages including python-jose, sentence-transformers, chromadb, pypdf, prometheus-fastapi-instrumentator, and python-json-logger).

### 3. Set Up PostgreSQL Database

1. Open your terminal or pgAdmin and create the PostgreSQL database:

```sql
CREATE DATABASE chatbot_db;
```

2. Note your database credentials (username, password, host, port, and database name).

### 4. Configure Backend Environment Variables

Create a `.env` file inside the `backend` directory:

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/chatbot_db
SECRET_KEY=your_super_secret_jwt_signing_key_here
```

Replace `your_groq_api_key`, `your_password`, and `your_super_secret_jwt_signing_key_here` with your actual secure credentials. (Note: If your database password contains special characters like `@`, make sure to URL encode them, e.g., `%40`).

**Security:** Never commit your `.env` file or expose your API keys and secret keys in the React frontend.

### 5. Start the Backend Server

From the `backend` directory, run:

```bash
uvicorn main:app --reload --port 8000
```

The application will automatically create the users and chat_messages tables in your PostgreSQL database upon startup.

The backend will run at:

- API: http://localhost:8000
- Metrics Endpoint: http://localhost:8000/metrics
- Interactive API documentation: http://localhost:8000/docs

### 6. Set Up the Frontend

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
```

#### Configure Frontend Environment Variables

Create a `.env` file inside the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start the React development server:

```bash
npm run dev
```

Open the application in your browser:

http://localhost:5173

## How It Works

The application follows a secure persistent request-response architecture backed by PostgreSQL, SQLAlchemy, Chroma vector embeddings, JWT validation middleware, structured JSON logging, Prometheus instrumentation, and a centralized frontend service layer.

```text
User / Auth State
 |
 +--> Unauthenticated --> Auth View (Sign In / Sign Up)
 |                             | (POST /signin or /signup via api.js)
 |                             v
 |                      Validate against PostgreSQL & Return Signed JWT
 |                             |
 +--> Authenticated --> Render Sidebar (with Recent Chats) + Main Panel
                            |
                            +--> Select Past Session (GET /sessions/:id)
                            |        |
                            |        v
                            |    Load Previous Conversation Messages
                            |
                            +--> Upload PDF (POST /upload-pdf)
                            |        |
                            |        v
                            |    Extract Text, Chunk & Embed into Chroma Vector Store
                            |
                            +--> Send Message (POST /chat + Bearer Token)
                                     v
                    FastAPI Backend (Verified via get_current_user dependency)
                                     |
                                     | Telemetry Middleware Inject X-Request-ID & Emit JSON Logs
                                     | Save User Message Tied to Authenticated User Email
                                     v
                             LangGraph StateGraph (graph.py)
                                     |
                                     | Retrieve Session-Specific RAG Context from Chroma
                                     | Load conversation state via thread_id
                                     | Append user message + context
                                     v
                             Groq Chat Model
                                     |
                                     | Generate response
                                     v
                             Save Assistant Reply to PostgreSQL
                                     |
                                     v
                             FastAPI JSON Response (returns reply & session_id)
                                     |
                                     v
                             React Updates Session & Refreshes Recent Chats Sidebar List
```

### Conversation Flow & Session Management

1. **Authentication:** The user registers or signs in via the `Auth` component using centralized API handlers (`api.js`). Credentials are verified against the PostgreSQL `users` table, checking Argon2 hashed passwords and returning a cryptographically signed JWT token.
2. **Sidebar & Recent Chats:** Upon login, the frontend fetches the user's historical chat sessions (`GET /sessions`) and populates the **Recent Chats** list in the sidebar.
3. **Switching Sessions:** Clicking on any session in the sidebar triggers `GET /sessions/{session_id}` to fetch and render that session's full message log.
4. **PDF Attachment & RAG:** Users can attach a PDF document using the clip icon (`POST /upload-pdf`), which extracts, chunks, and indexes the text into Chroma tagged with the active session ID. Subsequent questions query the vector store for precise context retrieval.
5. **Deleting PDFs:** Users can remove attached PDFs from active sessions (`DELETE /session-docs/{session_id}`), wiping the corresponding vector embeddings.
6. **Message Input:** The user enters a message in the main chat panel.
7. **API Request:** React uses the service layer to send the message, current `session_id`, and authorization Bearer token to the FastAPI backend (`/chat` endpoint).
8. **Token Validation & Logging**: FastAPI decodes and validates the JWT header via `get_current_user`. Custom telemetry middleware generates an `X-Request-ID` correlation tag and emits structured JSON log lines. Both user prompt and AI response are persisted in PostgreSQL.
9. **State Retrieval & LLM:** LangGraph retrieves existing conversation state via `thread_id`, appends the message, and calls the Groq model combined with retrieved document context.
10. **Response Handling:** FastAPI returns the AI reply along with the `session_id`. React updates state, displays the reply, and re-fetches session lists to update the sidebar.
11. **New Chat & Logout:**
   - Clicking **"+ New chat"** in the sidebar resets the active `session_id` and message view on the frontend.
   - Clicking **"Log out"** clears `localStorage` credentials and returns the user to the Authentication screen.

## Production Observability & Monitoring

ConvoRAG comes equipped with built-in telemetry tools designed for production cloud deployments (e.g., Kubernetes, Grafana, Prometheus, Datadog):

### 1. Structured JSON Logging
All application standard outputs (`stdout`) are formatted as single-line JSON logs containing `asctime`, `levelname`, `message`, and `request_id`. This allows log aggregation engines (Datadog, Loki, CloudWatch) to easily parse and query logs.

### 2. Request Tracing (`X-Request-ID`)
Every incoming HTTP request is assigned a unique UUID `X-Request-ID` header. This ID is passed along middleware execution and attached to error responses, making multi-step RAG retrieval and database queries easy to trace.

### 3. Prometheus Metrics Endpoint (`/metrics`)
FastAPI exposes real-time time-series data at `/metrics`. You can configure a Prometheus scraper to target this endpoint and connect **Grafana** to monitor:
- HTTP request counters by route and status code (`http_requests_total`)
- Latency percentiles and histograms (`http_request_duration_seconds`)
- System error rates (4xx/5xx responses)

## API Reference

### Health Check

**Endpoint:** `GET /`

Checks whether the backend is running.

Example response:

```json
{
  "status": "Chatbot API is running"
}
```

### Monitoring & Telemetry

#### Prometheus Metrics

**Endpoint:** `GET /metrics`

Exposes real-time Prometheus metrics for scrapers.

### Authentication

#### User Sign Up

**Endpoint:** `POST /signup`

Request body:

```json
{
  "name": "Vishwaraj",
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Example response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_name": "Vishwaraj"
}
```

#### User Sign In

**Endpoint:** `POST /signin`

Request body:

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

Example response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_name": "Vishwaraj"
}
```

### Session History

#### List User Sessions

**Endpoint:** `GET /sessions`

Headers: `Authorization: Bearer <access_token>`

Example response:

```json
[
  {
    "session_id": "a3b1c9d4-8e2f-4a1b-9c3d-5e6f7a8b9c0d",
    "title": "Hello, my name is Vishwaraj...",
    "created_at": "2026-03-30T10:15:30Z"
  }
]
```

#### Get Session Messages

**Endpoint:** `GET /sessions/{session_id}`

Headers: `Authorization: Bearer <access_token>`

Example response:

```json
{
  "session_id": "a3b1c9d4-8e2f-4a1b-9c3d-5e6f7a8b9c0d",
  "messages": [
    {
      "role": "user",
      "content": "Hello, my name is Vishwaraj.",
      "created_at": "2026-03-30T10:15:30Z"
    },
    {
      "role": "assistant",
      "content": "Hello Vishwaraj! Nice to meet you.",
      "created_at": "2026-03-30T10:15:32Z"
    }
  ]
}
```

### Knowledge Base & RAG

#### Upload and Index PDF

**Endpoint:** `POST /upload-pdf`

Content type: `multipart/form-data`

Headers: `Authorization: Bearer <access_token>`

Form Data:

- file: PDF file binary
- session_id: string (optional)

Example response:

```json
{
  "status": "success",
  "session_id": "a3b1c9d4-8e2f-4a1b-9c3d-5e6f7a8b9c0d",
  "filename": "document.pdf",
  "message": "PDF uploaded and indexed successfully."
}
```

#### Delete Session PDF Embeddings

**Endpoint:** `DELETE /session-docs/{session_id}`

Headers: `Authorization: Bearer <access_token>`

Example response:

```json
{
  "status": "success",
  "message": "PDF data cleared for session."
}
```

### Send a Chat Message

**Endpoint:** `POST /chat`

Content type: `application/json`  
Headers: `Authorization: Bearer <access_token>`

#### Initial Request (New Chat)

```json
{
  "session_id": null,
  "message": "Hello, my name is Vishwaraj."
}
```

Example response:

```json
{
  "session_id": "a3b1c9d4-8e2f-4a1b-9c3d-5e6f7a8b9c0d",
  "reply": "Hello Vishwaraj! Nice to meet you."
}
```

#### Follow-up Request (Continuing Conversation)

```json
{
  "session_id": "a3b1c9d4-8e2f-4a1b-9c3d-5e6f7a8b9c0d",
  "message": "What is my name?"
}
```

Example response:

```json
{
  "session_id": "a3b1c9d4-8e2f-4a1b-9c3d-5e6f7a8b9c0d",
  "reply": "Your name is Vishwaraj!"
}
```

## Troubleshooting

### PostgreSQL Connection Errors

- Verify that your PostgreSQL service is running.
- Check that your DATABASE_URL string in `.env` is formatted correctly: `postgresql://username:password@localhost:5432/chatbot_db`.
- Ensure special characters in database passwords are URL-encoded.

### Groq API Key & JWT Secret Errors

- Verify that the `.env` file exists in the backend directory with valid `GROQ_API_KEY` and `SECRET_KEY` values.
- Restart the backend after changing environment variables.

### Frontend Cannot Connect to Backend

- Confirm that FastAPI is running on port `8000`.
- Confirm that React is running on port `5173`.
- Verify that `VITE_API_BASE_URL` is set correctly in `frontend/.env`.
- Check the CORS configuration in `main.py`.

### Authentication & Token Errors

- Verify that `/signup` and `/signin` routes are correctly registered and included via `app.include_router(auth.router)`.
- Ensure frontend requests transmit the correct JWT Bearer token headers via `api.js`.

## Future Improvements

- Ability to rename and delete historical chat sessions directly from the sidebar
- Database persistence for LangGraph checkpointers (PostgresSaver) for multi-instance scaling
- Streaming LLM responses (Server-Sent Events / WebSockets)
- Deployment using Docker