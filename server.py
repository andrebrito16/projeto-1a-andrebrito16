import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index
from database.database import Database

CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

# Initialize database
database_instance = Database('getit')

print(f'Sever running on http://{SERVER_HOST}:{SERVER_PORT} 🚀')


while True:
    client_connection, client_address = server_socket.accept()
    print("Connection from: ", client_address)

    request = client_connection.recv(1024).decode()

    response = 'HTTP/1.1 200 OK\n\nHello World'

    route = extract_route(request)
    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request, database_instance)
    elif route.startswith('delete'):
        delete_id = route.split('/')[-1].split('?')[0]
        database_instance.delete(delete_id)
        response = index(request, database_instance)
    elif route.startswith('edit'):
        response = index(request, database_instance)
    else:
        response = build_response()

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()
