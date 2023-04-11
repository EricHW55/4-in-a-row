import numpy as np
from numpy import log as ln
import math
from copy import deepcopy
import random
from env import connect4
import os
import ast
from tqdm import trange
import sqlite3
from sqlite3 import Error
from typing import Tuple


class MCTF:
    def __init__(self):
        self.root_id = 0
        self.env = connect4(main_page=False)
        self.state = self.env.state  # deep copy? shallow copy?


    def __call__(self, tree_path, player):
        self.player = player
        self.con = self.connection(path=tree_path)
        node = self.node_search((0,))
        if node == None:  # root node 없음
            node = self.create_root_node(state=self.state, player=self.player)

        self.env.set_state(state=self.state)

        
        
    def connection(self, path:str):
        try:
            con = sqlite3.connect(path)
            return con
        except Error: print('Error')

    def node_search(self, node_id):
        sql = 'SELECT child, win, visit FROM TREE WHERE node_id=?'
        cur = self.con.cursor()
        cur.execute(sql, (str(node_id),))
        data = cur.fetchone()
        if data == None:
            return None
        child, win, visit = data
        tree = {'node_id' : node_id, \
                # 'state' : self.state, \
                # 'player' : self.player, \
                # 'state' : np.array(ast.literal_eval(state), dtype=np.int32).reshape((6,7)), \
                # 'player' : player, \
                'child' : ast.literal_eval(child), \
                # 'parent' : ast.literal_eval(parent), \
                'win' : win, \
                'visit' : visit}
        return tree


    def main(self, node_id:tuple = (0,), batch_size:int=1000):  # 4가지 phase를 통해 tree의 parameter update
        self.node_id =  node_id  # 현재 노드 id
        # expansion_visit_num = 10 # 확장 기준 방문 횟수 # hyperparameter

        if self.node_id == (0,) and self.node_search(node_id)['child'] == []: # root node? and child node X?
            self.expansion(node_id=self.node_id) # expansion -> simulation
        
        for _ in trange(batch_size): # batch_size 만큼 시뮬
            # if (_ % 10000) == 0: # <<<
            #     print('{}번 학습.'.format(_)) 

            self.simulation(node_id=self.node_id)


    def selection(self, node_id:tuple)->tuple: # node_id -> child_node_id
        def UCT(input_node_id:tuple, C:int=1.4) -> float:  # C : root(2)에 근사 # hyperparameter # input_node_id : 입력 노드
            node = self.node_search(input_node_id)
            win, visit = node['win'], node['visit']
            # win, visit = self.tree[input_node_id]['win'], self.tree[input_node_id]['visit']
            if visit == 0:
                return node, math.inf
            else:
                uct = (win/visit)  # 승률이 가장 높은 노드 고르기 

            return node, uct
            # if 
            # try: uct = (win/visit)*0.2 + C*( 8*ln(parent_visit)/visit )**0.5  # <<< UCT 변형
                
            # try: uct = (win/visit) + C*( ln(parent_visit)/visit )**0.5  # UCT formula / formula : x_i + C*root(ln(t)/n_i)
            # except ZeroDivisionError: return math.inf  # 0으로 나눈다면 무한대 반환

            # if (win/visit) == 1:uct = math.inf

            # return uct
  
        node = self.node_search(node_id)
        child_node_id = node['child']
        # child_node_id = self.tree[node_id]['child'] # 자식 노드 id 리스트
        child_node_uct = []; uct_app = child_node_uct.append
        child_node_list = []; cn_app = child_node_list.append # 자식 노드 (dict)
        for _id in child_node_id:
            n, u = UCT(input_node_id=_id)
            uct_app(u); cn_app(n)
            # uct_app(UCT(input_node_id=_id))  # 자식 노드들의 UCT 값을 child_node_uct에 저장

        # print(node_id); print(child_node_uct)
        n = child_node_uct.index(max(child_node_uct))
        selected_node_id = child_node_id[n]; selected_node = child_node_list[n]
        # selected_node_id = child_node_id[child_node_uct.index(max(child_node_uct))]  # UCT 값의 최대값을 받아온 뒤, index를 받아오고 그 값의 자식 노드 id 받아옴
        return selected_node_id, selected_node



if __name__ == "__main__":
    mctf = MCTF()
    mctf('tree.db', 1)