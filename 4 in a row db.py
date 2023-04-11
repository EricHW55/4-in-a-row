from env import connect4
from MCTF_DB_game import MCTF

screen = connect4(main_page=True)
screen.main()
node_id = (0,)  # 현재의 node id
mctf = MCTF()
mctf('tree.db', 1)
# print(mcts.tree)
# node_id = mcts.find_node(node_id=node_id, tree=tree, state=deepcopy(screen.state))
# print(node_id)

def agent_action(mctf, screen, node_id):
    node_id, node = mctf.selection(node_id=node_id)
    # node = node_search(con, node_id)
    # screen.state = node['state'] #deepcopy(tree[node_id]['state'])
    screen.action(node_id[-1])
    # screen.player *= -1
    return node_id

node_id = agent_action(mctf, screen, node_id)

while True: 
    x = screen.main()
    if not screen.done:
        ...
    if not x == None:
        node_id += (x,)
        print(node_id)
        node_id = agent_action(mctf, screen, node_id)
        # con.close()