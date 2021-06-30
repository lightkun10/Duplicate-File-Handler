import os
import sys

args = sys.argv

if len(args) <= 1:
    print("Directory is not specified")
    exit(1)

for root, dirs, files in os.walk(args[1], topdown=False):
    for file in files:
        print(os.path.join(root, file))