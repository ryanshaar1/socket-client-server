import socket
import os
import threading

def upload_file(client_socket, filename):
    client_socket.send(b'upload')
    client_socket.send(filename.encode())

    with open(filename, 'rb') as f:
        for data in f:
            client_socket.send(data)
    print("File sent successfully.")

def download_file(client_socket, filename):
    client_socket.send(b'download')
    client_socket.send(filename.encode())
    download_dir = r"C:\Users\Ryan\OneDrive\מסמכים\CODING\VSCODE\pythonLearning\python\מועדון המתכנתים\FileUploadAndDownloadSystem\downloading_files"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    filepath = os.path.join(download_dir, filename)
    with open(filepath, 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    print("File received successfully.")
    print("Download completed.")

def receive_message(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print('Received from server:', data)
        if data == "exit":
            break

def client_program():
    host = socket.gethostname()  
    port = 5000  
    client_socket = socket.socket()  
    client_socket.connect((host, port))  
    print("Connected to the server.")  
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    while True:
        choice = input("Do you want to upload, download, or exit? (u/d/exit): ")
        if choice == "exit":
            client_socket.send(choice.encode())
            break
        client_socket.send(choice.encode())
        if choice == "upload":
            filename = input("Enter filename to upload: ")
            upload_file(client_socket, filename)
        elif choice == "download":
            filename = input("Enter filename to download: ")
            download_file(client_socket, filename)
        else:
            pass

    client_socket.close()  
    receive_thread.join()  

if __name__ == '__main__':
    client_program()
