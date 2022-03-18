import compiler

while True:
    text = input("Leepy> ")
    result, error = compiler.run('<stdin>', text)

    if error: print(error.asString())
    else: print(result)

