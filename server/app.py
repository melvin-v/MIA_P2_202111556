from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]  # Reemplaza con la URL de tu aplicación React

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Puedes especificar los métodos HTTP permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Puedes especificar los encabezados permitidos
)

@app.get("/execute")
async def root():
    return {"Name": "Melvin Valencia", "Carne": "202111556"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
