import hashlib
from multiprocessing import Pool, Value
import itertools

PLACE_HOLDER = b'\\000P\\000D\\000F\\000K\\000W'
SEP = b'\\000'

TARGET = 'c0ffee'
PROCESS = 32

with open('CV.pdf', 'rb') as f:
    content = f.read()

sp1, sp2 = content.split(PLACE_HOLDER)
md5_p1 = hashlib.md5(sp1)

# number to string of 0-9, A-Z, a-z
def number_to_string(num) -> bytes:
    if num < 10:
        return str(num).encode()
    elif num < 36:
        return chr(num + 55).encode()
    else:
        return chr(num + 61).encode()

done = Value('b', False)

def check(i):
    global done
    if done.value:
        return
    s = b''
    for t in range(5):
        s += SEP + number_to_string(i % 62)
        i = i // 62

    md5_curr = md5_p1.copy()
    md5_curr.update(s)
    md5_curr.update(sp2)
    md5 = md5_curr.hexdigest()
    if md5.startswith(TARGET):
        print(s)
        with done.get_lock():
            done.value = True
        return True
    if md5.startswith(TARGET[:-2]):
        print(s, md5)


with Pool(processes=PROCESS) as pool:
    for result in pool.imap_unordered(check, range(100000000)):
        if result:
            pool.terminate()
            break
    