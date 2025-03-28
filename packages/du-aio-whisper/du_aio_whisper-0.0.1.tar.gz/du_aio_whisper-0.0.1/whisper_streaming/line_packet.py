#!/usr/bin/env python3

"""用于通过socket发送和接收单行文本的函数。

一行文本通过一个或多个固定大小的UTF-8字节包进行传输，包含：

  - 零个或多个UTF-8字节（不包含\n和\0），后跟

  - 根据需要填充零个或多个\0字节以达到PACKET_SIZE大小

最初来自ELITR项目的UEDIN团队。
"""

PACKET_SIZE = 65536


def send_one_line(socket, text, pad_zeros=False):
    """通过给定的socket发送一行文本。

    'text'参数应包含单行文本（换行符是可选的）。行边界由Python的
    str.splitlines()函数[1]确定。我们也将'\0'视为行终止符。
    如果'text'包含多行，则只发送第一行。

    如果发送失败，将抛出异常。

    [1] https://docs.python.org/3.5/library/stdtypes.html#str.splitlines

    参数：
        socket: socket对象。
        text: 要传输的文本行字符串。
    """
    text.replace('\0', '\n')
    lines = text.splitlines()
    first_line = '' if len(lines) == 0 else lines[0]
    # TODO: 是否有比'replace'更好的方法来处理错误的输入？
    data = first_line.encode('utf-8', errors='replace') + b'\n' + (b'\0' if pad_zeros else b'')
    for offset in range(0, len(data), PACKET_SIZE):
        bytes_remaining = len(data) - offset
        if bytes_remaining < PACKET_SIZE:
            padding_length = PACKET_SIZE - bytes_remaining
            packet = data[offset:] + (b'\0' * padding_length if pad_zeros else b'')
        else:
            packet = data[offset:offset+PACKET_SIZE]
        socket.sendall(packet)


def receive_one_line(socket):
    """从给定的socket接收一行文本。

    此函数将（尝试）接收单行文本。如果当前没有可用数据，
    它将阻塞直到数据可用或发送方关闭连接（此时将返回空字符串）。

    字符串不应包含任何换行符，但如果包含，则只返回第一行。

    参数：
        socket: socket对象。

    返回：
        表示单行的字符串（带有终止换行符）或
        如果连接已关闭则返回None。
    """
    data = b''
    while True:
        packet = socket.recv(PACKET_SIZE)
        if not packet:  # 连接已关闭
            return None
        data += packet
        if b'\0' in packet:
            break
    # TODO: 是否有比'replace'更好的方法来处理错误的输入？
    text = data.decode('utf-8', errors='replace').strip('\0')
    lines = text.split('\n')
    return lines[0] + '\n'


def receive_lines(socket):
    try:
        data = socket.recv(PACKET_SIZE)
    except BlockingIOError:
        return []
    if data is None:  # 连接已关闭
        return None
    # TODO: 是否有比'replace'更好的方法来处理错误的输入？
    text = data.decode('utf-8', errors='replace').strip('\0')
    lines = text.split('\n')
    if len(lines)==1 and not lines[0]:
        return None
    return lines
