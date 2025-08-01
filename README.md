# Chatbot 
## Backend
This is a Python backend for a chatbot using FastAPI.

### Structure
- `main.py`: Entry point for the FastAPI app
- `requirements.txt`: Python dependencies
- `app/`
  - `routes/`: API route definitions
  - `services/`: Business logic for chatbot
  - `models/`: Data models (Pydantic)

### Running the Project
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Active virtual environment:
   ```sh
   source venv/bin/activate 
   ```
3. Start the server:
   ```sh
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

4. Run Docker Compose to start the services in a containerized environment:
   ```sh
   docker-compose up
   ```

## frontend

This chatbot UI is made by create-react-app

### Structure
   - `src/`: React app source code

### Running the Project
1. Install dependencies:
```sh
   npm install
```
2. Start the server:
   ```sh
   npm start
   ```

The frontend will be available at `http://localhost:3000`.