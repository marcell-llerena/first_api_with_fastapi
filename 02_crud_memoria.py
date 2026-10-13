from typing import Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

db = {}
siguiente_id = 1

app = FastAPI(
    title="CRUD de viviendas (en memoria RAM)",
    description="Crud básico con FASTAPI y PYDANTIC",
    version="0.2"
)


class ViviendaBase(BaseModel):
    distrito: str = Field(
        ...,
        min_length=2,
        max_length=50,
        examples=["Miraflores"]
    )
    area_m2: float = Field(
        ...,
        gt=0,
        description="Area construida en m2",
        examples=[85.5]
    )
    habitaciones: int = Field(
        ...,
        ge=1,
        le=20,
        description="Número de habitaciones",
        examples=[3]
    )
    banios: int = Field(
        ...,
        ge=1,
        le=20,
        description="Número de banios",
        examples=[1]
    )
    precio: float = Field(
        ...,
        gt=0,
        description="Precio en USD",
        examples=[150000]
    )


class ViviendaCreate(ViviendaBase):
    """Lo que el cliente envia para CREAR"""


class ViviendaUpdate(BaseModel):
    distrito: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50
    )
    area_m2: Optional[float] = Field(None, gt=0)
    habitaciones: Optional[int] = Field(None, ge=1, le=20)
    banios: Optional[int] = Field(None, ge=1, le=20)
    precio: Optional[float] = Field(None, gt=0)

class ViviendaRead(ViviendaBase):
    id: int


@app.get("/", tags=["General"])
def raiz():
    return {"mensaje": "API de viviendas. Ve a /docs para probarla"}

# ------CREATE (POST)----------
@app.post(
    "/viviendas",
    response_model=ViviendaRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Viviendas"]
)
def crear_viviendas(datos: ViviendaCreate):
    global siguiente_id
    vivienda = ViviendaRead(id=siguiente_id, **datos.model_dump())
    db[siguiente_id] = vivienda
    siguiente_id += 1
    return vivienda

# ------READ (GET)------------
@app.get(
    "/viviendas",
    response_model=list[ViviendaRead],
    tags=["Viviendas"]
)
def listar_viviendas(
    distrito: Optional[str] = None
):
    resultado = list(db.values())
    if distrito:
        resultado = [
            v
            for v in resultado
            if v.distrito.lower() == distrito.lower()
        ]

    return resultado

@app.get(
    "/viviendas/{vivienda_id}",
    response_model=ViviendaRead,
    tags=["viviendas"]
)
def obtener_vivienda(vivienda_id: int):
    vivienda = db.get(vivienda_id)
    if vivienda is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vivienda {vivienda_id} no encontrada"
        )
    return vivienda

# ------UPDATE total (PUT)------------
@app.put(
    "/viviendas/{vivienda_id}",
    response_model=ViviendaRead,
    tags=["Viviendas"]
)
def reemplazar_vivienda(
    vivienda_id: int,
    datos: ViviendaCreate
):
    vivienda = ViviendaRead(id=vivienda_id, **datos.model_dump())
    db[vivienda_id] = vivienda
    return vivienda

# ------UPDATE parcial (PUT)------------
# Solo los campos que queramos cambiar
@app.patch(
    "/viviendas/{vivienda_id}",
    response_model=ViviendaRead,
    tags=["viviendas"]
)
def actualizar_vivienda(vivienda_id: int, datos: ViviendaUpdate):
    vivienda = db.get(vivienda_id)
    if vivienda is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vivienda {vivienda_id} no encontrada"
        )
    cambios = datos.model_dump(exclude_unset=True)
    actualizada = vivienda.model_copy(update=cambios)
    db[vivienda_id] = actualizada
    return actualizada


# ------DELETE (DELETE)------------
@app.delete(
    "/viviendas/{vivienda_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Viviendas"]
)
def eliminar_vivienda(vivienda_id: int):
    vivienda = db.get(vivienda_id)
    if vivienda is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vivienda {vivienda_id} no encontrada"
        )

    del db[vivienda_id]



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
