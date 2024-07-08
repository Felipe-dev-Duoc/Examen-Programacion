import sqlite3
import hashlib
from flask import Flask, request, jsonify

# Conectar a la base de datos
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
''')
conn.commit()

# Función para agregar usuarios a la base de datos
def agregar_usuario(nombre, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)', (nombre, password_hash))
    conn.commit()

# Agregar los usuarios con sus contraseñas
usuarios = [
    ("Fernando Salas", "1234"),
    ("Felipe Diaz", "1234"),
    ("Renato Lobos", "1234")
]

for nombre, password in usuarios:
    agregar_usuario(nombre, password)

# Crear aplicación web con Flask
app = Flask(__name__)

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    nombre = datos['nombre']
    password = datos['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)', (nombre, password_hash))
    conn.commit()
    
    return jsonify({'message': 'Usuario registrado con éxito'}), 201

@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    nombre = datos['nombre']
    password = datos['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('SELECT * FROM usuarios WHERE nombre=? AND password_hash=?', (nombre, password_hash))
    user = cursor.fetchone()
    
    if user:
        return jsonify({'message': 'Login exitoso'}), 200
    else:
        return jsonify({'message': 'Credenciales incorrectas'}), 401

if __name__ == '__main__':
    app.run(port=5800)
