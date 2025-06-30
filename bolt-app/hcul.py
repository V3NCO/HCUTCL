import re

class InputFieldCountException(Exception):
    pass

class NoInputFieldException(Exception):
    pass

def hcul(input):
    memory = [0] * 30*1000
    pointer = 0
    output = ""
    index = 0
    result = input
    has_input = False
    i = 0
    if input.count(":uuh:") > 1 or input.count(':noooovanish:') > 1:
        raise InputFieldCountException
    elif not input.count(":uuh:") == input.count(':noooovanish:'):
        raise InputFieldCountException
    elif input.count(":uuh:") == 0 or input.count(':noooovanish:'):
        pass
    else:
        input_field = re.search(r'(:uuh:.*?:noooovanish:)', input).group(1)
        result = input.replace(input_field, "")
        input_clean = input_field.replace(':uuh:', '').replace(':noooovanish:', '')
        has_input = True
    instructions = re.findall(r':[^:]+:', result)
    while i < len(instructions):
        match instructions[i]:
            case ":upvote:": pointer += 1
            case ":downvote:": pointer -= 1
            case ":yay:": memory[pointer] += 1
            case ":heavysob:": memory[pointer] -= 1
            case ":pf:": output += chr(memory[pointer])
            case ":sadge:": output += str(memory[pointer])
            case ":3c:":
                if has_input:
                    memory[pointer] = ord(input_clean[index])
                    index += 1
                else:
                    raise NoInputFieldException
            case ":dino-drake-yea:":
                if memory[pointer] == 0:
                    count = 1
                    while count > 0:
                        i += 1
                        if instructions[i] == ":dino-drake-yea:":
                            count += 1
                        elif instructions[i] == ":dino-drake-nah:":
                            count -= 1
            case ":dino-drake-nah:":
                if memory[pointer] != 0:
                    count = 1
                    while count > 0:
                        i -= 1
                        if instructions[i] == ":dino-drake-nah:":
                            count += 1
                        elif instructions[i] == ":dino-drake-yea:":
                            count -= 1
            case _:
                pass
        i += 1
    return output
