Primero creamos una carpeta donde se colocará el video a mostrar, el cliente.py y server.py.

Dentro de la carpeta abrimos una terminal y pondremos los siguientes comandos:

    1. cvlc -vvv videoplayback.mp4 --sout "#transcode{vcodec=mp4v,acodec=mpga}:rtp{proto=udp, mux=ts, dst=127.0.0.1, port=65534}" --loop --ttl 1

        Este comando con el videoplayback.mp4, genera el stream con destino IP 127.0.0.1 y puerto 65534, transmitido por protocolo RTP (Real-Time Transport Protocol).

    2. python3 server.py <ServerIP> <ServerPort>

        Se procede a levantar el puerto ServerPort (Puerto TCP donde el servidor aceptará conexiones) en la IP ServerIP (Dirección IP donde el servidor aceptará conexiones)

    3. vlc rtp://<ip_cliente>:<puerto_elegido>

        Este comando abre vlc en el cliente con la dirección IP del mismo y el puerto UDP en el que solicitó que le llegara el stream.
    
    4.python3 cliente.py <ServerIP> <ServerPort>

        El cliente se conecta a un servidor, ServerIP (Dirección IP del servidor al que se desea conectar) y ServerPort (Puerto del servidor al que se desea conectar)
        A continuación del paso 4, se ingresara: 

        CONECTAR <PUERTO_UDP_CLIENTE>\n
        INTERRUMPIR\n
        CONTINUAR\n
        DESCONECTAR\n

        Cada mensaje termina con \n para indicar el fin de línea.
        Cada vez que el mensaje llega correctamente al servidor, se mostrará en pantalla la siguiente respuesta enviada por el servidor: 

        OK\n


