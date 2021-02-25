import re
import operator

PRIORITY = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "(": 3,
    ")": 0
}

OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

def solve(input_string):
    results = []
    if not input_string:
        return None
    for char in input_string:
        try:
            results.append(float(char))
        except:
            try:
                last = float(results.pop())
                results.append(OPERATIONS[char](float(results.pop()), last))
            except:
                print("Invalid input, or devided by zero")
    return results[-1] if results else None


def parser(input_string):
    calculations, results = [], []
    filtered = input_string.replace(" ", "")
    spaced = re.sub(r'([\+\-\*\/\(\)])', r' \1 ', filtered)
    for i in spaced.split():
        try:
            float(i)
            results.append(i)
        except:
            while calculations:
                last = calculations[-1]
                if (PRIORITY[i] <= PRIORITY[last]) or (PRIORITY[i] < PRIORITY[last]):
                    if i != ")":
                        if last != "(":
                            results.append(calculations.pop())
                        else:
                            break
                    else:
                        if last != "(":
                            results.append(calculations.pop())
                        else:
                            calculations.pop()
                            break
                else:
                    break
            if i != ")":
                calculations.append(i)
    while calculations:
        results.append(calculations.pop())
    if results:
        return results
    return None


if __name__ == '__main__':
    string = input("Input your term here: ")
    parsed = parser(string)
    print(parsed)
    print("Answer is: {}".format(solve(parsed)))