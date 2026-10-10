from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Hola FASTAPI",
    description="Primer contacto con FASTAPI",
    version="0.1"
)

@app.get("/")
def raiz():
    return {"mensaje": "Hola, FASTAPI!"}

@app.get("/salud")
def salud():
    return {"estado": "ok"}

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"saludo": f"Hola {nombre}!"}

@app.get("/suma")
def sumar(param1: int, param2: int = 0, param3: int = 0):
    return {
        "param1": param1,
        "param2": param2,
        "param3": param3,
        "resultado": param1 + param2 + param3
    }

# Correr el script uv run 01_app_hola.py
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/salud
# http://127.0.0.1:8000/saludo/Marcell
# http://127.0.0.1:8000/suma?param1=10&param2=10&param3=15
if __name__ == "__main__":
    uvicorn.run(
        "01_app_hola:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
