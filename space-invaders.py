import pygame
import sys
import math
import os
import random
pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = ("0, 25")


def main():
    """
    Main Program
    """
    # Sets a clock
    fps = 30
    fpsClock = pygame.time.Clock()
    
    # Initializes screen depending on resolution of monitor
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w
    screen_height = infoObject.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("SPACE INVADERS")
    
    # Sets the initial location
    location = "title"

    # Initial variables
    ship_x = screen.get_width() / 2 - 50
    ship_y = screen.get_height() / 5 * 4
    ship_width = 100
    ship_height = 100
    bullet_x = []
    bullet_y = []
    alien_bullet_x = []
    alien_bullet_y = []
    level = 0
    alien_width = 80
    alien_height = 80
    start_location = screen.get_width() / 8 * 2.25
    aliens = spawn_aliens(level, alien_width, alien_height, start_location)
    coordinates = create_coordinates(screen, aliens, start_location, alien_width, alien_height)
    score = 0
    alien_direction = random.choice(["left", "right"])
    bullet_flag = False
    counter = 0
    direction = "stop"
    start_time = 0
    shoot_bullets = False
    message = "GAME OVER"
    
    # Loads fonts
    info_font = pygame.font.Font("virgo.ttf", 50)
    title_font = pygame.font.Font("virgo.ttf", 100)
    small_font = pygame.font.Font("virgo.ttf", 25)
    medium_font = pygame.font.Font("virgo.ttf", 30)
    
    # Loads images
    bulletImg = pygame.image.load("img/bullet.png")
    moonImg = pygame.image.load("img/moon.jpg").convert()
    shipImg = pygame.image.load("img/ship.png")
    alienImg = pygame.image.load("img/alien.png")
    alien2Img = pygame.image.load("img/alien1.png")
    alienBulletImg = pygame.image.load("img/alien_bullet.png")
    explosionImg = pygame.image.load("img/explosion.png")
    
    # Main game loop
    while True:
        # Displays the title page
        if location == "title":
            location = title_page(screen, moonImg, small_font, medium_font, title_font)
        # Plays the game
        elif location == "play":
            # Draws the background
            draw_image(screen, 0, 0, screen.get_width(), screen.get_height(), moonImg)

            # Displays score and level
            display_info(screen, score, level, info_font)

            # Draws the ship
            draw_ship(screen, ship_x, ship_y, ship_width, ship_height, shipImg)

            # Moves the ship
            ship_x = move_ship(screen, ship_x, direction)
            
            # Moves aliens
            start_location, alien_direction = move_alien(screen, start_location, coordinates, alien_width, alien_direction)
            
            # Draws aliens
            counter = draw_alien(screen, aliens, alienImg, alien2Img, alien_width, alien_height, start_location, counter)

            # Adds bullets to the screen
            start_time, bullet_flag = add_bullet(shoot_bullets, bullet_flag, bullet_x, bullet_y, ship_x, ship_y, start_time)
            
            # Checks for bullet shots and updates score if impact
            score = shoot(screen, bullet_x, bullet_y, bulletImg, coordinates, aliens, score, alien_width, alien_height)
            
            # Changes round if necessary
            level, aliens = change_round(screen, aliens, level, coordinates, start_location, alien_width, alien_height)

            # Updates coordinates
            coordinates = create_coordinates(screen, aliens, start_location, alien_width, alien_height)
            
            # Ends the game
            if level > 5 or alien_shoot(screen, level, coordinates, alien_bullet_x, alien_bullet_y, ship_x, ship_y, ship_width, ship_height, alienBulletImg):
                if level > 5:
                    message = "YOU WON!"
                else:
                    message = "GAME OVER"
                level = 1
                aliens = spawn_aliens(level, alien_width, alien_height, start_location)
                ship_x = screen.get_width() / 2 - 50
                ship_y = screen.get_height() / 5 * 4
                bullet_x = []
                bullet_y = []
                alien_bullet_x = []
                alien_bullet_y = []
                location = "end"
        # Ends the game
        elif location == "end":
            location, score, message = end_game(screen, score, message, info_font, title_font, medium_font, small_font)
        # Displays the instructions
        elif location == "instructions":
            location = rules(screen, moonImg, small_font, medium_font, title_font)
        
        # Keeps screen open until X is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key != pygame.K_SPACE:
                direction = "stop"
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                shoot_bullets = False
            if event.type == pygame.KEYDOWN:
                # Moves left
                if event.key == pygame.K_LEFT:
                    direction = "left"
                # Moves right
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                # Shoots a bullet
                if event.key == pygame.K_SPACE:
                    shoot_bullets = True
            
        # Updates the display
        pygame.display.update()

        # Makes sure animation doesn't go over 30 FPS
        fpsClock.tick(fps)


def title_page(screen, spaceImg, small_font, medium_font, title_font):
    """
    Displays the title page
    """
    # Displays the background
    screen.blit(spaceImg, (0, 0))

    # Displays game title
    white = (255, 255, 255)
    title_text = title_font.render("SPACE INVADERS", True, white)
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 4))
    screen.blit(title_text, title_rect)

    # Color for buttons
    black = (0, 0, 0)
    gray = (50, 50, 50)
    
    # Draws the buttons
    play = button(screen, "PLAY", medium_font, screen.get_width() - 300, screen.get_height() / 2, 250, 80, black, gray, white)
    instructions = button(screen, "INSTRUCTIONS", small_font, screen.get_width() - 300, screen.get_height() / 2 + 100, 250, 80, black, gray, white)

    # Returns a new location
    if play:
        return "play"
    elif instructions:
        return "instructions"
    else:
        return "title"


def rules(screen, spaceImg, small_font, medium_font, title_font):
    """
    Displays the instructions
    """
    # Displays the background
    screen.blit(spaceImg, (0, 0))

    # Displays game title
    white = (255, 255, 255)
    display_text(screen, ["INSTRUCTIONS"], title_font, white, screen.get_width() / 2, screen.get_height() / 4, 15)
    
    # Displays instructions
    instructions_text = ["THE OBJECTIVE OF THE GAME IS TO: ", "1. SHOOT ALIENS", "2. GET A HIGH SCORE"]
    display_text(screen, instructions_text, small_font, white, screen.get_width() / 2, screen.get_height() / 2, 15)

    # Displays controls
    c_text = ["MOVE: LEFT ARROW (LEFT), RIGHT ARROW (RIGHT)", "SHOOT: SPACE"]
    display_text(screen, c_text, small_font, white, screen.get_width() / 2, screen.get_height() / 4 * 3, 15)

    # Colors for the buttons
    black = (0, 0, 0)
    gray = (50, 50, 50)
    
    # Displays a button to play the game
    play = button(screen, "PLAY", medium_font, screen.get_width() - 300, screen.get_height() / 2, 250, 80, black, gray, white)

    # Returns a new location
    if play:
        return "play"
    else:
        return "instructions"


def change_round(screen, aliens, level, coordinates, start_location, alien_width, alien_height):
    """
    Changes the round if necessary
    """
    # Checks if all aliens are dead
    aliens_dead = True
    for row in aliens:
        for alien in row:
            if alien == 1:
                aliens_dead = False

    # Changes the round
    if aliens_dead:
        level += 1
        aliens = spawn_aliens(level, alien_width, alien_height, start_location)

    return level, aliens


def end_game(screen, score, message, info_font, title_font, medium_font, small_font):
    """
    Displays the end game screen
    """
    # Background color
    black = (0, 0, 0)
    screen.fill(black)

    # Displays the game over message
    white = (255, 255, 255)
    display_text(screen, [message], title_font, white, screen.get_width() / 2, screen.get_height() / 2, 15)
    
    # Displays the score
    score_text = ["SCORE: " + str(score)]
    display_text(screen, score_text, info_font, white, screen.get_width() / 2, screen.get_height() / 2 + 75, 15)

    # Displays buttons
    gray = (50, 50, 50)
    button_width = 250
    play = button(screen, "PLAY AGAIN", small_font, screen.get_width() / 2 - button_width / 2, screen.get_height() / 4 * 3, button_width, 80, white, gray, black)
    title = button(screen, "QUIT", medium_font, screen.get_width() / 2 - button_width / 2, screen.get_height () / 4 * 3 + 100, button_width, 80, white, gray, black)

    # Changes the location
    if play:
        score = 0
        return "play", score, message
    elif title:
        score = 0
        return "title", score, message
    else:
        return "end", score, message
    

def display_info(screen, score, level, info_font):
    """
    Displays the score
    """
    # Variables for text
    white = (255, 255, 255)
    
    # Displays the score text
    score_text = ["CURRENT SCORE: " + str(score)]
    display_text(screen, score_text, info_font, white, 15, 25, 15)

    # Displays the level text
    level_text = ["CURRENT LEVEL: " + str(level)]
    display_text(screen, level_text, info_font, white, 15, 75, 15)


def draw_ship(screen, ship_x, ship_y, ship_width, ship_height, shipImg):
    """
    Draws the ship
    """
    # Displays the ship
    draw_image(screen, ship_x, ship_y, ship_width, ship_height, shipImg)


def move_ship(screen, ship_x, direction):
    """
    Moves the ship
    """
    # Moves left
    if direction == "left":
        # Moves ship to other side of screen
        if ship_x <= -100:
            ship_x = screen.get_width()
        ship_x -= 10
    # Moves right
    if direction == "right":
        # Moves ship to other side of screen
        if ship_x >= screen.get_width():
            ship_x = -100
        ship_x += 10

    return ship_x


def spawn_aliens(alien_rows, alien_width, alien_height, start_location):
    """
    Spawns the aliens
    """
    # Spawns aliens
    aliens = []
    for i in range(alien_rows):
        # 1 = alien
        aliens.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    return aliens


def create_coordinates(screen, aliens, start_location, alien_width, alien_height):
    """
    Updates the coordinates for the aliens
    """
    # Adds coordinates of alien to a list
    coordinates = []
    for i in range(len(aliens)):
        row_coordinates = []
        for j in range(len(aliens[i])):
            if aliens[i][j] == 1:
                row_coordinates.append((start_location + alien_width * j, alien_height * i))
            else:
                row_coordinates.append((0, screen.get_height()))
        coordinates.append(row_coordinates)

    return coordinates

  
def draw_alien(screen, aliens, alienImg, alien2Img, alien_width, alien_height, start_location, counter):
    """
    Draws the aliens
    """
    # Draws the aliens
    for i in range(len(aliens)):
        for j in range(len(aliens[i])):
            if aliens[i][j] == 1:
                if counter < 6:
                    draw_image(screen, start_location + alien_width * j, alien_height * i, alien_width, alien_height, alienImg)
                elif counter < 12:
                    draw_image(screen, start_location + alien_width * j, alien_height * i, alien_width, alien_height, alien2Img)
    

    # Resets animation counter if needed
    counter += 1
    if counter == 12:
        counter = 0
    
    return counter


def move_alien(screen, start_location, coordinates, alien_width, alien_direction):
    """
    Moves the aliens
    """
    # Picks a direction for movement
    for i in range(len(coordinates)):
        for j in range(len(coordinates[i])):
            if coordinates[i][j][0] > screen.get_width() - alien_width:
                alien_direction = "left"
            elif coordinates[i][j][0] < 0:
                alien_direction = "right"

    # Moves right
    if alien_direction == "right":
        start_location += 10
    # Moves left
    else:
        start_location -= 10

    return start_location, alien_direction


def alien_shoot(screen, level, coordinates, x, y, ship_x, ship_y, ship_width, ship_height, bulletImg):
    """
    Allows aliens to shoot
    """
    end_game = False
    removeBullet = -1
    
    # Picks alien to shoot
    pick_alien_row = random.randint(0, 15 * level)
    pick_alien = random.randint(0, 9)
    if pick_alien_row < len(coordinates):
        if coordinates[pick_alien_row][pick_alien][1] != screen.get_height():
            x.append(coordinates[pick_alien_row][pick_alien][0])
            y.append(coordinates[pick_alien_row][pick_alien][1])
        
    # Draws each bullet
    for i in range(len(x)):
        draw_image(screen, x[i], y[i], 15, 30, bulletImg)
        y[i] += 10

        # Ends game if bullet made impact
        if ship_check_impact(screen, x[i], y[i], ship_x, ship_y, ship_width, ship_height):
            removeBullet = i
            end_game = True
        # Checks if bullet is offscreen
        if y[i] > screen.get_height() + bulletImg.get_height():
            removeBullet = i

    # Removes bullet
    if removeBullet > -1:
        x.pop(removeBullet)
        y.pop(removeBullet)

    return end_game
        

def ship_check_impact(screen, bullet_x, bullet_y, ship_x, ship_y, ship_width, ship_height):
    """
    Checks for bullet impact on ship
    """
    # Ends game if bullet hits ship
    if ship_x + ship_width > bullet_x > ship_x and ship_y + ship_height > bullet_y > ship_y:
        return True


def check_impact(screen, bullet_x, bullet_y, coordinates, aliens, alien_width, alien_height):
    """
    Checks for impact of bullet on alien
    """
    # Loops through coordinates
    for i in range(len(coordinates)):
        for j in range(len(coordinates[i])):
            # Returns true and removes alien if bullet made impact
            if coordinates[i][j][0] + alien_width > bullet_x > coordinates[i][j][0] and coordinates[i][j][1] + alien_height > bullet_y > coordinates[i][j][1]:
                coordinates[i][j] = (0, screen.get_height())
                aliens[i][j] = 0
                return True
    return False


def add_bullet(shoot_bullets, bullet_flag, bullet_x, bullet_y, ship_x, ship_y, start_time):
    """
    Adds a bullet to the screen
    """
    # Checks if space key is held
    if shoot_bullets:
        # Adds the bullet if timer is over
        if bullet_flag == False:
            # Timer to delay bullets
            start_time = pygame.time.get_ticks()
            bullet_flag = True

            # Adds a bullet to the screen
            bullet_x.append(ship_x + 25)
            bullet_y.append(ship_y)

        # Checks when timer is over
        if bullet_flag == True and pygame.time.get_ticks() - start_time >= 500:
            bullet_flag = False

    return start_time, bullet_flag


def shoot(screen, x, y, bulletImg, coordinates, aliens, score, alien_width, alien_height):
    """
    Shoots bullets
    """
    removeBullet = -1
    
    # Draws each bullet
    for i in range(len(x)):
        draw_image(screen, x[i], y[i], 15, 30, bulletImg)
        y[i] -= 10

        # Picks bullet to be removed
        if check_impact(screen, x[i], y[i], coordinates, aliens, alien_width, alien_height):
            score += 1
            removeBullet = i
        if y[i] < -50:
            removeBullet = i
    
    # Removes bullet if needed
    if removeBullet > - 1:
        x.pop(removeBullet)
        y.pop(removeBullet)

    return score

        
def draw_image(screen, x, y, scaled_width, scaled_height, image):
    """
    Draws an image and scales it to an appropriate width/height
    """
    # Loads images
    smaller_image = pygame.transform.scale(image, (scaled_width, scaled_height))

    # Displays the image
    screen.blit(smaller_image, (x, y))

            
def display_text(screen, text, font, color, x, y, margin):
    """
    Allows text to be displayed multiline.
    Text must be passed in through a list.
    """
    rendered_text = []

    # Renders all the text and appends it into a list
    for line in text:
        rendered_text.append(font.render(line, True, color))

    # Blits the line onto the screen
    for line in range(len(rendered_text)):
        line_rect = rendered_text[line].get_rect(center=(x, y + line * rendered_text[line].get_height() + margin * line))
        screen.blit(rendered_text[line], line_rect)


def button(screen, message, font, x, y, width, height, color, hover_color, text_color):
    """
    Checks for button presses and hovers
    """
    # Gets position of mouse cursor
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    
    # Checks if button is clicked
    if x + width > mouse_x > x and y + height > mouse_y > y:
        # Draws a button with a different color when hovered
        pygame.draw.rect(screen, hover_color, [x, y, width, height])

        # Checks if mouse is clicked
        if pygame.mouse.get_pressed()[0]:
            return True
    else:
        # Draws a normal button
        pygame.draw.rect(screen, color, [x, y, width, height])
                         
    # Displays text in button
    display_text(screen, [message], font, text_color, x + width / 2, y + height / 2, 15)

    return False

    
if __name__ == "__main__":
    main()

