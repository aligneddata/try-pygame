import pygame
import datetime
import random


def get_diff_in_seconds(dt1, dt2):
    dt_delta = dt2 - dt1
    return dt_delta.seconds + dt_delta.microseconds / 10**6


class Global:
    screen_width = 800
    screen_height = 640
    
    
class Bomb:
    radius = 20
    color = (255, 0, 0)
    speed = .3  # number of pixels per 1000ms
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.created_at = datetime.datetime.now()
        self.activated = True
    
    def adjust_position(self):
        new_time = datetime.datetime.now()
        self.y += Bomb.speed * get_diff_in_seconds(self.created_at, new_time)
              
    def in_screen(self):
        if self.y - Bomb.radius > Global.screen_height:  # upper point is lower than the screen bottom
            return False
        if self.y + Bomb.radius < 0:  # bottom point is higher than the screen top
            return False
        return True
    
    def draw(self, screen):
        if self.in_screen() and self.activated:
            pygame.draw.circle(screen, Bomb.color, (self.x, self.y), self.radius)
            self.adjust_position()


class BombList:
    bomb_creation_speed = .4  # number of new bombs per second
    
    def __init__(self):
        self.bombs = []
        bomb1 = Bomb(250, 40)
        self.bombs.append(bomb1)
        self.created_at = datetime.datetime.now()
        
    def draw(self, screen):
        for bomb in self.bombs:
            bomb.draw(screen)

     
    def generate_bomb(self):
        new_time = datetime.datetime.now()
        expected_number = get_diff_in_seconds(self.created_at, new_time) * BombList.bomb_creation_speed
        for i in range(int(expected_number) - len(self.bombs)):
            x = random.randint(Bomb.radius, Global.screen_width - Bomb.radius)
            y = 1 + 0 - Bomb.radius
            bomb = Bomb(x, y)
            self.bombs.append(bomb)
            print("Created a new bomb")

    def test_if_game_over(self):
        for bomb in self.bombs:
            if bomb.activated and bomb.y+Bomb.radius >= Global.screen_height:
                return True


class Shell:
    length = 30
    width = 5
    color = (0, 0, 255)
    speed = 2.  # number of pixels per second
    
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.y2 = self.y + Shell.length       
        self.created_at = datetime.datetime.now()
        self.activated = True
    
    def adjust_position(self):
        new_time = datetime.datetime.now()
        self.y -= Shell.speed * get_diff_in_seconds(self.created_at, new_time)
        self.y2 = self.y + Shell.length
     
    def in_screen(self):
        if self.y > Global.screen_height:  # upper point is lower than the screen bottom
            return False
        if self.y2 < 0:  # bottom point is higher than the screen top
            return False
        return True
    
    def draw(self, screen):
        if self.in_screen() and self.activated:
            pygame.draw.line(screen, 
                            Shell.color, 
                            (self.x, self.y), 
                            (self.x, self.y2), 
                            Shell.width)
            self.adjust_position()

    
        
class ShellList:   
    def __init__(self):
        self.shells = []
    
    def draw(self, screen):
        for shell in self.shells:
           shell.draw(screen)

    # tell if this shell is currently hitting the bomb
    # if the shell is not even in the range of the bomb, fail.
    # if in the range of x, and the shell's head enters into the domain of bomb y range, success.
    def test_if_hitting_target(self, bombList: BombList):
        for shell_id in range(len(self.shells)):
            for bomb_id in range(len(bombList.bombs)):
                shell = self.shells[shell_id]
                bomb = bombList.bombs[bomb_id]
                if shell.in_screen() and shell.activated and bomb.in_screen() and bomb.activated:
                    if shell.x >= (bomb.x - Bomb.radius) and shell.x <= (bomb.x + Bomb.radius) and shell.y >= (bomb.y - Bomb.radius) and shell.y <= (bomb.y + Bomb.radius):
                        shell.activated = False
                        bomb.activated = False
                        print("Target hit!")


class Cannon:
    height = 25
    width = 50
    color = (0, 255, 0)
    step_size = 2
    

class Text:
    def __init__(self, message):
        self.message = message
    
    def draw(self, screen):
        TEXT_COLOR = (255, 255, 255)
        BACKGROUND_COLOR = (0, 0, 0)
        font = pygame.font.SysFont(None, 48) 
        text = font.render(self.message, True, TEXT_COLOR)
        screen.fill(BACKGROUND_COLOR)
        screen.blit(text, (Global.screen_width/2 - 100, Global.screen_height/2)) 
        
class Game:
    game_over = False
    game_over_banner_delay = 5  # display game over text for 10 seconds
    game_over_time = None

    def kickoff_game_over_timer():
        if Game.game_over_time is None:
            Game.game_over_time = datetime.datetime.now()
            print("Game Over!")

    def time_to_exit_screen():
        if Game.game_over_time is None:
            return False
        new_time = datetime.datetime.now()
        #print(Game.game_over_time, new_time)
        if get_diff_in_seconds(Game.game_over_time, new_time) > Game.game_over_banner_delay:
            return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((Global.screen_width, Global.screen_height))
    pygame.display.set_caption('Air Defense')

    cannon = pygame.Rect((0, Global.screen_height - Cannon.height - 1, Cannon.width, Cannon.height))
    shell_list = ShellList()
    bomb_list = BombList()
            
    while not Game.game_over:  # game loop        
        screen.fill((0, 0, 0))
        

        bomb_list.generate_bomb()
        shell_list.test_if_hitting_target(bomb_list)

        pygame.draw.rect(screen, Cannon.color, cannon)
        shell_list.draw(screen)
        bomb_list.draw(screen)
        
        key = pygame.key.get_pressed()
        # move cannon up arrow key LEFT and RIGHT
        if key[pygame.K_LEFT] == True and cannon.left > 0:
            cannon.move_ip(-1*Cannon.step_size, 0)
        elif key[pygame.K_RIGHT] == True and cannon.right < Global.screen_width-1:
            cannon.move_ip(1*Cannon.step_size, 0)
        
        # event processing
        for event in pygame.event.get():  # event handler
            if event.type == pygame.QUIT:
                Game.game_over = True
            if event.type == pygame.KEYUP:
                key = event.key
                # fire cannon
                if key == pygame.K_SPACE:
                    print("Firing a shell")
                    shell = Shell(cannon.left + Cannon.width/2, cannon.top - Shell.length)
                    shell_list.shells.append(shell)
                
        # is game over 
        if bomb_list.test_if_game_over():
            Text("Game Over!").draw(screen)
            Game.kickoff_game_over_timer()
            
        if Game.time_to_exit_screen():
                Game.game_over = True

        # refresh screen
        pygame.display.update()        
         
    pygame.quit()  # clean


if __name__ == '__main__':
    main()
