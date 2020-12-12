import sys
import re

with open('input.txt') as f:
    lines = f.readlines()  # Read whole file

# For using test input instead of file input rename from lines_example to lines
lines_example = '''
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''[1:-1].split('\n')

program = []
for line in lines:
    line = line.rstrip('/n')
    (code, s, offset) = line.partition(" ")
    offset = int(offset)
    # print (code, offset)
    program.append([code, offset])


def call(program):
    acc = 0
    pos = 0
    positions = set()
    while True:
        if pos in positions:
            return 'loop', acc
        if pos == len(program):
            return 'terminated', acc
        positions.add(pos)
        (code, offset) = program[pos]
        # print(code, offset)
        if code == 'nop':
            pos += 1
        elif code == 'acc':
            acc += offset
            pos += 1
        elif code == 'jmp':
            pos += offset
        else:
            print('Unknown command')
        # print('>', pos, acc)


(status, acc) = call(program)
print('Acc at loop detection:', acc)
# 1939

changes = []
for line in range(0, len(program)):
    (code, offset) = program[line]
    if code == 'jmp':
        program[line] = ('nop', offset)
    elif code == 'nop':
        program[line] = ('jmp', offset)
    else:
        continue
    (r, acc) = call(program)
    if r == 'terminated':
        print('Acc at end of corrected program: ', acc)
        break
    program[line] = (code, offset)
# 2212
