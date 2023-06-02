import numpy as np
import sympy as sp
import time


resource_value = float(6)
accuracy = float(1)
functions = ['-x**2 + 6*x', ' -1.5*x**2 + 7*x', '-0.5*x**2 + 8*x']
constrains_matrix = [[0, 2], [0, 2], [3, 5]]


for index, constrain in enumerate(constrains_matrix):
    if constrain[0] > resource_value:
        print(
            f'! min resource value for the constrain number {index} is larger than all available resource. !')
        exit(0)


x = sp.Symbol('x')
parsed_functions = []

for i in range(len(functions)):
    raw_expression = functions[i]
    parsed = sp.sympify(raw_expression)
    parsed_functions.append(parsed)

functions = parsed_functions


list_of_decisions = []
for constrains in constrains_matrix:
    r_list = []
    current = constrains[0]

    while current <= constrains[1]:
        r_list.append(current)
        current += accuracy

    list_of_decisions.append(r_list)


def calculate_var_function(var_number, value):
    return functions[var_number].subs(x, value)


counter = 0
r = 0


def calc(initialValue):
    global r, counter
    results = []
    for decision in list_of_decisions[r]:
        counter += 1
        if initialValue - decision < 0:
            continue
        value = calculate_var_function(r, decision)
        if r < len(list_of_decisions) - 1:
            r += 1
            result = calc(initialValue - decision)
            all_decision_until_here = [decision]
            for i in range(len(result[0])):
                all_decision_until_here.append(result[0][i])

            total = value + result[1]
            results.append((all_decision_until_here, total))
        else:
            results.append(([decision], value))
    r -= 1
    if len(results) == 0:
        return ([decision], 0)

    max_index = 0
    max_value = 0

    for i in range(len(results)):
        if results[i][1] > max_value:
            max_index = i
            max_value = results[i][1]

    return results[max_index]


start_timer = time.time()
result = calc(resource_value)
end_timer = time.time()

print('the result of problem is : ', result[0])
print('total profit is: ', result[1])
print('all available resource was :', resource_value,
      'and total used resource is:', sum(result[0]))
print('all decisions count was : ', counter)
print('spend time to solve this problem was : ', end_timer - start_timer)
