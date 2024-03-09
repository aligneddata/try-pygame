import pygame

pygame.init()

screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption('Demo')

rect = pygame.Rect((300, 100, 50, 50))

game_over = False
while not game_over:  # game loop
    
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 0, 0), rect)
    pygame.draw.circle(screen, (0, 255, 0), (150,150), 30)
    pygame.draw.line(screen, (0, 0, 255), (100,200), (100,210),5)
    pygame.draw.polygon(screen, (0, 0, 255), ((300,250),(350,250),(325,225)))

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True and rect.left > 0:
        rect.move_ip(-1, 0)
    elif key[pygame.K_d] == True and rect.right < 799:
        rect.move_ip(1, 0)
    elif key[pygame.K_w] == True and rect.top > 0:
        rect.move_ip(0, -1)
    elif key[pygame.K_s] == True and rect.bottom < 639:
        rect.move_ip(0, 1)
        
    for event in pygame.event.get():  # event handler
        if event.type == pygame.QUIT:
            game_over = True
    
    pygame.display.update()
    
            
pygame.quit()  # clean

