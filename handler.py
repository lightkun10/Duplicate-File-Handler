import collections
import os
import sys
import hashlib

args = sys.argv

def check_dupes(file_dict):
    print("\nCheck for duplicates?")
    a = input()

    if a != 'yes' and a != 'no':
        print('Wrong option')
        check_dupes(file_dict)
    elif a == 'no':
        sys.exit()
    elif a == 'yes':
        hash_dict = {}
        for i in file_dict.items():
            if type(i[1]) == list:
                # Possible dupes
                for val in i[1]:
                    with open(val, 'rb') as file:
                        hash_obj = hashlib.md5()
                        file_inside = file.read()
                        hash_obj.update(file_inside)
                    hash_val = {val: hash_obj.hexdigest()}
                    hash_dict.update(hash_val)
        out_with_hash(file_dict, hash_dict)

def out_with_hash(file_dict, hash_dict):
    output = {}
    compare_with = hash_dict
    n = 0
    numbered_dict = {}
    for i0 in file_dict.items():
        for i1 in hash_dict.items():
            for i2 in compare_with.items():
                if i1[1] == i2[1] and i1[0] != i2[0] and i1[0] in i0[1]:
                    add_in = {i1[1]: [i1[0], i2[0]]}
                    output.update(add_in)
        print('\n' + str(i0[0]) + ' ' + 'bytes')
        for val in list(output.items()):
            if len(val[1]) > 1:
                print('Hash:' + ' ' + val[0])
                for out in val[1]:
                    n = n + 1
                    print(str(n) + '.' + ' ' + out)
                    numbered_dict[str(n)] = out
        output = {}
    delete_files(numbered_dict, file_dict)

def delete_files(numbered_dict, file_dict):
    print("\nDelete files?")
    a1 = input()

    if a1 != 'yes' and a1 != 'no':
        print('Wrong option')
        delete_files(numbered_dict, file_dict)
    elif a1 == 'no':
        sys.exit()
    elif a1 == 'yes':
        while True:
            size_s = 0
            print("\nEnter file numbers to delete:")
            num_del = input()
            choices = num_del.split(" ")
            if all(choice in numbered_dict for choice in choices) == False:
                print("Wrong choice")
            elif all(choice in numbered_dict for choice in choices):                    
                for size, file_dir in file_dict.items():
                    for numbered, fs in numbered_dict.items():
                        for choice in choices:
                            if choice == numbered and fs in file_dir:
                                os.remove(fs)
                                size_s = size_s + size 
                print(size_s)
                break
                

def get_files(sort_opt, frmt):
    file_dict = dict()
    for root, dirs, files in os.walk(args[1], topdown=False):
        for file in files:
            full_path = os.path.join(root, file)
            # print(os.path.join(root, file))
            # print(os.path.getsize(os.path.join(root, file)))
            f_name = os.path.basename(full_path)
            sz = os.path.getsize(full_path)
            """
            If there's a duplicate with exactly the same size
            """
            if sz in file_dict:
                a = []
                o = file_dict[sz]
                if type(o) == list:
                    for oz in o:
                        if len(frmt) != 0 and oz.split(".")[1] == frmt:
                            a.append(oz)
                        elif len(frmt) == 0:
                            a.append(oz)
                elif len(frmt) != 0 and o.split(".")[1] == frmt:
                    a.append(o)
                elif len(frmt) == 0:
                    a.append(o)
                file_dict[sz] = a
                if len(frmt) != 0 and full_path.split(".")[1] == frmt:
                    file_dict[sz].append(full_path)
                elif len(frmt) == 0:
                    file_dict[sz].append(full_path)
            elif len(frmt) != 0 and f_name.split(".")[1] == frmt:
                file_dict[sz] = full_path
            elif len(frmt) == 0:
                file_dict[sz] = full_path
    # print(sorted(file_dict, reverse=sort_opt))
    for size in sorted(file_dict, reverse=sort_opt):
        print(f"{size} bytes")
        if type(file_dict[size]) is list:
            for v2 in file_dict[size]:
                print(v2)
        else:
            print(file_dict[size])
        print()

    # Returned the sorted files with sizes
    return collections.OrderedDict(sorted(file_dict.items(), reverse=sort_opt))
                
            


if __name__ == "__main__":
    if len(args) <= 1:
        print("Directory is not specified")
        exit(1)

    file_format = input("\nEnter file format:\n")
    # True: "Descending", False: "Ascending"}
    sorting_opt = {1: True, 2: False}

    print("\nSize sorting options:")
    print("1. Descending\n2. Ascending\n")

    is_wrong_opt = True
    files = ''
    while is_wrong_opt:
        sort_choice = int(input("Enter a sorting option:\n"))
        try:
            # print(sorting_opt[sort_choice])
            files = get_files(sorting_opt[sort_choice], frmt=file_format)
            is_wrong_opt = False
        except KeyError:
            print("Wrong option\n")

    check_dupes(files)
