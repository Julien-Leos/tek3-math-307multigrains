import sys
import numpy as np

def isNumber(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def checkUsage(arg):
    if arg == "-h" or arg == "--help":
        print("USAGE:\t./307multigrains n1 n2 n3 n4 po pw pc pb ps\n\nDESCRIPTION")
        print("\tn1\tnumber of tons of fertilizer F1")
        print("\tn2\tnumber of tons of fertilizer F2")
        print("\tn3\tnumber of tons of fertilizer F3")
        print("\tn4\tnumber of tons of fertilizer F4")
        print("\tpo\tprice of one unit of oat")
        print("\tpw\tprice of one unit of wheat")
        print("\tpc\tprice of one unit of corn")
        print("\tpb\tprice of one unit of barley")
        print("\tps\tprice of one unit of soy")
        sys.exit(0)

def checkArgs(args):
    if len(args) != 9:
        print("Invalid number of arguments. Try ./307multigrains -h for usage")
        sys.exit(84)
    for arg in args:
        if isNumber(arg) == False:
            print("Arguments must be numbers. Try ./307multigrains -h for usage")
            sys.exit(84)
        elif float(arg) < 0:
            print("Arguments must be strictly positives. Try ./307multigrains -h for usage")
            sys.exit(84)

def parse(args):
    if len(args) == 1:
        checkUsage(args[0])
    checkArgs(args)
