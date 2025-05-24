import numpy as np
import pygame
import random

random.seed(2)
WIDTH = 1000
HEIGHT = 700
FPS = 50


class Ball:
    def __init__(self, pos_x, pos_y, left_paddle, right_paddle):
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
        self.colour = (255, 255, 255)
        self.radius = 40
        self.velocity = [random.choices([1, 2, 3, -1, -2, -3])[0], random.choices([1, 2, 3, -1, -2, -3])[0]]
        sf = 1 / (self.velocity[0]**2+self.velocity[1]**2)**0.5
        self.velocity = [self.velocity[0]*sf, self.velocity[1]*sf]
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_position(self):
        return self.pos_x, self.pos_y
    
    def collide(self): # takes a paddle object as an argument
        if self.pos_y-self.radius <= 0 or self.pos_y+self.radius >= HEIGHT:
            self.velocity = [self.velocity[0], self.velocity[1]*-1]

    def left_paddle_collide(self, paddle):
        if (self.pos_x-self.radius <= paddle.coord_2[0]) and (paddle.coord_1[1] <= self.pos_y <= paddle.coord_2[1]):
            self.velocity = [self.velocity[0]*-1, self.velocity[1]]

    def right_paddle_collide(self, paddle):
        if (self.pos_x+self.radius >= paddle.coord_1[0]) and (paddle.coord_1[1] <= self.pos_y <= paddle.coord_2[1]):
            self.velocity = [self.velocity[0]*-1, self.velocity[1]]
        
    def move(self):
        scale = 7
        self.pos_x += self.velocity[0]*scale
        self.pos_y += self.velocity[1]*scale
        self.collide()
        self.left_paddle_collide(self.left_paddle)
        self.right_paddle_collide(self.right_paddle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.pos_x, self.pos_y), self.radius)


class Paddle:
    def __init__(self, x1, y1, x2, y2): # 2 corners of the paddle
        self.colour = (255, 255, 255)
        self.speed = 5
        self.coord_1 = (x1, y1)
        self.coord_2 = (x2, y2)

    def move_up(self):
        if self.coord_1[1] > 0:
            self.coord_1 = (self.coord_1[0], self.coord_1[1]-self.speed)
            self.coord_2 = (self.coord_2[0], self.coord_2[1]-self.speed)

    def move_down(self):
        if self.coord_2[1] < HEIGHT:
            self.coord_1 = (self.coord_1[0], self.coord_1[1]+self.speed)
            self.coord_2 = (self.coord_2[0], self.coord_2[1]+self.speed)

    def draw(self, screen):
        rect_width = abs(self.coord_2[0] - self.coord_1[0])
        rect_height = abs(self.coord_2[1] - self.coord_1[1])
        rectangle = pygame.Rect(self.coord_1[0], self.coord_1[1], rect_width, rect_height)
        pygame.draw.rect(screen, self.colour, rectangle)

    

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_line(screen):
    points = np.linspace(0, HEIGHT*2, 30)
    for i in range(0, 16, 2):
        pygame.draw.line(screen, (255, 255, 255), (WIDTH//2, points[i]), (WIDTH//2, points[i+1]), width=5)


def check_lost(ball_position):
    if ball_position < 0:
        return 'left'
    elif ball_position > WIDTH:
        return 'right'
    else:
        return None
    

def reset():
    ball.pos_x = WIDTH//2
    ball.pos_y = HEIGHT//2


def main():
    global player_1_score, player_2_score, ball
    pygame.font.init()
    new_text = ''
    font = pygame.Font(None, 50)
    player_1_score = 5
    player_2_score = 5
    running = True
    game_started = False
    paddle_1 = Paddle(0, 0, 10, 280)
    paddle_2 = Paddle(WIDTH-10, 0, WIDTH, 60)
    ball = Ball(WIDTH//2, HEIGHT//2, paddle_1, paddle_2)
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    new_text = ''

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle_1.move_up()
        elif keys[pygame.K_s]:
            paddle_1.move_down()
        if keys[pygame.K_UP]:
            paddle_2.move_up()
        elif keys[pygame.K_DOWN]:
            paddle_2.move_down()

        draw_line(screen)
        ball.draw(screen)
        paddle_1.draw(screen)
        paddle_2.draw(screen)
        if game_started:
            ball.move()
        result = check_lost(ball.pos_x)
        if result:
            if result == 'left':
                player_1_score -= 1
            elif result == 'right':
                player_2_score -= 1
            if player_1_score == 0:
                new_text = 'Player 2 Wins!'
                player_1_score, player_2_score = 5, 5
                reset()
            elif player_2_score == 0:
                new_text = 'Player 1 Wins!'
                player_1_score, player_2_score = 5, 5
                reset()
            game_started = False
            reset()
        
        text = font.render(str(player_1_score)+'       '+str(player_2_score), False, (255, 255, 255))
        text_2 = font.render(new_text, False, (255, 255, 255))
        screen.blit(text, (WIDTH//2-50, 30))
        screen.blit(text_2, (WIDTH//2-70, 100))


        clock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    main()

