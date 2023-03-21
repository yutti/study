def bin_to_dec_hex(bin_num):
    try:
        return int(bin_num,2), hex(int(bin_num,2))
    except :
        return '--'

def dec_to_bin_hex(dec_num):
    try:
        return bin(int(dec_num)), hex(int(dec_num))
    except :
        return '--'

def hex_to_bin_dec(hex_num):
    try:
        return bin(int(hex_num,16)), int(hex_num,16)
    except :
        return '--'