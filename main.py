import sqlite3
import csv
from fastapi import FastAPI
from pydantic import BaseModel

# Crear la base de datos
class Item(BaseModel):
 nombres: str
 types: str
 total: int
 hp: int
 attack: int
 defense: int
 sp_attack: int
 sp_def: int
 spped: int
 

app = FastAPI()
@app.post("/agregar_pokemon/")
async def agregar_pokemon(item: Item):
    conn = sqlite3.connect("mundo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pokemones (nombres,types,total,hp,attack,defense,sp_attack,sp_def,spped) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (item.nombres, item.types, item.total, item.hp, item.attack, item.defense, item.sp_attack, item.sp_def, item.spped))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos agregados exitosamente"}

@app.get("/leer_pokemones/")
async def leer_pokemones():
    conn = sqlite3.connect("mundo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombres, types, total, hp, attack, defense, sp_attack, sp_def, spped FROM pokemones")
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        return [{"id": resultado[0], "nombres": resultado[1], "types": resultado[2] , "total": resultado[3] , "hp": resultado[4] , "attack": resultado[5] , "defense": resultado[6] , "sp_attack": resultado[7] , "sp_def": resultado[8] , "spped": resultado[9]} for resultado in resultados]
    else:
        return {"mensaje": "No hay datos en la base de datos"}


@app.get("/leer_pokemones/{id}/")
async def leer_pokemones(id: int):
    conn = sqlite3.connect("mundo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombres, types, total, hp, attack, defense, sp_attack, sp_def, spped FROM pokemones WHERE id=?", (id,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado is not None:
        return {"id": resultado[0], "nombres": resultado[1], "types": resultado[2] , "total": resultado[3] , "hp": resultado[4] , "attack": resultado[5] , "defense": resultado[6] , "sp_attack": resultado[7] , "sp_def": resultado[8] , "spped": resultado[9]}
    else:
        return {"mensaje": "Datos no encontrados"}

@app.put("/actualizar_pokemon/{id}/")
async def actualizar_pokemon(id: int, item: Item):
    conn = sqlite3.connect("mundo.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE pokemones SET nombres=?, types=?, total=?, hp=?, attack=?, defense=?, sp_attack=?, sp_def=?, spped=? WHERE id=?", (item.nombres, item.types, item.total, item.hp, item.attack, item.defense, item.sp_attack, item.sp_def, item.spped, id))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos actualizados exitosamente"}

@app.delete("/eliminar_pokemon/{id}/")
async def eliminar_pokemon(id: int):
    conn = sqlite3.connect("mundo.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pokemones WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos eliminados exitosamente"}


def create_pokemon_table():
    # Conexión a la base de datos "Mundo pokemon"
    conn = sqlite3.connect("mundo.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    # Crear la tabla "ranking" si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS pokemones(
    id INTEGER PRIMARY KEY, 
    nombres TEXT NOT NULL, 
    types TEXT NOT NULL, 
    total INTEGER NOT NULL,
    hp INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    sp_attack INTEGER NOT NULL,
    sp_def INTEGER NOT NULL,
    spped INTEGER NOT NULL)''')
    # Confirmar los cambios en la base de datos y cerrar la conexión
    conn.commit()
    conn.close()

def read_csv_file(csv_file):
 # Leer el archivo CSV y guardar los datos en una lista de diccionarios
 with open(csv_file, newline='') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]
 return data

def insert_data_to_pokemon_table(data):
 # Conexión a la base de datos "hot100.db"
 conn = sqlite3.connect("mundo.db")
 # Crear un cursor para interactuar con la base de datos
 cursor = conn.cursor()
 # Insertar cada fila de datos en la tabla "ranking"
 for row in data:
    cursor.execute("""
    INSERT INTO pokemones (nombres, types, total, hp, attack, defense, sp_attack, sp_def, spped)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (row["nombres"], row["types"], int(row["total"]), int(row["hp"]), int(row["attack"]), int(row["defense"]), int(row["sp_attack"]), int(row["sp_def"]), int(row["spped"])))
 # Confirmar los cambios en la base de datos y cerrar la conexión
 conn.commit()
 conn.close()


if __name__ == "__main__":
 
    # Nombre del archivo CSV que contiene los datos
    csv_file = "pokemones.csv"

    # Leer los datos del archivo CSV y guardarlos en una lista de diccionarios
    data_to_insert = read_csv_file(csv_file)

    # Crear la tabla "ranking" en la base de datos "hot100.db"
    create_pokemon_table()

    # Insertar los datos en la tabla "ranking" desde el archivo CSV
    insert_data_to_pokemon_table(data_to_insert)