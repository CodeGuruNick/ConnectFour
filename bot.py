def board_converter2(in_board):
    out_board, player1 = 0, 0
    counter = [0 for i in range(7)]
    for move in in_board:
        move = int(move)
        out_board += 1 << move + 7* counter[move]
        if sum(counter) % 2 == 1:
            player1 += 1 << move + 7* counter[move]
        counter[move] += 1
    player2 = player1 ^ out_board
    return player1, player2

def create_score2(player1, player2):
    board = player1 | player2
    tally1, tally2, weights = [0, 0, 0], [0, 0, 0], [2, 10, 1000]
    for i in range(len(bin(board)) - 23):
        for index, vertical in enumerate([129, 16513, 2113665]):
            for j in range(index + 1):
                vertical_four, vertical = 2113665 << i, vertical << i + 7*j
                if vertical_four & player1 == vertical and vertical_four & player2 == 0:
                    tally1[index] += 1
                if vertical_four & player2 == vertical and vertical_four & player1 == 0:
                    tally2[index] += 1
    for i in range(len(bin(board)) // 7 + 1):
        for k in range(4):
            for index, horizontal in enumerate([3, 7, 15]):
                for j in range(index + 1):
                    horizontal_four, horizontal = 15 << 7*i + k, horizontal << 7*i + k + j
                    if horizontal_four & player1 == horizontal and horizontal_four & player2 == 0:
                        tally1[index] += 1
                    if horizontal_four & player2 == horizontal and horizontal_four & player1 == 0:
                        tally2[index] += 1
    for i in range(3):
        for k in range(4):
            for index, diag1 in enumerate([257, 65793, 16843009]):
                for j in range(index + 1):
                    diag1_four, diag1 =  16843009 << 7*i + k, diag1 << 7*i + k + 8*j
                    if diag1_four & player1 == diag1 and diag1_four & player2 == 0:
                        tally1[index] += 1
                    if diag1_four & player2 == diag1 and diag1_four & player1 == 0:
                        tally2[index] += 1
    board, player1, player2 = bin(board)[2:], bin(player1)[2:], bin(player2)[2:]
    for i in range(0, len(board) // 7):
        board.join(player1[7*i:7*(i+ 1)][::-1])
    board = board[len(board)//2:]
    board, player1, player2 = int(board, 2), int(player1, 2), int(player2, 2)
    for i in range(3):
        for k in range(4):
            for index, diag1 in enumerate([257, 65793, 16843009]):
                for j in range(index + 1):
                    diag1_four, diag1 =  16843009 << 7*i + k, diag1 << 7*i + k + 8*j
                    if diag1_four & player1 == diag1 and diag1_four & player2 == 0:
                        tally1[index] += 1
                    if diag1_four & player2 == diag1 and diag1_four & player1 == 0:
                        tally2[index] += 1
    score = sum(weight*(p1 - p2) for p1, p2, weight in zip(tally1, tally2, weights))
    return score


class connect_four():
    def initial_moves(self, board):
        legal_moves = [str(i) for i in range(0, 7)]
        potential_move_index = 0
        while potential_move_index < len(legal_moves):
            if board.count(legal_moves[potential_move_index]) >= 6:
                del legal_moves[potential_move_index]
            else:
                potential_move_index += 1   
        return legal_moves

    def is_game_finished(self, test_board):
        test_board = self.board_converter(test_board)
        if test_board[0].count(0) == 0:
            return True
        else:
            total_of_totals = set()
            for row in range(0, 6):
                for column in range(0, 7):
                    for i in range(max(row - 2, 0), min(row + 1, 4)):
                        total = 0
                        for j in range(0, 4):
                            total += test_board[row + j - i][column]
                        total_of_totals.add(total)
                    for i in range(max(column - 3, 0), min(column + 1, 4)):
                        total = 0
                        for j in range(0, 4):
                            total += test_board[row][column + j - i]
                        total_of_totals.add(total)
                    for i in range(max(row - 2, 0, column - 3), min(column + 1, 4, row + 1)):
                        total = 0
                        for j in range(0, 4):
                            total += test_board[row + j - i][column + j - i]
                        total_of_totals.add(total)
                    for i in range(max(row - 2, 0, 3 - column), min(7 - column, 4, row + 1)):
                        total = 0
                        for j in range(0, 4):
                            total += test_board[row + j - i][column - j + i]
                        total_of_totals.add(total)
            if 4 in total_of_totals or 20 in total_of_totals:
                return True
            else:
                return False

    def board_converter(self, in_board):
        if '-' in in_board:
            return in_board
        else:
            out_board = [[0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0]]
            moves_played = len(in_board)
            for moves in range(0, moves_played):
                red_or_yellow = 4*((moves + 1) % 2) + 1
                row = 5
                while out_board[row][int(in_board[moves])] != 0:
                    row -= 1
                out_board[row][int(in_board[moves])] = red_or_yellow
            return out_board

    def create_score(self, board):
        row_weights = [2, 10, 1000]
        test_board = self.board_converter(board)
        score = 0
        for red_or_yellow in [1, 5]:
            row_tallies = [0, 0, 0]
            for connection_type in [2, 3, 4]:
                for row in range(6):
                    for test_move in range(4):
                        total = 0
                        for j in range(4):
                            total += test_board[row][test_move + j]
                        if total / red_or_yellow / connection_type == 1:
                            row_tallies[connection_type - 2] += 1
                for row in range(3):
                    for test_move in range(7):
                        total = 0
                        for j in range(4):
                            total += test_board[row + j][test_move]
                        if total / red_or_yellow / connection_type == 1:
                            row_tallies[connection_type - 2] += 1
                    for test_move in range(4):
                        total = 0
                        for j in range(4):
                            total += test_board[row + j][test_move + j]
                        if total / red_or_yellow / connection_type == 1:
                            row_tallies[connection_type - 2] += 1
                    for test_move in range(3, 7):
                        total = 0
                        for j in range(4):
                            total += test_board[row + j][test_move - j]
                        if total / red_or_yellow / connection_type == 1:
                            row_tallies[connection_type - 2] += 1
            if red_or_yellow == 1:
                for i in range(0, 3):
                    score += row_tallies[i]*row_weights[i]
            else:
                for i in range(0, 3):
                    score -= row_tallies[i]*row_weights[i]
        return score

class tree_object(connect_four):
    def __init__(self, board, depth, old_self):
        self.board = board
        self.depth = depth
        self.old_self = old_self
        self.alpha = old_self.alpha
        self.beta = old_self.beta
        self.score = 0
        self.done_game = self.is_game_finished(self.board)
        
    def __next__(self):
        return next(self.next_child)
    
    def give_children(self, children):
        if self.done_game is False:
            self.children = children
            self.next_child = iter(children)

class tree(connect_four):
    def __init__(self, board, depth):
        self.board, self.depth = board, depth
        self.old_self = None
        self.alpha = -10000
        self.beta = 10000
        self.children = [tree_object(
            self.board + move, 1, self) for move in super().initial_moves(self.board)]
        self.next_child = iter(self.children)
        self.best_move = 0
        self.expand_tree()
        
    def __next__(self):
        return next(self.next_child)

    def going_up(self, object_index):
        if len(object_index.old_self.board) % 2 == 1:
            object_index.old_self.alpha = max(object_index.old_self.alpha, object_index.beta)
        else:
            object_index.old_self.beta = min(object_index.alpha, object_index.old_self.beta)

    def previous(self, object_index, current_depth):
        while current_depth > 1 and object_index == object_index.old_self.children[-1]:
            self.going_up(object_index)
            object_index, current_depth = object_index.old_self, current_depth - 1
        if object_index != self:
            self.going_up(object_index)
            object_index = object_index.old_self
        current_depth = current_depth - 1
        return object_index, current_depth
    
    def initializing_alpha_beta(self, object_index):
        for child in object_index.children:
##            t, y = board_converter2(child.board)
            child.score = super().create_score(child.board)
        if len(object_index.board) % 2 == 1:
            object_index.alpha = max(object_index.alpha, max([child.score for child in object_index.children]))
        else:
            object_index.beta = min(object_index.beta, min([child.score for child in object_index.children]))
    
    def expand_tree(self):
        object_index, current_depth = self, 1
        while current_depth > 0:
            if object_index.alpha >= object_index.beta:
                object_index, current_depth = self.previous(object_index, current_depth)
                continue
            object_index, current_depth = next(object_index), current_depth + 1
            object_index.alpha, object_index.beta = object_index.old_self.alpha, object_index.old_self.beta
            object_index.give_children([tree_object(object_index.board + move,  current_depth, object_index) for move in super().initial_moves(object_index.board)])
            if object_index.done_game is True:
##                t, y = board_converter2(object_index.board)
                object_index.score = super().create_score(object_index.board)
                object_index.alpha, object_index.beta = object_index.score, object_index.score
                object_index, current_depth = self.previous(object_index, current_depth)
            elif current_depth >= self.depth:
                self.initializing_alpha_beta(object_index)
                object_index, current_depth = self.previous(object_index, current_depth)
        if len(self.board) % 2 == 1:
            self.best_move = [child.board[-1] for child in self.children if child.beta == self.alpha][0]
        else:
            self.best_move = [child.board[-1] for child in self.children if child.alpha == self.beta][0]

if __name__ == "__main__":
    print(tree('', 7).best_move)
