# GavinWare Version 1

# NOTE: Ignore the "requests" is not defined warning, it is defined on line 19 or line 41 when it is automatically installed with your permission.

import sys, random, json, os, importlib
os.chdir(os.path.dirname(os.path.realpath(__file__)))

needed_modules = ['requests', 'numpy', 'pygame-ce']

for module in needed_modules:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    try:
        if module == 'pygame-ce':
            # Imports pygame
            pygame = importlib.import_module(module[:6])
        else:
            globals()[module] = importlib.import_module(module)
    except ImportError:
        print(f'The following module has to be installed:\n"{module}"')
        while True:
            try:
                install_module = input("Do you want it installed? (y/n): ").lower()
                if install_module in ("y", "n"):
                    break
                else:
                    raise ValueError('You must type "y" or "n".')
            except ValueError as v:
                print(v)
        if 'y' in install_module:
            try:
                return_code = os.system(f'pip install {module}' if os.name == 'nt' else f'pip3 install {module}')
                if return_code != 0:
                    raise ImportError('Unable to install module: {module}')
                else:
                    if module == 'pygame-ce':
                        # Imports pygame
                        pygame = importlib.import_module(module[:6])
                    else:
                        globals()[module] = importlib.import_module(module)
            except ImportError as i:
                print(i)
        else:
            print("Exiting program...")
            sys.exit()

from pathlib import Path
from buttons import Button
from spritesheet import SpriteSheet
from mouse import Mouse
from interactive_items import Interactive_Item

pygame.init()
dev_mode = False

screen_width = int(pygame.display.Info().current_w // 2)
screen_height = int(pygame.display.Info().current_h * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("GavinWare")
pygame.display.set_icon(pygame.image.load("gavinware_icon.png").convert_alpha())

clock = pygame.time.Clock()
item_scale = round(screen_width / 350)
button_scale = round(screen_width / 400)
small_button_scale = round(screen_width / 500)
font_size = round(screen_width / 26)
big_font_size = round(screen_width / 5)
big_font = pygame.font.Font("FFFFORWA.ttf", font_size)
font = pygame.font.Font("FFFFORWA.ttf", font_size)
small_font = pygame.font.Font("FFFFORWA.ttf", 15)
medium_font = pygame.font.Font("FFFFORWA.ttf", round(screen_width / 50))
running = True
game_state = "main_menu"
main_menu_buttons = []
main_menu_button_index = 0
pause_menu_buttons = []
pause_menu_button_index = 0
fade_alpha = 255
fade_direction = 1
FPS = 60
gavinware_music = pygame.mixer.music
current_music = "gavinware_menu.mp3"
gavinware_music.load(current_music)
gavinware_music.play(-1)

# Button mappings
red_button = pygame.K_w # Red Button
pause_button = pygame.K_d # Blue Button
white_button = pygame.K_s # White Button
yellow_button = pygame.K_a # Yellow Button
left_move = pygame.K_LEFT
right_move = pygame.K_RIGHT
up_move = pygame.K_UP
down_move = pygame.K_DOWN

# Gameplay variables
game_score = 0
game_lives = 5
microgame_failed = False
microgame_set = False
microgame_conf_set = False
current_microgame = None
boss_mode = False
boss_finished = False
microgames_played = 0

filter_button_pressed = False
paused = False
pause_start = 0
total_paused = 0
arrow_direction = 1
arrow_x = 0.0
arrow_y = 0.0
up_times = 0
down_times = 0
soda_shake = False
kuvira_play = False
peasant_1_play = False
peasant_2_play = False
peasant_3_play = False
kuvira_hp = 200
earthshield_hp = 15
katara_hp = 200
katara_stamina = 70
azula_hp = 200
azula_stamina = 100
azula_jumping = False
azula_falling = False
azula_freeze = False
azula_lightning = False
azula_velocity_Y = 0
fireshield_on = False
fireshield_cooldown = False
fireball_cooldown = False
ice_shard_cooldown = False
waterfall_cooldown = False
waterheal_cooldown = False
waterheal_on = False
freeze_heal_cooldown = False
waterfall_on = False
earthshield_on = False
kuvira_attack_time = pygame.time.get_ticks() - total_paused
azula_attack_time = pygame.time.get_ticks() - total_paused
azula_lightning_time = pygame.time.get_ticks() - total_paused
dialog_time = pygame.time.get_ticks() - total_paused
shear_stun = False

# Save variables
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_index_1 = 0
letter_index_2 = 0
letter_index_3 = 0
letter_1 = letters[letter_index_1]
letter_2 = letters[letter_index_2]
letter_3 = letters[letter_index_3]
single_letter_index = 0
score_name = letter_1 + letter_2 + letter_3
scoreboard_path = Path("scoreboard.json")
try:
    DATABASE_PATH = "https://scoreboard-cde81-default-rtdb.firebaseio.com/.json"
    scoreboard_request = requests.get(DATABASE_PATH)
    scoreboard_request.raise_for_status()
    firebase_data = scoreboard_request.json()
    with open(scoreboard_path, 'w') as sp:
        json.dump(firebase_data, sp, indent=4)
except requests.exceptions.HTTPError as err:
    print(f"Error fetching data from Firebase: HTTP error occurred: {err}")
    print(f"Response status code: {scoreboard_request.status_code}")
    print(f"Response content: {scoreboard_request.text}")
except requests.exceptions.RequestException as err:
    print(f"Error fetching data from Firebase: An unexpected request error occurred: {err}")
    print("Please check your internet connection or the DATABASE_URL.")

play_button = Button("Play_Button.png", "Selected_Play_Button.png", main_menu_buttons, main_menu_button_index, button_scale)
exit_button = Button("Leave_Button.png", "Leave_Button_Selected.png", main_menu_buttons, main_menu_button_index, button_scale)

play_pause_button = Button("Play_Button.png", "Selected_Play_Button.png", pause_menu_buttons, pause_menu_button_index, button_scale)
exit_pause_button = Button("Leave_Button.png", "Leave_Button_Selected.png", pause_menu_buttons, pause_menu_button_index, button_scale)

gavin_boombox_animation = SpriteSheet("gavinWare_boombox.png", (75, 80), (7, 7), scale=item_scale)
mouse = Mouse("Select_Mouse.png", "Select_Mouse_Ring.png", screen=(screen_width, screen_height), speed=12, scale=2)
mouse_display = pygame.sprite.Group()
mouse_display.add(mouse)

# Interaction for interactive object item
def filter_button(color):
    global current_filter, filter_button_pressed

    if not filter_button_pressed:
        match color:
            case "red":
                current_filter = "red"
            case "green":
                current_filter = "green"
            case "blue":
                current_filter = "blue"
            case "inverted":
                current_filter = "inverted"
        
    filter_button_pressed = True

red_microgame_button = Interactive_Item("button_images/red_button.png", filter_button, scale=small_button_scale)
green_button = Interactive_Item("button_images/green_button.png", filter_button, scale=small_button_scale)
blue_button = Interactive_Item("button_images/blue_button.png", filter_button, scale=small_button_scale)
inverted_button = Interactive_Item("button_images/invert_button.png", filter_button, scale=small_button_scale)

change_image_buttons = [red_microgame_button, green_button, blue_button, inverted_button]
change_image_button_sprites = pygame.sprite.Group()
change_image_button_sprites.add(red_microgame_button, green_button, blue_button, inverted_button)

# Microgames
def change_image(wait_time=9000):
    global game_state, game_score, microgame_failed, filter_button_pressed, microgame_conf_set, filters, goal_filter, current_filter, game_time, pause_time, game_lives, current_microgame, change_image_buttons, display_image, microgames_played
    if game_state == "microgame":
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks() - total_paused
        elapsed_time = current_time - game_time
        time_left = (wait_time - elapsed_time) // 1000
        if time_left < 0:
            time_left = 0
        
        if not microgame_conf_set:
            mouse.rect.x = round(screen_width / 2) - round(mouse.image.get_width() / 2)
            mouse.rect.y = round(screen_height / 2) - round(mouse.image.get_height() / 2)
            filters = ["red", "green", "blue", "inverted"]
            goal_filter = random.choice(filters)
            filters.remove(goal_filter)
            filters.append("standard")
            current_filter = random.choice(filters)
            microgame_conf_set = True
            random.shuffle(change_image_buttons)
            for position, button in enumerate(change_image_buttons):
                button.rect.centerx = round(screen_width * (position+1)/5)
        
        if filter_button_pressed and time_left > 3:
            game_time = pygame.time.get_ticks() - total_paused - (wait_time - 3000)

        if current_time - game_time >= wait_time and not paused:
            if current_filter == goal_filter:
                microgame_failed = False
                game_score += 1
            else:
                game_lives -= 1
                microgame_failed = True
            current_microgame = None
            game_time = pygame.time.get_ticks() - total_paused
            try:
                pause_time = 0
            except:
                pass
            microgames_played += 1
            game_state = "intermission"

        match current_filter:
            case "standard":
                display_image = pygame.image.load("leopard_images/leopard_standard.jpg").convert_alpha()
            case "red":
                display_image = pygame.image.load("leopard_images/leopard_red.jpg").convert_alpha()
            case "green":
                display_image = pygame.image.load("leopard_images/leopard_green.jpg").convert_alpha()
            case "blue":
                display_image = pygame.image.load("leopard_images/leopard_blue.jpg").convert_alpha()
            case "inverted":
                display_image = pygame.image.load("leopard_images/leopard_inverted.jpg").convert_alpha()

        screen.blit(display_image, (round(screen_width/2) - round(display_image.get_width()/2), round(screen_height/2) - round(display_image.get_width()/2)))
        red_microgame_button.rect.y = screen_height - red_microgame_button.image.get_height() - 125
        green_button.rect.y = screen_height - green_button.image.get_height() - 125
        blue_button.rect.y = screen_height - blue_button.image.get_height() - 125
        inverted_button.rect.y = screen_height - inverted_button.image.get_height() - 125
        change_image_button_sprites.draw(screen)
        mouse_display.draw(screen)
        action_label = medium_font.render(f"Change Filter To {goal_filter.capitalize()}!", False, (255, 255, 255))
        if not filter_button_pressed and time_left > 3:
            time_left_label = font.render(str(time_left), False, (255, 255, 0))
            screen.blit(time_left_label, (screen_width - time_left_label.get_width(), 0))
        else:
            time_left_label = big_font.render(str(time_left), False, (255, 0, 0))
            screen.blit(time_left_label, (round(screen_width/2) - round(time_left_label.get_width()/2), round(screen_height/2) - round(time_left_label.get_height()/2)))
        screen.blit(action_label, (0, round(time_left_label.get_height()/2) - round(action_label.get_height()/2)))

def fire_out(wait_time=8000):
    global random_fire, game_state, game_score, game_time, game_lives, microgame_conf_set, fire_stamina, original_fire_stamina, fire_color, fire_image, fire_text, current_microgame, microgame_failed, pause_time, microgames_played
    if game_state == "microgame":
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks() - total_paused
        elapsed_time = current_time - game_time
        time_left = (wait_time - elapsed_time) // 1000
        if time_left < 0:
            time_left = 0
        
        if not microgame_conf_set:
            random_fire = random.choice((True, False))
            fire_stamina = random.randint(1, 6)
            original_fire_stamina = fire_stamina
            fire_color = random.choice(("RED", "YELLOW", "WHITE"))
            microgame_conf_set = True
        elif fire_stamina < 0:
            fire_stamina = 0
        
        if fire_stamina <= 0 and time_left > 3:
            game_time = pygame.time.get_ticks() - total_paused - (wait_time - 3000)

        if fire_stamina != original_fire_stamina and random_fire:
            fire_color = random.choice(("RED", "YELLOW", "WHITE"))
            original_fire_stamina = fire_stamina
        
        if current_time - game_time >= wait_time and not paused:
            if fire_stamina <= 0:
                microgame_failed = False
                game_score += 1
            else:
                game_lives -= 1
                microgame_failed = True
            current_microgame = None
            game_time = pygame.time.get_ticks() - total_paused
            try:
                pause_time = 0
            except:
                pass
            microgames_played += 1
            game_state = "intermission"
        
        match fire_color:
            case "RED":
                fire_text = font.render("Press W!", False, (255, 0, 0))
                fire_image = pygame.image.load("flame_images/red_flame.png").convert_alpha()
            case "YELLOW":
                fire_text = font.render("Press A!", False, (255, 255, 0))
                fire_image = pygame.image.load("flame_images/yellow_flame.png").convert_alpha()
            case "WHITE":
                fire_text = font.render("Press S!", False, (255, 255, 255))
                fire_image = pygame.image.load("flame_images/white_flame.png").convert_alpha()
        
        if fire_stamina > 0:
            fire_image = pygame.transform.scale_by(fire_image, item_scale)
            fire_image_rect = fire_image.get_rect()
            fire_image_rect.centerx = screen_width // 2
            fire_image_rect.centery = screen_height // 2
            screen.blit(fire_image, fire_image_rect)
            screen.blit(fire_text, (round(screen_width / 2) - round(fire_text.get_width() / 2), round(screen_height / 2) - round(fire_image.get_height() / 2) - fire_text.get_height()))
        
        fire_stamina_rect = pygame.draw.rect(screen, (255, 0, 0), ((screen_width // 2) - ((fire_stamina * 90) // 2), screen_height - 125, fire_stamina * 100, 50))
        fire_stamina_rect.x = round(screen_width / 2) - round((fire_stamina * 90) / 2)
        
        action_label = medium_font.render(f"Extinguish Fire Using Button Color!", False, (255, 255, 255))
        if fire_stamina > 0 and time_left > 3:
            time_left_label = font.render(str(time_left), False, (255, 255, 0))
            screen.blit(time_left_label, (screen_width - time_left_label.get_width(), 0))
        else:
            time_left_label = big_font.render(str(time_left), False, (255, 0, 0))
            screen.blit(time_left_label, (round(screen_width/2) - round(time_left_label.get_width()/2), round(screen_height/2) - round(time_left_label.get_height()/2)))
        screen.blit(action_label, (0, round(time_left_label.get_height()/2) - round(action_label.get_height()/2)))

def place_arrow(wait_time=15000, arrow_speed=450):
    global game_state, game_score, game_time, game_lives, microgame_conf_set, current_microgame, microgame_failed, pause_time, arrow_placed, aang_arrow, aang_arrow_rect, arrow_x, arrow_y, arrow_direction, arrow_left_right, microgames_played
    if game_state == "microgame":
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks() - total_paused
        elapsed_time = current_time - game_time
        time_left = (wait_time - elapsed_time) // 1000
        if time_left < 0:
            time_left = 0
        
        aang_face = pygame.image.load("aang_images/aang.png").convert_alpha()
        aang_face = pygame.transform.scale_by(aang_face, item_scale)
        aang_face_rect = aang_face.get_rect()
        aang_face_rect.x = round(screen_width/2) - round(aang_face.get_width()/2)
        aang_face_rect.y = round(screen_height/2) - round(aang_face.get_height()/2)
        screen.blit(aang_face, aang_face_rect)

        if not microgame_conf_set:
            arrow_placed = False
            arrow_left_right = random.choice((True, False))
            aang_arrow = pygame.image.load("aang_images/aang_arrow.png").convert_alpha()
            aang_arrow = pygame.transform.scale_by(aang_arrow, item_scale)
            aang_arrow_rect = aang_arrow.get_rect()
            if arrow_left_right:
                arrow_x = 0.0
                aang_arrow_rect.x = 0
            else:
                arrow_x = round(screen_width/2) - round(aang_arrow.get_width()/2)
                aang_arrow_rect.x = round(screen_width/2) - round(aang_arrow.get_width()/2)
            if not arrow_left_right:
                arrow_y = 0.0
                aang_arrow_rect.y = 0
            else:
                arrow_y = round(screen_height/2) - round(aang_face.get_height()/2)
                aang_arrow_rect.y = round(screen_height/2) - round(aang_face.get_height()/2)
            arrow_direction = 1
            microgame_conf_set = True
        
        if current_time - game_time >= wait_time and not paused:
            if arrow_placed and aang_arrow_rect.colliderect(aang_face_rect):
                microgame_failed = False
                game_score += 1
            else:
                game_lives -= 1
                microgame_failed = True
            current_microgame = None
            game_time = pygame.time.get_ticks() - total_paused
            try:
                pause_time = 0
            except:
                pass
            microgames_played += 1
            game_state = "intermission"
        
        if not arrow_placed:
            try:
                if arrow_left_right:
                    arrow_x += arrow_direction * arrow_speed * dt
                    aang_arrow_rect.x = round(arrow_x)

                    if aang_arrow_rect.right >= screen_width:
                        aang_arrow_rect.right = screen_width
                        arrow_x = aang_arrow_rect.x
                        arrow_direction = -1

                    if aang_arrow_rect.left <= 0:
                        aang_arrow_rect.left = 0
                        arrow_x = aang_arrow_rect.x
                        arrow_direction = 1
                else:
                    arrow_y += arrow_direction * arrow_speed * dt
                    aang_arrow_rect.y = round(arrow_y)

                    if aang_arrow_rect.top <= 0:
                        aang_arrow_rect.top = 0
                        arrow_y = aang_arrow_rect.y
                        arrow_direction = 1
                    
                    if aang_arrow_rect.bottom >= screen_height:
                        aang_arrow_rect.bottom = screen_height
                        arrow_y = aang_arrow_rect.y
                        arrow_direction = -1

            except Exception as e:
                print("Error moving arrow:", e)
        elif time_left > 3:
            game_time = pygame.time.get_ticks() - total_paused - (wait_time - 3000)

        screen.blit(aang_arrow, aang_arrow_rect)
        action_label = medium_font.render("Place Arrow on Aang!", False, (255, 255, 255))
        if not arrow_placed and time_left > 3:
            time_left_label = font.render(str(time_left), False, (255, 255, 0))
            screen.blit(time_left_label, (screen_width - time_left_label.get_width(), 0))
        else:
            time_left_label = big_font.render(str(time_left), False, (255, 0, 0))
            screen.blit(time_left_label, (round(screen_width/2) - round(time_left_label.get_width()/2), round(screen_height/2) - round(time_left_label.get_height()/2)))
        screen.blit(action_label, (0, round(time_left_label.get_height()/2) - round(action_label.get_height()/2)))

soda_can = SpriteSheet("soda_can.png", (58, 77), (4, 1), scale=item_scale)
button_press = SpriteSheet("button_press.png", (80, 80), (9, 1), scale=item_scale)
def shake_can(wait_time=8000):
    global game_state, game_score, game_time, game_lives, microgame_conf_set, current_microgame, microgame_failed, pause_time, press_w_label, soda_finished, up_times, down_times, soda_shake_amount, soda_shake, soda_stop_fizz, microgames_played 
    if game_state == "microgame":
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks() - total_paused
        elapsed_time = current_time - game_time
        time_left = (wait_time - elapsed_time) // 1000
        if time_left < 0:
            time_left = 0
        
        if not microgame_conf_set:
            soda_finished = False
            soda_shake = random.choice((True, False))
            soda_shake_amount = random.randint(10, 20)
            soda_stop_fizz = soda_shake_amount
            down_times = 0
            up_times = 0
            microgame_conf_set = True
        
        if current_time - game_time >= wait_time and not paused:
            if soda_finished:
                microgame_failed = False
                game_score += 1
            else:
                game_lives -= 1
                microgame_failed = True
            current_microgame = None
            game_time = pygame.time.get_ticks() - total_paused
            try:
                pause_time = 0
            except:
                pass
            microgames_played += 1
            game_state = "intermission"
        
        if soda_finished and time_left > 3:
            game_time = pygame.time.get_ticks() - total_paused - (wait_time - 3000)
        
        # Checks if the up_times or down_times are 1/3, 2/3, 3/3
        # Also, I decided to round down for this logic

        if soda_shake:
            if not soda_finished:
                arrow_up = pygame.image.load("arrow.png").convert_alpha()
                arrow_up = pygame.transform.scale_by(arrow_up, item_scale)
                arrow_down = pygame.transform.rotate(arrow_up, 180)
                screen.blit(arrow_up, (round(screen_width/2) - round(arrow_up.get_width()/2), round(screen_height/2) - round(soda_can.image.get_height()/2) - arrow_up.get_height()))
                screen.blit(arrow_down, (round(screen_width/2) - round(arrow_down.get_width()/2), round(screen_height/2) + round(soda_can.image.get_height()/2)))
            if down_times < soda_shake_amount or up_times < soda_shake_amount:
                if down_times < soda_shake_amount // 3 or up_times < soda_shake_amount // 3:
                    soda_can.image = soda_can.sprites[0]
                elif (down_times >= soda_shake_amount // 3 or up_times >= soda_shake_amount // 3) and (down_times < (soda_shake_amount // 3) * 2 or up_times < (soda_shake_amount // 3) * 2):
                    soda_can.image = soda_can.sprites[1]
                elif (down_times >= (soda_shake_amount // 3) * 2 or up_times >= (soda_shake_amount // 3) * 2) and (down_times < (soda_shake_amount // 3) * 3 or up_times < (soda_shake_amount // 3) * 3):
                    soda_can.image = soda_can.sprites[2]
            else:
                soda_can.image = soda_can.sprites[3]
                soda_finished = True
        else:
            if not soda_finished:
                button_press.play(20)
                screen.blit(button_press.image, (round(screen_width/2) - round(button_press.image.get_width()/2), 0))
            if soda_stop_fizz >= soda_shake_amount or soda_stop_fizz >= soda_shake_amount // 2:
                soda_can.image = soda_can.sprites[2]
            elif soda_stop_fizz < soda_shake_amount // 2 and soda_stop_fizz > 0:
                soda_can.image = soda_can.sprites[1]
            elif soda_stop_fizz == 0:
                soda_can.image = soda_can.sprites[0]
                soda_finished = True

        press_w_label = font.render("Keep Pressing W!", False, (255, 0, 0))
        screen.blit(soda_can.image, (round(screen_width/2) - round(soda_can.image.get_width()/2), round(screen_height/2) - round(soda_can.image.get_height()/2)))
        if not soda_finished and not soda_shake:
            screen.blit(press_w_label, (round(screen_width / 2) - round(press_w_label.get_width() / 2), round(screen_height/2) - round(soda_can.image.get_height()/2) - press_w_label.get_height()))
        
        action_label = medium_font.render("Shake the Soda Can!", False, (255, 255, 255)) if soda_shake else medium_font.render(f"Stop Soda Shakeup!", False, (255, 255, 255))
        if not soda_finished and time_left > 3:
            time_left_label = font.render(str(time_left), False, (255, 255, 0))
            screen.blit(time_left_label, (screen_width - time_left_label.get_width(), 0))
        else:
            time_left_label = big_font.render(str(time_left), False, (255, 0, 0))
            screen.blit(time_left_label, (round(screen_width/2) - round(time_left_label.get_width()/2), round(screen_height/2) - round(time_left_label.get_height()/2)))
        screen.blit(action_label, (0, round(time_left_label.get_height()/2) - round(action_label.get_height()/2)))
    
kuvira = SpriteSheet("kuvira.png", (66, 149), (4, 1), item_scale)
azula = SpriteSheet("azula.png", (68, 160), (5, 1), item_scale)
peasant_1 = SpriteSheet("peasant.png", (153, 167), (5, 4), item_scale)
peasant_2 = SpriteSheet("peasant.png", (153, 167), (5, 4), item_scale)
peasant_3 = SpriteSheet("peasant.png", (153, 167), (5, 4), item_scale)
def shear_peasants(wait_time=8000):
    global game_state, game_score, game_time, game_lives, microgame_conf_set, current_microgame, microgame_failed, pause_time, peasants_to_shear, peasants_sheared, kuvira_play, peasant_1_play, peasant_2_play, peasant_3_play, microgames_played
    if game_state == "microgame":
        screen.fill((0, 0, 0))
        current_time = pygame.time.get_ticks() - total_paused
        elapsed_time = current_time - game_time
        time_left = (wait_time - elapsed_time) // 1000
        if time_left < 0:
            time_left = 0
        
        if not microgame_conf_set:
            if kuvira.image != kuvira.sprites[0]:
                kuvira.image = kuvira.sprites[0]
            peasants_to_shear = random.randint(1, 3)
            peasants_sheared = 0
            microgame_conf_set = True
        
        if current_time - game_time >= wait_time and not paused:
            if peasants_sheared >= peasants_to_shear:
                microgame_failed = False
                game_score += 1
            else:
                game_lives -= 1
                microgame_failed = True
            current_microgame = None
            game_time = pygame.time.get_ticks() - total_paused
            try:
                pause_time = 0
            except:
                pass
            kuvira.image = kuvira.sprites[0]
            peasant_1.image = peasant_1.sprites[0]
            peasant_2.image = peasant_2.sprites[0]
            peasant_3.image = peasant_3.sprites[0]
            microgames_played += 1
            game_state = "intermission"
        
        if peasants_sheared >= peasants_to_shear and time_left > 3:
            game_time = pygame.time.get_ticks() - total_paused - (wait_time - 3000)
        
        if kuvira_play and kuvira.image != kuvira.sprites[len(kuvira.sprites) - 1]:
            kuvira.play(10)
        else:
            kuvira.image = kuvira.sprites[0]
            kuvira_play = False
        
        if peasant_1_play and peasant_1.image != peasant_1.sprites[len(peasant_1.sprites) - 1]:
            peasant_1.play(30)
        else:
            peasant_1_play = False
        
        if peasant_2_play and peasant_2.image != peasant_2.sprites[len(peasant_2.sprites) - 1]:
            peasant_2.play(30)
        else:
            peasant_2_play = False
        
        if peasant_3_play and peasant_3.image != peasant_3.sprites[len(peasant_3.sprites) - 1]:
            peasant_3.play(30)
        else:
            peasant_3_play = False

        kuvira_left = round(screen_width * 4/5) - kuvira.image.get_width() // 2

        match peasants_to_shear:
            case 1:
                screen.blit(peasant_1.image, (round(kuvira_left * 1/2) - round(peasant_1.image.get_width() / 2), screen_height - peasant_1.image.get_height()))

            case 2:
                screen.blit(peasant_1.image, (round(kuvira_left * 2/3) - round(peasant_1.image.get_width() / 2), screen_height - peasant_1.image.get_height()))
                screen.blit(peasant_2.image, (round(kuvira_left * 1/3) - round(peasant_2.image.get_width() / 2), screen_height - peasant_2.image.get_height()))

            case 3:
                screen.blit(peasant_1.image, (round(kuvira_left * 3/4) - round(peasant_1.image.get_width() / 2), screen_height - peasant_1.image.get_height()))
                screen.blit(peasant_2.image, (round(kuvira_left * 2/4) - round(peasant_2.image.get_width() / 2), screen_height - peasant_2.image.get_height()))
                screen.blit(peasant_3.image, (round(kuvira_left * 1/4) - round(peasant_3.image.get_width() / 2), screen_height - peasant_3.image.get_height()))

        screen.blit(kuvira.image, (round(screen_width * 4/5) - round(kuvira.image.get_width() / 2), screen_height - kuvira.image.get_height()))
        
        action_label = medium_font.render("Shear the Peasants!", False, (255, 255, 255))
        if not peasants_sheared >= peasants_to_shear and time_left > 3:
            time_left_label = font.render(str(time_left), False, (255, 255, 0))
            screen.blit(time_left_label, (screen_width - time_left_label.get_width(), 0))
        else:
            time_left_label = big_font.render(str(time_left), False, (255, 0, 0))
            screen.blit(time_left_label, (round(screen_width/2) - round(time_left_label.get_width()/2), round(screen_height/2) - round(time_left_label.get_height()/2)))
        screen.blit(action_label, (0, round(time_left_label.get_height()/2) - round(action_label.get_height()/2)))

fireball_container = []
fireball_sprites = pygame.sprite.Group()

# Interaction for interactive object item
def fireball_blast(enemy_hit=True):
    global kuvira_hp, katara_hp, current_microgame, boss_finished
    if enemy_hit and not boss_finished:
        if current_microgame == kuvira_vs_azula:
            kuvira_hp -= 5
        elif current_microgame == azula_vs_katara:
            katara_hp -= 5

# Override for fireball
def fireball_interacted(self, interaction_argument):
    if interaction_argument == None:
        self.interaction()
    else:
        self.interaction(interaction_argument)
    fireball_container.remove(self)
    fireball_sprites.remove(self)
    self.kill()

boulder_container = []
boulder_sprites = pygame.sprite.Group()
def boulder_interacted(self, interaction_argument):
    if interaction_argument == None:
        self.interaction()
    else:
        self.interaction(interaction_argument)
    boulder_container.remove(self)
    boulder_sprites.remove(self)
    self.kill()

def boulder_strike(azula_hit=True):
    global azula_hp, boss_finished
    if azula_hit and not boss_finished:
        azula_hp -= 10

shear_container = []
shear_sprites = pygame.sprite.Group()
def shear_strike(azula_hit=True):
    global shear_stun, azula_hp, boss_finished
    if azula_hit and not boss_finished:
        azula_hp -= 10
        shear_stun = True

def shear_interacted(self, interaction_argument):
    if interaction_argument == None:
        self.interaction()
    else:
        self.interaction(interaction_argument)
    shear_container.remove(self)
    shear_sprites.remove(self)
    self.kill()

azula_dialog = [pygame.mixer.Sound("azula_dialog_1.mp3"), pygame.mixer.Sound("azula_dialog_2.mp3"), pygame.mixer.Sound("azula_dialog_3.mp3"), pygame.mixer.Sound("azula_dialog_4.mp3"), pygame.mixer.Sound("azula_dialog_5.mp3")]
azula_win_dialog = [pygame.mixer.Sound("azula_win_1.mp3"), pygame.mixer.Sound("azula_win_2.mp3")]
kuvira_dialog = [pygame.mixer.Sound("kuvira_dialog_1.mp3"), pygame.mixer.Sound("kuvira_dialog_2.mp3"), pygame.mixer.Sound("kuvira_dialog_3.mp3"), pygame.mixer.Sound("kuvira_dialog_4.mp3"), pygame.mixer.Sound("kuvira_dialog_5.mp3")]
kuvira_win_dialog = pygame.mixer.Sound("kuvira_win_1.mp3")

speaker_azula = True

current_azula_win_dialog = random.choice(azula_win_dialog)

def kuvira_vs_azula():
    global game_state, game_score, game_time, game_lives, microgame_conf_set, current_microgame, microgame_failed, pause_time, azula_hp, azula_stamina, kuvira_hp, fireshield_on, fireshield_cooldown, azula_velocity_Y, azula_jumping, azula_falling, fireball_cooldown, earthshield, kuvira_play, fireshield, kuvira_attack_time, shear_stun, microgames_played, earthshield, earthshield_on, earthshield_hp, dialog_time, speaker_azula, earthshield_play, earthshield_rect, boss_finished, current_azula_win_dialog
    if game_state == "microgame":
        screen.fill((0, 0, 0))

        current_time = pygame.time.get_ticks() - total_paused

        if not microgame_conf_set:
            game_time = current_time
            boss_finished = False
            fireball_container.clear()
            azula_falling = False
            azula.image = azula.sprites[0]
            azula.image = pygame.transform.flip(azula.sprites[0], True, False)
            kuvira.image = kuvira.sprites[0]
            kuvira.image = pygame.transform.flip(kuvira.sprites[0], True, False)
            azula_hp = 200
            azula_stamina = 100
            kuvira_hp = 200
            earthshield_hp = 15
            earthshield_play = False
            microgame_conf_set = True
        else:
            if not azula_jumping or azula_falling:
                azula.image = pygame.transform.flip(azula.sprites[0], True, False)
            else:
                azula.image = pygame.transform.flip(azula.sprites[2], True, False)
            
            if not kuvira_play:
                kuvira.image = pygame.transform.flip(kuvira.sprites[0], True, False)
            
            if earthshield_hp < 0:
                earthshield_on = False
                try:
                    del earthshield
                    del earthshield_rect
                except:
                    pass
        
        if (kuvira_hp <= 0 or azula_hp <= 0) and not paused:
            if kuvira_hp <= 0:
                if not boss_finished:
                    current_azula_win_dialog = random.choice(azula_win_dialog)
                    current_azula_win_dialog.play()
                    game_score += 5
                    if game_lives < 5:
                        game_lives += 1
                    boss_finished = True
                microgame_failed = False
            else:
                if not boss_finished:
                    kuvira_win_dialog.play()
                    game_lives -= 1
                    boss_finished = True
                microgame_failed = True
            if kuvira_win_dialog.get_num_channels() <= 0 and azula_hp <= 0:
                current_microgame = None
                game_time = pygame.time.get_ticks() - total_paused
                try:
                    pause_time = 0
                except:
                    pass
                fireshield_on = False
                fireshield_cooldown = False
                shear_stun = False
                earthshield_on = False
                azula_jumping = False
                azula_falling = False
                try:
                    del fireshield
                except:
                    pass
                azula.image = azula.sprites[0]
                kuvira.image = kuvira.sprites[0]
                for shear in shear_container[:]:
                    shear.interacted(False)
                for boulder in boulder_container[:]:
                    boulder.interacted(False)
                for fireball in fireball_container[:]:
                    fireball.interacted(False)
                microgames_played += 1
                game_state = "intermission"
            elif kuvira_hp <= 0:
                if current_azula_win_dialog.get_num_channels() <= 0:
                    current_microgame = None
                    game_time = pygame.time.get_ticks() - total_paused
                    try:
                        pause_time = 0
                    except:
                        pass
                    fireshield_on = False
                    fireshield_cooldown = False
                    shear_stun = False
                    earthshield_on = False
                    azula_jumping = False
                    azula_falling = False
                    try:
                        del fireshield
                    except:
                        pass
                    azula.image = azula.sprites[0]
                    kuvira.image = kuvira.sprites[0]
                    for shear in shear_container[:]:
                        shear.interacted(False)
                    for boulder in boulder_container[:]:
                        boulder.interacted(False)
                    for fireball in fireball_container[:]:
                        fireball.interacted(False)
                    microgames_played += 1
                    game_state = "intermission"
        
        kuvira_rect = kuvira.image.get_rect()
        kuvira_rect.x = 0
        kuvira_rect.y = screen_height - kuvira.image.get_height()

        for fireball in fireball_container:
            fireball.rect.x -= 600 * dt
            try:
                if fireball.rect.colliderect(kuvira_rect):
                    fireball.interacted(True)
                elif fireball.rect.colliderect(earthshield_rect):
                    fireball.interacted(False)
                    earthshield_hp -= 5
                elif fireball.rect.x < 0:
                    fireball.interacted(False)
            except NameError:
                if fireball.rect.colliderect(kuvira_rect):
                    fireball.interacted(True)
                elif fireball.rect.x < 0:
                    fireball.interacted(False)
        
        azula_rect = azula.image.get_rect()
        azula_rect.x = screen_width - azula.image.get_width()
        azula_rect.y = screen_height - azula.image.get_height()

        if azula_jumping:
            if not azula_falling:
                azula_velocity_Y -= 40
                azula_rect.y += azula_velocity_Y
            else:
                azula_velocity_Y += 20
                azula_rect.y += azula_velocity_Y
        else:
            azula_velocity_Y = 0
        
        if azula_velocity_Y <= -screen_height // 2 - azula.image.get_height():
            azula_falling = True

        if azula_rect.y >= screen_height - azula.image.get_height():
            azula_rect.y = screen_height - azula.image.get_height()
            azula_jumping = False
            azula_falling = False
        
        if shear_stun:
            azula.image = pygame.transform.flip(azula.sprites[1], True, False)
            if current_time - game_time > 2000:
                shear_stun = False
                game_time = current_time

        screen.blit(azula.image, azula_rect)
        screen.blit(kuvira.image, kuvira_rect)
        action_label = small_font.render("Defeat Kuvira!", False, (0, 255, 0))
        hint_1_label = medium_font.render("Jump to dodge metal strips", False, (150, 150, 150))
        hint_2_label = medium_font.render("Earth walls burn in 4 hits", False, (150, 75, 0))
        firebend_label = small_font.render("Press W to firebend", False, (255, 0, 0))
        jump_label = small_font.render("Press S to jump", False, (255, 255, 255))
        fireshield_label = small_font.render("Press and hold A to fireshield", False, (255, 255, 0))
        fireball_sprites.draw(screen)
        boulder_sprites.draw(screen)
        shear_sprites.draw(screen)

        if fireshield_on:
            fireshield = pygame.draw.circle(screen, (0, 255, 255), (screen_width - azula.image.get_width() // 2, screen_height - azula.image.get_height() // 2), (azula.image.get_height() // 2) * 1.1)
            if azula_stamina > 0:
                azula_stamina -= 1
        else:
            try:
                del fireshield
            except:
                pass
            if azula_stamina < 100:
                azula_stamina += 1
            elif fireshield_cooldown:
                fireshield_cooldown = False

        # Kuvira fight cycle
        if current_time - kuvira_attack_time > 2000 and not earthshield_on and not boss_finished:
            kuvira_action = random.choices(("Shear", "Boulder", "Earthshield"), weights=(0.45, 0.45, 0.1), k=1) if not shear_stun else random.choices(("Shear", "Boulder", "Earthshield"), weights=(0, 0.65, 0.35), k=1)
            kuvira_action = str(kuvira_action[0])
            kuvira_play = True
            match kuvira_action:
                case "Shear":
                    shear = Interactive_Item("kuvira_shear.png", shear_strike, (0, screen_height - kuvira.image.get_height()), item_scale)
                    shear.rect.y = screen_height - shear.image.get_height()
                    shear_container.append(shear)
                    shear_sprites.add(shear)
                case "Boulder":
                    boulder = Interactive_Item("kuvira_earth.png", boulder_strike, (0, screen_height - kuvira.image.get_height() - round(kuvira.image.get_height() // 10)), item_scale // 2)
                    boulder.interacted = boulder_interacted.__get__(boulder, Interactive_Item)
                    boulder_container.append(boulder)
                    boulder_sprites.add(boulder)
                case "Earthshield":
                    earthshield = SpriteSheet("kuvira_earth_wall.png", (66, 149), (8, 4), item_scale)
                    earthshield_hp = 15
                    earthshield_on = True
                    earthshield_play = True
            kuvira_attack_time = current_time
        
        try:
            earthshield_rect = earthshield.image.get_rect()
            earthshield_rect.x = kuvira.image.get_width()
            earthshield_rect.y = screen_height - earthshield.image.get_height()
        except NameError:
            pass

        try:
            if earthshield_play and earthshield.current_frame != len(earthshield.sprites) - 1:
                earthshield.play(100)
            else:
                earthshield_play = False
            screen.blit(earthshield.image, earthshield_rect)
        except NameError:
            pass
        
        # Checks if the kuvira animation is finished
        if kuvira_play:
            kuvira.play(10)
            # Flips the current frames so that its original frames don't get flipped
            if kuvira.image in kuvira.sprites:
                kuvira.image = pygame.transform.flip(kuvira.image, True, False)
            
            if kuvira.current_frame == len(kuvira.sprites) - 1:
                kuvira_play = False
        
        for boulder in boulder_container:
            boulder.rect.x += 600 * dt
            try:
                if boulder.rect.colliderect(azula_rect):
                    boulder.interacted(True)
                elif boulder.rect.colliderect(fireshield):
                    boulder.interacted(False)
                elif boulder.rect.x > screen_width:
                    boulder.interacted(False)
            except NameError:
                if boulder.rect.colliderect(azula_rect):
                    boulder.interacted(True)
                elif boulder.rect.x > screen_width:
                    boulder.interacted(False)
        
        for shear in shear_container:
            shear.rect.x += 600 * dt
            if not shear_stun:
                try:
                    if shear.rect.colliderect(azula_rect) and not shear_stun:
                        shear.interacted(True)
                    elif shear.rect.colliderect(fireshield):
                        shear.interacted(False)
                    elif shear.rect.x > screen_width:
                        shear.interacted(False)
                except NameError:
                    if shear.rect.colliderect(azula_rect) and not shear_stun:
                        shear.interacted(True)
                    elif shear.rect.x > screen_width:
                        shear.interacted(False)
            else:
                shear.interacted(False)

        if fireball_cooldown:
            if current_time - game_time > 1000:
                game_time = current_time
                fireball_cooldown = False
        
        if azula_stamina < 0:
            azula_stamina = 0
        
        if azula_stamina > 100:
            azula_stamina = 100
        
        if azula_stamina <= 0:
            fireshield_cooldown = True
            fireshield_on = False
        
        if current_time - dialog_time > 5000 and not boss_finished:
            if speaker_azula:
                azula_current_dialog = random.choice(azula_dialog)
                azula_current_dialog.set_volume(1.0)
                azula_current_dialog.play()
            else:
                kuvira_current_dialog = random.choice(kuvira_dialog)
                kuvira_current_dialog.set_volume(1.0)
                kuvira_current_dialog.play()
            speaker_azula = not speaker_azula
            dialog_time = current_time

        if not azula_hp <= 0:
            # Azula Stamina Rect
            if not fireshield_cooldown:
                pygame.draw.rect(screen, (0, 255, 255), (round(screen_width / 2) - round((azula_stamina * item_scale) / 2), screen_height - 50, azula_stamina * item_scale, 30))
            else:
                pygame.draw.rect(screen, (195, 0, 16), (round(screen_width / 2) - round((azula_stamina * item_scale) / 2), screen_height - 50, azula_stamina * item_scale, 30))

            # Azula HP Rect
            pygame.draw.rect(screen, (255, 0, 0), (round(screen_width / 2) - round((azula_hp * item_scale) / 2), screen_height - 80, azula_hp * item_scale, 30))

        if not azula_hp <= 0:
            player_label = small_font.render("Your HP & Stamina (Azula)", False, (255, 255, 255), wraplength=screen_width)
            screen.blit(player_label, (round(screen_width / 2) - round(player_label.get_width() / 2), screen_height - 80 - player_label.get_height()))
        else:
            lose_label = font.render("You (Azula) Lose!", False, (255, 0, 0))
            screen.blit(lose_label, (screen_width // 2 - lose_label.get_width() // 2, screen_height - lose_label.get_height() - 50))
            
        kuvira_sublabel = small_font.render("The Earth Empire Dictator:", False, (255, 255, 255), wraplength=screen_width)
        kuvira_label = medium_font.render("Kuvira", False, (255, 255, 255), wraplength=screen_width)

        if not kuvira_hp <= 0:
            # Kuvira HP Rect
            pygame.draw.rect(screen, (0, 255, 0), (round(screen_width / 2) - round((kuvira_hp * item_scale) / 2), kuvira_sublabel.get_height() + kuvira_label.get_height() + 20, kuvira_hp * item_scale, 30))
            screen.blit(kuvira_sublabel, (round(screen_width / 2) - round(kuvira_sublabel.get_width() / 2), 20))
            screen.blit(kuvira_label, (round(screen_width / 2) - round(kuvira_label.get_width() / 2), 20 + kuvira_sublabel.get_height()))
        else:
            win_label = font.render("You (Azula) Win!", False, (0, 255, 0))
            screen.blit(win_label, (round(screen_width / 2) - round(win_label.get_width() / 2), 20))

        screen.blit(action_label, (0, 0))
        screen.blit(hint_1_label, (0, action_label.get_height()))
        screen.blit(hint_2_label, (0, action_label.get_height() + hint_1_label.get_height()))
        screen.blit(firebend_label, (screen_width - firebend_label.get_width(), 0))
        screen.blit(jump_label, (screen_width - jump_label.get_width(), firebend_label.get_height()))
        screen.blit(fireshield_label, (screen_width - fireshield_label.get_width(), jump_label.get_height() + firebend_label.get_height()))

ice_shard_container = []
ice_shard_sprites = pygame.sprite.Group()
# Interaction for interactive object item
def ice_shard_blast(azula_hit=True):
    global azula_hp
    if azula_hit:
        azula_hp -= 5
    else:
        pass

# Override for ice shard
def ice_shard_interacted(self, interaction_argument):
    if interaction_argument == None:
        self.interaction()
    else:
        self.interaction(interaction_argument)
    ice_shard_container.remove(self)
    ice_shard_sprites.remove(self)
    self.kill()
katara = SpriteSheet("katara.png", (64, 145), (2, 1), item_scale)
katara_dialog = [pygame.mixer.Sound("katara_dialog_1.mp3"), pygame.mixer.Sound("katara_dialog_2.mp3"), pygame.mixer.Sound("katara_dialog_3.mp3"), pygame.mixer.Sound("katara_dialog_4.mp3"), pygame.mixer.Sound("katara_dialog_5.mp3")]
katara_win_dialog = pygame.mixer.Sound("katara_win_1.mp3")
def azula_vs_katara():
    global game_state, game_score, game_time, game_lives, microgame_conf_set, current_microgame, microgame_failed, pause_time, azula_hp, katara_hp, katara_stamina, microgames_played, dialog_time, speaker_azula, ice_shard_cooldown, waterfall_on, waterfall, waterfall_rect, waterfall_cooldown, waterfall_play, waterfall_exists, azula_freeze, freeze_heal_cooldown, azula_attack_time, azula_lightning, azula_lightning_time, waterheal_on, waterheal_cooldown, lightning, lightning_rect, lightning_play, boss_finished, current_azula_win_dialog
    screen.fill((0, 0, 0))

    current_time = pygame.time.get_ticks() - total_paused

    if not microgame_conf_set:
        game_time = current_time
        boss_finished = False
        fireball_container.clear()
        fireball_sprites.empty()
        azula.image = azula.sprites[0]
        katara.image = katara.sprites[0]
        azula_hp = 250
        katara_hp = 200
        katara_stamina = 70
        waterfall_exists = False
        waterfall_on = False
        waterfall_play = False
        waterfall_cooldown = False
        lightning_play = False
        microgame_conf_set = True
    else:
        if katara_stamina <= 0:
            katara_stamina = 0
        if katara_stamina >= 70:
            katara_stamina = 70
        
        if katara_hp >= 200:
            katara_hp = 200
        
        if katara_hp < 0:
            katara_hp = 0
        
    if (katara_hp <= 0 or azula_hp <= 0) and not paused:
        if azula_hp <= 0:
            if not boss_finished:
                katara_win_dialog.play()
                game_score += 5
                boss_finished = True
            microgame_failed = False
        else:
            if not boss_finished:
                current_azula_win_dialog = random.choice(azula_win_dialog)
                current_azula_win_dialog.play()
                game_lives -= 1
                boss_finished = True
            microgame_failed = True
        
        if current_azula_win_dialog.get_num_channels() <= 0 and katara_hp <= 0:
            current_microgame = None
            game_time = pygame.time.get_ticks() - total_paused
            try:
                pause_time = 0
            except:
                pass
            try:
                del waterfall
                del waterfall_rect
            except:
                pass
            try:
                del lightning
                del lightning_rect
            except:
                pass
            azula.image = azula.sprites[0]
            for fireball in fireball_container[:]:
                fireball.interacted(False)
            for ice_shard in ice_shard_container[:]:
                ice_shard.interacted(False)
            microgames_played += 1
            game_state = "intermission"
        elif katara_win_dialog.get_num_channels() <= 0 and azula_hp <= 0:
            current_microgame = None
            game_time = pygame.time.get_ticks() - total_paused
            try:
                pause_time = 0
            except:
                pass
            try:
                del waterfall
                del waterfall_rect
            except:
                pass
            try:
                del lightning
                del lightning_rect
            except:
                pass
            azula.image = azula.sprites[0]
            for fireball in fireball_container[:]:
                fireball.interacted(False)
            for ice_shard in ice_shard_container[:]:
                ice_shard.interacted(False)
            microgames_played += 1
            game_state = "intermission"
    
    azula_rect = azula.image.get_rect()
    azula_rect.x = 0
    azula_rect.y = screen_height - azula.image.get_height()

    katara_rect = katara.image.get_rect()
    katara_rect.x = screen_width - katara.image.get_width()
    katara_rect.y = screen_height - katara.image.get_height()

    if waterfall_on:
        if not waterfall_exists:
            waterfall = SpriteSheet("waterfall.png", (100, 149), (3, 3), item_scale)
            waterfall_play = True
            waterfall_exists = True
        try:
            waterfall_rect = waterfall.image.get_rect()
            waterfall_rect.x = screen_width - katara.image.get_width() - waterfall.image.get_width()
            waterfall_rect.y = screen_height - katara.image.get_height()
        except:
            pass
        if katara_stamina > 0:
            katara_stamina -= 1
        if katara_stamina <= 0:
            waterfall_cooldown = True
            waterfall_on = False
    else:
        try:
            del waterfall
            del waterfall_rect
        except:
            pass
        if katara_stamina >= 70:
            waterfall_cooldown = False
        waterfall_exists = False
    
    if not waterfall_on and katara_stamina < 70 and not freeze_heal_cooldown and not waterheal_on and not boss_finished: 
        katara_stamina += 1
    
    try:
        if waterfall_play:
            waterfall.play(60)
            if waterfall.current_frame == len(waterfall.sprites) - 1:
                waterfall_play = False
    except NameError:
        pass

    try:
        screen.blit(waterfall.image, waterfall_rect)
    except NameError:
        pass
    
    if waterheal_on:
        katara_hp += 1
        katara_stamina -= 1
        if katara_stamina < 0:
            waterheal_cooldown = True
            waterheal_on = False
    else:
        if katara_stamina >= 70:
            waterheal_cooldown = False

    for ice_shard in ice_shard_container:
        ice_shard.rect.x -= 600 * dt
        if ice_shard.rect.colliderect(azula_rect):
            ice_shard.interacted(True)

    if ice_shard_cooldown:
        if current_time - game_time > 800:
            game_time = current_time
            ice_shard_cooldown = False
    
    if freeze_heal_cooldown:
        if current_time - game_time > 3000:
            game_time = current_time
            azula_freeze = False
            katara_stamina = 70
            freeze_heal_cooldown = False
    
    if azula_freeze:
        azula.image = azula.sprites[3]
    elif azula_lightning:
        azula.image = azula.sprites[4]
    else:
        azula.image = azula.sprites[0]

    # Speaking Cycle
    if current_time - dialog_time > 5000 and not boss_finished:
        if speaker_azula:
            azula_current_dialog = random.choice(azula_dialog)
            azula_current_dialog.set_volume(1.0)
            azula_current_dialog.play()
        else:
            katara_current_dialog = random.choice(katara_dialog)
            katara_current_dialog.set_volume(1.0)
            katara_current_dialog.play()
        speaker_azula = not speaker_azula
        dialog_time = current_time
    
    #  Azula fight cycle
    if current_time - azula_attack_time > 1200 and not azula_freeze and not azula_lightning and not boss_finished:
        azula_action = random.choices(("Fire", "Lightning"), weights=(0.85, 0.15), k=1)
        azula_action = str(azula_action[0])
        match azula_action:
            case "Fire":
                fireball = Interactive_Item("azula_fire.png", fireball_blast, (0, screen_height - round(azula.image.get_height() / 2)), item_scale // 2)
                fireball.interacted = fireball_interacted.__get__(fireball, Interactive_Item)
                fireball.image = pygame.transform.flip(fireball.image, True, False)
                fireball.rect.y = screen_height - fireball.image.get_height()
                fireball_container.append(fireball)
                fireball_sprites.add(fireball)
            case "Lightning":
                azula_lightning_time = current_time
                azula.image = azula.sprites[4]
                azula_lightning = True
        azula_attack_time = current_time
    
    if current_time - azula_lightning_time > 3000 and azula_lightning and not azula_freeze and not boss_finished:
        lightning = SpriteSheet("lightning.png", (164, 34), (2, 10), (screen_width, item_scale * 15), True)
        lightning_play = True
        azula_lightning = False
    
    try:
        lightning_rect = lightning.image.get_rect()
        lightning_rect.x = 0
        lightning_rect.y = screen_height - azula.image.get_height() // 2
    except NameError:
        pass

    if lightning_play:
        try:
            lightning.play(20)
            if lightning.current_frame == len(lightning.sprites) - 1:
                lightning_play = False
        except NameError:
            pass
    
    for fireball in fireball_container:
        fireball.rect.x += 600 * dt
        try:
            if fireball.rect.colliderect(katara_rect):
                katara_hp -= 10
                fireball.interacted(True)
            elif fireball.rect.colliderect(waterfall_rect):
                fireball.interacted(False)
        except NameError:
            if fireball.rect.colliderect(katara_rect):
                fireball.interacted()

    screen.blit(azula.image, azula_rect)
    screen.blit(katara.image, katara_rect)
    fireball_sprites.draw(screen)
    ice_shard_sprites.draw(screen)
    try:
        screen.blit(lightning.image, lightning_rect)
    except NameError:
        pass
    
    try:
        if azula_freeze:
            del lightning_rect
            del lightning
        elif lightning_rect.colliderect(katara_rect) and lightning_play == False and not boss_finished:
            katara_hp -= 50
            del lightning_rect
            del lightning
        elif boss_finished:
            del lightning_rect
            del lightning
    except NameError:
        pass
    
    action_label = small_font.render("Defeat Azula!", False, (0, 255, 0))
    hint_label = medium_font.render("When Azula is about to charge, freezing her will be useful.", False, (0, 0, 255), wraplength=screen_width // 6)
    icebend_label = small_font.render("Press W to icebend", False, (255, 0, 0))
    heal_label = small_font.render("Press S to heal", False, (255, 255, 255))
    waterfall_label = small_font.render("Press and hold A to make a waterfall", False, (255, 255, 0))
    freeze_label = small_font.render("Press UP to freeze Azula", False, (255, 255, 255))
    screen.blit(action_label, (0, 0))
    screen.blit(hint_label, (0, action_label.get_height()))
    screen.blit(icebend_label, (screen_width - icebend_label.get_width(), 0))
    screen.blit(heal_label, (screen_width - heal_label.get_width(), icebend_label.get_height()))
    screen.blit(waterfall_label, (screen_width - waterfall_label.get_width(), heal_label.get_height() + icebend_label.get_height()))
    screen.blit(freeze_label, (screen_width - freeze_label.get_width(), heal_label.get_height() + icebend_label.get_height() + waterfall_label.get_height()))

    # Reminder for beginners to freeze Azula
    if azula_lightning:
        freeze_reminder_label = small_font.render("Freeze Azula NOW!", False, (0, 0, 255))
        screen.blit(freeze_reminder_label, (azula.image.get_width() // 2 - freeze_reminder_label.get_width() // 2, screen_height - azula.image.get_height() - freeze_reminder_label.get_height()))
    
    # Add cooldown variable for katara

    if not katara_hp <= 0:
        if not waterfall_cooldown and not waterheal_cooldown:
            pygame.draw.rect(screen, (0, 255, 255), (round(screen_width / 2) - round((katara_stamina * item_scale) / 2), screen_height - 50, katara_stamina * item_scale, 30))
        else:
            pygame.draw.rect(screen, (195, 0, 16), (round(screen_width / 2) - round((katara_stamina * item_scale) / 2), screen_height - 50, katara_stamina * item_scale, 30))
        pygame.draw.rect(screen, (0, 0, 255), (round(screen_width / 2) - round((katara_hp * item_scale) / 2), screen_height - 80, katara_hp * item_scale, 30))
        player_label = small_font.render("Your HP & Stamina (Katara)", False, (255, 255, 255), wraplength=screen_width)
        screen.blit(player_label, (round(screen_width / 2) - round(player_label.get_width() / 2), screen_height - 80 - player_label.get_height()))
    else:
        lose_label = font.render("You (Katara) Lose!", False, (255, 0, 0))
        screen.blit(lose_label, (screen_width // 2 - lose_label.get_width() // 2, screen_height - lose_label.get_height() - 50))

    # Azula HP Rect
    if not azula_hp <= 0:
        azula_sublabel = small_font.render("The Fire Nation Princess:", False, (255, 255, 255), wraplength=screen_width)
        azula_label = medium_font.render("Azula", False, (255, 255, 255), wraplength=screen_width)
        pygame.draw.rect(screen, (255, 0, 0), (round(screen_width / 2) - round((azula_hp * item_scale) / 2),  azula_sublabel.get_height() + azula_label.get_height() + 20, azula_hp * item_scale, 30))
        screen.blit(azula_sublabel, (round(screen_width / 2) - round(azula_sublabel.get_width() / 2), 20))
        screen.blit(azula_label, (round(screen_width / 2) - round(azula_label.get_width() / 2), 20 + azula_sublabel.get_height()))
    else:
        win_label = font.render("You (Katara) Win!", False, (0, 255, 0))
        screen.blit(win_label, (round(screen_width / 2) - round(win_label.get_width() / 2), 20))
    
    action_label = small_font.render("Defeat Azula!", False, (0, 255, 0))
    hint_label = medium_font.render("When Azula is about to charge, freezing her will be useful.", False, (0, 0, 255), wraplength=screen_width // 6)
    icebend_label = small_font.render("Press W to icebend", False, (255, 0, 0))
    heal_label = small_font.render("Press S to heal", False, (255, 255, 255))
    waterfall_label = small_font.render("Press and hold A to make a waterfall", False, (255, 255, 0))
    freeze_label = small_font.render("Press UP to freeze Azula", False, (255, 255, 255))
    screen.blit(action_label, (0, 0))
    screen.blit(hint_label, (0, action_label.get_height()))
    screen.blit(icebend_label, (screen_width - icebend_label.get_width(), 0))
    screen.blit(heal_label, (screen_width - heal_label.get_width(), icebend_label.get_height()))
    screen.blit(waterfall_label, (screen_width - waterfall_label.get_width(), heal_label.get_height() + icebend_label.get_height()))
    screen.blit(freeze_label, (screen_width - freeze_label.get_width(), heal_label.get_height() + icebend_label.get_height() + waterfall_label.get_height()))

microgames = [change_image, fire_out, place_arrow, shake_can, shear_peasants]
bosses = [kuvira_vs_azula, azula_vs_katara]

# Functional Functions
def score_eligible():
    global scoreboard_data
    if scoreboard_path.exists():
        with open(scoreboard_path, "r") as f:
            try:
                scoreboard_data = json.load(f)
            except:
                if game_score >= 1:
                    return True
                else:
                    return False
            scores = [score for score in scoreboard_data.values() if isinstance(score, int)]
            scores.sort()
            scores.reverse()
            for score in scores:
                if game_score > score:
                    return True
            return False
    elif game_score >= 1:
        return True

def add_score(player_name, new_score):
    global scoreboard_data
    if scoreboard_path.exists():
        try:
            DATABASE_PATH = "https://scoreboard-cde81-default-rtdb.firebaseio.com/.json"
            scoreboard_request = requests.get(DATABASE_PATH)
            scoreboard_request.raise_for_status()
            firebase_data = scoreboard_request.json()
            with open(scoreboard_path, 'w') as sp:
                json.dump(firebase_data, sp, indent=4)
        except requests.exceptions.HTTPError as err:
            print(f"Error fetching data from Firebase: HTTP error occurred: {err}")
            print(f"Response status code: {scoreboard_request.status_code}")
            print(f"Response content: {scoreboard_request.text}")
        except requests.exceptions.RequestException as err:
            print(f"Error fetching data from Firebase: An unexpected request error occurred: {err}")
            print("Please check your internet connection or the DATABASE_URL.")
        with open(scoreboard_path, "r") as f:
            scoreboard_data = json.load(f)
            scores = [score for score in scoreboard_data.values() if isinstance(score, int)]
            for score in scores:
                if new_score > score:
                    keys = [key for key in scoreboard_data.keys() if isinstance(scoreboard_data[key], int)]
                    for i, key in enumerate(keys):
                        if new_score > scoreboard_data[key]:
                            for j in range(len(keys) - 2, i, -1):
                                scoreboard_data[keys[j]] = scoreboard_data[keys[j - 1]]
                                scoreboard_data["score_names"][j] = scoreboard_data["score_names"][j - 1]
                            scoreboard_data[key] = new_score
                            scoreboard_data["score_names"][i] = player_name
                            break
                    break   

            with open(scoreboard_path, "w") as f:
                json.dump(scoreboard_data, f, indent=4)                  

def default_values():
    global microgame_conf_set, microgame_set, microgame_failed, filter_button_pressed
    microgame_set = False
    microgame_conf_set = False
    microgame_failed = False
    filter_button_pressed = False

def intermission_time(wait_time=1900):
    global game_state, microgame_conf_set, game_time, pause_time, boss_mode
    if microgames_played != 0 and microgames_played % 9 == 0 or dev_mode:
        boss_mode = True
    else:
        boss_mode = False
    current_time = pygame.time.get_ticks() - total_paused
    if current_time - game_time >= wait_time and not paused:
        default_values()
        game_time = pygame.time.get_ticks() - total_paused
        try:
            pause_time = 0
        except:
            pass
        if game_lives > 0:
            game_state = "microgame"
        else:
            game_state = "game_over"

# Display functions
def main_menu():
    if game_state == "main_menu":
        screen.fill((0, 0, 0))
        gavinware_logo = pygame.image.load("GavinWare_Logo.png").convert_alpha()
        screen.blit(gavinware_logo, (round(screen_width/2) - round(gavinware_logo.get_width() / 2), 55))
        screen.blit(play_button.image, (0, screen_height - 270))
        screen.blit(exit_button.image, (screen_width - exit_button.image.get_width(), screen_height - 270))
        gavin_boombox_animation.play(40, 0, 15)
        screen.blit(gavin_boombox_animation.image, (round(screen_width/2) - round(gavin_boombox_animation.image.get_width()/2), round(screen_height/2) - round(gavin_boombox_animation.image.get_height()/2)))
        press_play_label = font.render("Press W to select", False, (255, 0, 0))
        press_play_label.set_alpha(fade_alpha)
        screen.blit(press_play_label, (round(screen_width/2) - round(press_play_label.get_width()/2), screen_height - 125))
    else:
        pass

def pause_menu():
    if paused:
        screen.fill((0, 0, 0))
        pause_label = font.render("Paused", False, (255, 255, 255))
        gavin_boombox_animation.play(4, 30, 34)
        screen.blit(gavin_boombox_animation.image, (round(screen_width/2) - round(gavin_boombox_animation.image.get_width()/2), round(screen_height/2) - round(gavin_boombox_animation.image.get_height()/2)))
        screen.blit(pause_label, (round(screen_width/2) - round(pause_label.get_width()/2), 55))
        screen.blit(play_pause_button.image, (0, screen_height - 270))
        screen.blit(exit_pause_button.image, (screen_width - exit_pause_button.image.get_width(), screen_height - 270))
        press_play_label = font.render("Press W to select", False, (255, 0, 0))
        press_play_label.set_alpha(fade_alpha)
        screen.blit(press_play_label, (round(screen_width/2) - round(press_play_label.get_width()/2), screen_height - 125))

def intro_screen():
    if game_state == "intro":
        screen.fill((0, 0, 0))
        gavinware_title_label = font.render("Welcome to GavinWare!", False, (0, 180, 255))
        gavinware_description = medium_font.render("Welcome to the fun, engaging game of GavinWare! Which is DEFINITELY NOT inspired by a similar game whose main character is a rival to a famous plumber who steps on turtles. Come enjoy many of my microgames!", False, (255, 255, 255), wraplength=screen_width)
        reading_disclaimer = medium_font.render("BASIC READING ABILITY NEEDED FOR THIS GAME, hints will be shown on the top corners of the screen", False, (255, 0, 0), wraplength=screen_width)
        button_mappings_image = pygame.image.load("keyboard_example.png").convert_alpha()
        confirm_label = font.render("Press W to continue", False, (255, 0, 0))
        confirm_label.set_alpha(fade_alpha)
        pause_label = font.render("Press D to pause", False, (0, 0, 255))
        pause_label.set_alpha(fade_alpha)
        screen.blit(gavinware_title_label, (round(screen_width/2) - round(gavinware_title_label.get_width()/2), 55))
        screen.blit(gavinware_description, (0, round(screen_height/2) - round((gavinware_description.get_height() + reading_disclaimer.get_height() + button_mappings_image.get_height()) / 3)))
        screen.blit(reading_disclaimer, (0, round(screen_height/2) - round((gavinware_description.get_height() + reading_disclaimer.get_height() + button_mappings_image.get_height()) / 3) + gavinware_description.get_height()))
        screen.blit(button_mappings_image, (round(screen_width / 2) - round(button_mappings_image.get_width() / 2), round(screen_height/2) - round((gavinware_description.get_height() + reading_disclaimer.get_height() + button_mappings_image.get_height()) / 3) + button_mappings_image.get_height()))
        screen.blit(confirm_label, (round(screen_width/2) - round(confirm_label.get_width()/2), screen_height - 125))
        screen.blit(pause_label, (round(screen_width/2) - round(pause_label.get_width()/2), screen_height - 125 - pause_label.get_height()))
    else:
        pass

def intermission_screen():
    if game_state == "intermission":
        screen.fill((0, 0, 0))
        boss_label = font.render("BOSS INCOMING!", False, (255, 0, 0))
        current_score_label = font.render(f"Current Score: {game_score}", False, (0, 180, 255))
        game_lives_label = font.render(f"Lives Left: {game_lives}", False, (0, 180, 255))
        screen.blit(current_score_label, (round(screen_width/2) - round(current_score_label.get_width() / 2), 55))

        if not boss_mode:
            if microgame_failed:
                gavin_boombox_animation.play(40, 15, 30)
            else:
                gavin_boombox_animation.play(40, 0, 15)
        else:
            screen.blit(boss_label, (round(screen_width / 2) - round(boss_label.get_width() / 2), 55 + current_score_label.get_height() + round(boss_label.get_height() / 2)))
            gavin_boombox_animation.play(24, 35)

        screen.blit(gavin_boombox_animation.image, (round(screen_width/2) - round(gavin_boombox_animation.image.get_width()/2), round(screen_height/2) - round(gavin_boombox_animation.image.get_height()/2)))
        screen.blit(game_lives_label, (round(screen_width/2) - round(game_lives_label.get_width()/2), screen_height - 125))

def game_over_screen():
    global game_score
    if game_state == "game_over":
        screen.fill((0, 0, 0))
        game_over_label = font.render("Game Over!", False, (255, 255, 255))
        final_score_label = font.render(f"Final Score: {game_score}", False, (255, 255, 255))
        confirm_label = font.render("Press W to continue", False, (255, 0, 0))
        confirm_label.set_alpha(fade_alpha)
        screen.blit(game_over_label, (round(screen_width/2) - round(game_over_label.get_width()/2), 55))
        screen.blit(final_score_label, (round(screen_width/2) - round(final_score_label.get_width()/2), round(screen_height/2) - round(final_score_label.get_height()/2)))
        screen.blit(confirm_label, (round(screen_width/2) - round(confirm_label.get_width()/2), screen_height - 125))

def set_name_screen():
    if game_state == "set_name":
        screen.fill((0, 0, 0))
        match single_letter_index:
            case 0:
                letter_1_label = font.render(letter_1, False, (255, 255, 0))
                letter_2_label = font.render(letter_2, False, (255, 255, 255))
                letter_3_label = font.render(letter_3, False, (255, 255, 255))
            case 1:
                letter_1_label = font.render(letter_1, False, (255, 255, 255))
                letter_2_label = font.render(letter_2, False, (255, 255, 0))
                letter_3_label = font.render(letter_3, False, (255, 255, 255))
            case 2:
                letter_1_label = font.render(letter_1, False, (255, 255, 255))
                letter_2_label = font.render(letter_2, False, (255, 255, 255))
                letter_3_label = font.render(letter_3, False, (255, 255, 0))
        set_name_label = font.render("You got a high score! Set your name.", False, (255, 255, 255))
        controls_label = medium_font.render("Press UP and DOWN to change letter value.", False, (255, 255, 0))
        screen.blit(set_name_label, (round(screen_width/2) - round(set_name_label.get_width()/2), 55))
        screen.blit(letter_1_label, (round(screen_width * 1/4) - round(letter_1_label.get_width() * 1/4), round(screen_height/2) - round(letter_1_label.get_height()/2)))
        screen.blit(controls_label, (round(screen_width / 2) - round(controls_label.get_width() / 2), 55 + set_name_label.get_height()))
        screen.blit(letter_2_label, (round(screen_width * 2/4) - round(letter_2_label.get_width() * 2/4), round(screen_height/2) - round(letter_2_label.get_height()/2)))
        screen.blit(letter_3_label, (round(screen_width * 3/4) - round(letter_3_label.get_width() * 3/4), round(screen_height/2) - round(letter_3_label.get_height()/2)))
        confirm_label = font.render("Press W to continue", False, (255, 0, 0))
        confirm_label.set_alpha(fade_alpha)
        screen.blit(confirm_label, (round(screen_width/2) - round(confirm_label.get_width()/2), screen_height - 125))

def scoreboard_screen():
    if game_state == "scoreboard_screen":
        screen.fill((0, 0, 0))
        scoreboard_label = font.render("Scoreboard", False, (255, 255, 255))
        confirm_label = font.render("Press W to continue", False, (255, 0, 0))
        confirm_label.set_alpha(fade_alpha)
        score_1_label = font.render(f"1 - {scoreboard_data["score_names"][0]}: {scoreboard_data["score_1"]}", False, (255, 255, 0))
        screen.blit(score_1_label,
            (round(screen_width/2) - round(score_1_label.get_width()/2),
            round(screen_height * 1/10) - round(score_1_label.get_height()/2) + 55 + scoreboard_label.get_height() + 40))

        score_2_label = font.render(f"2 - {scoreboard_data["score_names"][1]}: {scoreboard_data["score_2"]}", False, (255, 255, 0))
        screen.blit(score_2_label,
            (round(screen_width/2) - round(score_2_label.get_width()/2),
            round(screen_height * 2/10) - round(score_2_label.get_height()/2) + 55 + scoreboard_label.get_height() + 40))

        score_3_label = font.render(f"3 - {scoreboard_data["score_names"][2]}: {scoreboard_data["score_3"]}", False, (255, 255, 0))
        screen.blit(score_3_label,
            (round(screen_width/2) - round(score_3_label.get_width()/2),
            round(screen_height * 3/10) - round(score_3_label.get_height()/2) + 55 + scoreboard_label.get_height() + 40))

        score_4_label = font.render(f"4 - {scoreboard_data["score_names"][3]}: {scoreboard_data["score_4"]}", False, (255, 255, 0))
        screen.blit(score_4_label,
            (round(screen_width/2) - round(score_4_label.get_width()/2),
            round(screen_height * 4/10) - round(score_4_label.get_height()/2) + 55 + scoreboard_label.get_height() + 40))

        score_5_label = font.render(f"5 - {scoreboard_data["score_names"][4]}: {scoreboard_data["score_5"]}", False, (255, 255, 0))
        screen.blit(score_5_label,
            (round(screen_width/2) - round(score_5_label.get_width()/2),
            round(screen_height * 5/10) - round(score_5_label.get_height()/2) + 55 + scoreboard_label.get_height() + 40))

        screen.blit(scoreboard_label, (round(screen_width/2) - round(scoreboard_label.get_width()/2), 55))
        screen.blit(confirm_label, (round(screen_width/2) - round(confirm_label.get_width()/2), screen_height - 125))


while running:
    for button in main_menu_buttons:
        button.button_list = main_menu_buttons
        button.button_index = main_menu_button_index
    
    for button in pause_menu_buttons:
        button.button_list = pause_menu_buttons
        button.button_index = pause_menu_button_index

    if game_state == "microgame" and current_microgame == change_image and not filter_button_pressed and not paused:
        mouse.mouse_move()
        if pygame.sprite.spritecollideany(mouse, change_image_button_sprites):
            mouse.image = mouse.selected_image
        else:
            mouse.image = mouse.original_image
    else:
        mouse.image = mouse.original_image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == red_button:
                if not paused:
                    match game_state:
                        case "main_menu":
                            if play_button.pressed(event.key):
                                game_state = "intro"
                            if exit_button.pressed(event.key):
                                pygame.quit()
                                sys.exit()
                        case "intro":
                            game_time = pygame.time.get_ticks()
                            game_state = "intermission"
                        case "game_over":
                            if score_eligible():
                                game_state = "set_name"
                            else:
                                game_state = "scoreboard_screen"
                        case "set_name":
                            score_name = letter_1 + letter_2 + letter_3
                            add_score(score_name, game_score)
                            game_state = "scoreboard_screen"
                        case "scoreboard_screen":
                            try:
                                with open(scoreboard_path, 'r') as sp:
                                    scoreboard_data = json.load(sp)
                                data_to_upload = json.dumps(scoreboard_data)
                                DATABASE_PATH = "https://scoreboard-cde81-default-rtdb.firebaseio.com/.json"
                                scoreboard_request = requests.put(DATABASE_PATH, data=data_to_upload)
                                scoreboard_request.raise_for_status()
                            except FileNotFoundError:
                                print(f"Error: The file '{scoreboard_path}' was not found.")
                            except json.JSONDecodeError:
                                print(f"Error: Could not decode JSON from '{scoreboard_path}'. Please check the file's format.")
                            except requests.exceptions.HTTPError as err:
                                print(f"HTTP error occurred: {err}")
                                print(f"Response content: {scoreboard_request.text}")
                            except requests.exceptions.RequestException as err:
                                print(f"An error occurred: {err}")
                            pygame.quit()
                            sys.exit()
                        case _ if current_microgame == shake_can:
                            if soda_shake:
                                if up_times < soda_shake_amount and (up_times == down_times or up_times < down_times):
                                    up_times += 1
                            elif not soda_shake and soda_stop_fizz > 0:
                                soda_stop_fizz -= 1
                        case "microgame":
                            match current_microgame:
                                case _ if current_microgame == change_image:
                                    if not paused:
                                        for button in change_image_buttons:
                                            if button == red_microgame_button:
                                                if mouse.rect.colliderect(button.rect):
                                                    button.interacted("red")
                                                    break
                                            if button == green_button:
                                                if mouse.rect.colliderect(button.rect):
                                                    button.interacted("green")
                                                    break
                                            if button == blue_button:
                                                if mouse.rect.colliderect(button.rect):
                                                    button.interacted("blue")
                                                    break
                                            if button == inverted_button:
                                                if mouse.rect.colliderect(button.rect):
                                                    button.interacted("inverted")
                                                    break
                                case _ if current_microgame == fire_out:
                                    if fire_color == "RED":
                                        fire_stamina -= 1
                                case _ if current_microgame == place_arrow:
                                    arrow_placed = True
                                case _ if current_microgame == shear_peasants:
                                    if peasants_sheared < peasants_to_shear:
                                        match peasants_sheared:
                                            case 0:
                                                peasant_1_play = True
                                            case 1:
                                                peasant_2_play = True
                                            case 2:
                                                peasant_3_play = True
                                        kuvira_play = True
                                        peasants_sheared += 1
                                case _ if current_microgame == kuvira_vs_azula:
                                    if not azula_jumping and not fireshield_on and not fireshield_cooldown and not fireball_cooldown and not shear_stun and not boss_finished:
                                        fireball = Interactive_Item("azula_fire.png", fireball_blast, (screen_width - azula.image.get_width(), screen_height - round(azula.image.get_height() / 2)), item_scale // 2)
                                        fireball.interacted = fireball_interacted.__get__(fireball, Interactive_Item)
                                        fireball_container.append(fireball)
                                        fireball_sprites.add(fireball)
                                        fireball_cooldown = True
                                
                                case _ if current_microgame == azula_vs_katara:
                                    if not ice_shard_cooldown and not waterheal_cooldown and not waterfall_cooldown and not waterfall_on and not freeze_heal_cooldown and not boss_finished:
                                        ice_shard = Interactive_Item("ice_shard.png", ice_shard_blast, (screen_width - katara.image.get_width(), screen_height - round(katara.image.get_height() / 2)), item_scale)
                                        ice_shard.interacted = ice_shard_interacted.__get__(ice_shard, Interactive_Item)
                                        ice_shard_container.append(ice_shard)
                                        ice_shard_sprites.add(ice_shard)
                                        katara.image = katara.sprites[1]
                                        ice_shard_cooldown = True

                elif exit_pause_button.pressed(event.key):
                    game_state = "game_over"
                    paused = False
            
            if event.key == white_button:
                if not paused:
                    if game_state == "microgame":
                        match current_microgame:
                            case _ if current_microgame == fire_out:
                                if fire_color == "WHITE":
                                    fire_stamina -= 1
                            case _ if current_microgame == kuvira_vs_azula:
                                    if not azula_jumping and not fireshield_on and not fireshield_cooldown and not shear_stun and not boss_finished:
                                        azula_jumping = True
                            case _ if current_microgame == azula_vs_katara:
                                if not waterheal_cooldown and not waterfall_on and not waterfall_cooldown and not boss_finished:
                                    katara.image = katara.sprites[1]
                                    waterheal_on = True
                            case _ if current_microgame == shake_can:
                                if soda_shake:
                                    if down_times < soda_shake_amount and (up_times == down_times or down_times < up_times):
                                        down_times += 1
            
            if event.key == yellow_button:
                if not paused:
                    if game_state == "microgame":
                        match current_microgame:
                            case _ if current_microgame == fire_out:
                                if fire_color == "YELLOW":
                                    fire_stamina -= 1
                            case _ if current_microgame == kuvira_vs_azula:
                                if not fireshield_cooldown and not azula_jumping and not shear_stun and not boss_finished:
                                    if azula_stamina > 0:
                                        fireshield_on = True
                                    else:
                                        fireshield_on = False
                            case _ if current_microgame == azula_vs_katara:
                                if not waterfall_cooldown and not freeze_heal_cooldown and not waterfall_on and not waterheal_cooldown and not boss_finished:
                                    if katara_stamina > 0:
                                        waterfall_on = True
                                        katara.image = katara.sprites[1]
                                    else:
                                        waterfall_on = False

            if event.key == left_move:
                if game_state == "main_menu" and not paused:
                    if main_menu_button_index != 0:
                        main_menu_button_index -= 1
                elif paused:
                    if pause_menu_button_index != 0:
                        pause_menu_button_index -= 1
                elif game_state == "set_name":
                    if single_letter_index != 0:
                        single_letter_index -= 1

            if event.key == right_move:
                if game_state == "main_menu" and not paused:
                    if main_menu_button_index != len(main_menu_buttons) - 1:
                        main_menu_button_index += 1
                elif paused:
                    if pause_menu_button_index != len(pause_menu_buttons) - 1:
                        pause_menu_button_index += 1
                elif game_state == "set_name":
                    if single_letter_index != 2:
                        single_letter_index += 1
            
            if event.key == up_move:
                if game_state == "set_name" and not paused:
                    match single_letter_index:
                        case 0:
                            if letter_index_1 > 0:
                                letter_index_1 -= 1
                                letter_1 = letters[letter_index_1]
                            else:
                                letter_index_1 = len(letters) - 1
                                letter_1 = letters[letter_index_1]
                        case 1:
                            if letter_index_2 > 0:
                                letter_index_2 -= 1
                                letter_2 = letters[letter_index_2]
                            else:
                                letter_index_2 = len(letters) - 1
                                letter_2 = letters[letter_index_2]
                        case 2:
                            if letter_index_3 > 0:
                                letter_index_3 -= 1
                                letter_3 = letters[letter_index_3]
                            else:
                                letter_index_3 = len(letters) - 1
                                letter_3 = letters[letter_index_3]
                elif game_state == "microgame":
                    match current_microgame:
                        case _ if current_microgame == shake_can:
                            if soda_shake:
                                if up_times < soda_shake_amount and (up_times == down_times or up_times < down_times):
                                    up_times += 1
                        case _ if current_microgame == azula_vs_katara:
                            if not waterfall_cooldown and not freeze_heal_cooldown and not waterheal_cooldown and not boss_finished:
                                azula_freeze = True
                                katara_stamina = 0
                                azula_lightning = False
                                freeze_heal_cooldown = True
            
            if event.key == down_move:
                if game_state == "set_name" and not paused:
                    match single_letter_index:
                        case 0:
                            if letter_index_1 < len(letters) - 1:
                                letter_index_1 += 1
                                letter_1 = letters[letter_index_1]
                            else:
                                letter_index_1 = 0
                                letter_1 = letters[letter_index_1]
                        case 1:
                            if letter_index_2 < len(letters) - 1:
                                letter_index_2 += 1
                                letter_2 = letters[letter_index_2]
                            else:
                                letter_index_2 = 0
                                letter_2 = letters[letter_index_2]
                        case 2:
                            if letter_index_3 < len(letters) - 1:
                                letter_index_3 += 1
                                letter_3 = letters[letter_index_3]
                            else:
                                letter_index_3 = 0
                                letter_3 = letters[letter_index_3]
                elif game_state == "microgame":
                    match current_microgame:
                        case _ if current_microgame == shake_can:
                            if soda_shake:
                                if down_times < soda_shake_amount and (up_times == down_times or down_times < up_times):
                                    down_times += 1
            
            if event.key == pause_button and game_state == "microgame" or event.key == pause_button and game_state == "intermission" or play_pause_button.pressed(event.key) and paused:
                if not paused:
                    pause_start = pygame.time.get_ticks()
                    if game_state == "intermission":
                        gavinware_music.stop()
                    paused = True
                else:
                    total_paused += pygame.time.get_ticks() - pause_start
                    pause_menu_button_index = 0
                    if game_state == "intermission":
                        gavinware_music.play()
                    paused = False
        
        elif event.type == pygame.KEYUP:
            if event.key == red_button:
                if game_state == "microgame":
                    match current_microgame:
                        case _ if current_microgame == azula_vs_katara:
                            katara.image = katara.sprites[0]

            if event.key == yellow_button:
                if game_state == "microgame":
                    match current_microgame:
                        case _ if current_microgame == kuvira_vs_azula:
                            fireshield_on = False
                        case _ if current_microgame == azula_vs_katara:
                            waterfall_on = False
                            waterfall_play = False
                            katara.image = katara.sprites[0]
            
            if event.key == white_button:
                if game_state == "microgame":
                    match current_microgame:
                        case _ if current_microgame == azula_vs_katara:
                            katara.image = katara.sprites[0]
                            waterheal_on = False

        elif event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            item_scale = round(screen_width / 350)
            button_scale = round(screen_width / 400)
            small_button_scale = round(screen_width / 500)
            font_size = round(screen_width / 26)
            gavin_boombox_animation.update_size(item_scale)
            for fireball in fireball_container:
                fireball.update_size(item_scale // 2)
            for boulder in boulder_container:
                boulder.update_size(item_scale // 2)
            for shear in boulder_container:
                shear.update_size(item_scale)
            soda_can.update_size(item_scale)
            kuvira.update_size(item_scale)
            azula.update_size(item_scale)
            katara.update_size(item_scale)
            try:
                earthshield.update_size(item_scale)
            except NameError:
                pass
            try:
                waterfall.update_size(item_scale)
            except NameError:
                pass
            peasant_1.update_size(item_scale)
            peasant_2.update_size(item_scale)
            peasant_3.update_size(item_scale)
            mouse.screen = (screen_width, screen_height)
            for button in main_menu_buttons:
                button.update_size(button_scale)
            try:
                for position, button in enumerate(change_image_buttons):
                    button.rect.centerx = round(screen_width * (position+1)/5)
                    button.update_size(small_button_scale)
            except:
                pass
            font = pygame.font.Font("FFFFORWA.ttf", font_size)
            small_font = pygame.font.Font("FFFFORWA.ttf", 15)
            medium_font = pygame.font.Font("FFFFORWA.ttf", round(screen_width / 50))
    
    if not paused:
        match game_state:
            case "main_menu":
                main_menu()
                if current_music != "gavinware_menu.mp3":
                    gavinware_music.stop()
                    current_music = "gavinware_menu.mp3"
                    gavinware_music.load(current_music)
                    gavinware_music.set_volume(1.0)
                    gavinware_music.play(-1)
            case "intro":
                intro_screen()
                if current_music != "gavinware_menu.mp3":
                    gavinware_music.stop()
                    current_music = "gavinware_menu.mp3"
                    gavinware_music.load(current_music)
                    gavinware_music.set_volume(1.0)
                    gavinware_music.play(-1)
            case "intermission":
                intermission_screen()
                if not boss_mode:
                    intermission_time()
                else:
                    intermission_time(7000)
                if not boss_mode:
                    if not microgame_failed:
                        if current_music != "gavinware_win.mp3":
                            gavinware_music.stop()
                            current_music = "gavinware_win.mp3"
                            gavinware_music.load(current_music)
                            gavinware_music.set_volume(1.0)
                            gavinware_music.play(-1)
                    else:
                        if current_music != "gavinware_lose.mp3":
                            gavinware_music.stop()
                            current_music = "gavinware_lose.mp3"
                            gavinware_music.load(current_music)
                            gavinware_music.set_volume(1.0)
                            gavinware_music.play(-1)
                else:
                    if current_music != "gavinware_boss_next.mp3":
                        gavinware_music.stop()
                        current_music = "gavinware_boss_next.mp3"
                        gavinware_music.load(current_music)
                        gavinware_music.set_volume(1.0)
                        gavinware_music.play(-1)
            case "microgame":
                if not microgame_set:
                    if not boss_mode:
                        current_microgame = random.choice(microgames)
                        gavinware_music.stop()
                        current_music = random.choice(("random_1.mp3", "random_2.mp3", "random_3.mp3", "random_4.mp3", "random_5.mp3"))
                        gavinware_music.load(current_music)
                        gavinware_music.set_volume(1.0)
                        gavinware_music.play(-1)
                    else:
                        current_microgame = random.choice(bosses)
                        if current_music != "gavinware_boss.mp3":
                            gavinware_music.stop()
                            current_music = "gavinware_boss.mp3"
                            gavinware_music.load(current_music)
                            gavinware_music.set_volume(0.5)
                            gavinware_music.play(-1)
                    microgame_set = True
                elif current_microgame != None:
                    current_microgame()
            case "game_over":
                game_over_screen()
            case "set_name":
                set_name_screen()
            case "scoreboard_screen":
                scoreboard_screen()
    else:
        pause_menu()
    
    for button in main_menu_buttons:
        button.button_focus()
    
    for button in pause_menu_buttons:
        button.button_focus()
    
    fade_alpha += (2 * fade_direction)
    if fade_alpha >= 255:
        fade_alpha = 255
        fade_direction = -1
    elif fade_alpha <= 0:
        fade_alpha = 0
        fade_direction = 1

    if game_lives < 0:
        game_lives = 0
    elif game_lives > 5:
        game_lives = 5
    
    dt = clock.tick(FPS) / 1000
    pygame.display.flip()