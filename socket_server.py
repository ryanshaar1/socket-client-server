import socket
import os

def receive_file(conn, filename):
    # Specify the directory to save uploaded files
    upload_dir = r"C:\Users\Ryan\OneDrive\מסמכים\CODING\VSCODE\pythonLearning\python\מועדון המתכנתים\FileUploadAndDownloadSystem\upload_files"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    filepath = os.path.join(upload_dir, filename)
    with open(filepath, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    print("File received successfully.")

def send_file(conn, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            for data in f:
                conn.send(data)
        print("File sent successfully.")
    else:
        conn.send(b'File not found.')

def server_program():
    host = socket.gethostname()
    port = 5000  
    server_socket = socket.socket()  
    server_socket.bind((host, port))  
    server_socket.listen(2)
    print("Server is listening on", host, ":", port)  
    conn, address = server_socket.accept()  
    print("Connection from:", address)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user:", data)
        if data == "upload":
            filename = conn.recv(1024).decode()
            receive_file(conn, filename)
        elif data == "download":
            filename = conn.recv(1024).decode()
            send_file(conn, filename)
            print("Sent", filename)
            conn.send(b'Download completed.')
        else:
            message = input(' -> ')
            conn.send(message.encode())

    conn.close()

if __name__ == '__main__':
    server_program()
