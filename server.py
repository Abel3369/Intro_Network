import socket
import json
import argparse
import logging
import select
import struct
import time


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p',
                        dest="port",
                        type=int,
                        default='9999',
                        help='port number to listen on')
    parser.add_argument('--loglevel', '-l',
                        dest="loglevel",
                        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'],
                        default='INFO',
                        help='log level')
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()  # parse the command-line arguments

    # set up logging
    log = logging.getLogger("myLogger")
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    level = logging.getLevelName(args.loglevel)
    log.setLevel(level)
    log.info(f"running with {args}")

    log.debug("waiting for new clients...")
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(("", args.port))
    serverSock.listen()
    recv_buffer = 1024

    clientList = []
    socketList = [serverSock]

    while True:
        readable, writable, _ = select.select(socketList, [], [])

        for sock in readable:
            # 处理新连接
            if sock == serverSock:
                clientSock, addr = serverSock.accept()
                log.info(f"New connection from {addr}")
                socketList.append(clientSock)
            else:
                # 处理来自客户端的消息
                try:
                    # packed_len = sock.recv(4)  # 获取消息长度
                    msg = sock.recv(recv_buffer)
                    # if packed_len:
                    #     msg_len = struct.unpack('!L', packed_len)[0]
                    #     json_data = sock.recv(msg_len)  # 获取消息内容
                    #     print(json_data)
                    if msg:
                        # 将消息转发给其他所有的客户端
                        for s in socketList:
                            if s != serverSock and s != sock:
                                try:
                                    s.send(msg)  # 保持原始格式转发
                                except:
                                    s.close()
                                    socketList.remove(s)
                    else:
                        # 客户端断开连接
                        log.info(f"Client disconnect: {sock.getpeername()}")
                        socketList.remove(sock)
                        sock.close()
                except socket.error as e:
                    log.error(f"Socket error: {e}")
                    socketList.remove(sock)
                    sock.close()
    serverSock.close()


if __name__ == "__main__":
    exit(main())
