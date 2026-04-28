from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="task-api", version="0.1.0")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
