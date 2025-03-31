def E1(x):
    return x * 2

def E2(x):
    return x ** 2

def E3(x):
    return x + 10

def E4(x):
    return x - 5

def E5(x, y):
    return x * y

def E6(x, y):
    return x / y if y != 0 else "Error: Division by zero"

def E7(s):
    return s.upper()

def E8(s):
    return s.lower()

def E9(s):
    return s[::-1]

def show(function_name):
    """Displays information about the requested function(s)."""
    functions = {
        "E1": "E1(x): Returns x * 2",
        "E2": "E2(x): Returns x ** 2",
        "E3": "E3(x): Returns x + 10",
        "E4": "E4(x): Returns x - 5",
        "E5": "E5(x, y): Returns x * y",
        "E6": "E6(x, y): Returns x / y (handles zero division)",
        "E7": "E7(s): Converts string to uppercase",
        "E8": "E8(s): Converts string to lowercase",
        "E9": "E9(s): Reverses the string",
    }
    
    if function_name == "E1-9":
        for key, desc in functions.items():
            print(desc)
    elif function_name in functions:
        print(functions[function_name])
    else:
        print("Function not found. Use 'E1-9' to see all functions.")
