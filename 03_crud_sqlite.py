from typing import Optional, Annotated

from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI, HTTPException, Query, status, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select


# Documentación
# https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/#the-with-block

# 1. Inicializar conexión a la base de datos
DATABASE_URL = "sqlite:///./viviendas.db"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


# 2. Crear los esquemas
class ViviendaBase(SQLModel):
    distrito: str = Field(min_length=2, max_length=50)
    area_m2: float = Field(gt=0)
    habitaciones: int = Field(ge=1, le=10)
    banios: int = Field(ge=1, le=10)
    precio: float = Field(gt=0)

class ViviendaCreate(ViviendaBase):
    """Crear Vivienda"""

class ViviendaUpdate(SQLModel):
    distrito: Optional[str] = Field(min_length=2, max_length=50)
    area_m2: Optional[float] = Field(gt=0)
    habitaciones: Optional[int] = Field(ge=1, le=10)
    banios: Optional[int] = Field(ge=1, le=10)
    precio: Optional[float] = Field(gt=0)

class ViviendaRead(ViviendaBase):
    id: int

# 3. Crear las tablas
class Vivienda(ViviendaBase, table=True):
    id: int = Field(default=None, primary_key=True)

# 4. Inicializa las tablas o crea si estas no existan al iniciar el programa
@asynccontextmanager
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# 5. Crear todos los endpoints
app = FastAPI(
    title="CRUD de viviendas (SQLite)",
    description="Crud básico con FASTAPI, SQLModel, SQLite",
    version="0.3",
    lifespan=lifespan
)

@app.get("/", tags=["General"])
def raiz():
    return {"mensaje": "API de viviendas. Ve a /docs para probarla"}


@app.post(
    "/viviendas",
    response_model=ViviendaRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Viviendas"]
)
def crear_viviendas(datos: ViviendaCreate, session: SessionDep):
    vivienda = Vivienda.model_validate(datos)
    session.add(vivienda)
    session.commit()
    session.refresh(vivienda)
    return vivienda

@app.get(
    "/viviendas",
    response_model=list[ViviendaRead],
    tags=["Viviendas"]
)
def listar_viviendas(
    session: SessionDep,
    distrito: Optional[str] = None
):
    consulta = select(Vivienda)
    if distrito:
        consulta = consulta.where(Vivienda.distrito == distrito)

    return session.exec(consulta).all()

# ------DELETE (DELETE)------------
@app.delete(
    "/viviendas/{vivienda_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Viviendas"]
)
def eliminar_vivienda(session:SessionDep, vivienda_id: int):
    vivienda = session.get(Vivienda, vivienda_id)
    if vivienda is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vivienda {vivienda_id} no encontrada"
        )

    session.delete(vivienda)
    session.commit()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        # reload=True
    )
