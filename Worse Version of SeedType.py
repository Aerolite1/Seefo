def javaHashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

def search(seed, start, amount):
    res = []
    base = ""
    while len(res) < amount:
        base += start
        dist = seed - javaHashcode(base)
        while dist < 0:
            dist += 1 << 32
        while 31**len(base) > dist:
            nxt = ""
            tmp = dist
            for char in base:
                c = ord(char) + tmp % 31
                tmp //= 31
                nxt = chr(c) + nxt
            res.append(nxt)
            if len(res) >= amount:
                return res
            dist += 1 << 32
            
mode = input("Int to Str (Finds strings that return the same seed as integer) - 1\nStr to Int (Translates string to integer that returns the same seed) - 2\nStr to Str (Creates more strings that return the same seed) - 3\n\nSelect translation mode:")
if mode == "1":
    seednum = input("Enter seed as integer: ")
    iterations = input("!Warning! High number of strings will lead to slow run time.\n\nHow many strings to find: ")
    print(search(int(seednum), "<", int(iterations)))
elif mode == "2":
    seedstr = input("Enter seed as string: ")
    print("The seed", '"' + seedstr + '"', "is", javaHashcode(seedstr))
elif mode == "3":
    seedstr = input("Enter seed as string: ")
    start_seed = javaHashcode(seedstr)
    iterations = input("!Warning! High number of strings will lead to slow run time.\n\nHow many strings to find: ")
    print(search(int(start_seed), "<", int(iterations))) 
else:
    print("Invalid Input")
    quit()
    