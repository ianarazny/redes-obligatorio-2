import re
import socket
import sys
import threading

class clientSender:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

socket_senders = []
socket_interrupted = []

s1 = threading.Semaphore(1)
s2 = threading.Semaphore(1)

def udp_eater_puker(host):
    receptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receptor.bind(('127.0.0.1', 65534))
    emisor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(True):
        data, client_address = receptor.recvfrom(2048)
        s1.acquire()
        for item in socket_senders:
            emisor.sendto(data, (item.ip, item.port))
        s1.release()
    receptor.close()
    emisor.close()
    return

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(20)
        print(f"Escuchando en {host}:{port}")

        udp_thread = threading.Thread(target=udp_eater_puker, args=(host,))
        udp_thread.start()

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Nuevo cliente registrado en {client_address}")
            client_thread = threading.Thread(target=CONTROLSTREAM, args=(client_socket,client_address))
            client_thread.start()

        server_socket.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

def CONTROLSTREAM(cliente, cliente_address):
    buff =''
    port = 0
    conecction_pattern = r'CONECTAR (\d+)\n'
    interrupted = False
    try:
        while(True):
            data = cliente.recv(1024)
            buff = data.decode()
            match = re.search(conecction_pattern, buff)
            cliente.send(('OK\n').encode('utf-8'))
            if(match):
                port = match.group(1)
                break
        
        position = buff.find('CONECTAR '+port)
        buff = buff[(position + len('CONECTAR '+port) + 1):]

        # creación del struct para transmisión de data al cliente
        cs = clientSender(cliente_address[0], int(port))
        s1.acquire()
        socket_senders.append(cs)
        s1.release()
        # así queda almacenado el socket udp escucha de esta conexión en el server

        while(buff != 'DESCONECTAR\n'):
            buff = ''
            while(buff.find("\n") == -1):
                buff = cliente.recv(1024).decode()

            if(buff == 'INTERRUMPIR\n'):
                if(not interrupted):
                    s1.acquire()
                    socket_senders.remove(cs)
                    s1.release()

                    s2.acquire()
                    socket_interrupted.append(cs)
                    s2.release()

                    interrupted = True
            if(buff == 'CONTINUAR\n'):
                if(interrupted):
                    s2.acquire()
                    socket_interrupted.remove(cs)
                    s2.release()

                    s1.acquire()
                    socket_senders.append(cs)
                    s1.release()

                    interrupted = False
            
            cliente.send(('OK\n').encode('utf-8'))
        
        cliente.close()
        if(interrupted):
            s2.acquire()
            socket_interrupted.remove(cs)
            s2.release()
        else:
            s1.acquire()
            socket_senders.remove(cs)
            s1.release()
        print("Cliente Desconectado")
        return

    except Exception as e:
        print("Cliente Desconectado")
        print(f"Error: {e}")
        e.print_exc()
    finally:
        cliente.close()   



def main():
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    start_server(server_ip, server_port)

if __name__ == "__main__":
    main()
