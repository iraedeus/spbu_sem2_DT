import random
import socket
from threading import Thread

from loguru import logger


class Server:
    def __init__(self, current_port: str, first_port: str, second_port: str) -> None:
        self.current_port = current_port
        self.first_port = first_port
        self.second_port = second_port

    def give_response(self, players: list[tuple[socket.socket, str]], data: bytes) -> None:
        def swap_ports() -> None:
            if self.current_port == self.first_port:
                self.current_port = self.second_port
            else:
                self.current_port = self.first_port

        received_port = int(str(data)[2 : len(str(data)) - 1].split(" ")[-1])
        if received_port == self.current_port:
            for player in players:
                player[0].sendall(data)
            swap_ports()

    def get_row_column(self, conn: socket.socket, addr: str, all_players: list[tuple[socket.socket, str]]) -> None:
        while True:
            data = conn.recv(1024)
            if data:
                self.give_response(all_players, data)
            else:
                conn.close()
                logger.info(f"{addr} has been disconnected")
                break


def main(ip: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind((ip, port))
    sock.listen(2)
    logger.info(f"Started server with ip: {ip}, port: {port}")
    server = Server("", "", "")
    while True:
        conn1, addr1 = sock.accept()
        logger.info(f"Connected from {addr1}")
        conn2, addr2 = sock.accept()
        logger.info(f"Connected from {addr2}")
        server.first_port = addr1[1]
        server.second_port = addr2[1]
        server.current_port = random.choice([server.first_port, server.second_port])

        thread_1 = Thread(target=server.get_row_column, args=(conn1, addr1, [(conn1, addr1), (conn2, addr2)]))
        thread_2 = Thread(target=server.get_row_column, args=(conn2, addr2, [(conn1, addr1), (conn2, addr2)]))
        thread_1.start()
        thread_2.start()


if __name__ == "__main__":
    main("127.0.0.1", 55555)
