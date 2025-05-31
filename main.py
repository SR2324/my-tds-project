# main.py
from fastapi import FastAPI
# ... other imports

app = FastAPI( # <--- ENSURE THIS IS NAMED 'app'
    title="TDS Virtual TA API",
    # ...
)
# ... your endpoints like @app.post("/api/")
