import numpy as np
import pygame
from copy import deepcopy
from time import sleep

pygame.init()

class connect4:
    def __init__(self, width:int=7, height:int=6, player:int=1, main_page:bool=True):
        self.state = np.zeros((height, width), dtype=np.int32)
        self.player = player
        self.done = True

        self.last_pos = (None, None)  # 마지막으로 둔 수의 좌표 (x,y)

        if main_page:  # 창을 실행 한다면
            self.main_page()
        # while self.done:
        

    def __call__(self) -> bool:  # 게임 끝? -> True or Not
        return self.done


    def set_state(self, state):
        self.state = deepcopy(state)

    def change_player(self, player:int=-1): # 기본값 -1 : 항상 플레이어를 바꾼다. 1이면 안바꿈. -1이면 바꿈.
        self.player *= player
    

    def main(self, return_k:int=None) -> int:
        self.screen.fill((255, 255, 255)) #단색으로 채워 화면 지우기
        pygame.display.set_caption('4 in a row - {}'.format('Red' if self.player==1 else 'Blue'))

        event = pygame.event.poll() #이벤트 처리
        if event.type == pygame.QUIT:
            # break
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = self.mouse_pos()
            pos = self.check_pos(pos)
            # print(pos)  # (x, 1)  # y pos 않씀
            # self.change_state(pos[0])
            self.action(x_pos=pos[0])
            return_k = pos[0]
            
            # self.player *= -1 # <<<
            # self.check_end()
            # print(pos)

        if event.type == pygame.KEYDOWN: # 키보드 누름
            k_num = int(event.key-pygame.K_0) - 1 # 눌린 키 - 0번 키 : 눌린 숫자. -1 : 1번(키보드) -> 0번(게임 판)
            self.action(x_pos=k_num)
            return_k = k_num
            

        self.clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값
        self.make_lines()
        self.keep_circle()
        self.last_ston_rect() # <<<
        pygame.display.update() #모든 화면 그리기 업데이트
        self.check_end()

        # pygame.quit() 
        return return_k

    def main_page(self):
        self.WINDOW_WIDTH = 700
        self.WINDOW_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT)) #화면 크기 설정
        pygame.display.set_caption('4 in a row')
        self.clock = pygame.time.Clock() 

        # self.grid_pos = [[(x*100,y*100) for x in range(7)] for y in range(6)]

    def action(self, x_pos) -> bool:
        done = self.change_state(x_pos)
        self.player *= -1 # <<<
        return done


    def mouse_pos(self):
        return pygame.mouse.get_pos()


    def check_pos(self, pos)->int:
        x = pos[0]; y = pos[1]
        return (x//100, y//100)


    def make_lines(self):
        for i in range(7):
            pygame.draw.line(self.screen, (0, 0, 0), [i*100, 0], [i*100, 600], 5)
        for i in range(6):
            pygame.draw.line(self.screen, (0, 0, 0), [0, i*100], [700, i*100], 5)


    def change_state(self, x, y=5):
        # x = pos[0]; y = 5
        for i in range(6):
            if self.state[i][x] == 0:y = i
            elif self.state[i][x] != 0:break
        if self.state[y][x] != 0: 
            y = None
            self.player *= -1  # return으로 돌아가서 action에서 self.player 부호 바꾸는거 방지
            return False

        self.state[y][x] = self.player
        self.last_pos = (x,y)

        return True


    def keep_circle(self):
        for x in range(7):
            for y in range(6):
                if self.state[y][x] == 1:
                    pygame.draw.circle(self.screen, (255,0,0), [x*100+50,y*100+50], 50-10, 0)
                elif self.state[y][x] == -1:
                    pygame.draw.circle(self.screen, (0,0,255), [x*100+50,y*100+50], 50-10, 0)


    def check_end(self):
        r1,r2,r3 = 0,0,0
        r1 = self.check_verticle()
        r2 = self.check_horizontal()
        r3 = self.check_diagonal()
        if r1 == 1 or r2 == 1 or r3 == 1:
            print('Red win'); self.done = False
        elif r1 == -1 or r2 == -1 or r3 == -1:
            print('Blue win'); self.done= False

        # elif r1 == 0 and r2 == 0 and r3 == 0 and not 0 in self.state:#<<<
        #     self.done = False

        if not self.done:
            pygame.quit()

        
    def check_finish(self) -> int:  # for mcts algorithms
        r1,r2,r3 = 0,0,0
        r1 = self.check_verticle(screen=False)
        r2 = self.check_horizontal(screen=False)
        r3 = self.check_diagonal(screen=False)
        if r1 == 1 or r2 == 1 or r3 == 1: win = 1  # 승
        elif r1 == -1 or r2 == -1 or r3 == -1: win = -1  # 패
        elif r1 == 0 and r2 == 0 and r3 == 0 and 0 in self.state: win = None # 게임 끝남X
        elif r1 == 0 and r2 == 0 and r3 == 0 and not 0 in self.state: win = 0 # 무승부

        return win


    def check_horizontal(self, screen:bool=True):
        results = 0
        for y in range(6):
            for x in range(4):
                if self.state[y][x] == 1 and self.state[y][x+1] == 1 and self.state[y][x+2] == 1 and self.state[y][x+3] == 1:
                    results = 1; 
                    if screen: self.draw_rect([x,x+1,x+2,x+3],[y,y,y,y], results)
                if self.state[y][x] == -1 and self.state[y][x+1] == -1 and self.state[y][x+2] == -1 and self.state[y][x+3] == -1:
                    results = -1; 
                    if screen: self.draw_rect([x,x+1,x+2,x+3],[y,y,y,y], results)
        return results

    def check_verticle(self, screen:bool=True):
        results = 0
        for y in range(3):
            for x in range(7):
                if self.state[y][x] == 1 and self.state[y+1][x] == 1 and self.state[y+2][x] == 1 and self.state[y+3][x] == 1:
                    results = 1; 
                    if screen: self.draw_rect([x,x,x,x],[y,y+1,y+2,y+3], results)
                if self.state[y][x] == -1 and self.state[y+1][x] == -1 and self.state[y+2][x] == -1 and self.state[y+3][x] == -1:
                    results = -1; 
                    if screen: self.draw_rect([x,x,x,x],[y,y+1,y+2,y+3], results)
        return results
    
    def check_diagonal(self, screen:bool=True):
        results = 0
        for y in range(3):  
            for x in range(4):
                if self.state[y][x] == 1 and self.state[y+1][x+1] == 1 and self.state[y+2][x+2] == 1 and self.state[y+3][x+3] == 1:
                    results = 1; 
                    if screen: self.draw_rect([x,x+1,x+2,x+3],[y,y+1,y+2,y+3], results)
                if self.state[y][x] == -1 and self.state[y+1][x+1] == -1 and self.state[y+2][x+2] == -1 and self.state[y+3][x+3] == -1:
                    results = -1; 
                    if screen: self.draw_rect([x,x+1,x+2,x+3],[y,y+1,y+2,y+3], results)

        for y in range(3):  
            for x in range(3,7):
                if self.state[y][x] == 1 and self.state[y+1][x-1] == 1 and self.state[y+2][x-2] == 1 and self.state[y+3][x-3] == 1:
                    results = 1; 
                    if screen: self.draw_rect([x,x-1,x-2,x-3],[y,y+1,y+2,y+3], results)
                if self.state[y][x] == -1 and self.state[y+1][x-1] == -1 and self.state[y+2][x-2] == -1 and self.state[y+3][x-3] == -1:
                    results = -1; 
                    if screen: self.draw_rect([x,x-1,x-2,x-3],[y,y+1,y+2,y+3], results)

        return results


    def draw_rect(self, pos_x:list, pos_y:list, results:int):
        # print(pos_x, pos_y)
        win_player = 'BLUE' if results == -1 else 'RED'
        pygame.display.set_caption(f'4 in a row - {win_player} WIN')
        for n,i in enumerate(pos_x):
            pygame.draw.rect(self.screen, (255,255,100), [i*100, pos_y[n]*100, 100, 100], 10)
            # print([i, pos_y[n], 100, 100])
            pygame.display.update()
            sleep(0.2)
        pygame.display.update(); sleep(1.5)


    def last_ston_rect(self):
        x,y = self.last_pos[0], self.last_pos[1]
        if x == None:return
        pygame.draw.rect(self.screen, (255,100,255), [x*100, y*100, 100, 100], 10)
        # pygame.display.update()


if __name__ == "__main__":
    env = connect4(player=1)
    # env()
    while True:    
        env.main()

        if not env():break
    # env.make_lines()
