from MCTF_DB_save_once import MCTF
from time import time
from tqdm import tqdm

mctf = MCTF()

state = mctf.state
tree_path = 'tree.db'
mctf(tree_path=tree_path, player=1)


# 단위 : s(초)
train_time = 3600 * 0 \
            + 60 * 30 \
            + 0
# 30m/0.8h, 40m/1h, 1h/1.5h, 4h:5.5h


train_num = 0
print('\nTrainning...\n')
with tqdm(total=train_time) as pbar:
    pbar.set_description('학습률'); bar_time = round(time(), 2)
    start_time = int(time())
    while int(time()) - start_time < train_time:
        batch_size = 100
        mctf.main(batch_size=batch_size) 
        train_num += batch_size

        pbar.update(round(time()-bar_time))
        bar_time = round(time(), 2)
mctf.save_all()


train_time = int(time() - start_time)

print(f'\n학습 시간 : {round(train_time/3600, 5)}h')
print(f'학습 횟수 : {train_num}')
print(f'{train_num/train_time}/s')
