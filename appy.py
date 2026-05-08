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
    
    # Mantenemos esto por si acaso, pero no insertamos nada nuevo
    cur.execute('CREATE TABLE IF NOT EXISTS visitas (id serial PRIMARY KEY, nombre varchar(100));')
    
    # 1. HEMOS ELIMINADO EL INSERT AUTOMÁTICO (A)
    # Ahora la web solo leerá lo que tú metas manualmente desde DBeaver.
    
    # Consultamos los datos ordenados por ID para que no se desordenen
    cur.execute('SELECT id, nombre FROM visitas ORDER BY id ASC;')
    filas = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Enviamos los datos al index.html
    return render_template('index.html', visitas=filas)

if __name__ == "__main__":
    app.run(debug=True)