from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Configura tus credenciales de la base de datos
DATABASE_HOST = os.getenv('DATABASE_HOST') 
DATABASE_USER = os.getenv('DATABASE_USER') 
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
TABLE_NAME = os.getenv('TABLE_NAME') 

# Conexión a la base de datos MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    return conn

# Endpoint de ejemplo para consultar datos
@app.route('/name/<name>', methods=['GET'])
def consulta(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Usar dictionary=True para obtener resultados como diccionarios
    cursor.execute('SELECT * FROM {TABLE_NAME} where name = %{name}%') 
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Retorna los resultados como JSON
    return jsonify(rows)

@app.route('/set/<name>/<version>/<quantity>', methods=['POST'])
def set_data(name, version, quantity):
    # check if name and version actually exist
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM {TABLE_NAME} where name = %{name}% and version = %{version}%')
    if cursor.fetchone() is not None:
        cursor.execute('UPDATE {TABLE_NAME} SET quantity = %{quantity}% WHERE name = %{name}% and version = %{version}%')
        return jsonify({'message': 'Updated'})
    else:
        cursor.execute('INSERT INTO {TABLE_NAME} (name, version, quantity) VALUES (%s, %s, %s)', (name, version, quantity))
        return jsonify({'message': 'Inserted'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
