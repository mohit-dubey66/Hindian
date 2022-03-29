import interpreter

while True:
    text = input("Leepy> ")
    result, error = interpreter.run('<stdin>', text)

    if error: print(error.asString())
    else: print(result)

