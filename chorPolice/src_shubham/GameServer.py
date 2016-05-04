from Game import Game
import socket
from Cheetah.Template import Lock
from distutils.cmd import Command

class Server:
    """
        Class Implementing the Game Server
    """
    def __init__(self):
        """
            __init__(Server) -> None
            Initializes the Game Server
        """
        self.game = Game("arena.txt")
        self.lock = threading.lock()    # To control concurrent access to the game
        self.connections = []   # List of incoming connections, each connection is a client_thread
        self.socket = None  # Socket to be used for communication
        self.started = False  # Status of the server
    
    
    def start_server(self):
        """
            start_server(Server) -> None
            Starts the server and prepares it to accept new connections
        """
        assert not self.started, "Server has already been started"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open a socket
        self.socket.bind((self.socket.gethostname(), 8694)) # Bind the  socket
        self.socket.listen(5)   # Start listening, max 5 pending connection requests
        self.started = True
        connect_thread = threading.thread(target="__connect")
                
    
    def stop_server(self):
        """
            stop_server(Server) -> None
            Stops the server and closes all the connections
        """
        self.started = False
        
                
    def __connect(self):
        """
            __connect(Server) -> None
            Keeps on listening for new connections and connects to them as they are available
        """
        while self.started:
            (client_socket, address) = serversocket.accept()
            client = ClientThread(self, client_socket, address)
            self.connections.append(client)
            
    
    def start_game(self):
        """
            start_game(Server) ->
            Starts the game on this server
        """
        self.game.start_game()
    
            
    class ClientThread:
        """
            ClientThread is an inner class for Server which abstracts the thread for each client
        """
        def __init__(self, server, socket, addr):
            """
                __init(ClientThread, Server, socket, address) -> None
                Initializes the client thread 
            """
            self.server = server
            self.socket = socket
            self.address = addr
            self.id = -1    # Id for this client in the game
            self.add_client_to_game()    # Adds this client to the game
            
        
        def add_client_to_game(self):
            """
                add_client_to_game(ClientThread) -> None
                Adds this client to the Game
            """
            self.socket.send("__TYPE__")
            type = self.socket.recv(1024)
            
            if (self.server.game.is_valid_type(type)):
                self.server.lock.acquire()  # Acquire Lock
                self.send_arena()    # Send Initial Arena
                pos = self.get_initial_position()   # Get initial position from the client
                self.id = self.server.game.init_player(pos, type) # Request to add player
                self.server.lock.release()  # Release the lock
                t = threading.thread("start_listening")
                
                
        def send_arena(self):
            """
                send_arena(ClientThread) -> None
                Sends the arena to the client
            """
            self.socket.send("__ARENA__")   # Send arena command
            self.socket.send(str(len(str(self.server.game))))   # Send arena length in characters
            self.socket.send(str(self.server.game)) # Send the arena
            
            
        def get_initial_position(self):
            """
                get_initial_positon(ClientThread) -> (int, int)
                Recieves the initial requested position from the client
            """
            self.socket.send("__POSITION__")    # Send position Command
            position = self.socket.recv(1024)   # Wait for position
            nums = position.split("() ,")
            return (int(nums[0]), int(nums[1]))
        
        
        def start_listening(self):
            """
                start_listening(ClientThread) -> None
                Start listening for move requests
            """ 
            while True:
                command = self.socket.recv(1024)
                self.server.lock.acquire()
                try:
                    self.server.game.move(self.id, command)
                finally:
                    self.server.lock.release()