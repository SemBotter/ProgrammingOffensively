import os
def hello_world():
    return "Hello, world! From Python"

def test(message):
    directory = os.getcwd()
    return message + ": " + directory

if __name__ == "__main__":
    print("Main!")
else:
    print(__name__)
    
msg = hello_world()
print(test(msg))