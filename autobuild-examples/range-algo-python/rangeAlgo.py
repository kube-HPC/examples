def start(args):
    print('algorithm: range start')
    input = args['input'][0]
    array = list(range(1, input + 1))
    print("Array is: ", array)
    return array