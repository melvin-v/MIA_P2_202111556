def coding_str(string,size):
    return string.encode('utf-8')[:size].ljust(size, b'\0')

def get_sizeB(size,unit):
    return size if unit == "b" else (size * 1000 if unit == "k" else size * 1000 * 1000 )