import hindian

while True:
    text = input("Leepy> ")
    result, error = hindian.run('<stdin>', text)

    if error: print(error.asString())
    else: print(result)

