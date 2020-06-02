participants = ['人','機'] #参加者を表す
state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']] #盤面
    
def checking(state): #盤面のチェックを行う。一つ目の要素は勝者の記号。二つ目の要素はゲームが終了状態かを記録
    flag = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] ==' ':
                flag = 1
    if flag ==0:
        return None, "draw"
    #横の列を確認する。ただし、空の時は除く。
    if (state[0][0] == state[1][0] and state[1][0] == state[2][0] and state[0][0] != ' '):
        return state[0][0], "yes"
    if (state[0][1] == state[1][1] and state[1][1] == state[2][1] and state[0][1] != ' '):
        return state[0][1], "yes"
    if (state[0][2] == state[1][2] and state[1][2] == state[2][2] and state[0][2] != ' '):
        return state[0][2], "yes"
    #対角成分を確認する。ただし、空の時は除く。
    if (state[0][0] == state[1][1] and state[1][1] == state[2][2] and state[0][0] != ' '):
        return state[1][1], "yes"
    if (state[2][0] == state[1][1] and state[1][1] == state[0][2] and state[2][0] != ' '):
        return state[1][1], "yes"
    #縦方向を確認する。ただし、空の時は除く。
    if (state[0][0] == state[0][1] and state[0][1] == state[0][2] and state[0][0] != ' '):
        return state[0][0], "yes"
    if (state[1][0] == state[1][1] and state[1][1] == state[1][2] and state[1][0] != ' '):
        return state[1][0], "yes"
    if (state[2][0] == state[2][1] and state[2][1] == state[2][2] and state[2][0] != ' '):
        return state[2][0], "yes"   
    return None, "no"

def movement(state, player, block): #操作を表す。既に埋まっていたらもう一度選ぶように指示する。
    if state[int((block-1)/3)][(block-1)%3] ==' ':
        state[int((block-1)/3)][(block-1)%3] = player
    else:
        block = int(input("違う場所を選んでください。"))
        movement(state, player, block)
    
def minmax(state, player): #minmax法
    winner , done = checking(state) #現在の状況を受け取る
    #まず報酬の設定を行う。
    if done == "yes" and winner == '機': #AIが勝つ報酬
        return 1000
    elif done == "yes" and winner == '人': #人間が勝つ報酬
        return -1
    elif done == "draw": #引き分けの場合
        return 0
    moves = [] #動きの情報を格納する配列
    empty = [] #空の場所を記録する。
    for i in range(3):
        for j in range(3):
            if state[i][j] ==' ':
                empty.append(i*3 + (j+1)) #空の場所を記録
    for empblock in empty: #置ける場所についてループ
        move = {} #dict型でpoint,indexを持つ。
        move['index'] = empblock
        newsituation = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        for i in range(3):
            for j in range(3):
                newsituation[i][j]=state[i][j]
        movement(newsituation, player, empblock)     
        if player == '機': #機はAIを表す。    
            result = minmax(newsituation, '人') #minmax法により算出されるポイントを保存
            move['point'] = result
        else: #人間
            result = minmax(newsituation, '機') #minmax法により算出されるポイントを保存
            move['point'] = result
        
        moves.append(move)
        #以上が以下からminmax法を行う上での準備
    #最も良い手を探す。ここからがminmax法の本質部分
    best_move = None
    if player == '機': #AIについて 
        best = -10000000
        for move in moves: #可能な動きについて
            if move['point'] > best: #今までのbestを超えるなら
                best = move['point'] #bestを更新
                best_move = move['index'] #その時の動きを取得
    else: #人間について
        best = 10000000
        for move in moves: #可能な動きについて
            if move['point'] < best: #今までのbestより小さいなら
                best = move['point'] #bestを更新
                best_move = move['index'] #その時の動きを取得
                
    return best_move #以上から最も良い動きを取得

def display_board(state): #盤面の図示
    print(' | ' + str(state[0][0]) + ' | ' + str(state[0][1]) + ' | ' + str(state[0][2]) + ' | ')
    print(' | ' + str(state[1][0]) + ' | ' + str(state[1][1]) + ' | ' + str(state[1][2]) + ' | ')
    print(' | ' + str(state[2][0]) + ' | ' + str(state[2][1]) + ' | ' + str(state[2][2]) + ' | ')
#以下は実際にゲームを行う
current_state = "no"
state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
display_board(state)
precedent = input("人間(人)かAI(機)のどちらが先行かを選んでください。")
winner = None
# 以下では記号であらわすのが面倒なため簡単のためにinde人で表すことにする。
if precedent == '人':
    current_player_idx = 0
else:
    current_player_idx = 1
        
while current_state == "no":
    if current_player_idx == 0: #人間の番
        block_choice = int(input("1~9から数字を選んでください。"))
        movement(state ,participants[current_player_idx], block_choice)
    else:   #AIの番
        block_choice = minmax(state, participants[current_player_idx])
        movement(state ,participants[current_player_idx], block_choice)
        print("AIが選んだ数字は" + str(block_choice))
    display_board(state)
    winner, current_state = checking(state) #その時の状態を受け取る。
    if winner != None: #勝者が確定した時
        print(str(winner) + "の勝ちです。")
    else: #勝者が確定していないので次のターンへ
        current_player_idx = not current_player_idx
        
    if current_state =="draw":
        print("引き分けです。")

