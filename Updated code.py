from machine import Pin, SPI, PWM
import framebuf
import time
import random
import sys
from time import sleep




# Color constants
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000
YELLOW = GREEN + RED
MAGENTA = RED + BLUE
CYAN = BLUE + GREEN

class LCD_0inch96(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 160
        self.height = 80
        
        self.cs = Pin(9, Pin.OUT)
        self.rst = Pin(12, Pin.OUT)
        self.cs(1)
        self.spi = SPI(1, 10000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
        self.dc = Pin(8, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.Init()
        self.SetWindows(0, 0, self.width-1, self.height-1)
        
    def reset(self):
        self.rst(1)
        time.sleep(0.2) 
        self.rst(0)
        time.sleep(0.2)         
        self.rst(1)
        time.sleep(0.2) 
        
    def write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))

    def write_data(self, buf):
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def backlight(self, value):  # value: min:0  max:1000
        pwm = PWM(Pin(13))  # BL
        pwm.freq(1000)
        if value >= 1000:
            value = 1000
        data = int(value * 65536 / 1000)       
        pwm.duty_u16(data)  
        
    def Init(self):
        self.reset() 
        self.backlight(1000)  # Set backlight to a valid value
        # Initialize the LCD with commands
        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x21) 
        self.write_cmd(0xB1)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_cmd(0xB2)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_cmd(0xB3) 
        self.write_data(0x05)  
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_data(0x05)
        self.write_data(0x3A)
        self.write_data(0x3A)
        self.write_cmd(0xB4)
        self.write_data(0x03)
        self.write_cmd(0xC0)
        self.write_data(0x62)
        self.write_data(0x02)
        self.write_data(0x04)
        self.write_cmd(0xC1)
        self.write_data(0xC0)
        self.write_cmd(0xC2)
        self.write_data(0x0D)
        self.write_data(0x00)
        self.write_cmd(0xC3)
        self.write_data(0x8D)
        self.write_data(0x6A)   
        self.write_cmd(0xC4)
        self.write_data(0x8D) 
        self.write_data(0xEE) 
        self.write_cmd(0xC5)
        self.write_data(0x0E)    
        self.write_cmd(0xE0)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x02)
        self.write_data(0x03)
        self.write_data(0x0E)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x07)
        self.write_data(0x0A)
        self.write_data(0x12)
        self.write_data(0x27)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)
        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)
        self.write_data(0x03)
        self.write_data(0x03)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x02)
        self.write_data(0x08)
        self.write_data(0x0A)
        self.write_data(0x13)
        self.write_data(0x26)
        self.write_data(0x36)
        self.write_data(0x00)
        self.write_data(0x0D)
        self.write_data(0x0E)
        self.write_data(0x10)
        self.write_cmd(0x3A) 
        self.write_data(0x05)
        self.write_cmd(0x36)
        self.write_data(0xA8)
        self.write_cmd(0x29) 
        
    def SetWindows(self, Xstart, Ystart, Xend, Yend):  # example max:0,0,159,79
        Xstart = Xstart + 1
        Xend = Xend + 1
        Ystart = Ystart + 26
        Yend = Yend + 26
        self.write_cmd(0x2A)
        self.write_data(0x00)              
        self.write_data(Xstart)      
        self.write_data(0x00)              
        self.write_data(Xend) 
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend)
        self.write_cmd(0x2C) 
        
    def display(self):
        self.SetWindows(0, 0, self.width-1, self.height-1)       
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)        

# Colour Mixing Routine
def colour(R, G, B):  # Compact method!
    mix1 = ((R & 0xF8) * 256) + ((G & 0xFC) * 8) + ((B & 0xF8) >> 3)
    return (mix1 & 0xFF) * 256 + int((mix1 & 0xFF00) / 256)  # low nibble first

# ==== Main ====



    

# Main loop
KEY_UP = Pin(2, Pin.IN, Pin.PULL_UP)
KEY_DOWN = Pin(18, Pin.IN, Pin.PULL_UP)
KEY_LEFT = Pin(16, Pin.IN, Pin.PULL_UP)
KEY_RIGHT = Pin(20, Pin.IN, Pin.PULL_UP)
KEY_A = Pin(15, Pin.IN, Pin.PULL_UP)
KEY_B = Pin(17, Pin.IN, Pin.PULL_UP)

lcd = LCD_0inch96()  # Initialise the screen


# Modify the show_menu() function to include Pong option
BUTTON_DELAY = 0.01  # Adjust this delay as needed

is_bst = False  # Update this manually depending on the season



# Initialize UART for USB communication
uart = machine.UART(0, baudrate=115200)

# GitHub URL for updates
GITHUB_URL = "https://raw.githubusercontent.com/olly1083/nas/refs/heads/main/DashOScode"



def show_menu():   

    # Clear the screen and display the menu
    lcd.fill(BLACK)
    lcd.text("DASH OS", 50, 10, BLUE)
    lcd.text("RIGHT. Apps", 30, 40, WHITE)
    lcd.text("LEFT. Info", 30, 50, WHITE)
    lcd.text("UP. Update", 30, 60, WHITE)
    lcd.display()

    while True:
        if not KEY_RIGHT.value() == 1:  # If right button is pressed
            time.sleep(BUTTON_DELAY)  # Debounce delay
            if not KEY_RIGHT.value() == 1:  # Check again to confirm
                return "apps"  # Move to apps menu

        if not KEY_LEFT.value() == 1:  # If left button is pressed
            time.sleep(BUTTON_DELAY)  # Debounce delay
            if not KEY_LEFT.value() == 1:  # Check again to confirm
                return "info"  # Move to info menu
            
        if not KEY_UP.value() == 1:  # If UP is pressed
            time.sleep(BUTTON_DELAY)  # Debounce delay
            if not KEY_UP.value() == 1:  # Check again to confirm
                return "update"  # Move to Pong menu
            
        time.sleep(0.1)  # Short delay for loop
def apps():
    lcd.fill(BLACK)
    lcd.text("Apps", 30, 10, BLUE)
    lcd.text("A. Space Invaders", 10, 30, WHITE)
    lcd.text("B. Snake", 10, 40, WHITE)
    lcd.text("UP. Pong", 10, 50, WHITE)
    lcd.text("DOWN. PongAI", 10, 60, WHITE)
    lcd.display()

    while True:
        if not KEY_A.value() == 1:  # If A is pressed
            time.sleep(BUTTON_DELAY)  # Debounce delay
            if not KEY_A.value() == 1:  # Check again to confirm
                return "space"  # Move to Space Invaders menu
            
        if not KEY_B.value() == 1:  # If B is pressed
            time.sleep(BUTTON_DELAY)  # Debounce delay
            if not KEY_B.value() == 1:  # Check again to confirm
                return "snake"  # Move to Snake menu
            
        if not KEY_UP.value() == 1:  # If UP is pressed
            time.sleep(BUTTON_DELAY)  # Debounce delay
            if not KEY_UP.value() == 1:  # Check again to confirm
                return "pong"  # Move to Pong menu

        if not KEY_DOWN.value() == 1:  # If DOWN is pressed
            time.sleep(BUTTON_DELAY)  # Debounce delay
            if not KEY_DOWN.value() == 1:  # Check again to confirm
                return "pongAI"  # Move to PongAI menu

        time.sleep(0.1)  # Short delay for loop
        
# Function to display info
def info():
    lcd.fill(BLACK)
    lcd.text("INFO", 30, 10, BLUE)
    lcd.text("DashOS 0.0.1", 10, 30, WHITE)
    lcd.text("release", 10, 50, WHITE)
    lcd.text("By LoopDevs", 10, 70, WHITE)
    lcd.display()
    time.sleep(5)  # Display info for a while
    
def update():
    lcd.fill(BLACK)
    lcd.text("UPDATE", 30, 10, BLUE)
    lcd.text("Go To", 10, 30, WHITE)
    lcd.text("bit.ly/4fno5uv", 10, 40, WHITE)
    lcd.text("It tells you", 10, 50, WHITE) 
    lcd.text("how to update", 10, 60, WHITE)
    lcd.display()
    time.sleep(5)  # Display info for a while

# Space Invaders Game Variables
player_x = 70
player_y = 60
bullets = []
aliens = [(x, y) for x in range(10, 151, 30) for y in range(10, 40, 10)]
alien_bullets = []
bullet_color = RED
alien_bullet_color = WHITE
alien_color = GREEN
game_running = True
game_over = False
alien_direction = 1  # 1 for right, -1 for left
alien_speed = 1  # Speed of alien movement
alien_attack_delay = 0  # Counter for attack delay
alien_shooting_interval = 20  # Interval between alien shots
alien_shoot_counter = 0  # Counter for tracking alien shoot timing

# Pong Game Variables
paddle_width = 10
paddle_height = 20
ball_size = 5

# Initial positions
left_paddle_y = 30
right_paddle_y = 30
ball_x = 80
ball_y = 40
ball_direction_x = 1  # 1 for right, -1 for left
ball_direction_y = 1  # 1 for down, -1 for up

def draw_paddles():
    # Draw left paddle
    lcd.fill_rect(155, left_paddle_y, paddle_width, paddle_height, WHITE)
    # Draw right paddle
    lcd.fill_rect(0, right_paddle_y, paddle_width, paddle_height, WHITE)

def draw_ball():
    lcd.fill_rect(ball_x, ball_y, ball_size, ball_size, WHITE)

def update_ball():
    global ball_x, ball_y, ball_direction_x, ball_direction_y

    # Move the ball
    ball_x += ball_direction_x * 2  # Adjust speed as needed
    ball_y += ball_direction_y * 2

    # Check for collisions with the top and bottom
    if ball_y <= 0 or ball_y >= 80 - ball_size:
        ball_direction_y *= -1  # Reverse direction

    # Check for collisions with paddles
    if (ball_x <= paddle_width and 
        left_paddle_y <= ball_y <= left_paddle_y + paddle_height) or \
       (ball_x >= 160 - paddle_width - ball_size and 
        right_paddle_y <= ball_y <= right_paddle_y + paddle_height):
        ball_direction_x *= -1  # Reverse direction

    # Reset ball if it goes out of bounds
    if ball_x < 0 or ball_x > 160:
        ball_x, ball_y = 80, 40  # Reset ball position
        ball_direction_x *= -1  # Change direction

def pong_game():
    global left_paddle_y, right_paddle_y
    while game_running:
        lcd.fill(BLACK)  # Clear the screen
        draw_paddles()   # Draw paddles
        draw_ball()      # Draw ball
        lcd.display()    # Show the frame

        # Paddle controls
        if not KEY_UP.value() == 1 and right_paddle_y > 0:  # Move right paddle up
            right_paddle_y -= 2
        if not KEY_DOWN.value() == 1 and right_paddle_y < 80 - paddle_height:  # Move right paddle down
            right_paddle_y += 2
        if not KEY_A.value() == 1 and left_paddle_y > 0:  # Move left paddle up
            left_paddle_y -= 2
        if not KEY_B.value() == 1 and left_paddle_y < 80 - paddle_height:  # Move left paddle down
            left_paddle_y += 2

        update_ball()  # Update ball position

        time.sleep(0.05)  # Control the speed of the game

# Modify the show_menu() function to include Pong option


paddle_width = 5
paddle_height = 20
ball_size = 6
paddle_speed = 2
ball_speed_x = 2
ball_speed_y = 2

# Paddle positions
left_paddle_y = 30
right_paddle_y = 30
ball_x = 80
ball_y = 40

# AI Control Variables
ai_speed = 2  # Speed of AI paddle movement

def draw_paddles2():
    lcd.fill_rect(155, left_paddle_y, paddle_width, paddle_height, WHITE)  # Left paddle
    lcd.fill_rect(0, right_paddle_y, paddle_width, paddle_height, WHITE)  # Right paddle

def draw_ball2():
    lcd.fill_rect(ball_x, ball_y, ball_size, ball_size, WHITE)  # Ball

def move_ball2():
    global ball_x, ball_y, ball_direction_x, ball_direction_y

    # Move the ball
    ball_x += ball_direction_x * 2  # Adjust speed as needed
    ball_y += ball_direction_y * 2

    # Check for collisions with the top and bottom
    if ball_y <= 0 or ball_y >= 80 - ball_size:
        ball_direction_y *= -1  # Reverse direction

    # Check for collisions with paddles
    if (ball_x <= paddle_width and 
        left_paddle_y <= ball_y <= left_paddle_y + paddle_height) or \
       (ball_x >= 160 - paddle_width - ball_size and 
        right_paddle_y <= ball_y <= right_paddle_y + paddle_height):
        ball_direction_x *= -1  # Reverse direction

    # Reset ball if it goes out of bounds
    if ball_x < 0 or ball_x > 160:
        ball_x, ball_y = 80, 40  # Reset ball position
        ball_direction_x *= -1  # Change direction

def ai_control():
    global left_paddle_y
    if ball_y < left_paddle_y:
        left_paddle_y -= ai_speed  # Move AI paddle up
    if ball_y > left_paddle_y + paddle_height:
        left_paddle_y += ai_speed  # Move AI paddle down

    # Keep the paddle within screen bounds
    if left_paddle_y < 0:
        left_paddle_y = 0
    if left_paddle_y > 80 - paddle_height:  # Adjust for paddle height
        left_paddle_y = 80 - paddle_height

def pong_game2():
    global left_paddle_y, right_paddle_y
    while game_running:

        lcd.fill(BLACK)  # Clear the screen
        ai_control()     # Move the AI paddle
        move_ball2()      # Update ball position
        draw_paddles2()   # Draw paddles
        draw_ball2()      # Draw ball
        lcd.display()    # Show the frame
        time.sleep(0.05) # Control the game speed
        

        # Paddle controls
        if not KEY_UP.value() == 1 and right_paddle_y > 0:  # Move right paddle up
            right_paddle_y -= 2
        if not KEY_DOWN.value() == 1 and right_paddle_y < 80 - paddle_height:  # Move right paddle down
            right_paddle_y += 2

        update_ball()  # Update ball position

        time.sleep(0.05)  # Control the speed of the game
        
# Game Loop
while True:
    choice = show_menu()
    
    if choice == "info":         
        info()
        lcd.display()
        
    if choice == "update":         
        update()
        lcd.display()
        
    elif choice == "apps":
        apps()
        while True:
            choice = apps()
            if choice == "space":

                
                # Space Invaders Game Code Here
                # Draw aliens
                def check_collisions():
                    global bullets, aliens
                    for bullet in bullets[:]:
                        for alien in aliens[:]:
                            if (bullet[0] >= alien[0] and bullet[0] <= alien[0] + 20 and
                                    bullet[1] >= alien[1] and bullet[1] <= alien[1] + 10):
                                bullets.remove(bullet)
                                aliens.remove(alien)
                                break
                def shoot_alien_bullets():
                    global alien_shoot_counter, alien_bullets
                    # Each alien has a chance to shoot
                    for alien in aliens:
                        if random.randint(0, alien_shooting_interval) == 0:  # Random chance to shoot
                            alien_bullets.append([alien[0] + 6, alien[1] + 10])  # Spawn bullet just below the alien

                def draw_alien_bullets():
                    for bullet in alien_bullets:
                        lcd.fill_rect(bullet[0], bullet[1], 2, 5, alien_bullet_color)

                def move_alien_bullets():
                    global alien_bullets
                    for bullet in alien_bullets[:]:
                        bullet[1] += 2  # Move bullet downwards
                        if bullet[1] > 80:  # If bullet goes out of bounds
                            alien_bullets.remove(bullet)

                def check_alien_bullet_collisions():
                    global game_over, player_x, player_y
                    for bullet in alien_bullets[:]:
                        # Check if the bullet's position collides with the player's position
                        if (bullet[0] >= player_x and bullet[0] <= player_x + 15 and
                            bullet[1] >= player_y and bullet[1] <= player_y + 10):
                            game_over = True  # Player hit by alien bullet
                        break
                    
                def game_over_screen():
                    lcd.fill(BLACK)
                    lcd.text("GAME OVER!", 30, 30, RED)
                    lcd.text("Press A to restart", 30, 50, WHITE)
                    lcd.display()
            
                    while True:
                        if not KEY_A.value() == 1:  # Restart game
                            machine.reset()  # Reset the machine to restart the game
                        time.sleep(0.1)
                
                
                def draw_aliens():
                    for alien in aliens:
                        lcd.fill_rect(alien[0], alien[1], 15, 10, alien_color)

                def draw_player():
                    lcd.fill_rect(player_x, player_y, 15, 10, WHITE)

                def draw_bullets():
                    for bullet in bullets:
                        lcd.fill_rect(bullet[0], bullet[1], 2, 5, bullet_color)

                def game_over_screen():
                    lcd.fill(BLACK)
                    lcd.text("GAME OVER!", 30, 30, RED)
                    lcd.display()
                    time.sleep(2)
                    machine.reset()

                # Game Loop
                while True:
                    choice = apps()
                    if choice == "space":
                        game_running = True
                        while game_running:
                            # Player shooting logic
                            if not KEY_A.value() == 1:  # If A key is pressed
                                bullets.append([player_x + 6, player_y - 5])  # Fire player bullet
                                time.sleep(0.2)  # Delay to avoid multiple bullet firing

                            # Move player
                            if not KEY_LEFT.value() == 1 and player_x > 0:
                                player_x -= 2
                            if not KEY_RIGHT.value() == 1 and player_x < 145:
                                player_x += 2

                            # Move player bullets
                            for bullet in bullets[:]:
                                bullet[1] -= 2
                                if bullet[1] < 0:
                                    bullets.remove(bullet)

                            # Alien shooting logic
                            alien_shoot_counter += 1
                            if alien_shoot_counter >= alien_shooting_interval:
                                shoot_alien_bullets()  # Allow aliens to shoot
                                alien_shoot_counter = 0  # Reset counter

                            # Move alien bullets
                            move_alien_bullets()  # Move bullets shot by aliens

                            # Clear screen and redraw
                            lcd.fill(BLACK)
                            draw_aliens()
                            draw_player()
                            draw_bullets()
                            draw_alien_bullets()  # Draw alien bullets
                            lcd.display()

                            # Check for collisions
                            check_collisions()  # Check for player bullet collisions
                            check_alien_bullet_collisions()  # Check for collisions with alien bullets

                            # Game over condition (if player is hit)
                            if game_over:
                                game_over_screen()  # Show game over screen
                                machine.reset()  # Exit the game loop
                        # Show game over screen
                        game_over_screen()
                pass  # Placeholder for Space Invaders code
            elif choice == "snake":
                        # Snake Game Variables
                snake = [(80, 40), (70, 40), (60, 40)]  # Initial snake position
                snake_direction = (10, 0)  # Moving right
                food_position = (random.randint(0, 15) * 10, random.randint(0, 7) * 10)  # Random food position
                score = 0

                def draw_snake():
                    for segment in snake:
                        lcd.fill_rect(segment[0], segment[1], 10, 10, GREEN)  # Draw the snake segments

                def draw_food():
                    lcd.fill_rect(food_position[0], food_position[1], 10, 10, RED)  # Draw the food

                def update_snake():
                    global food_position, score
                    head_x, head_y = snake[0]
                    new_head_x = head_x + snake_direction[0]
                    new_head_y = head_y + snake_direction[1]

                    # Check for collisions with walls
                    if new_head_x < 0 or new_head_x >= 160 or new_head_y < 0 or new_head_y >= 80 or (new_head_x, new_head_y) in snake:
                        return False  # Game over

                    snake.insert(0, (new_head_x, new_head_y))  # Move the snake by adding a new head

                    # Check for food collision
                    if (new_head_x, new_head_y) == food_position:
                        score += 1  # Increase the score
                        food_position = (random.randint(0, 15) * 10, random.randint(0, 7) * 10)  # New food position
                    else:
                        snake.pop()  # Remove the tail if no food is eaten

                    return True

                def snake_game():
                    global snake_direction, game_running
                    while game_running:
                        lcd.fill(BLACK)  # Clear the screen
                        draw_snake()  # Draw the snake
                        draw_food()  # Draw the food
                        lcd.text("Score: {}".format(score), 5, 5, WHITE)  # Display the score
                        lcd.display()  # Show the frame
                        if not KEY_UP.value() == 1 and snake_direction != (0, 10):  # If UP key is pressed and not moving down
                            snake_direction = (0, -10)
                        if not KEY_DOWN.value() == 1 and snake_direction != (0, -10):  # If DOWN key is pressed and not moving up
                            snake_direction = (0, 10)
                        if not KEY_LEFT.value() == 1 and snake_direction != (10, 0):  # If LEFT key is pressed and not moving right
                            snake_direction = (-10, 0)
                        if not KEY_RIGHT.value() == 1 and snake_direction != (-10, 0):  # If RIGHT key is pressed and not moving left
                            snake_direction = (10, 0)

                        if not update_snake():  # Update the snake and check for game over
                            lcd.fill(BLACK)
                            lcd.text("Game Over!", 50, 30, WHITE)
                            lcd.text("Score: {}".format(score), 50, 50, WHITE)
                            lcd.display()
                            time.sleep(2)
                            machine.reset()
                        
                        time.sleep(0.1)  # Control the speed of the game
                
                snake_game()
                
                pass
            elif choice == "pong":
                pong_game()  # Start Pong game
                
                pass
            elif choice == "pongAI":
                pong_game2()  # Start Pong game
                
                pass
            elif choice == "apps":
                apps()
                lcd.display()
                
                pass
            elif choice == "info":
                info()
                lcd.display()
                

                

                
                pass
            elif choice == "back":
                show_menu()
                lcd.display() 
        while True:
            choice = apps()
            if choice == "space":

                
                # Space Invaders Game Code Here
                # Draw aliens
                def check_collisions():
                    global bullets, aliens
                    for bullet in bullets[:]:
                        for alien in aliens[:]:
                            if (bullet[0] >= alien[0] and bullet[0] <= alien[0] + 20 and
                                    bullet[1] >= alien[1] and bullet[1] <= alien[1] + 10):
                                bullets.remove(bullet)
                                aliens.remove(alien)
                                break
                def shoot_alien_bullets():
                    global alien_shoot_counter, alien_bullets
                    # Each alien has a chance to shoot
                    for alien in aliens:
                        if random.randint(0, alien_shooting_interval) == 0:  # Random chance to shoot
                            alien_bullets.append([alien[0] + 6, alien[1] + 10])  # Spawn bullet just below the alien

                def draw_alien_bullets():
                    for bullet in alien_bullets:
                        lcd.fill_rect(bullet[0], bullet[1], 2, 5, alien_bullet_color)

                def move_alien_bullets():
                    global alien_bullets
                    for bullet in alien_bullets[:]:
                        bullet[1] += 2  # Move bullet downwards
                        if bullet[1] > 80:  # If bullet goes out of bounds
                            alien_bullets.remove(bullet)

                def check_alien_bullet_collisions():
                    global game_over, player_x, player_y
                    for bullet in alien_bullets[:]:
                        # Check if the bullet's position collides with the player's position
                        if (bullet[0] >= player_x and bullet[0] <= player_x + 15 and
                            bullet[1] >= player_y and bullet[1] <= player_y + 10):
                            game_over = True  # Player hit by alien bullet
                        break
                    
                def game_over_screen():
                    lcd.fill(BLACK)
                    lcd.text("GAME OVER!", 30, 30, RED)
                    lcd.text("Press A to restart", 30, 50, WHITE)
                    lcd.display()
            
                    while True:
                        if not KEY_A.value() == 1:  # Restart game
                            machine.reset()  # Reset the machine to restart the game
                        time.sleep(0.1)
                
                
                def draw_aliens():
                    for alien in aliens:
                        lcd.fill_rect(alien[0], alien[1], 15, 10, alien_color)

                def draw_player():
                    lcd.fill_rect(player_x, player_y, 15, 10, WHITE)

                def draw_bullets():
                    for bullet in bullets:
                        lcd.fill_rect(bullet[0], bullet[1], 2, 5, bullet_color)

                def game_over_screen():
                    lcd.fill(BLACK)
                    lcd.text("GAME OVER!", 30, 30, RED)
                    lcd.display()
                    time.sleep(2)
                    machine.reset()

                # Game Loop
                while True:
                    choice = apps()
                    if choice == "space":
                        game_running = True
                        while game_running:
                            # Player shooting logic
                            if not KEY_A.value() == 1:  # If A key is pressed
                                bullets.append([player_x + 6, player_y - 5])  # Fire player bullet
                                time.sleep(0.2)  # Delay to avoid multiple bullet firing

                            # Move player
                            if not KEY_LEFT.value() == 1 and player_x > 0:
                                player_x -= 2
                            if not KEY_RIGHT.value() == 1 and player_x < 145:
                                player_x += 2

                            # Move player bullets
                            for bullet in bullets[:]:
                                bullet[1] -= 2
                                if bullet[1] < 0:
                                    bullets.remove(bullet)

                            # Alien shooting logic
                            alien_shoot_counter += 1
                            if alien_shoot_counter >= alien_shooting_interval:
                                shoot_alien_bullets()  # Allow aliens to shoot
                                alien_shoot_counter = 0  # Reset counter

                            # Move alien bullets
                            move_alien_bullets()  # Move bullets shot by aliens

                            # Clear screen and redraw
                            lcd.fill(BLACK)
                            draw_aliens()
                            draw_player()
                            draw_bullets()
                            draw_alien_bullets()  # Draw alien bullets
                            lcd.display()

                            # Check for collisions
                            check_collisions()  # Check for player bullet collisions
                            check_alien_bullet_collisions()  # Check for collisions with alien bullets

                            # Game over condition (if player is hit)
                            if game_over:
                                game_over_screen()  # Show game over screen
                                machine.reset()  # Exit the game loop
                        # Show game over screen
                        game_over_screen()
                pass  # Placeholder for Space Invaders code
            elif choice == "snake":
                        # Snake Game Variables
                snake = [(80, 40), (70, 40), (60, 40)]  # Initial snake position
                snake_direction = (10, 0)  # Moving right
                food_position = (random.randint(0, 15) * 10, random.randint(0, 7) * 10)  # Random food position
                score = 0

                def draw_snake():
                    for segment in snake:
                        lcd.fill_rect(segment[0], segment[1], 10, 10, GREEN)  # Draw the snake segments

                def draw_food():
                    lcd.fill_rect(food_position[0], food_position[1], 10, 10, RED)  # Draw the food

                def update_snake():
                    global food_position, score
                    head_x, head_y = snake[0]
                    new_head_x = head_x + snake_direction[0]
                    new_head_y = head_y + snake_direction[1]

                    # Check for collisions with walls
                    if new_head_x < 0 or new_head_x >= 160 or new_head_y < 0 or new_head_y >= 80 or (new_head_x, new_head_y) in snake:
                        return False  # Game over

                    snake.insert(0, (new_head_x, new_head_y))  # Move the snake by adding a new head

                    # Check for food collision
                    if (new_head_x, new_head_y) == food_position:
                        score += 1  # Increase the score
                        food_position = (random.randint(0, 15) * 10, random.randint(0, 7) * 10)  # New food position
                    else:
                        snake.pop()  # Remove the tail if no food is eaten

                    return True

                def snake_game():
                    global snake_direction, game_running
                    while game_running:
                        lcd.fill(BLACK)  # Clear the screen
                        draw_snake()  # Draw the snake
                        draw_food()  # Draw the food
                        lcd.text("Score: {}".format(score), 5, 5, WHITE)  # Display the score
                        lcd.display()  # Show the frame
                        if not KEY_UP.value() == 1 and snake_direction != (0, 10):  # If UP key is pressed and not moving down
                            snake_direction = (0, -10)
                        if not KEY_DOWN.value() == 1 and snake_direction != (0, -10):  # If DOWN key is pressed and not moving up
                            snake_direction = (0, 10)
                        if not KEY_LEFT.value() == 1 and snake_direction != (10, 0):  # If LEFT key is pressed and not moving right
                            snake_direction = (-10, 0)
                        if not KEY_RIGHT.value() == 1 and snake_direction != (-10, 0):  # If RIGHT key is pressed and not moving left
                            snake_direction = (10, 0)

                        if not update_snake():  # Update the snake and check for game over
                            lcd.fill(BLACK)
                            lcd.text("Game Over!", 50, 30, WHITE)
                            lcd.text("Score: {}".format(score), 50, 50, WHITE)
                            lcd.display()
                            time.sleep(2)
                            machine.reset()
                        
                        time.sleep(0.1)  # Control the speed of the game
                
                snake_game()
                
                pass
            elif choice == "pong":
                pong_game()  # Start Pong game
                
                pass
            elif choice == "pongAI":
                pong_game2()  # Start Pong game
                
                pass
            elif choice == "apps":
                apps()
                lcd.display()
                
                pass
            elif choice == "info":
                info()
                lcd.display()
                
                pass
            elif choice == "update":
                update()
                lcd.display()
                





