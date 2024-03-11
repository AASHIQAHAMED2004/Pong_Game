import pygame
pygame.init()

#parameters
S_Width = 1080
S_Height = 720
P_Width = 20
P_Height = 130
FPS = 60
ball_radius = 12
Color = (0,255,65)
Black = (0,0,0)
SCORE_FONT = pygame.font.SysFont("comicsans",50)
WINNING_SCORE = 10


win = pygame.display.set_mode((S_Width,S_Height))
pygame.display.set_caption("pong")
 
class Paddles:
    COLOUR = Color
    VELOCITY = 4
    def __init__(self,x,y,width,height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self,win):
        pygame.draw.rect(win,self.COLOUR,(self.x,self.y,self.width,self.height))

    def move(self, up =True):
        if up:
            self.y -=self.VELOCITY
        else:
            self.y +=self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class BALL:
    MAX_VELOCITY = 5
    COLOUR = Color
    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VELOCITY
        self.y_vel = 0

    def draw(self,win):
        pygame.draw.circle(win,self.COLOUR,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def handle_paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY>=0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height<=S_Height:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY>=0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]and right_paddle.y + right_paddle.VELOCITY + right_paddle.height<=S_Height:
        right_paddle.move(up=False)

def handle_collosion(ball,left_paddle,right_paddle):
    if ball.y + ball.radius >=S_Height:
        ball.y_vel*= -1

    elif ball.y - ball.radius <= 0:
        ball.y_vel*= -1

    if ball.x_vel < 0 :
        #ball moving towards left
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel*= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
                #ball moving towards right
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x :
                ball.x_vel*= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def draw(win,Paddles,ball,left_score,right_score):
    win.fill(Black)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, Color)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, Color)
    win.blit(left_score_text, (S_Width//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (3 * (S_Width//4) -right_score_text.get_width()//2, 20))

    for paddle in Paddles:
        paddle.draw(win)

    for i in range(10,S_Height,S_Height//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win,Color,(S_Width//2-5,i,10,S_Height//20))
    ball.draw(win)
    
    pygame.display.update()

def main ():
    run=True
    clock = pygame.time.Clock()

    left_paddle = Paddles(10,(S_Height//2)-(P_Height//2),P_Width,P_Height)
    right_paddle = Paddles((S_Width-10-P_Width),(S_Height//2)-(P_Height//2),P_Width,P_Height)
    ball=BALL(S_Width //2 ,S_Height //2 ,ball_radius)
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(win,[left_paddle,right_paddle],ball,left_score,right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,left_paddle,right_paddle)
        ball.move()
        handle_collosion(ball,left_paddle,right_paddle)


        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > S_Width:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, Color)
            win.blit(text, (S_Width//2 - text.get_width() //2, S_Height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == '__main__':
    main()