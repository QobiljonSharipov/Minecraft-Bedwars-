from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()



app = Ursina()
player = FirstPersonController()

Sky()
boxes = []
game_over = False
player_lives = 3  
jon = Text(text=player_lives, scale=2, color=color.red, position=(-0.8, -0.4), enabled=True)
win_text = Text(text='', scale=3, color=color.blue, position=(-0.3, 0.4), enabled=False)

zones = {'yellow': [], 'blue': []}
boundary_width = 50
boundary_height = 20
gap_width = 20

for i in range(boundary_height):
    if i == 10:
        red = Button(model='cube', position=(4, 1, 10), texture='live.png', parent=scene, origin_y=0.5, collider='box')
        boxes.append(red)
        blues = Button(model='cube', position=(45, 1, 10), texture='live.png', parent=scene, origin_y=0.5, collider='box')
        boxes.append(blues)
    else:
        for j in range(boundary_width):
            if (boundary_width // 2 - gap_width // 2) <= j < (boundary_width // 2 + gap_width // 2):
                continue
            elif 1 <= i < boundary_height - 1 and 1 <= j < boundary_width - 1:
                if j < boundary_width // 2:
                    box = Button(color=color.yellow, model='cube', position=(j, 0, i), texture='grass.png', parent=scene, origin_y=0.5)
                    zones['yellow'].append(box)
                else:
                    box = Button(color=color.blue, model='cube', position=(j, 0, i), texture='grass.png', parent=scene, origin_y=0.5)
                    zones['blue'].append(box)
                boxes.append(box)
            else:
                if i == 0 or i == boundary_height - 1 or j == 0 or j == boundary_width - 1:
                    border_box = Button(color=color.gray, model='cube', position=(j, 1, i), texture='stone.png', parent=scene, origin_y=0.5, collider='box')
                else:
                    border_box = Button(color=color.gray, model='cube', position=(j, 0, i), texture='stone.png', parent=scene, origin_y=0.5, collider='box')
                boxes.append(border_box)

block_types = ['sakura1.png', 'glass.png', 'grass.png']
current_block = 0

def input(key):
    global current_block, player_lives, game_over

    if game_over:  
        return

    if key == 'scroll down':
        current_block = (current_block + 1) % len(block_types)
    if key == 'scroll up':
        current_block = (current_block - 1) % len(block_types)
    if key == 'left mouse down':
        for box in boxes:
            if box.hovered:
                new = Button(color=color.white, model='cube', position=box.position + mouse.normal, texture=block_types[current_block], parent=scene, origin_y=0.5)
                boxes.append(new)
    if key == 'right mouse down':
        for box in boxes:
            if box.hovered:
                boxes.remove(box)
                destroy(box)
            elif blues.hovered:
                win_text.text = "Red team winner"
                win_text.enabled = True
            elif red.hovered:
                win_text.text = "Blue team winner"
                win_text.enabled = True

def update():
    global player_lives, game_over

    if player.y < -10:  
        player_lives -= 1  
        jon.text = str(player_lives)
        if player_lives > 0:
            player.position = Vec3(0, 10, 0)  
        else:
            player.position = Vec3(0, 10, 0)  
            game_over = True 
            win_text.text = "Game Over! Siz kuzatuvchi rejimdasiz."
            win_text.enabled = True

    if game_over:
        player.speed = 0  

app.run()
