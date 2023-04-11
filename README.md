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
> > SQLite DB 제작. # Table : TREE (node_id, state, player, child, parent, win, visit) # PK : node_id
> ### 7. tree_txt_to_db.py
> > .txt 파일(텍스트 파일)로 저장된 트리를 데이터 베이스로 저장
> ### 8. MCTF_DB.py
> > .db 파일(데이터 베이스)에서 데이터를 읽어 학습 시키고 저장함. 학습이 진행하면서 업데이트 된 데이터를 즉시 데이터 베이스에서 수정함.
> ### 9. train_db.py
> > MCTF_DB.py를 이용해 에이전트를 학습시키는 코드. 기존의 학습 횟수만큼 학습하는 방법대신 정해진 시간동안 학습하는 방법으로 변경.
> ### 10. MCTF_DB_game.py
> > 4 in a row.py에서 사용하는 함수들 제작.
> ### 11. 4 in a row db.py
> > 기존 4 in a row.py에서 .txt 파일 대신에 .db 파일을 읽어옴. 모든 데이터를 읽어오지 않고 현재 상태에 대한 데이터만 읽어온다.
------------
> ### 12. MCTF_DB_save_once.py
> > 학습이 진행되면서 즉시 데이터를 업데이트하는 MCTF_DB.py에서 한번에 업데이트 하는 방식으로 바꾼 코드.
> ### 13. train_db_save_all.py
> > MCTF_DB_save_once.py를 사용해 에이전트를 학습시키는 코드.
