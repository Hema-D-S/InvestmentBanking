# Investment Banking Backend (FastAPI + MongoDB)

## Setup

1. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Set up MongoDB:**

   - Make sure MongoDB is running locally or update `MONGODB_URI` in `.env`.

3. **Set environment variables:**

   - Edit `.env` with your `MONGODB_URI` and `SECRET_KEY`.

4. **Run the server:**

   ```sh
   uvicorn app.main:app --reload
   ```

5. **API Docs:**
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

- `POST /register` — Register a new user
- `POST /login` — Login and get JWT token
- `GET /me` — Get current user info (requires JWT)
