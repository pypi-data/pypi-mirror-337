from pwn import *
import ctypes
from typing import Callable

io = tube()

# recv
r   = io.recv
rl  = io.recvline
ru  = io.recvuntil
r64: Callable[[], int] = lambda: u64(io.recv(6)+p16(0))

# send
s   = io.send
sa  = io.sendafter
sl  = io.sendline
sla = io.sendlineafter

# cast
i8:   Callable[[int], int] = lambda value: ctypes.c_int8(value).value
i16:  Callable[[int], int] = lambda value: ctypes.c_int16(value).value
i32:  Callable[[int], int] = lambda value: ctypes.c_int32(value).value
i64:  Callable[[int], int] = lambda value: ctypes.c_int64(value).value
ui8:  Callable[[int], int] = lambda value: ctypes.c_uint8(value).value
ui16: Callable[[int], int] = lambda value: ctypes.c_uint16(value).value
ui32: Callable[[int], int] = lambda value: ctypes.c_uint32(value).value
ui64: Callable[[int], int] = lambda value: ctypes.c_uint64(value).value
f32:  Callable[[int], int] = lambda value: ctypes.c_float(value).value
f64:  Callable[[int], int] = lambda value: ctypes.c_double(value).value

# safe linking
protect_ptr = lambda pos, ptr: pos ^ ptr
reaval_ptr  = protect_ptr

def wrapper(gb: dict[str, any]):
    io: tube = gb['io']
    gb['r']   = io.recv
    gb['rl']  = io.recvline
    gb['ru']  = io.recvuntil
    gb['r64'] = lambda: u64(io.recv(6)+p16(0))
    gb['s']   = io.send
    gb['sa']  = io.sendafter
    gb['sl']  = io.sendline
    gb['sla'] = io.sendlineafter

def dbg(gb: dict[str, any], expects = ['_base', '_ptr']):
    for (key, value) in gb.items():
        for expect in expects:
            if expect in key and isinstance(value, int):
               info(f"{key}: {hex(value)}")
    pause()