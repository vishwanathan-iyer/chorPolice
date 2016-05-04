from __builtin__ import str
import os
from operator import pos


class Game:
    
    def __init__(self, arena_file):
        """
            __init__(Game, str) -> None
            Initializes the game board
        """
        self.rows = 0   # Number of rows in the arena
        self.cols = 0   # Number of columns in the arena
        self.next_id = 0    # Id to be assigned to the next player
        self.players = []   # self.players[i] returns the character for i'th player
        self.player_pos = []    # self.player_pos[i] return the position of i'th player
        self.started = False    # True if the game has started and False otherwise
        self.num_police = 0    # Number of policemen present
        self.arena = self.load_arena(arena_file)
    
    def load_arena(self, arena_file):
        """
            load_arena(Game) -> list of list of str
            Reads the arena from the file. The file must be in the following format
            Number of rows
            Number of columns
            One matrix row per line
            
            Space in file indicates walkable area, x indicates wall. Arena must be bounded by walls
            on all sides except for a slot for exit on bottom right
            
            arena[i][j] contains x if there is a wall at that location and '' otherwise
        """
        
        
        assert os.path.isfile(arena_file), "Can not find the specified arena file."
        
        arena = []  # Initialize the arena
        
        f = open(arena_file, 'r')
        
        self.rows = int(f.readline())
        self.cols = int(f.readline())
        
        row = 0;
        for line in f:
            col = 0
            arena.append([])
            line = line.strip()
            for character in line:
                arena[row].append(character)
                col += 1
            assert (col == self.cols), "File format is invalid"
            row += 1
        assert (row == self.rows), "File format is invalid"
        
        f.close()
        
        return arena
    
        
    def init_player(self, pos, type):
        """
            init_player(Game, (int, int), str) -> int
            Initializes the position of the player.
            pos: Specified position in the form (x, y)
            type: "chor" if a chor and police if a police
            Returns an id for the specified player if successful and None otherwise
        """
        (x, y) = pos
        assert not self.started, "Can not add players once the game has started"
        assert (self.arena[x][y] == " "), "Specified position is not available"
        assert (self.next_id < 100), "Can not add more than 1 player"
        
        id = self.next_id
        
        if type == "chor":
            if "c" in self.players:
                assert 0, "Can not have more than 1 chor in a game"
                return None
            
            self.players.append("c")
            self.player_pos.append(pos)
            (x, y) = pos
            self.arena[x][y] = "c"
            self.next_id += 1
            return id
                   
        elif type == "police":
            symbol = "p" + str(self.num_police)
            self.players.append(symbol)
            self.player_pos.append(pos)
            (x, y) = pos
            self.arena[x][y] = symbol
            self.next_id += 1
            self.num_police += 1
        
        else:
            assert 0, "Invalid type specified"
            return None
        
    
    def get_symbol(self, id):
        """
            get_symbol(Game, int) -> str
            Returns the symbol associated with the given id
        """
        assert ((id < len(self.players))  and id >= 0), "Invalid ID specified"
        return self.players[id]
    
    
    def get_position(self, id):
        """
            get_position(Game, int) -> (int, int)
            Returns the position of the specified id on the arena
        """
        assert ((id < len(self.players))  and id >= 0), "Invalid ID specified"
        return self.player_pos[id]
    
    
    def is_valid_move(self, id, new_pos):
        """
            is_valid_move(Game, int, (int, int)) -> bool
            Returns True if the specified new position is feasible for the given id in a single
            step and False otherwise
        """
        assert ((id < len(self.players))  and id >= 0), "Invalid ID specified"
        
        (x, y) = self.player_pos[id]
        (new_x, new_y) = new_pos
        
        if ((abs(new_x - x) > 1) or (abs(new_y - y) > 1)):  # Movnig more than 1 position
            return False
        
        if (new_x < 0 or new_x >= self.cols or new_y < 0 or new_y >= self.rows):    # Outside range
            return False
        
        if (self.arena[new_x][new_y] != " "):   # New position is not free
            return False
            
        return True
        
    
    def move(self, id, direction):
        """
            move(self, int, str) -> bool
            Moves the robot in the direction specified. If the specified move is not available
            then the player stays put
            Returns true if the move was successful
            Must not be called from outside this class
        """
        assert ((id < len(self.players))  and id >= 0), "Invalid ID specified"
        
        (x, y) = self.player_pos[id]
        
        if direction == "up":
            new_pos = (x - 1, y)
        elif direction == "down":
            new_pos = (x + 1, y)
        elif direction == "left":
            new_pos = (x, y - 1)
        elif direction == "right":
            new_pos = (x, y + 1)
        elif direction == "none":
            new_pos = (x, y)
        else:
            assert 0, "Invalid move specified"
            
        if (self.is_valid_move(id, new_pos)):
            self.player_pos[id] = new_pos
            (new_x, new_y) = new_pos
            self.arena[x][y] = " "  # Mark the old position vacant
            self.arena[new_x][new_y] = self.get_symbol(id)  # New position is now filled up
            return True
        
        return False



    def print_arena(self):
        for row in self.arena:
            for col in row:
                print col,
            print ""
    
        

if __name__ == '__main__':
    g = Game("arena.txt")
    g.print_arena()
    id = g.init_player((1, 1), "chor")
    while(True):
        direction = input("Enter direction: ")
        g.move(id, direction)
        g.print_arena()