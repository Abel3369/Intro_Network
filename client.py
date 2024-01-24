"""
A skeleton from which you should write your client.
"""

import socket
import json
import argparse
import logging
import select
import sys
import time
import datetime
import struct

from message import UnencryptedIMMessage


def parseArgs():
    """
    parse the command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p',
                        dest="port",
                        type=int,
                        default='9999',
                        help='port number to connect to')
    parser.add_argument('--server', '-s',
                        dest="server",
                        required=True,
                        help='server to connect to')
    parser.add_argument('--nickname', '-n',
                        dest="nickname",
                        required=True,
                        help='nickname')
    parser.add_argument('--loglevel', '-l',
                        dest="loglevel",
                        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'],
                        default='INFO',
                        help='log level')
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()

    # set up the logger
    log = logging.getLogger("myLogger")
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    level = logging.getLevelName(args.loglevel)

    log.setLevel(level)
    log.info(f"running with {args}")

    log.debug(f"connecting to server {args.server}")
    try:
        s = socket.create_connection((args.server, args.port))
        log.info("connected to server")
    except:
        log.error("cannot connect")
        exit(1)

    # here's a nice hint for you...
    readSet = [s, sys.stdin]

    while True:
        read_sockets, _, _ = select.select(readSet, [], [])

        for sock in read_sockets:
            if sock == s:
                # 处理从服务器接收到的消息
                packed_len = sock.recv(4)  # 获取消息长度,这代表的是？？？？
                if packed_len:
                    msg_len = struct.unpack('!L', packed_len)[0]
                    json_data = sock.recv(msg_len).decode()  # 获取消息内容
                    message = UnencryptedIMMessage()
                    message.parseJSON(json_data)  # 反序列化消息
                    print(message)  # 显示消息
                else:
                    log.info("Disconnected from server.")
                    return
            else:
                # 处理用户输入
                message_text = sys.stdin.readline().strip()
                if message_text:
                    msg = UnencryptedIMMessage(args.nickname, message_text)
                    packed_size, json_data = msg.serialize()
                    s.sendall(packed_size + json_data)


if __name__ == "__main__":
    exit(main())
