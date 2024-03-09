import pygame
import datetime

class Global:
    screen_width = 800
    screen_height = 640
    
    
class Bomb:
    radius = 15
    color = (255, 0, 0)
    speed = 0.5  # number of pixels per 1000ms
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.created_at = datetime.datetime.now()
    
    def adjust_position(self):
        new_time = datetime.datetime.now()
        time_diff = new_time - self.created_at
        self.y += Bomb.speed * (time_diff.total_seconds() * 1000) / 1000
              
    def draw(self, screen):
        self.adjust_position()
        pygame.draw.circle(screen, Bomb.color, (self.x, self.y), self.radius)


class BombList: 
    def __init__(self):
        self.bombs = []
        bomb1 = Bomb(250, 40)
        bomb2 = Bomb(300, 50)
        self.bombs.append(bomb1)
        self.bombs.append(bomb2)
        
    def draw(self, screen):
        for bomb in self.bombs:
            bomb.draw(screen)


class Shell:
    length = 30
    width = 5
    color = (0, 0, 255)
    speed = 1  # number of pixels per 1000ms
    
    def __init__(self, x, y):
        self.x = x
        self.y = y        
        self.created_at = datetime.datetime.now()
    
    def adjust_position(self):
        new_time = datetime.datetime.now()
        time_diff = new_time - self.created_at
        self.y -= Bomb.speed * (time_diff.total_seconds() * 1000) / 1000

    def draw(self, screen):
        self.adjust_position()
        pygame.draw.line(screen, 
                         Shell.color, 
                         (self.x, self.y), 
                         (self.x, self.y+Shell.length), 
                         Shell.width)

        
class ShellList:   
    def __init__(self):
        self.shells = []
        shell1 = Shell(0,0)
        shell2 = Shell(100, 10)
        shell3 = Shell(200, 20)
        self.shells.append(shell1)
        self.shells.append(shell2)
        self.shells.append(shell3)
    
    def draw(self, screen):
        for shell in self.shells:
           shell.draw(screen)


class Cannon:
    height = 25
    width = 50
    color = (0, 255, 0)
    step_size = 2
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((Global.screen_width, Global.screen_height))
    pygame.display.set_caption('Demo')

    cannon = pygame.Rect((0, Global.screen_height - Cannon.height - 1, Cannon.width, Cannon.height))
    shell_list = ShellList()
    bomb_list = BombList()
            
    game_over = False
    while not game_over:  # game loop        
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, Cannon.color, cannon)
        shell_list.draw(screen)
        bomb_list.draw(screen)
        
        key = pygame.key.get_pressed()
        # move cannon up arrow key LEFT and RIGHT
        if key[pygame.K_LEFT] == True and cannon.left > 0:
            cannon.move_ip(-1*Cannon.step_size, 0)
        elif key[pygame.K_RIGHT] == True and cannon.right < Global.screen_width-1:
            cannon.move_ip(1*Cannon.step_size, 0)
        # fire cannon
        elif key[pygame.K_SPACE] == True:
            shell = Shell(cannon.left + Cannon.width/2, cannon.top - Shell.length)
            shell_list.shells.append(shell)
        
        # event processing
        for event in pygame.event.get():  # event handler
            if event.type == pygame.QUIT:
                game_over = True
        
        # refresh screen
        pygame.display.update()
         
    pygame.quit()  # clean


if __name__ == '__main__':
    main()
