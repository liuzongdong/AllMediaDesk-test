import re
import operator
from flask import Flask, abort, request, render_template
from werkzeug.utils import secure_filename
import json

OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

PRIORITY = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "(": 3,
    ")": 0
}

def solve(input_string):
    results = []
    if not input_string:
        return None
    for char in input_string:
        try:
            results.append(float(char))
        # Use try-catch block to handle the operations, cause we cannot float a operation
        except:
            last = float(results.pop())
            try:
                results.append(OPERATIONS[char](float(results.pop()), last))
            except:
                print("Divided by Zero is not allowed")
    return results[-1] if results else None

# Postfix
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


def get_results(string):
    filtered = string.replace(" ", "")
    spaced = re.sub(r'([\+\-\*\/\(\)])', r' \1 ', filtered)
    # print (spaced.replace("x", "1"))
    X = []
    Y = []
    result = []
    for i in range(-100, 100, 1):
        X.append(i)
        if i < 0:
            i = "(" + "0 - " + str(i).replace("-", "") + ")"
        parsed = parser(spaced.replace("x", str(i)))
        # print("Answer is: {}".format(solve(parsed)))
        if solve(parsed) != None:
            Y.append(solve(parsed))
        else:
            Y.append(None)
    # print(X)
    
    return [{'x': x, 'y': y} for x, y in zip(X, Y)]


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/plot', methods = ['POST'])
def plot():
    content = request.get_json(force=True)
    data = json.dumps(get_results(content['term']), ensure_ascii = False)
    print (data)
    return data



if __name__ =='__main__':
    app.run(host = "0.0.0.0", port = 5000, threaded = True, debug = True)