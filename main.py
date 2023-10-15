import json
import os
from termcolor import colored, cprint

rotation_lists = []

last_advanced_rotation_index = -1
class Rotation:
    name = ''
    priority = 1
    
    # In minutes
    time_spent = 0

    def __init__(self, name, priority = 1, time_spent = 0):
        self.name = name
        self.priority = priority
        self.time_spent = time_spent

    def to_obj(self):
        return {'name': self.name, 'priority': self.priority, 'time_spent': self.time_spent}
    
    def set_priority(self, priority):
        self.priority = priority

    def inc(self, time_spent = 30):
        self.num_inc = self.num_inc + time_spent


class RotationsList:
    name = ''
    rotations = []
    current_index = 0

    def __init__(self, name, rotations):
        self.name = name
        self.rotations = rotations

    def next(self):
        print('Next...')

        if self.current_index + 1 == len(self.rotations):
            self.current_index = 0
        else:
            self.current_index = self.current_index + 1

    def set_index(self, index):
        self.current_index = index

    def get(self):
        return self.rotations[self.current_index]

    def to_obj(self):
        return {'name': self.name,
                'rotations': [r.to_obj() for r in self.rotations],
                'current_index': self.current_index}


def add_new_rotation_form():
    rl_name = input('Rotation list name: ')
    rots = []
    rot_name = ''

    i = 1
    while True:
        rot_name = input(f'#{i} rotation item name (q to exit): ')
        if rot_name == 'q':
            break
        rots.append(Rotation(rot_name))

        i = i + 1

    rotation_lists.append(RotationsList(rl_name, rots))


def print_rotation_lists():
    i = 0
    for rl in rotation_lists:
        print(colored(f'#{i + 1}: {rl.name}', attrs=["reverse"]))

        j = 0
        for rot in rl.rotations:
            text = f'    {j + 1}. {rot.name}'
            
            if (j == rl.current_index):
              print(colored(f'{text} (*)', "yellow"), end='')
            else:
                print(f'{text}', end='')
            print()
            j = j + 1

        print()
        i = i + 1


def advance_rotation(rotation_index = -1):
    # index = input('Enter rotation number: ')
    global last_advanced_rotation_index
    if rotation_index == -1:
      index = last_advanced_rotation_index
    else:
      index = rotation_index - 1
      last_advanced_rotation_index = index
    if index < 0 or index >= len(rotation_lists):
        pass

    rotation_lists[index].next()

    rl = rotation_lists[index]
    print(colored(f'{rl.name}', attrs=["reverse"]))

    j = 0
    for rot in rl.rotations:
        text = f'    {j + 1}. {rot.name}'
        
        if (j == rl.current_index):
          print(colored(f'{text} (*)', "yellow"), end='')
        else:
            print(f'{text}', end='')
        print()
        j = j + 1

    print()

def delete_rotation(rotation_index):
    rotation = rotation_lists[rotation_index - 1]
    print(f'Deleted rotation "{rotation.name}"\n')
    rotation_lists.pop(rotation_index - 1)

# Write logic to load json file
config_file = open('./lists.json')

data = json.load(config_file)

for rl in data:
    deserialized_rots = [Rotation(x['name'], x['priority'], x['time_spent']) for x in rl['rotations']]
    new_item = RotationsList(rl['name'], deserialized_rots)
    new_item.set_index(rl['current_index'])
    rotation_lists.append(new_item)

while True:
    print('Select an option:')
    print('a) Add a new rotation')
    print('v) View rotations')
    print('q) Quit the app')
    print('n) Advance a rotation')
    print('d) Delete a rotation')

    option_raw = input('\nEnter your option: ')

    option = option_raw[0]
    if option == 'a':
        add_new_rotation_form()
    if option == 'v':
        print_rotation_lists()
    if option == 'n':
        rotation_index = None
        if option_raw[1:] == '':
          rotation_index = -1
        else:
          rotation_index = int(option_raw[1:])
        advance_rotation(rotation_index)
        pass
    if option == 'q':
        f = open('lists.json', 'w')
        f.write(json.dumps([rl.to_obj() for rl in rotation_lists]))
        print('\nGoodbye!')
        break
    if option == 'd':
        delete_rotation(int(option_raw[1:]))
