from flask import Flask, jsonify, request, send_from_directory, redirect, session
from flask_cors import CORS  
from Analizador.analizador import analizador
import os
from Global.Global import mounted_partitions

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api-execute', methods=['POST'])
def execute():
    data = request.get_json()
    data = data.get('entry')
    data = data.replace('\r', '')
    data = data.split('\n')
    data = [elemento for elemento in data if elemento != '']
    data = analizador(data)
    return jsonify( {'salida': data})

image_folder = "/home/melvin/archivos/reports"
@app.route('/get_all_images', methods=['GET'])
def get_all_images():
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    
    # Envía la lista de nombres de archivos al cliente en formato JSON
    return jsonify(images=image_files)

@app.route('/get_image/<image_name>', methods=['GET'])
def get_image(image_name):
    image_path = os.path.join(image_folder, image_name)
    return send_from_directory(image_folder, image_name, as_attachment=True)

app.secret_key = 'tu_clave_secreta'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    flag = False
    id = data['id']
    username = data['username']
    password = data['password']
    print(id, username, password)
    for element in mounted_partitions:
        if element[0] == id:
            flag = True
            break
    
    # Verifica las credenciales del usuario
    if username == 'root' and password == '123' and flag:
        session['username'] = username
        return jsonify({'status': 200})
    else:
        return jsonify({'status': 401})

if __name__ == '__main__':
    app.run(host= 'localhost',port= 8000,)