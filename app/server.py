from fastapi import FastAPI
from app.resources.nfl_injuries_resource import get_all_injuries

app = FastAPI()

@app.get("/nfl/injuries", tags=["resources"])
def nfl_injuries():
    """Fetch all NFL injuries (cached, refreshed every 24h)."""
    return get_all_injuries()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
