# 4 in a row RL
------------
## CODE
------------
> ### 1. env.py
> > 4 in a row ( connect four ) 게임 코드
> ### 2. MCTF.py
> > MCTF 알고리즘 구현 코드. # MCTF(Monte Carlo Tree Flow) : MCTS + Node Drop
> ### 3. train.py
> > env.py와 MCTF.py를 불러와 강화학습을 진행하는 코드. Tree를 .txt 파일로 저장
> ### 4. 4 in a row.py
> > train.py로 학습시킨 Tree를 불러와 env.py에서 게임을 진행하는 코드
------------
> ### 5. MCTS.py
> > MCTS 알고리즘 구현 코드. # MCTS 알고리즘을 통해 학습을 시키는 train.py는 업로드 X
------------
> ### +) tree_nd.txt
> > train.py로 학습한 Tree 저장 파일. 용량 문제로 업로드 X
------------
> ### 6. create_db.py
> > SQLite DB 제작. # Table : TREE (node_id, state, player, child, parent, win, visit)
> ### 7. tree_txt_to_db.py
> > .txt 파일(텍스트 파일)로 저장된 트리를 데이터 베이스로 저장
