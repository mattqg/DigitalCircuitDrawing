# todo: write object -> has all variables (name, etc.) except for list of variables
# write module object that has name, position, input, output, etc
# have model detect handwriting to pick object type then connect them to each other


import json

def unstringify(file_name):
    with open(file_name) as f:
        variables = json.load(f)
        f.close()

    total_data = json.loads(variables['data'])[0]

    for obj in total_data:
        name = obj[0]
        data = obj[1]

    return variables, total_data


def stringify(output_name, st):
    with open(output_name, 'w') as f:
        f.write(json.dumps(st))
        f.close()


v, d = unstringify('test5.board')
stringify('test5.board', v)
