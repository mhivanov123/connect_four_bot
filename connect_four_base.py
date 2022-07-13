import random
import copy

class connect_four():
    def __init__(self):
        self.board = [['*' for _ in range(6)] for _ in range(7)]
        self.end = False
        self.tie = False

    def get_available(self):
        return [str(n) for n in range(7) if any(item=='*' for item in self.board[n])]
                        
    def move(self,col,piece):
        find = self.board[int(col)].index('*')
        self.board[int(col)][find] = piece
        self.check(piece,(int(col),find))

    def check(self,piece,coord):
        col,row = coord[0],coord[1]
        if any([2 < row and self.board[col][row-3] == self.board[col][row-2] == self.board[col][row-1] == self.board[col][row] == piece,
        col < 4 and self.board[col][row] == self.board[col+1][row] == self.board[col+2][row] == self.board[col+3][row] == piece,
        0 < col < 5 and self.board[col-1][row] == self.board[col][row] == self.board[col+1][row] == self.board[col+2][row] == piece,
        1 < col < 6 and self.board[col-2][row] == self.board[col-1][row] == self.board[col][row] == self.board[col+1][row] == piece,
        2 < col and self.board[col-3][row] == self.board[col-2][row] == self.board[col-1][row] == self.board[col][row] == piece,
        row < 3 and col < 4 and self.board[col][row] == self.board[col+1][row+1] == self.board[col+2][row+2] == self.board[col+3][row+3] == piece,
        0 < row < 4 and 0 < col < 5 and self.board[col-1][row-1] == self.board[col-1][row-1] == self.board[col+1][row+1] == self.board[col+2][row+2] == piece,
        1 < row < 5 and 1 < col < 6 and self.board[col-2][row-2] == self.board[col-1][row-1] == self.board[col][row] == self.board[col+1][row+1] == piece,
        2 < row and 2 < col and self.board[col-3][row-3] == self.board[col-2][row-2] == self.board[col-1][row-1] == self.board[col][row] == piece,
        col < 4 and row > 3 and self.board[col][row] == self.board[col+1][row-1] == self.board[col+2][row-2] == self.board[col+3][row-3] == piece,
        0 < col < 5 and 2 < row < 5 and self.board[col-1][row+1] == self.board[col][row] == self.board[col+1][row-1] == self.board[col+2][row-2] == piece,
        1 < col < 6 and 1 < row < 4 and self.board[col-2][row+2] == self.board[col-1][row+1] == self.board[col][row] == self.board[col+1][row-1] == piece,
        2 < col and row < 3 and self.board[col-3][row+3] == self.board[col-2][row+2] == self.board[col-1][row+1] == self.board[col][row] == piece]):
            self.end = True
        else:
            if all(all(self.board[m][n] != '*' for n in range(6)) for m in range(7)):
                self.end = True  
                self.tie = True

    def board2string(self):
        return ''.join([''.join(x) for x in self.board])

    def __str__(self):
        res = ''
        for r in range(len(self.board[0])):
            temp = '|'
            for c in range(len(self.board)):
                temp+=self.board[c][r]
                temp+='|'
            res=temp+'\n'+res
        return res

class c4_game():
    def __init__(self,game,player1,player2):
        self.game = game
        self.p1 = player1
        self.p2 = player2
        self.order = self.p1.piece
        
    def move_request(self,player):
        """
        ask player to make move
        """
        player.get_move(self.game)

    def play(self):
        """
        continue waking moves until game is over
        """
        while not self.game.end:
            if self.order == self.p1.piece:
                self.move_request(self.p1)
                self.order = self.p2.piece
            
            elif self.order == self.p2.piece:
                self.move_request(self.p2)
                self.order = self.p1.piece

        else:
            if self.game.tie:
                self.p1.temp.append('tie')
                self.p2.temp.append('tie')
            elif self.order == self.p1.piece:
                self.p1.temp.append('loss')
                self.p2.temp.append('win')
            else:
                self.p2.temp.append('loss')
                self.p1.temp.append('win')

            self.p1.update_memory(self.game)
            self.p2.update_memory(self.game)

class player():
    def __init__(self,piece):
        self.piece = piece
        self.opp = 'X' if piece == 'O' else 'O'
        self.learning_rate = 0.9
        self.eve = 0.2
        self.memory = {}
        self.temp = []

    def get_move(self,board):
        """
        give action to be taken
        """
        s = board.board2string()
        available = board.get_available()

        if random.random() < self.eve and s in self.memory:
            a = max([(key,value) for key,value in self.memory[s].items() if key in available],key = lambda x: x[1])[0]

        else:
            a = random.choice(available)

        board.move(a,self.piece)
        s_ = copy.deepcopy(board.board)
        self.temp.append((s,a,s_))
        

    def update_memory(self,board):
        """
        q learning function. rewards 1 for 
        """
        for n in range(len(self.temp)-2,-1,-1):
            s = self.temp[n][0]
            a = self.temp[n][1]
            s_ = self.temp[n][2]

            if self.temp[n+1] == 'win':
                r = 1
                pred = 0
            elif self.temp[n+1] == 'loss':
                r = -1
                pred = 0
            elif self.temp[n+1] == 'tie':
                r = -1
                pred = 0
            else:
                r = 0
                pred = self.predict_state(s_)
            
            if s in self.memory:         
                if a in self.memory[s]:
                    self.memory[s][a] = (1- self.learning_rate)*self.memory[s][a] + self.learning_rate*(r+pred)
                else:
                    self.memory[s][a] = self.learning_rate*(r + pred)
            else:
                self.memory[s] = {a: self.learning_rate*(r + pred)}
        self.temp = []
        
    def pseudo_available(self,board):
        return [str(n) for n in range(7) if any(item=='*' for item in board[n])]

    def pseudo_move(self,board,col):
        copy_board = copy.deepcopy(board)
        find = copy_board[int(col)].index('*')
        copy_board[int(col)][find] = self.opp
        return self.board2string(board)

    def string2board(self,string):
        board = []
        while string:
            board.append([x for x in string[:6]])
            string = string[6:]
        return board

    def board2string(self,board):
        return ''.join([''.join(x) for x in board])

    def predict_state(self,board):
        opts = self.pseudo_available(board)
        num_opts = max(len(opts)-1,1)

        ret = 0
        for move in opts:
            fake_board_str = self.pseudo_move(board,move)
            ret += max(self.memory.get(fake_board_str,{0:0}).values())
        return ret/num_opts