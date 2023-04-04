from MCTS_NodeDrop import MCTF
from time import time

mctf = MCTF()

state = mctf.state
print('Loading Tree...')
tree = mctf.load_tree('tree_nd.txt')
print('Training')

mctf(state=state, player=1)
mctf.tree = tree


start_time = time()
batch_size = 2000000 # 100000000 : 13.32361h  # 6000000 : 7.74083h  # 40000000 : 5.6127h  # 2000000  : 0.29h # 1390000 : 0.3416h  # 10000000 : 1.42694h # 5000000 : 0.6h # 35000000 : 5.013h  # 50000000 : 7h over
mctf.main(batch_size=batch_size) 

print('\nSaving Tree')
mctf.save_tree('tree_nd.txt')
train_time = int(time() - start_time)

print(f'\n학습 시간 : {train_time/3600}h')
