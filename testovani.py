def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def check_bit_possitive(value, bit):
    return value & (1 << bit)

def find_byte(note):
    return note // 7

def find_bit_position(note):
    return note % 7

if __name__ == "__main__":
    a = [0 for i in range(5)]
    c = 56
    c -= 52
    byte = find_byte(c)
    bite_possition = find_bit_position(c)
    if check_bit_possitive(a[byte], bite_possition):
        a[byte] = clear_bit(a[byte], bite_possition)
    else:
        a[byte] = set_bit(a[byte], bite_possition)

    b = 5



