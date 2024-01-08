import enchant

d = enchant.Dict('en_US')
filepath = 'output.txt'
word_list = []

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
    iterations = input("\nHow many strings to find: ")
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
    iterations = input("\nHow many strings to find: ")
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
        
def sister_seeds():
    seed = input("Input seed: ")
    if seed.isnumeric() == False:     
        seed = javaHashcode(seed)
    elif seed.isnumeric() == True:
        seed = int(seed)
    print("\nListing 65536 sister seeds, starting with", '"' + str(seed) + '"', '(' + str(seed) + ')\n')
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
        
def seed4word():
    seed = int(input("Input seed:"))
    iterations = input("How many strings per sister seed? ")
    print("'Possible' typos and close strings:\n")
    seed &= ((1 << 48) - 1)
    sister_seeds = [(i << 48) + seed for i in range(1 << 16)]
    check_pos = int(iterations) - 1    
    for seed in sister_seeds:
        sister_strings = search(int(seed), "<", int(iterations))
        while check_pos != 0:
            check1 = d.check(sister_strings[check_pos])
            if check1 == True:
                word_list.append(sister_strings[check_pos])
                check_pos = check_pos - 1
            elif check1 == False:
                check2 = d.suggest(sister_strings[check_pos])
                if len(check2) > 0:
                    print(sister_strings[check_pos], "->", check2)
                check2.clear()
                check_pos = check_pos - 1
    print("\nTrue English words:\n", word_list)
                
mode = input("Int to Str (Finds strings that return the same seed as integer) - 1\nStr to Int (Translates string to integer that returns the same seed) - 2\nStr to Str (Creates more strings that return the same seed) - 3\nList 2^16 sister seeds from input (works for integer or string) - 4\nFind potential words from strings with the same structure seed as input (unlikely to find a real word, slow and prone to errors) - 5\n\nSelect mode:")

if mode == "1":
    int2str()
elif mode == "2":
    str2int()
elif mode == "3":
    str2str()
elif mode == "4":
    sister_seeds()
elif mode == "5":
    seed4word()
else:
    print("Invalid Input")
    quit()