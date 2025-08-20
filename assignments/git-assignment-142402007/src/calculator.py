import sys

def add(a, b):
    return a + b

if __name__ == "__main__":
    # sys.argv[0] is the filename, so numbers start from sys.argv[1]
    if len(sys.argv) != 3:
        print("Usage: python3 calculator.py <num1> <num2>")
    else:
        num1 = int(sys.argv[1])
        num2 = int(sys.argv[2])
        result = add(num1, num2)
        print(f"{num1} + {num2} = {result}")
