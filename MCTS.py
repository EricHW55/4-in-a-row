import numpy as np
from numpy import log as ln
import math
from copy import deepcopy
import random
from env import connect4
import os
import ast
from time import sleep
from tqdm import trange


class MCTS:
    def __init__(self):
        self.tree = {}
        self.root_id = 0
        self.env = connect4(main_page=False)
        self.state = self.env.state  # deep copy? shallow copy?


    def __call__(self, state, player):
        self.state = state # <<<< 굳이 해야함? 다시 확인 필요
        self.player = player
        self.create_root_node(state=self.state, player=self.player)

        self.env.set_state(state=self.state)
        

    def create_root_node(self, state, player:int):
        self.tree[(0,)] = { 'state' : state,
                            'player' : player,
                            'child' : [],
                            'parent' : None,
                            'win' : 0,
                            'visit' : 0 }


    def main(self, node_id:tuple = (0,), batch_size:int=1000):  # 4가지 phase를 통해 tree의 parameter update
        self.node_id =  node_id  # 현재 노드 id
        # expansion_visit_num = 10 # 확장 기준 방문 횟수 # hyperparameter

        if self.node_id == (0,) and self.tree[self.node_id]['child'] == []: # root node? and child node X?
            self.expansion(node_id=self.node_id) # expansion -> simulation
        
        for _ in trange(batch_size): # batch_size 만큼 시뮬
            # if (_ % 1000000) == 0: # <<<
            #     print('{}번 학습.'.format(_)) 

            self.simulation(node_id=self.node_id)
            
    
    def expansion(self, node_id:tuple):  # 전제 // 게임이 끝나지 않음 == 현재 노드 != 리프 노드
        current_node_state = deepcopy(self.tree[node_id]['state'])  # 혹시 몰라 deep copy
        self.env.player = deepcopy(self.tree[node_id]['player']) # <<<,
        node_num = 0; child_node_list = []; cnl_app = child_node_list.append
        for x in range(7):  # 할 수 있는 action 수 : 7
            # 전제 // env의 state == node의 state 
            done = self.env.action(x_pos=x)  # x번째의 action 취함 / action 가능 여부를 done에 저장. if not 0 in x행: done -> False else: done -> True
            if done: # action이 가능했다면, // 만약 action이 불가능이었다면, player 안바뀜. 따라서 change_player는 조건문 안에서 실행
                state = deepcopy(self.env.state)  # action 후의 env의 state 받아옴
                self.tree[node_id+(node_num,)] = {  'state' : state,  # 트리 확장
                                                    'player' : self.env.player,
                                                    'child' : [],
                                                    'parent' : node_id,
                                                    'win' : 0,
                                                    'visit' : 0 }
                self.env.set_state(state=current_node_state)  # 현재 노드의 상태로 되돌림
                self.env.change_player()  # action 이후의 바뀐 player를 원상복구시킴
                cnl_app( node_id+(node_num,) )
                node_num += 1
        # self.env.change_player() # <<,

        self.tree[node_id]['child'] = child_node_list  # 확장한 노드의 child key의 value를 자식 노드들의 id의 리스트로 업데이트



    def selection(self, node_id:tuple)->tuple: # node_id -> child_node_id
        def UCT(input_node_id:tuple, C:int=1.4) -> float:  # C : root(2)에 근사 # hyperparameter # input_node_id : 입력 노드
            win, visit = self.tree[input_node_id]['win'], self.tree[input_node_id]['visit']
            parent_node_id = self.tree[input_node_id]['parent']  # 입력 된 노드의 부모 노드 id
            parent_visit = self.tree[parent_node_id]['visit']

            try: uct = (win/visit)*0.3 + C*( 8*ln(parent_visit)/visit )**0.5  # <<< UCT 변형
                
            # try: uct = (win/visit) + C*( ln(parent_visit)/visit )**0.5  # UCT formula / formula : x_i + C*root(ln(t)/n_i)
            except ZeroDivisionError: return math.inf  # 0으로 나눈다면 무한대 반환

            # if (win/visit) == 1:uct = math.inf

            return uct

        child_node_id = self.tree[node_id]['child'] # 자식 노드 id 리스트
        child_node_uct = []; uct_app = child_node_uct.append
        for n,_id in enumerate(child_node_id):
            uct_app(UCT(input_node_id=_id))  # 자식 노드들의 UCT 값을 child_node_uct에 저장

        selected_node_id = child_node_id[child_node_uct.index(max(child_node_uct))]  # UCT 값의 최대값을 받아온 뒤, index를 받아오고 그 값의 자식 노드 id 받아옴
        return selected_node_id

    
    def simulation(self, node_id:tuple):  # simulation function에서의 node_id : 시뮬레이션 과정에서 리프노드의 id / self.node_id : 입력 받은 node_id(주로 root node_id : (0,))
        expansion_visit_num = 10 # 확장(expansion) 기준 방문 횟수 # hyperparameter

        def random_playout(node_id:tuple) -> int: # 랜덤 게임 진행
            state = self.tree[node_id]['state']
            self.env.set_state(state=deepcopy(state))  # 혹시 몰라 deepcopy
            self.env.player = deepcopy(self.tree[node_id]['player'])  # <<<
            game_done = False
            while not game_done:
                action_number = [i for i in range(7)]  # 선택 가능한 action 수
                action = random.choice(action_number)   # actino random으로 선택
                action_done = self.env.action(x_pos=action)  # action 진행
                while not action_done:  # action이 안된다면
                    self.env.change_player()
                    action = random.choice(action_number)  # action 다시 선택
                    action_done = self.env.action(x_pos=action)  # action 진행

                game_done = True if not self.env.check_finish() == None else False  # if 게임이 끝 True else False

            return self.env.check_finish()


        # leaf node에 도달할 때 까지 child node 선택 후 이동 (UCT)
        while self.tree[node_id]['child'] != []:  # 자식 노드가 있는 동안 반복
            node_id = self.selection(node_id=node_id)  # 자식 노드를 선택 by UCT
        self.env.set_state(state=deepcopy(self.tree[node_id]['state']))

        if self.tree[node_id]['visit'] >= expansion_visit_num and self.tree[node_id]['child'] == []: # 일정량 이상 방문시 & 자식 노드가 없을 때
            if self.env.check_finish() == None: # if 게임이 끝나지 않음
                self.expansion(node_id=node_id) # 노드 확장

        if self.env.check_finish() == None:  # 리프노드가 게임 종결 상태가 아니라면, 즉 노드의 state가 승부가 난 상태가 아니라면
            win = random_playout(node_id=node_id) # 랜덤 게임 한 판 진행 # 게임 종결 기준 한 판 -> 승부가 난다. (승, 무, 패)
            self.backpropagation(node_id=node_id, win=win)  # 역전파
        elif self.env.check_finish() != None:  # 노드의 state가 끝난 상태라면
            self.backpropagation(node_id=node_id, win=self.env.check_finish())  # 역전파
        # <<< random_playout을 통해 역전파 코딩 시작. 여기부터 #<<< 


    def backpropagation(self, node_id:tuple, win:int):
        while not node_id == (0,):  # if not root node?
            self.tree[node_id]['visit'] += 1
            self.tree[node_id]['win'] += win  # 승부 결과 1:승, 0:무, -1:패
            node_id = self.tree[node_id]['parent'] # 부모 노드로 이동
        
        self.tree[node_id]['visit'] += 1; self.tree[node_id]['win'] += win # root node에서 진행


    def find_node(self, node_id:tuple, tree:dict, state) -> tuple:
        if node_id == None:
            return None
        child_node_list = tree[node_id]['child']
        for i in child_node_list:
            if (state == tree[i]['state']).all():
                return i
        
        return None  # 없다
    
     
    def save_tree(self, path:str):
        path = os.path.abspath(path)
        tree_list = list(deepcopy(self.tree))
        with open(path, 'w', encoding='UTF-8') as f:
            for node in tree_list:
                win = deepcopy(self.tree[node]['win']); visit = deepcopy(self.tree[node]['visit'])
                player = deepcopy(self.tree[node]['player'])
                parent = deepcopy(self.tree[node]['parent']); child = deepcopy(self.tree[node]['child'])
                state = list(deepcopy(self.tree[node]['state'].flatten()))

                f.writelines('{}:{}/{}/{}/{}/{}/{}\n'.format(node, state, player, \
                                                             child, parent, win, visit))


    def load_tree(self, path:str) -> dict:
        path = os.path.abspath(path)
        with open('tree.txt','r',encoding='utf-8') as f:
            line = f.readlines()

        tree = {}
        for i in line:
            data = i.split(':')
            node = ast.literal_eval(data[0])
            data = data[1].split('/')
            state = np.array(ast.literal_eval(data[0]), dtype=np.int32).reshape((6,7))
            player = ast.literal_eval(data[1])
            child = ast.literal_eval(data[2]); parent = ast.literal_eval(data[3])
            win = ast.literal_eval(data[4]); visit = ast.literal_eval(data[5])
            tree[node] = {  'state' : state,    \
                            'player' : player,  \
                            'child' : child,    \
                            'parent' : parent,  \
                            'win' : win,        \
                            'visit' : visit }  
        return tree
            



if __name__ == "__main__":
    mcts = MCTS()
    state = mcts.state
    mcts(state=state, player=1)
    mcts.main(batch_size=100000000)
    mcts.save_tree('tree.txt')
    # tree = mcts.load_tree('tree.txt')
    # while True:    
    #     node_id = input('node_id : '); node_id = node_id.split(',')
    #     node_id = [int(i) for i in node_id]
    #     node_id = tuple(node_id)
    #     print(tree[node_id])
    # print(mcts.tree)
    # print(len(list(mcts.tree)))