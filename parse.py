# todo: write object -> has all variables (name, etc.) except for list of variables
# write module object that has name, position, input, output, etc

import json

def unstringify(file_name):
    with open(file_name) as f:
        variables = json.load(f)
        f.close()

    total_data = json.loads(variables['data'])[0]

    for obj in total_data:
        name = obj[0]
        data = obj[1]
    
    return variables


def stringify(output_name, st):
    with open(output_name, 'w') as f:
        f.write(json.dumps(st))
        f.close()

v = unstringify('extras/test6.board')
print(v)

# v = dict (name, zoom, var ,etc)
# d = list [button1, button2] -> for button1 list['button', dict] -> dict pos, width, output, etc
stringify('test6.board', v)

class Board:
    def __init__(self, name):
        self.name = name
        self.offset = {"x": 0, "y": 0}
        self.zoom = 100
        self.variables = {}
        self.variableReferences = {}
        self.data = []

    def add_button(self, button):
        self.data.append(button)

    def stringify(self, output):
        output_dict = {'name': self.name, 'offset': self.offset, 'zoom': self.zoom, 'variables': self.variables,
         'variableReferences': self.variableReferences}
        
        formatted_data = [button.format() for button in self.data]
        output_dict['data'] = json.dumps([formatted_data, []], separators=(',', ':'))

        with open(f'saves/{output}.board', 'w') as f:
            f.write(json.dumps(output_dict, separators=(',', ':')))


class Button:
    def __init__(self, type, id, name, x, y, width, height, rotation, properties={}, input=[], output=[]):
        self.type = type
        self.id = id
        self.name = name
        self.pos = {'x': x, 'y':y}
        self.width = width
        self.height = height
        self.rotation = rotation
        self.properties = properties
        self.input = input
        self.output = output

    def add_input(self, input_button):
        add_dict = {}
        add_dict['id'] = input_button.id
        add_dict['pos'] = input_button.pos
        add_dict['value'] = input_button.value
        self.input.append(add_dict)

    def add_output(self, output_button):
        add_dict = {}
        add_dict['id'] = output_button.id
        add_dict['pos'] = output_button.pos
        add_dict['value'] = self.value
        self.output.append(add_dict)

    def format(self):
        # list['button', dict] -> dict pos, width, output, etc
        info_dict = {'id': self.id, 'name': self.name, 'pos': self.pos, 'width': self.width, 'height': self.height, 'rotation': self.rotation, 'properties': self.properties, 'input': self.input, 'output': self.output}
        return [self.type, (info_dict)]

# num_buttons = 2
# board = Board('test1')
# board.add_button(Button("Input", 0, "Input#0", (5, -2), 2, 1, 0, {}, [], [{"id": 1, "pos": {"side": 1, "pos": 0}, "value": 0}]))
# print(board.data[0].output)



    
