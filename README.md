### Chatbot - RAG+MCP

requirements.txt with all the required packages.

Step 1: Clone the github repository
```git clone https://github.com/Chaithra-J/OSO.Earth.git```

Step 2: Navigate to the Project Directory 
```cd OSO.Earth```

Step 3: Create a Virtual Environment
```python3 -m venv venv```

Step 4: Activate the environment
For Windows (command prompt):
```venv\Scripts\activate.bat```

For MacOS:
```source venv/bin/activate```

Step 5: Install Dependencies 
```pip install -r requirements.txt```

Step 6: Run Application
On VS Code terminal:
```python -m uvicorn app.main:app --reload```

### High-level Architecture
```
Frontend (App / Web / Chat UI)
        |
        v
AI Orchestrator (Agent Logic)
        |
        ├── RAG (Knowledge Brain)
        |     └── Habit science, tips, frameworks
        |
        ├── MCP Tools (Action Layer)
        |     ├── User memory
        |     ├── Habit tracker
        |     ├── Gamification engine
        |     └── Notifications
        |
        └── LLM (Reasoning + Conversation)
```
