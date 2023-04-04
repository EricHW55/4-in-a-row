from env import connect4
from MCTF import MCTF
from copy import deepcopy
import random
from time import sleep

mcts = MCTF()
state = mcts.state
mcts(state=state, player=1)
# mcts.main(batch_size=10000000)
# tree = deepcopy(mcts.tree)
print('Loading Tree...')
tree = mcts.load_tree('tree_nd.txt')
mcts.tree = tree

screen = connect4(main_page=True)
# state = screen.state
node_id = (0,)  # 현재의 node id

# print(mcts.tree)
# node_id = mcts.find_node(node_id=node_id, tree=tree, state=deepcopy(screen.state))
# print(node_id)
node_id = mcts.selection(node_id=node_id, train=False)
screen.state = deepcopy(tree[node_id]['state'])
screen.player *= -1

while True:    
    x = screen.main()
    if not screen.done:
        print('regame')
        screen = connect4(main_page=True)
        node_id = (0,)

        node_id = mcts.selection(node_id=node_id, train=False)
        screen.state = deepcopy(tree[node_id]['state'])
        screen.player *= -1
        
        x = screen.main()
    if not x == None: 
        # print(x)
        # print(tree[node_id]['state'])
        node_id = mcts.find_node(node_id=node_id, tree=tree, state=deepcopy(screen.state))
        # print(tree[node_id]['state'])
        if node_id == None or tree[node_id]['child'] == []:  # tree에 없다면
            print('no tree')
            action_list = [_ for _ in range(7)]
            action_done = screen.action(x_pos=random.choice(action_list))
            # action = random.choice(action_number)   # actino random으로 선택
            # action_done = self.env.action(x_pos=action)  # action 진행
            while not action_done:  # action이 안된다면
                screen.change_player()
                # action = random.choice(action_number)  # action 다시 선택
                action_done = screen.action(x_pos=random.choice(action_list))  # action 진행
        else :
            # print(node_id)
            # print(tree[node_id]['child'])
            sleep(0.2)
            node_id = mcts.selection(node_id=node_id, train=False)
            screen.state = deepcopy(tree[node_id]['state'])
            screen.player *= -1
            print(tree[node_id]['child'])
        # state = deepcopy(screen.state)
        # print(screen.state)
    
# print(mcts.tree)
# print(len(list(mcts.tree)))

