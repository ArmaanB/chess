class Board:
    board = [
        [10, 11, 9, 8, 7, 9, 11, 10],
        [0, 12, 12, 12, 12, 12, 12, 12],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 12, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [4, 5, 3, 2, 1, 3, 5, 4],
    ]
    selected_tile = None

    def __init__(self):
        pass

    def get_tile(self,index):
        return self.board[index[1]][index[0]]

    def set_tile(self,index,value):
        self.board[index[1]][index[0]] = value

    def mouse_click(self,index):
        if (
            self.get_tile(index) != 0
            and self.get_tile(index) <= 6
        ):
            self.selected_tile = index
        else:
            if self.selected_tile is not None:
                self.move_piece(self.selected_tile,index)
                self.selected_tile = None

    def move_piece(self,old,new):
        save_board = [[y for y in x] for x in self.board]

        if self.piece_can_move(self.get_tile(old),old,new):
            self.set_tile(new,self.get_tile(old))
            self.set_tile(old,0)

        for item in enumerate(self.board):
            if 1 in item[1]:
                king_index = (item[1].index(1),item[0])

        if self.in_check(king_index,1):
            self.board = save_board

    def piece_can_move(self,piece,old,new):
        xd = abs(old[0] - new[0])
        yd = abs(old[1] - new[1])
        piece = (piece - 1) % 6 + 1
        if piece == 1:
            return (xd <= 1 and yd <= 1)
        elif piece == 2:
            return self.bishop_check(old,new) or self.rook_check(old,new)
        elif piece == 3:
            return self.bishop_check(old,new)
        elif piece == 4:
            return self.rook_check(old,new)
        elif piece == 5:
            return ((xd == 1 and yd == 2) or (xd == 2 and yd == 1))
        elif piece == 6:
            if new[1] >= old[1]:
                return False
            if xd == 0:
                if self.get_tile(new) != 0:
                    return False
                return (yd == 1 or (yd == 2 and old[1] == 6))
            elif xd == 1:
                return (self.get_tile(new) != 0 and yd == 1)
        return False

    def bishop_check(self,old,new):
        if abs(old[0] - new[0]) == abs(old[1] - new[1]):
            xm = sign(new[0] - old[0])
            ym = sign(new[1] - old[1])
            x = old[0] + xm
            y = old[1] + ym
            while x != new[0]:
                if self.get_tile((x,y)) != 0:
                    return False
                x += xm
                y += ym
            return True
        return False

    def rook_check(self,old,new):
        if old[1] == new[1]:
            for i in range(min(old[0],new[0]) + 1,max(old[0],new[0])):
                if self.get_tile((i,old[1])) != 0:
                    return False
            return True
        elif old[0] == new[0]:
            for i in range(min(old[1],new[1]) + 1,max(old[1],new[1])):
                if self.get_tile((old[0],i)) != 0:
                    return False
            return True
        return False

    def in_check(self,pos,attacker):
        offset = attacker * 6

        if (
            self.rook_attack(pos,1,False,offset) or
            self.rook_attack(pos,-1,False,offset) or
            self.rook_attack(pos,1,True,offset) or
            self.rook_attack(pos,-1,True,offset)
        ):
            return True

        if (
            self.bishop_attack(pos,1,1,offset) or
            self.bishop_attack(pos,-1,1,offset) or
            self.bishop_attack(pos,1,-1,offset) or
            self.bishop_attack(pos,-1,-1,offset)
        ):
            return True

        knights = [
            (-1,-2),
            (-2,-1),
            ( 1,-2),
            ( 2,-1),
            (-1, 2),
            (-2, 1),
            ( 1, 2),
            ( 2, 1)
        ]
        for item in knights:
            test = (pos[0] + item[0],pos[1] + item[1])
            if not self.in_bounds(test):
                continue
            if self.get_tile(test) == offset + 5:
                return True

        around = [
            (0,1),
            (1,1),
            (1,0),
            (1,-1),
            (0,-1),
            (-1,-1),
            (-1,0),
            (-1,1)
        ]
        for item in around:
            test = (pos[0] + item[0],pos[1] + item[1])
            if not self.in_bounds(test):
                continue
            if self.get_tile(test) == offset + 1:
                return True

        pawn_direction = 1
        if attacker == 1:
            pawn_direction = -1
        if (
            self.get_tile((pos[0] + 1,pos[1] + pawn_direction)) == offset + 6 or
            self.get_tile((pos[0] - 1,pos[1] + pawn_direction)) == offset + 6
        ):
            return True

        return False

    def bishop_attack(self,pos,x_sign,y_sign,offset):
        for i in range(1,8):
            test = (pos[0] + x_sign * i,pos[1] + y_sign * i)
            if not self.in_bounds(test):
                break
            if self.get_tile(test) != 0:
                if self.get_tile(test) in [offset + 3,offset + 4]:
                    return True
                break
        return False

    def rook_attack(self,pos,direction,row,offset):
        end = 8
        if direction == -1:
            end = -1
        for i in range(pos[1] + direction,end,direction):
            test = (i,pos[1])
            if row:
                test = (pos[0],i)
            if self.get_tile(test) != 0:
                if self.get_tile(test) in [offset + 2,offset + 4]:
                    return True
                break

    def in_bounds(self,pos):
        return (
            pos[0] >= 0 and
            pos[0] < 8 and
            pos[1] >= 0 and
            pos[1] < 8
        )

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0
