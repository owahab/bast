#!/usr/bin/env python
''' This file mainly dispatches calls.
'''

def main():
    from bt import main
    global bast
    bast = main.bast()

if __name__ == "__main__":
    main()
