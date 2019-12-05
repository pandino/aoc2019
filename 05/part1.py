#!/bin/env python
input_code = '3,225,1,225,6,6,1100,1,238,225,104,0,1101,11,91,225,1002,121,77,224,101,-6314,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1102,74,62,225,1102,82,7,224,1001,224,-574,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,28,67,225,1102,42,15,225,2,196,96,224,101,-4446,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,86,57,225,1,148,69,224,1001,224,-77,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,82,83,225,101,87,14,224,1001,224,-178,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,38,35,225,102,31,65,224,1001,224,-868,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,57,27,224,1001,224,-84,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1101,61,78,225,1001,40,27,224,101,-89,224,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1006,224,329,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,344,101,1,223,223,1107,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,374,101,1,223,223,7,677,677,224,102,2,223,223,1005,224,389,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,404,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,419,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,434,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,464,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,479,101,1,223,223,1007,226,677,224,1002,223,2,223,1006,224,494,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,524,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,539,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,554,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,569,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,599,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,614,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,629,101,1,223,223,108,226,677,224,102,2,223,223,1005,224,644,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,659,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226'

#input_code = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'

def get_opcode(instruction):
    return int(str(instruction)[-2:])

def get_modes(instruction, num_of_params):
    template = '{:0>' + str(num_of_params + 2) + '}'
    normalized = template.format(str(instruction))[-3:(-4 - num_of_params):-1]
    return [int(mode) for mode in normalized]

def get_parameters(code, instruct_pointer, modes):
    '''Retrieve the parameters, resolving the indirections based on the modes'''
    params = list()
    for i, mode in enumerate(modes, start=1):
        ref = code[instruct_pointer+i]
        if mode == 0:
            params.append(code[ref])
        else:
            params.append(ref)
    return params

def run():

    code = [int(i) for i in input_code.split(',')]

    instruct_pointer = 0
    cycle = 0

    while True:
        cycle += 1
        instruction = code[instruct_pointer]
        opcode = get_opcode(instruction)
        skip = 1
        if opcode == 99:
            break        
        if opcode == 1:
            modes = get_modes(instruction, 2)
            result = sum(get_parameters(code, instruct_pointer, modes))
            dest = code[instruct_pointer + 3]
            code[dest] = result
            skip = 4
        elif opcode == 2:
            modes = get_modes(instruction, 2)
            params = get_parameters(code, instruct_pointer, modes)
            product = 1
            for param in params:
                product *= param
            dest = code[instruct_pointer + 3]
            code[dest] = product
            skip = 4
        elif opcode == 3:
            i = int(input('Input a number: '))
            dest = code[instruct_pointer + 1]
            code[dest] = i
            skip = 2
        elif opcode == 4:
            modes = get_modes(instruction, 1)
            output = get_parameters(code, instruct_pointer, modes)[0]
            print(output)
            skip = 2
        elif opcode == 5:
            modes = get_modes(instruction, 2)
            test, dest = get_parameters(code, instruct_pointer, modes)[0:2]
            if test == 0:
                skip = 3
            else:
                skip = 0
                instruct_pointer = dest
        elif opcode == 6:
            modes = get_modes(instruction, 2)
            test, dest = get_parameters(code, instruct_pointer, modes)[0:2]
            if test == 0:
                skip = 0
                instruct_pointer = dest
            else:
                skip = 3
        elif opcode == 7:
            modes = get_modes(instruction, 2)
            a, b = get_parameters(code, instruct_pointer, modes)[0:2]
            dest = code[instruct_pointer + 3]
            if a < b:
                code[dest] = 1
            else:
                code[dest] = 0
            skip = 4
        elif opcode == 8:
            modes = get_modes(instruction, 2)
            a, b = get_parameters(code, instruct_pointer, modes)[0:2]
            dest = code[instruct_pointer + 3]
            if a == b:
                code[dest] = 1
            else:
                code[dest] = 0
            skip = 4
        else:
            print(f'Error. Unable to process op ({opcode}) at [{instruct_pointer}]')
        instruct_pointer += skip

run()