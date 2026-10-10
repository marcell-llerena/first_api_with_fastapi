from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="CRUD de viviendas (en memoria RAM)",
    description="Crud básico con FASTAPI y PYDANTIC",
    version="0.2"
)

@app.get("/", tags=["General"])
def raiz():
    return {"mensaje": "API de viviendas. Ve a /docs para probarla"}

# uv run 02_crud_memoria.py
# https://www.postman.com/downloads/
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "02_crud_memoria:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
