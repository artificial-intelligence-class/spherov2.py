def recvall(s, size):
    data = bytes()
    while len(data) < size:
        n = s.recv(size - len(data))
        if not n:
            raise Exception
        data += n
    return data
