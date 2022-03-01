import random
import copy as cp

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True   
        
        # detect drop phase
        count = 0
        for row in range(5):
            for col in range(5):
                if state[row][col] == self.my_piece:
                    count += 1
        if count == 4:
            drop_phase = False
    
        move = []
        
        if not drop_phase:
            j = Teeko2Player.Max_Value(self, state, -1, drop_phase)
            for row in range(5):
                for col in range(5):
                    if state[row][col] != j[row][col]:
                      if state[row][col] == ' ':
                          move.insert(0,(row,col))
                      else:
                          move.append((row,col))
        else:
            j = Teeko2Player.Max_Value(self, state, -1, drop_phase)
            for row in range(5):
                for col in range(5):
                    if state[row][col] != j[row][col]:
                      move.insert(0,(row,col))
        return move

    def Max_Value(self, state, depth, drop_phase):
        #stop recursion if final state or required depth is met
        if Teeko2Player.game_value(self,state) == -1:
            return -1
        if depth >= 0:
            return Teeko2Player.heuristic_game_value(self, state)
        # initialize a value smaller than any h value of all succ
        value = -2
        # initialze 'j' used to store best succ
        j = state
        #  all succ of current state
        succ = Teeko2Player.succ(self, state, drop_phase)
        # increment of depth 
        depth += 1
        # loop over all current succ
        for i in range (len(succ)):
            # recursive minimax algorithm to get a succ with best h value
            if Teeko2Player.Max_Value(self, succ[i], depth, drop_phase) > value:
                #update value and j if better succ is found
                value = Teeko2Player.Max_Value(self, succ[i], depth, drop_phase)
                j = succ[i]
        return j
    
    def succ(self, state, drop_phase):
        succ = []
        move = []
        selfcopy = Teeko2Player()
        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col]==' ':
                        move.clear()
                        move.append((row,col))
                        selfcopy.board = cp.deepcopy(self.board)
                        selfcopy.my_piece = cp.copy(self.my_piece)
                        Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                        succ.append(selfcopy.board)
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        if row+1<=4:
                            if state[row+1][col] == ' ':
                                move.clear()
                                move.append((row,col))
                                move.insert(0,(row+1,col))
                                selfcopy.board = cp.deepcopy(self.board)
                                selfcopy.my_piece = cp.copy(self.my_piece)
                                Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                succ.append(selfcopy.board)
                            if col-1>=0:
                                if state[row+1][col-1] == ' ':
                                    move.clear()
                                    move.append((row,col))
                                    move.insert(0,(row+1,col-1))
                                    selfcopy.board = cp.deepcopy(self.board)
                                    selfcopy.my_piece = cp.copy(self.my_piece)
                                    Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                    succ.append(selfcopy.board)
                            if col+1<=4:
                                if state[row+1][col+1] == ' ':
                                    move.clear()
                                    move.append((row,col))
                                    move.insert(0,(row+1,col+1))
                                    selfcopy.board = cp.deepcopy(self.board)
                                    selfcopy.my_piece = cp.copy(self.my_piece)
                                    Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                    succ.append(selfcopy.board)
                            if row-1>=0:
                                if state[row-1][col] == ' ':
                                    move.clear()
                                    move.append((row,col))
                                    move.insert(0,(row-1,col))
                                    selfcopy.board = cp.deepcopy(self.board)
                                    selfcopy.my_piece = cp.copy(self.my_piece)
                                    Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                    succ.append(selfcopy.board)
                            if col-1>=0:
                                 if state[row-1][col-1] == ' ':
                                     move.clear()
                                     move.append((row,col))
                                     move.insert(0,(row-1,col-1))
                                     selfcopy = cp.deepcopy(self)
                                     selfcopy.board = cp.deepcopy(self.board)
                                     selfcopy.my_piece = cp.copy(self.my_piece)
                                     Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                     succ.append(selfcopy.board)
                            if col+1<=4:
                                 if state[row-1][col+1] == ' ':
                                     move.clear()
                                     move.append((row,col))
                                     move.insert(0,(row-1,col+1))
                                     selfcopy.board = cp.deepcopy(self.board)
                                     selfcopy.my_piece = cp.copy(self.my_piece)
                                     Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                     succ.append(selfcopy.board)
                            if col+1<=4:
                                if state[row][col+1] == ' ':
                                    move.clear()
                                    move.append((row,col))
                                    move.insert(0,(row,col+1))
                                    selfcopy.board = cp.deepcopy(self.board)
                                    selfcopy.my_piece = cp.copy(self.my_piece)
                                    Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                    succ.append(selfcopy.board)
                            if col-1>=0:
                                if state[row][col-1] == ' ':
                                    move.clear()
                                    move.append((row,col))
                                    move.insert(0,(row,col-1))
                                    selfcopy.board = cp.deepcopy(self.board)
                                    selfcopy.my_piece = cp.copy(self.my_piece)
                                    Teeko2Player.place_piece(selfcopy, move, self.my_piece)
                                    succ.append(selfcopy.board)
        return succ
        
    def heuristic_game_value(self,state):
        if Teeko2Player.game_value(self,state) == 1 or Teeko2Player.game_value(self,state) == -1:
          return Teeko2Player.game_value(self,state)
        value = 0.0
        for row in range(1,4):
            for col in range(1,4):
                if(state[row][col] == self.my_piece):
                    value += 0.01 * (2 - abs(row - 2))
                    value += 0.01 * (2 - abs(col - 2))
                    if state[row+1][col] == ' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
                    if state[row+1][col+1] == ' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
                    if state[row+1][col-1] == ' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
                    if state[row][col-1] == ' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
                    if state[row][col+1] == ' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
                    if state[row-1][col] == ' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
                    if state[row-1][col-1] == ' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
                    if state[row-1][col+1] ==' ':
                        value += 0.01
                        if state[row+1][col] == self.my_piece:
                            value += 0.02
        for row in state:
            for i in range(3):
                if row[i] == row[i+1] == row[i+2] == self.my_piece:
                    if i != 0 and row[i-1] == ' ': value += 0.01
                    if i != 2 and row[i+3] == ' ': value += 0.01

        for col in range(5):
            for row in range(3):
                if state[row][col] == state[row+1][col] == state[row+2][col] == self.my_piece:
                    if row != 0 and state[row-1][col] == ' ': value += 0.01
                    if row != 2 and state[row+3][col] == ' ': value += 0.01
                    
        return value
    
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for row in range(0,2):
            for col in range(0,2):
                if state[row][col] != ' ' and state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3] == state[row][col]:
                    return 1 if state[row][col]==self.my_piece else -1
                
        # check / diagonal wins
        for row in range(0,2):
            for col in range(3,5):
                if state[row][col] != ' ' and state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3] == state[row][col]:
                    return 1 if state[row][col]==self.my_piece else -1
                
        # check diamond wins
        for col in range(1,4):
            for i in range(1,4):
                if state[row][col] == ' ' and state[row+1][col] == state[row-1][col] == state[row][col+1] == state[row][col-1] and state[row+1][col] != ' ':
                    return 1 if state[row+1][col]==self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()