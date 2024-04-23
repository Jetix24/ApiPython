import sqlite3
import csv
from fastapi import FastAPI
from pydantic import BaseModel
# Crear la base de datos
class Item(BaseModel):
 song: str
 artist: str
 position: int

app = FastAPI()
@app.post("/agregar_elemento/")
async def agregar_elemento(item: Item):
    conn = sqlite3.connect("hot100.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ranking (artist, song, position) VALUES (?, ?, ?)", (item.artist, item.song, item.position))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos agregados exitosamente"}

@app.get("/leer_elementos/")
async def leer_elementos():
    conn = sqlite3.connect("hot100.db")
    cursor = conn.cursor()
    cursor.execute("SELECT position, song, artist FROM ranking")
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        return [{"position": resultado[0], "song": resultado[1], "artist": resultado[2]} for resultado in resultados]
    else:
        return {"mensaje": "No hay datos en la base de datos"}


@app.get("/leer_elemento/{id}/")
async def leer_elemento(id: int):
    conn = sqlite3.connect("hot100.db")
    cursor = conn.cursor()
    cursor.execute("SELECT position, song, artist FROM ranking WHERE id=?", (id,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado is not None:
        return {"position": resultado[0], "song": resultado[1], "artist": resultado[2]}
    else:
        return {"mensaje": "Datos no encontrados"}

@app.put("/actualizar_elemento/{id}/")
async def actualizar_elemento(id: int, item: Item):
    conn = sqlite3.connect("hot100.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE ranking SET artist=?, song=?, position=? WHERE id=?", (item.artist, item.song, item.position, id))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos actualizados exitosamente"}

@app.delete("/eliminar_elemento/{id}/")
async def eliminar_elemento(id: int):
    conn = sqlite3.connect("hot100.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ranking WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos eliminados exitosamente"}


def create_ranking_table():
    # Conexión a la base de datos "hot100.db"
    conn = sqlite3.connect("hot100.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    # Crear la tabla "ranking" si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS ranking(
    id INTEGER PRIMARY KEY, 
    artist TEXT NOT NULL, 
    song TEXT NOT NULL, 
    position INTEGER NOT NULL)''')

    # Confirmar los cambios en la base de datos y cerrar la conexión
    conn.commit()
    conn.close()


def read_csv_file(csv_file):
 # Leer el archivo CSV y guardar los datos en una lista de diccionarios
 with open(csv_file, newline='') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]
 return data
def insert_data_to_ranking_table(data):
 # Conexión a la base de datos "hot100.db"
 conn = sqlite3.connect("hot100.db")
 # Crear un cursor para interactuar con la base de datos
 cursor = conn.cursor()
 # Insertar cada fila de datos en la tabla "ranking"
 for row in data:
    cursor.execute("""
    INSERT INTO ranking (artist, song, position)
    VALUES (?, ?, ?)
    """, (row["Artist"], row["Song"], int(row["Position"])))
 # Confirmar los cambios en la base de datos y cerrar la conexión
 conn.commit()
 conn.close()


if __name__ == "__main__":
 
 # Crear la tabla "ranking" en la base de datos "hot100.db"
    create_ranking_table()
 # Nombre del archivo CSV que contiene los datos
    csv_file = "Billboard Hot 100-07-08-2023.csv"

    # Leer los datos del archivo CSV y guardarlos en una lista de diccionarios
    data_to_insert = read_csv_file(csv_file)


 # Insertar los datos en la tabla "ranking" desde el archivo CSV
    insert_data_to_ranking_table(data_to_insert)