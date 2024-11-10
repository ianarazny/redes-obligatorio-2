import socket
import sys
import re

def conectar(server_ip, server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((server_ip, server_port))
        conectadoUDP = False
        pattern_aux = r'^(INTERRUMPIR|CONTINUAR)\n$'
        pattern_con = r'^(CONECTAR (\d+))\n$'
        pattern_dcon = r'^(DESCONECTAR)\n$'

        while (True):
            entrada = input("")
            entrada = entrada + "\n"

            aux = re.match(pattern_aux, entrada)
            if (aux):
                # Envía el comando al servidor
                server.send((aux.group(1) + "\n").encode('utf-8'))
                respuesta = server.recv(1024).decode()
                print(respuesta)
            
            conn = re.match(pattern_con, entrada)
            if (not conectadoUDP and conn):
                    # Si no esta conectado y solicitó hacerlo
                    try :
                        puerto_str = conn.group(2)
                        puerto_int = int(puerto_str)
                        if (puerto_int <= 1024) :
                            print("El puerto debe ser mayor que 1024.")
                            break
                        server.send("CONECTAR {}\n".format(puerto_int).encode('utf-8'))
                        respuesta = server.recv(1024).decode()
                        if (respuesta == "OK\n"):
                            conectadoUDP = True
                        print(respuesta)     
                    except ValueError:
                        print("CONECTAR debe seguirse de un número de puerto.")
            elif (conectadoUDP and conn):
                print("Finalice la sesión actual para recibir en un nuevo puerto")
            
            dconn = re.match(pattern_dcon, entrada)
            if (dconn):
                server.send((dconn.group(1) + "\n").encode('utf-8'))
                respuesta = server.recv(1024).decode()
                print(respuesta)
                server.close()
                return
            
            if(not aux and not conn and not dconn):
                print("NO OK")
            
    except Exception as e:
        print("ERROR DE CONEXION")
        e.print_exc()
    finally:
        server.close()

def main():
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    conectar(server_ip, server_port)

if __name__ == "__main__":
    main()
