

BYTE_SIZE = 3
BYTE_ORDER = 'big'

def bytize_lambda(byte_size, byteorder):
    def bytize(b_s, b_o, *args):
        bytes = bytearray(b_s * len(args))
        for i in range(len(args)):
            bytes[i * b_s: (i + 1) * b_s] = args[i].to_bytes(b_s, b_o)
        return bytes
    return lambda *args: bytize(byte_size, byteorder,*args)

toByteArray = bytize_lambda(BYTE_SIZE, BYTE_ORDER)

def get_from_bytes_lambda(byte_size, byteorder):
    def get_from_bytes(b_s, b_o, bytes):
        return [int.from_bytes(bytes[i * b_s: (i + 1) * b_s], b_o) for i in
                range(len(bytes) // b_s)]
    return lambda *args: get_from_bytes(byte_size, byteorder, *args)

fromByteArray = get_from_bytes_lambda(BYTE_SIZE, BYTE_ORDER)

