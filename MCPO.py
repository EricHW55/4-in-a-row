import numpy as np
from copy import deepcopy
import random
from env import connect4
import math

class MCTF:
    def __init__(self):
        self.root_id = 0
        self.tree = {}


    def __call__(self, player:int, main_page:bool):
        self.player = player; self.main_page = main_page
        self.env = connect4(main_page=main_page)
        self.state = self.env.state  # deep copy? shallow copy?
        self.env.set_state(state=self.state)   


    
    def main(self, node_id:tuple = (0,), batch_size:int=1000):  # 4가지 phase를 통해 tree의 parameter update
        self.node_id =  node_id  # 현재 노드 id       
        for _ in range(batch_size): # batch_size 만큼 시뮬
            # if (_ % 10000) == 0: # <<<
            #     print('{}번 학습.'.format(_)) 

            self.simulation(node_id=self.node_id)
            
    def random_playout(self, node_id:tuple, first:bool=True) -> int: # 랜덤 게임 진행
        for i in node_id[1:]:
            action_done = self.env.action(x_pos=i)
            if not action_done and first: return -math.inf # 못 두는 수
            elif not action_done and not first: return math.inf
        game_done = False
        while not game_done:
            action_number = [i for i in range(7)]  # 선택 가능한 action 수
            action = random.choice(action_number)   # actino random으로 선택
            action_done = self.env.action(x_pos=action)  # action 진행
            while not action_done:  # action이 안된다면
                self.env.change_player()
                action_number.remove(action)  # 안되는 action 제거
                action = random.choice(action_number)  # action 다시 선택
                action_done = self.env.action(x_pos=action)  # action 진행

            if self.main_page: self.env.main()

            game_done = True if not self.env.check_finish() == None else False  # if 게임이 끝 True else False

        return self.env.check_finish()

    def mcpo(self, node_id:tuple, num:int, page:bool=False, first:bool=True) -> float:
        win = 0
        for _ in range(num):
            if first:win += self.random_playout(node_id, first)
            else: win -= self.random_playout(node_id, first)
            self.env = connect4(main_page=page)
        # print(node_id[-1]+1, 'win :', win) 
        winning_rate = ((num+win)/2)/num
        # print('승률 : {}%'.format(winning_rate))
        return winning_rate
        # return win

    def mcpo_action(self, node_id:tuple, num:int, page:bool=False, first:bool=True) -> int:
        win = 0
        for _ in range(num):
            if first:win += self.random_playout(node_id, first)
            else: win -= self.random_playout(node_id, first)
            self.env = connect4(main_page=page)
        # print(node_id[-1]+1, 'win :', win) 
        # winning_rate = ((num+win)/2)/num
        # print('승률 : {}%'.format(winning_rate))
        # return winning_rate
        return win

    def select_action(self, node_id:tuple, num:int, first:bool=True):
        action_win = []; app = action_win.append
        for i in range(7):
            node = node_id + (i,)
            # num = 500
            # num *= (43-len(node_id))/len(node_id)
            win = self.mcpo_action(node_id=node, num=num, page=False, first=first)
            # print('action : {}, win : {}'.format(i, win))
            app(win)
        # print(action_win)
        return action_win.index(max(action_win))
    


    def backpropagation(self, node_id:tuple, win:int):
        while not node_id == (0,):  # if not root node?
            node = self.node_search(node_id)
            node['visit'] += 1
            node['win'] += win  # 승부 결과 1:승, 0:무, -1:패
            node_id = node['parent'] # 부모 노드로 이동
        
        node = self.node_search(node_id)
        node['visit'] += 1; node['win'] += win # root node에서 진행
    

if __name__ == "__main__":
    mctf = MCTF()
    mctf(1, False)
    node_id = (0,)
    def select_action(node_id, first:bool):
        action_win = []; app = action_win.append
        for i in range(7):
            node = node_id + (i,)
            num = 600
            # num *= (43-len(node_id))/len(node_id)
            win = mctf.mcpo(node_id=node, num=num, page=False, first=first)
            # print('action : {}, win : {}'.format(i, win))
            app(win)
        # print(action_win)
        return action_win.index(max(action_win))


    from env import connect4

    screen = connect4(main_page=True)
    screen.main()
    node_id = (0,)  # 현재의 node id

    first = True
    action_num = select_action(node_id, first)
    screen.action(action_num)
    node_id += (action_num, )
    # print(node_id)
    while True: 
        x = screen.main()
        if not screen.done:
            screen = connect4(main_page=True)
            # screen.main()
            node_id = (0,)  # 현재의 node id
        if not x == None:
            node_id += (x,)
            action_num = select_action(node_id, first)
            screen.action(action_num)
            node_id += (action_num, )




"""
결과
총합 
48전 37승 3무 8패 (후공) / 32전 24승 2무 6패 (선공)
80전 61승 5무 14패 (총합)
76.25% / 6.25% / 17.5%

오지원 :                       1전 1승 (선공)
전영욱 : 16전 13승 2무 1패 (후공) / 8전 8승 (선공)
오정석 :                       2전 2승 (선공)
이새미르 : 5전 2승 3패 (후공) / 6전 1승 1무 4패 (선공)
손유찬 : 3전 3승 (후공)
권민준 : 2전 1승 1패 (후공) / 1전 1무 (선공)
조성우 : 3전 2승 1무 (후공)  / 3전 3승 (선공)
이현서 : 16전 15승 1패 (후공) / 7전 6승 1패 (선공)
유성현 : 1전 1패 (후공) / 3전 2승 1패 (선공)
기현서 : 2전 1승 1패 (후공) / 1전 1승 (선공)

connect4 online : 2전 2승 (후공) OO / num : 500
                : 3전 2승 1패 (선공) OXO / num : 500
https://www.cbc.ca/kids/games/play/connect-4
"""
