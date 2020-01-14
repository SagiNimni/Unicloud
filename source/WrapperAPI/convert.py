KB = 1024
MB = 1000000
GB = 1000000000


def convert_bytes_to_kb(bytes_amount):
    kb_memory = bytes_amount / KB
    return str(kb_memory) + "KB"


def convert_bytes_to_mb(bytes_amount):
    mb_memory = bytes_amount / KB / KB
    if mb_memory % 1 == 0:
        return mb_memory, 0.0
    else:
        kb_memory = MB * (mb_memory % 1)
        kb_memory = convert_bytes_to_kb(kb_memory)
        mb_memory = mb_memory - (mb_memory % 1)
        return mb_memory, kb_memory


def convert_bytes_to_gb(bytes_amount):
    gb_memory = bytes_amount / KB / KB / KB
    if gb_memory % 1 == 0:
        return gb_memory, 0.0
    else:
        mb_memory = GB * (gb_memory % 1)
        mb_memory, kb_memory = convert_bytes_to_mb(mb_memory)
        gb_memory = gb_memory - (gb_memory % 1)
        return gb_memory, mb_memory