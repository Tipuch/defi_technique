# -*- coding: utf-8 -*-
import itertools
import sys

OPERATIONS = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}


def main():
    input_str = sys.argv[1]
    # get the input from command line and format it properly
    numbers_arg = input_str[0: input_str.find('=')].strip().split(' ')
    numbers_arg = list(map(int, numbers_arg))
    goal_arg = input_str[input_str.find('=') + 1:].strip()
    goal_arg = int(goal_arg)
    # start recursive solver
    solve(numbers_arg, goal_arg, '')


def solve(numbers, goal, operation):
    # check if last solution is the right one
    if len(numbers) == 1 and numbers[0] == goal:
        # print result and stop the program (otherwise comment 'raise SystemExit' out to have all solutions)
        print('{0} = {1}'.format(operation, str(goal)))
        raise SystemExit

    # loop through every unique couple of numbers and do every possible operation
    for x, y in get_unique_couples(numbers):
        temp_result = do_op(x, '+', y)
        solve(copy_and_replace_two_for_one(x, y, temp_result, numbers), goal,
              get_new_operation(x, '+', y, operation))

        # check for operators '-' and '/' that the operation is legal
        temp_result = do_op(x, '-', y)
        if temp_result:
            solve(copy_and_replace_two_for_one(x, y, temp_result, numbers), goal,
                  get_new_operation(x, '-', y, operation))

        temp_result = do_op(y, '-', x)
        if temp_result:
            solve(copy_and_replace_two_for_one(x, y, temp_result, numbers), goal,
                  get_new_operation(y, '-', x, operation))

        temp_result = do_op(x, '*', y)
        solve(copy_and_replace_two_for_one(x, y, temp_result, numbers), goal,
              get_new_operation(x, '*', y, operation))

        temp_result = do_op(x, '/', y)
        if temp_result:
            solve(copy_and_replace_two_for_one(x, y, temp_result, numbers), goal,
                  get_new_operation(x, '/', y, operation))

        temp_result = do_op(y, '/', x)
        if temp_result:
            solve(copy_and_replace_two_for_one(x, y, temp_result, numbers), goal,
                  get_new_operation(y, '/', x, operation))

    return None


def do_op(x, op, y):
    # check if the operation is invalid and if not make the operation
    if op == '-' and get_invalid_op(x, op, y):
        return None
    if op == '/' and get_invalid_op(x, op, y):
        return None
    return OPERATIONS[op](x, y)


def get_invalid_op(x, op, y):
    # return operation if it is illegal otherwise return None
    if op == '/' and y == 0:
        return x, op, y
    if x < y and op == '-':
        return x, op, y
    if op == '/' and not isinstance(OPERATIONS[op](x, y), int):
        return x, op, y
    return None


def get_unique_couples(numbers):
    return [couple for couple in itertools.combinations(numbers, 2)]


def copy_and_replace_two_for_one(x, y, result, numbers):
    # replace the couple used by its result in subsequent recursive calls
    new_numbers = numbers[:]
    # copy numbers to be able to use it in the next operations in the solve method
    new_numbers.remove(x)
    new_numbers.remove(y)
    new_numbers.insert(0, result)
    return new_numbers


def get_new_operation(x, op, y, current_operation):
        return '{0} ( {1} {2} {3} )'.format(current_operation, x, op, y)


if __name__ == "__main__":
    main()
