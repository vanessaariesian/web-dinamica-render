import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

# Conexión a la base de datos usando la variable de entorno de Render
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Creamos una tabla de ejemplo si no existe
    cur.execute('CREATE TABLE IF NOT EXISTS visitas (id serial PRIMARY KEY, nombre varchar(100));')
    
    # Insertamos un dato de prueba para ver algo en pantalla
    cur.execute('INSERT INTO visitas (nombre) VALUES (%s)', ('Angela y Vanessa',))
    conn.commit()
    
    # Consultamos los datos
    cur.execute('SELECT * FROM visitas;')
    filas = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('index.html', visitas=filas)

if __name__ == "__main__":
    app.run(debug=True)