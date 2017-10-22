import numpy as np

class Reversi ():
    
    def __init__ (self, n=8):
        
        ### あるマスの周囲を探索するのに使用
        self.dx = np.array([1, 1, 1, 0, 0, -1, -1, -1])
        self.dy = np.array([1, 0, -1, 1, -1, 1, 0, -1])
        
        ### n:辺の長さ
        ### board:盤面を表す2dのndarray
        ### 黒=1, 白=-1, 空白=0
        self.n = n
        self.board = np.zeros(self.n*self.n).reshape(self.n, self.n)
        self.keep_board = self.board.copy()
        
        ### 真ん中に黒白2個ずつ置いてゲームスタート
        self.board[self.n//2][self.n//2] = -1
        self.board[self.n//2-1][self.n//2-1] = -1
        self.board[self.n//2-1][self.n//2] = 1
        self.board[self.n//2][self.n//2-1] = 1
        
        ### 黒が先手
        self.turn = 1
    
        ### パスの回数を記憶
        self.pass_ = 0
        self.keep_pass_ = self.pass_
        
        ### 確定石の個数を記録しておく
        self.memo = np.zeros(self.n*self.n).reshape(self.n, self.n)
        
        ### 場所による評価
        self.score = np.array([[30, -12, 0, -1, -1, 0, -12, 30], [-12, -15, -3, -3, -3, -3, -15, -12], [0, -3, 0, -1, -1, 0, -3, 0], [-1, -3, -1, -1, -1, -1, -3, -1], [-1, -3, -1, -1, -1, -1, -3, -1], [0, -3, 0, -1, -1, 0, -3, 0], [-12, -15, -3, -3, -3, -3, -15, -12], [30, -12, 0, -1, -1, 0, -12, 30]])
        
        self.board_ex = np.array([[-1., -1., -1., -1., -1., -1., -1.,  1.], [-1., -1., -1., -1., -1., -1., -1.,  1.], [-1., -1., -1., -1., -1., -1., -1.,  1.], [-1., -1., -1., -1., -1., -1., -1.,  1.], [-1., -1., -1., -1., -1., -1., -1.,  1.], [-1., -1., -1.,  1.,  1.,  1.,  1.,  1.], [-1., -1., -1., 0., 0., 0.,  0.,  1.], [1.,  1.,  -1.,  1.,  1.,  -1.,  -1.,  -1.]])
        
        self.x = -1
        self.y = -1

                                    
    def search (self):
        ### 基本的にspaceが欲しい関数
        ### space:手番のプレーヤーが置くことができるマスと開放度の2dのndarray
        ### space = [x, y]
        
        ### spaceの初期化
        self.space = np.array([]).astype(np.uintc)

        ### 全探索
        for h in range(self.n):
            for w in range(self.n):
                sign = 1
                
                ### h,wをx,yに置き換える(なくても良い)
                x, y = h, w
                
                ### すでに置いてあるマスはNG
                if self.board[x][y] == 0:
                
                    ### board[x][y]の周囲を調べる
                    for i in range(8):
                        
                        ### 盤面をはみ出すケースと周囲が自色or空白のケースを削除
                        if 0 <= x + self.dx[i] <= self.n - 1 and 0 <= y + self.dy[i] <= self.n - 1 and self.board[x+self.dx[i]][y+self.dy[i]] == -self.turn:
                        
                            idx_x = x + self.dx[i]
                            idx_y = y + self.dy[i]
                        
                            ### (dx,dy)の方向に黒白を見ていく
                            while True:
                        
                                ### 盤面をはみ出すケースを削除
                                if idx_x < 0 or idx_x >= self.n or idx_y < 0 or idx_y >= self.n:
                                    break
                                
                                ### マスが空白のケースを削除
                                if self.board[idx_x][idx_y] == 0:
                                    break
                                
                                ### 相手色なら次へ
                                elif self.board[idx_x][idx_y] == -self.turn:
                                    
                                    ###次のマスへ
                                    idx_x += self.dx[i]
                                    idx_y += self.dy[i]
                                
                                ### 自色ならそこで終了
                                elif self.board[idx_x][idx_y] == self.turn:
                                    #if len(self.space) == 0:
                                    self.space = np.append(self.space, np.array([x, y])).reshape(-1, 2)
                                    sign = 0
                                    break
                                    
                                ### errorの場合
                                else:
                                    print("Error")
                                    
                            if sign == 0:
                                break
                                    

    def put (self):
        ### boardを更新
        
        ### 置くところがなければパス
        if len(self.space) == 0:
            self.turn *= -1
            self.pass_ += 1
            
        else:
            self.pass_ = 0
    
            ### turn(1 or -1)を置く
            self.board[self.x][self.y] = self.turn
        
            ### 間のものをひっくり返す
            ### 置いた座標の次のところから最終地点に着くまで回す
            self.obvert()
        
            ### 手番を交代
            self.turn *= -1
            
    def com_turn (self):
        ### コンピュータの手番
        
        ### おける場所を探す
        self.search()
        
        if len(self.space) == 0:
            self.put()
            print("パスします")
        
        else:
            self.choose()
        
            ### 置く
            self.put()
            
            print(self.x, self.y)
            
    def my_turn (self):
        ### 自分の手番
        
        ### おける場所を探す
        self.search()
        
        ### 置く場所ない場合
        if len(self.space) == 0:
            print("パスします")
            self.pass_ += 1
            self.turn *= -1
            
        ### 置くとこをinputする
        else:
            self.pass_ = 0
            while True:
                print("どこに置きますか？")
                message = input()
                
                try:
                    ### 数字なら普通
                    self.x, self.y = map(int, message.split())
                        
                except ValueError:
                    ### 違ったら対応
                    
                    if message == "待った":
                        self.board = self.keep_board.copy()
                        self.pass_ = self.keep_pass_
                        return self.my_turn()
                    
                    elif message == "盤":
                        print(self.board)
                        continue
                        
                ### 数字が正当ならOK
                if self.x in self.space[:, 0] and self.y in self.space[:, 1]:
                    break
                    
                else:
                    print("そこには置けません")
            
            ### 待った用に保持
            self.keep_board = self.board.copy()
            self.keep_pass_ = self.pass_
            
            ### turn(1 or -1)を置く
            self.board[self.x][self.y] = self.turn
        
            ### ひっくり返す
            self.obvert()
            
            ### 手番を交代
            self.turn *= -1
    
    
    def judge (self):
        ### 勝敗を判定する
        
        if sum(sum(self.board == np.zeros(self.n**2).reshape(self.n, self.n) + 1)) > sum(sum(self.board == np.zeros(self.n**2).reshape(self.n, self.n) - 1)):
            print("Black Win!!!")
        elif sum(sum(self.board == np.zeros(self.n**2).reshape(self.n, self.n) + 1)) < sum(sum(self.board == np.zeros(self.n**2).reshape(self.n, self.n) - 1)):
            print("White Win!!!")
        else:
            print("Draw")
            
    def obvert (self):
        ### ひっくり返す関数
        
        ### 8方向に見ていき、自色に当たるまで繰り返す
        for i in range(8):
            x = self.x + self.dx[i]
            y = self.y + self.dy[i]
            
            aim = []
            
            while True:
                if 0 <= x < self.n and 0 <= y < self.n:
                    if self.board[x][y] == 0:
                        break
                
                    elif self.board[x][y] == self.turn:
                        for pos in aim:
                            self.board[pos[0], pos[1]] = self.turn
                        break
                            
                    elif self.board[x][y] == -self.turn:
                        aim.append([x, y])
                        x += self.dx[i]
                        y += self.dy[i]
                
                else:
                    break



    def place_score (self):
        ### 場所による局面評価を返す
        
        score = 0
        
        for h in range(self.n):
            for w in range(self.n):
                if self.board[h][w] == self.turn:
                    score += self.score[h][w]
        
        return score
    
    
    def side (self):
        ### 辺に石があるかないかをboolで返す
        
        for h in range(self.n):
            if h == 0 or h == 7:
                for w in range(7):
                    if self.board[h][w] != 0:
                        return True
                    
            else:
                if self.board[h][0] != 0 or self.board[h][7] != 0:
                    return True
        
        return False
    
    def corner (self):
        ### 各角4マスに石があるかないかをboolで返す
        
        for h in [0, 1, 6, 7]:
            for w in [0, 1, 6, 7]:
                if self.board[h][w] == self.turn:
                    return True
                
        return False
                
                    
    def choose (self):
        ### 序盤、中盤、終盤で戦略を変える
        ### start:序盤で使う関数
        ### middle:中盤で使う関数
        ### end:終盤で使う関数
        
        ### 序盤は手数が20手になるか、辺に石が来るまで
        if sum(sum(self.board != np.zeros_like(self.board))) <= 20 and not self.side():
            ### 局面評価値
            self.choose_score()
            
        ### 中盤は手数が54手になるまで
        elif sum(sum(self.board != np.zeros_like(self.board))) <= 54:
            ### 置ける位置が少なくなるように打つ
            self.choose_next_space()
            
        ### 終盤はそれ以降
        else:
            ### 全読み
            self.choose_count()
            
            
    def choose_score (self):
        ### 局面評価値を返す
        
        ### score:各々の場所に打った後の評価値のarray
        score = np.array([]).astype(np.uintc)
            
        ### selfを記憶
        X = self.x
        Y = self.y
        board = self.board.copy()
            
        ### 考えうる手全てで評価値を計算
        for i in range(len(self.space)):
                
            ### 盤面を変える
            self.x = self.space[i][0]
            self.y = self.space[i][1]
            self.board[self.x][self.y] = self.turn
            self.obvert()
                
            ### 評価値計算
            score = np.append(score, self.place_score())
                
            ### 元に戻す
            self.x = X
            self.y = Y
            self.board = board.copy()
                
        ### 最大値の中からランダムに選んで決定
        idx = np.random.choice(np.flatnonzero(score == score.max()))
        self.x = self.space[idx][0]
        self.y= self.space[idx][1]
        
        return score
        
        
            
    def choose_next_space(self):
        ### 次の相手の選択肢をなくすように打つ
        board = self.board.copy()
        turn = self.turn 
        space = self.space.copy()
        next_space = np.array([])
        
        if len(space) != 0:
            for i in range(len(space)):
                self.board = board.copy()
                self.space = space.copy()
                self.x = space[i][0]
                self.y = space[i][1]
                self.board[self.x][self.y] = turn
                self.turn = turn
                self.obvert()
                self.turn = -turn
                self.search()
                next_space = np.append(next_space, len(self.space))
                
                if len(next_space) != 0:
                    
                    ### X置きについて
                    punish_x = 15
                    reward_x = 3
                    if space[i][0] == 1 and space[i][1] == 1:
                        if board[0][0] != turn:
                            next_space[i] += punish_x
                        else:
                            next_space[i] -= reward_x
                    elif space[i][0] == 1 and space[i][1] == 6:
                        if board[0][7] != turn:
                            next_space[i] += punish_x
                        else:
                            next_space[i] -= reward_x
                    elif space[i][0] == 6 and space[i][1] == 1:
                        if board[7][0] != turn:
                            next_space[i] += punish_x
                        else:
                            next_space[i] -= reward_x
                    elif space[i][0] == 6 and space[i][1] == 6:
                        if board[6][6] != turn:
                            next_space[i] += punish_x
                        else:
                            next_space[i] -= reward_x

                    ### C置きについて
                    punish_c = 10
                    reward_c = 5
                    if space[i][0] == 0 and space[i][1] == 1:
                        if board[0][0] != turn:
                            next_space[i] += punish_c
                        else:
                            next_space[i] -= reward_c
                    elif space[i][0] == 1 and space[i][1] == 0:
                        if board[0][0] != turn:
                            next_space[i] += punish_c
                        else:
                            next_space[i] -= reward_c
                    elif space[i][0] == 0 and space[i][1] == 6:
                        if board[0][7] != turn:
                            next_space[i] += punish_c
                        else:
                            next_space[i] -= reward_c
                    elif space[i][0] == 1 and space[i][1] == 7:
                        if board[0][7] != turn:
                            next_space[i] += punish_c
                        else:
                            next_space[i] -= reward_c
                    elif space[i][0] == 6 and space[i][1] == 0:
                        if board[7][0] != turn:
                            next_space[i] += punish_c
                        else:
                            next_space[i] -= reward_c
                    elif space[i][0] == 7 and space[i][1] == 1:
                        if board[7][0] != turn:
                            next_space[i] += punish_x
                        else:
                            next_space[i] -= reward_x
                    elif space[i][0] == 6 and space[i][1] == 7:
                        if board[7][7] != turn:
                            next_space[i] += punish_c
                        else:
                            next_space[i] -= reward_c
                    elif space[i][0] == 7 and space[i][1] == 6:
                        if board[7][7] != turn:
                            next_space[i] += punish_x
                        else:
                            next_space[i] -= reward_x

                    ### 直後に四隅を取られる時は置かない
                    if len(self.space) != 0:
                        if np.array([0, 0]) in self.space or np.array([0, 7]) in self.space or np.array([7, 0]) in self.space or np.array([7, 7]) in self.space:
                            next_space[i] += 20
            
            
            idx = np.argmin(next_space)
            self.x = space[idx][0]
            self.y = space[idx][1]

        ###元に戻す
        self.board = board.copy()
        self.turn = turn
        self.space = space.copy()
   

    def dfs_count (self, s=1, pass_=0):
        
        ### 自分に都合よく打った時の次の一手を返す
        if s == 1:
            max_s = sum(sum(self.board==0))
            self.max_s = max_s
            
            ### init_xyには各手順の初手だけ記憶させる
            self.per_xy = []
            self.stone = np.array([])
            
            self.board_array = np.zeros((max_s+10)*self.n*self.n).reshape(max_s+10, self.n, self.n)
            self.space_list = [[] for i in range(max_s + 10)]
            self.turn_memo = self.turn

            ### self.spaceの初期化
            
            self.search()
            
            if max_s == 0:
                ### 最初のboard, spaceを記憶
                self.board_array[0] = self.board.copy()
                self.space_list[0]  = self.space.copy()
                pass
        
            elif max_s == 1:
                ### 最初のboard, spaceを記憶
                self.board_array[0] = self.board.copy()
                self.space_list[0]  = self.space.copy()
                self.x = self.space[0][0]
                self.y = self.space[0][1]
                self.per_xy.append([self.x, self.y, self.turn])
                
            else:
                ### 最初のboard, spaceを記憶
                self.board_array[0] = self.board.copy()
                self.space_list[0]  = self.space.copy()
                
                if len(self.space) == 0:
                    ### 置くところがないなら予測しない
                    self.res = np.array([])
                    self.dfs_count(s+1, pass_+1)
                    
                else:
                    l_0 = len(self.space)
                    for i in range(l_0):
                        self.turn = ((-1)**(s+1)) * self.turn_memo
                        ### 一番はじめは記憶
                        if i == 0:
                            self.board_array[s] = self.board.copy()
                            self.space_list[s]  = self.space.copy() 
                            
                        ### 分岐を遡り、selfに代入
                        self.board = self.board_array[s].copy()
                        self.space = self.space_list[s].copy()

                        self.x = self.space[i][0]
                        self.y = self.space[i][1]

                        ### 自色を置く
                        self.board[self.x][self.y] = self.turn

                        ### ひっくり返す
                        self.obvert()

                        ### 手筋を記憶
                        self.res = np.array([self.x, self.y, self.turn]).copy()

                        ### s=2へ
                        self.dfs_count(s+1, 0)
                            
        else:
            max_s = sum(sum(self.board == 0))
            self.turn = ((-1)**(s+1)) * self.turn_memo
            self.search()
            
            if max_s == 0:
                ### 全部埋まってたら終わり
                self.stone = np.append(self.stone, (len(self.stone), sum(sum(self.board == self.turn_memo)))).copy().reshape(-1, 2)
                while (len(self.res) < self.max_s * 3):
                    self.res = np.append(self.res, 1)
                self.per_xy.append(self.res)
            
            elif len(self.space) == 0:
                if pass_ >= 1:
                    ### パスが続いて終わった時
                    self.stone = np.append(self.stone, (len(self.stone), sum(sum(self.board == self.turn_memo)) + 0.5 * sum(sum(self.board == 0)))).copy().reshape(-1, 2)
                    while (len(self.res) < self.max_s * 3):
                        self.res = np.append(self.res, 1)
                    self.per_xy.append(self.res)
                else:
                    ### 一回目ならパス
                    self.dfs_count(s+1, 1)
                    
            else:
                l_1 = len(self.space)
                ### 全探索
                for i in range(l_1):
                    if i == 0:
                        ### s-1ターン目の直後のboard
                        self.board_array[s] = self.board.copy()
                        self.space_list[s] = self.space.copy()

                    self.board = self.board_array[s].copy()
                    self.space = self.space_list[s].copy()
                    self.x = self.space[i][0]
                    self.y = self.space[i][1]
                    self.turn = ((-1)**(s+1)) * self.turn_memo
                    self.res = self.res[: (self.max_s - max_s) * 3].copy()
                    self.board[self.x][self.y] = self.turn
                    self.obvert()
                    self.res = np.hstack((self.res, np.array([self.x, self.y, self.turn]))).copy()
                    self.dfs_count(s+1, 0)

                
    def MinMax (self):
        lst = [[] for i in range(self.max_s)]
        lst[self.max_s-1] = self.stone.copy()
        per_xy = self.per_xy.copy()
        for k in range(self.max_s-1):
            lst_ = np.array([])
            sign = -1
            for i in range(len(lst[self.max_s-1-k])):
                if sign < i:
                    if i == len(lst[self.max_s-1-k]) - 1:
                        res = np.array([lst[self.max_s-1-k][i]])
                    else:
                        res = np.array([lst[self.max_s-1-k][i]])
                        for j in range(i+1, len(lst[self.max_s-1-k])):
                            if (per_xy[int(lst[self.max_s-1-k][i][0])][:3*(self.max_s-1-k-1)] - per_xy[int(lst[self.max_s-1-k][j][0])][:3*(self.max_s-1-k-1)] == 0).all():
                                sign = j
                                res = np.append(res, lst[self.max_s-1-k][j]).reshape(-1, 2)
                            else:
                                break
                    if per_xy[int(lst[self.max_s-1-k][i][0])][3*(self.max_s-1-k)-1] == self.turn_memo:
                        lst_0 = res[0]
                        for j in range(len(res)):
                            if lst_0[1] < res[j][1]:
                                lst_0 = res[j]
                        lst_ = np.append(lst_, lst_0).reshape(-1, 2)
                    else:
                        lst_0 = res[0]
                        for j in range(len(res)):
                            if lst_0[1] > res[j][1]:
                                lst_0 = res[j]
                        lst_ = np.append(lst_, lst_0).reshape(-1, 2)
            lst[-2-k] = lst_
            
        ### per_xyのインデックスと最後の自色の数
        return lst
    
    def choose_count (self):
        ### 全読みを実行
        
        self.dfs_count()
        self.dfs_recover()
        if self.max_s != 1:
            best = self.per_xy[int(np.array((self.MinMax())[0]).ravel()[0])]
            self.x = best[0]
            self.y = best[1]
        else:
            if self.per_xy[0][2] == self.turn:
                self.x = self.per_xy[0][0]
                self.y = self.per_xy[0][1]
        self.dfs_recover()
        
    def dfs_recover (self):
        ### dfsした後に、元に戻す
        
        self.turn = self.turn_memo
        self.board = self.board_array[0].copy()
        self.space = self.space_list[0].copy()
    
    
#### 対局
if __name__ == "__main__":
    re = Reversi()
    while re.pass_ < 2:
        re.my_turn()
        re.com_turn()
    re.judge()
