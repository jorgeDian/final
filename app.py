from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# Configurar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a la base de datos MongoDB
client = MongoClient('mongodb+srv://camilo:bLnRuVtBKoXsczqd@cluster0.ffmtk6k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Cluster0']  # Nombre de tu base de datos
collection = db['data']  # Nombre de tu colección

@app.post("/")
async def save_json(json_data: dict):
    try:
        # Eliminar todos los documentos anteriores en la colección
        collection.delete_many({})
        
        # Insertar los datos JSON en la colección de MongoDB
        result = collection.insert_one(json_data)
        
        return {'message': 'JSON data saved successfully', 'inserted_id': str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def get_json_data():
    try:
        # Obtener todos los documentos de la colección
        cursor = collection.find({})
        
        # Convertir los documentos a una lista de diccionarios
        json_data = [{**document, '_id': str(document['_id'])} for document in cursor]
        
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
