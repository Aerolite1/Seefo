filepath = 'output.txt'

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
            
def int2str():
    seednum = input("Enter seed as integer: ")
    iterations = input("!Warning! High number of strings will lead to slow run time.\n\nHow many strings to find: ")
    print_method = input("\n[ ] - 1\nList - 2\nSave to File - 3\nPrint method: ")
    if print_method == "2":
        print("\nListing possible strings for the seed: " + '"' + seednum + '"', "\n")
        printint = search(int(seednum), "<", int(iterations))
        for i in printint:
            print(i)
    elif print_method == "1":
        print("\n", search(int(seednum), "<", int(iterations)))
    elif print_method =="3":
        with open(filepath, 'w') as file:
            result = search(int(seednum), "<", int(iterations))
            for i in result:
                file.write(i + '\n') 
    else:
        print("Invalid input")
        quit()
        
def str2int():
    seedstr = input("Enter seed as string: ")
    print("The seed", '"' + seedstr + '"', "is", javaHashcode(seedstr))

def str2str():
    seedstr = input("Enter seed as string: ")
    start_seed = javaHashcode(seedstr)
    iterations = input("!Warning! High number of strings will lead to slow run time.\n\nHow many strings to find: ")
    print_method = input("\n[ ] - 1\nList - 2\nSave to File - 3\nPrint method: ")
    if print_method == "2":
        print("\nListing possible strings for the seed: " + '"' + seedstr + '"', "\n")
        printint = search(int(start_seed), "<", int(iterations))
        for i in printint:
            print(i)
    elif print_method == "1":
        print("\n", search(int(start_seed), "<", int(iterations)))
    elif print_method =="3":
        with open(filepath, 'w') as file:
            result = search(int(seedstr), "<", int(iterations))
            for i in result:
                file.write(i + '\n')      
    else:
        print("Invalid input")
        quit()
        
def str2sister_seeds():
    seed = input("Input seed as string: ")
    first_seed = javaHashcode(seed)
    print("\nListing 65536 sister seeds, starting with", '"' + seed + '"', '(' + str(first_seed) + ')\n')
    seed &= ((1 << 48) - 1)
    sister_seeds = [(i << 48) + first_seed for i in range(1 << 16)]
    print_method = input("\nList - 1\nSave to File - 2\nPrint method: ")
    if print_method == "1":
        for first_seed in sister_seeds:
            print(seed)
    elif print_method =="2":
        with open(filepath, 'w') as file: 
            for first_seed in sister_seeds:
                result = str(first_seed) + '\n'
                file.write(str(result))
    else:
        print("Invalid input")
        quit()
        
def int2sister_seeds():
    seed = int(input("Input seed as integer: "))
    print("\nListing 65536 sister seeds, starting with", '"' + str(seed) + '"\n')
    seed &= ((1 << 48) - 1)
    sister_seeds = [(i << 48) + seed for i in range(1 << 16)]
    print_method = input("\nList - 1\nSave to File - 2\nPrint method: ")
    if print_method == "1":
        for seed in sister_seeds:
            print(seed)
    elif print_method =="2":
        with open(filepath, 'w') as file: 
            for seed in sister_seeds:
                result = str(seed) + '\n'
                file.write(str(result))
    else:
        print("Invalid input")
        quit()
        
mode = input("Int to Str (Finds strings that return the same seed as integer) - 1\nStr to Int (Translates string to integer that returns the same seed) - 2\nStr to Str (Creates more strings that return the same seed) - 3\nList 2^16 sister seeds from integer - 4\nList 2^16 sister seeds from string - 5\n\nSelect mode:")

if mode == "1":
    int2str()
elif mode == "2":
    str2int()
elif mode == "3":
    str2str()
elif mode == "4":
    int2sister_seeds()
elif mode == "5":
    str2sister_seeds()
else:
    print("Invalid Input")
    quit()