from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
import uvicorn
from monte_carlo import run_monte_carlo

app = FastAPI(title="Blood Bank Simulation API")
BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML = BASE_DIR / "index.html"

# Essential for allowing our frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def serve_frontend():
    """
    Serve the dashboard page directly from the API host.
    """
    return FileResponse(INDEX_HTML)


@app.get("/favicon.ico")
async def favicon():
    """
    Avoid noisy 404 logs when the browser requests a favicon.
    """
    return Response(status_code=204)

class SimulationParams(BaseModel):
    replications: int = 100
    days: int = 365
    max_shelf_life: int = 35
    avg_donations: int = 10
    avg_sched_demand: int = 7
    avg_emer_demand: int = 3
    reorder_point: Optional[int] = None
    order_quantity: Optional[int] = None

@app.post("/simulate")
async def run_simulation(params: SimulationParams):
    """
    Endpoint that takes parameters from the UI and runs the Monte Carlo simulation.
    Returns the average metrics to be graphed on the dashboard.
    """
    results = run_monte_carlo(
        params.replications,
        params.days,
        params.max_shelf_life,
        params.avg_donations,
        params.avg_sched_demand,
        params.avg_emer_demand,
        params.reorder_point,
        params.order_quantity
    )
    return results

if __name__ == "__main__":
    print("Starting Blood Bank Simulation API Backend on port 8080...")
    uvicorn.run("api:app", host="127.0.0.1", port=8080, reload=True)
