import pygame
import os

pygame.font.init() #Font mixer
pygame.mixer.init() #Sound mixer for sound effect
pygame.init() #instantiation pygame app

WIDTH, HEIGHT = 900, 500 #Width and height of the sceren we're going to open
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("War Spaceship") #Sets the caption for the window name

#COLOR CODES, refer the docs [RGB format]
COLOR_WHITE = (255, 255, 255) #If you mix red, green, blue we get white
COLOR_BLACK = (0, 0, 0) #no RGB
COLOR_RED  = (255, 0, 0) #only red
COLOR_YELLOW = (255, 255, 0) #Red and green gives yellow
COLOR_MAGENTA = (255, 0, 255) 


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) #The x coordinate of the border will start from the width/2-5 pixel which will be in the middle of the screen 

FPS = 60 #The loop will keep running at a different speed for each computer and this means it may take more time or less time based on the computers performance #This is why we use FPS

VEL = 5 #Velocity of spaceship
BULLET_VEL = 7 #Bullet Speed
BULLET_NUM_MAX = 3 #No. of max bullets

#Both the below variables are for creating 2 different USEREVENTS having same usercode, thats why we add a different number to both
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40 #Aspect Ratio of both spaceships

#YELLOW SPACESHIP FORMATTING
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Pygame_Rocket', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

#RED SPACESHIP FORMATTING
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Pygame_Rocket', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Pygame_Rocket', 'space.png')), (WIDTH, HEIGHT)) #We always, load, transform and scale the image to make sure it fits in our window

HEALTH_FONT = pygame.font.SysFont('comicsans', 40) 
WINNER_FONT = pygame.font.SysFont('cambria', 100, bold=True)

#OPENING AND PLAYING SOUND EFFECTS
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Pygame_Rocket', 'Grenade+1.mp3'))
BULLET_FIRE = pygame.mixer.Sound(os.path.join('Pygame_Rocket', 'Gun+Silencer.mp3'))
WINNER_SOUND_EFFECT = pygame.mixer.Sound(os.path.join('Pygame_Rocket', 'Victory.mp3'))

#THE FUNCTIONS USED IN THE BELOW PARTS OF CODE ARE :
#1.For drawing the red, yellow spaceship and bullets as well as indicating the characters health - drawing()
#2.To move the characters in the desired direction restriction it to go into some places, updating the characters position as we move every __ pixels - yellow_motion() & red_motion()
#3.For handling bullet firing direction, bullet velocity and bullet color, size - handle_bullets()
#4.For declaring a winner - winner()
#5.For keeping all of the code together and calling all the functions - main()

def drawing(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): #First we have to draw the window, the spaceship and the border between both, then we ofc update so the code gets executed
    WINDOW.blit(SPACE, (0, 0))#pygame fills the window with colors only RGB, so the tuple will be numbers inclusive of 0 to 255
    pygame.draw.rect(WINDOW, COLOR_WHITE, BORDER) #Drawing a border in the middle

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, COLOR_RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, COLOR_YELLOW)

    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #.blit is used to draw 
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, COLOR_RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, COLOR_YELLOW, bullet)

    pygame.display.update() #If you dont type this. anything you write will not be executed

def yellow_motion(entered_keys, yellow): #Takes WASD to move the yellow spaceship
        if entered_keys[pygame.K_a] and yellow.x - VEL > 0: #Left
            yellow.x -= VEL 
        if entered_keys[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #Right
            yellow.x += VEL
        if entered_keys[pygame.K_w] and yellow.y - VEL > 0: #Up 
            yellow.y -= VEL
        if entered_keys[pygame.K_s]and yellow.y + VEL + yellow.height < HEIGHT - 16: #Down
            yellow.y += VEL

def red_motion(entered_keys, red): #Arrow Keys to move the red spaceship
        if entered_keys[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #Left
            red.x -= VEL
        if entered_keys[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #Right
            red.x += VEL
        if entered_keys[pygame.K_UP] and red.y - VEL > 0: #Up 
            red.y -= VEL
        if entered_keys[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 16: #Down
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #Checks if the bullet collides with the characters
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:  
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #Checks if the bullet collides with the characters
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def winner(text):
    draw_text = WINNER_FONT.render(text, 1, COLOR_MAGENTA)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    clock = pygame.time.Clock() #Telling pygame to run the file at 60 frames per second on any computer

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #Rect takes x,y,width,height
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    run = True
    while run: #Like a infintite that keeps the game running till the while loop is false
        clock.tick(FPS) #Ensures that the computer only runs the loop 60 times for second no matter what
        for event in pygame.event.get(): #This is a event loop
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < BULLET_NUM_MAX:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) #The bullets firing from yellow should go to the right and should come from the middle of the character
                    yellow_bullets.append(bullet)
                    BULLET_FIRE.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < BULLET_NUM_MAX:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5) 
                    red_bullets.append(bullet)
                    BULLET_FIRE.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"
            WINNER_SOUND_EFFECT.play()

        if yellow_health <= 0:
            winner_text = "Red Wins!"
            WINNER_SOUND_EFFECT.play()

        if winner_text != "":
            winner(winner_text)
            break

        entered_keys = pygame.key.get_pressed() #To move the the yellow spaceship according to the user input entered keys

        drawing(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) #Calling the drawing function to blit the spaceships

        yellow_motion(entered_keys, yellow)
        red_motion(entered_keys, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    main() #Rerunning the main file so that the game doesn't quit and instead restarts


if __name__ == '__main__':
    main()
