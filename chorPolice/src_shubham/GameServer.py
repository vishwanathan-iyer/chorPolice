from Game import Game
import socket
import threading
import re

class Server:
    """
        Class Implementing the Game Server
    """
    def __init__(self, port):
        """
            __init__(Server, int) -> None
            Initializes the Game Server
        """
        self.game = Game("arena.txt")
        self.lock = threading.Lock()    # To control concurrent access to the game
        self.connections = []   # List of incoming connections, each connection is a client_thread
        self.soc = None  # Socket to be used for communication
        self.port = port    # Port number on which to listen
        self.started = False  # Status of the server
        self.can_recieve_commands = False
    
                
    def start_server(self):
        """
            start_server(Server) -> None
            Starts the server and prepares it to accept new connections
        """
        assert not self.started, "Server has already been started"
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open a socket
        self.soc.bind((socket.gethostname(), self.port)) # Bind the  socket
        self.soc.listen(5)   # Start listening, max 5 pending connection requests
        self.started = True
        connect_thread = threading.Thread(target = self.connect)
        connect_thread.start()
        
        key = "0"
        while key != "1":
            key = input("Enter 1 to start the game: ")
            if key == "1":
                self.can_recieve_commands = True
                self.start_game()
            
    
    def stop_server(self):
        """
            stop_server(Server) -> None
            Stops the server and closes all the connections
        """
        self.started = False
            
    
    def connect(self):
        """
            connect(Server) -> None
            Keeps on listening for new connections and connects to them as they are available
        """
        while self.started:
            (client_socket, address) = self.soc.accept()
            client = ClientThread(self, client_socket, address)
            self.connections.append(client)
    
    def start_game(self):
        """
            start_game(Server) ->
            Starts the game on this server
        """
        self.game.start_game()
        self.send_arena()
        
    
    def send_arena(self):
        """
            send_arena(Server) -> None
            Calls send_arena function on all the clients
        """
        for connection in self.connections:
            connection.send_arena()
    
            
            
            
            
class ClientThread:
    """
        ClientThread abstracts the thread for each client
    """
    def __init__(self, server, socket, addr):
        """
            __init__(ClientThread, Server, socket, address) -> None
            Initializes the client thread 
        """
        self.server = server
        self.soc = socket
        self.address = addr
        self.recieved = ""  # This is a dirty solution, fix this!
        self.connected = False  # Part of the dirty solution
        self.from_listening = False # Part of dirty solution
        self.id = -1    # Id for this client in the game
        self.add_client_to_game()    # Adds this client to the game
        
    
    def add_client_to_game(self):
        """
            add_client_to_game(ClientThread) -> None
            Adds this client to the Game
        """
        self.soc.send("__TYPE__")
        type = self.soc.recv(1024)
        
        if (self.server.game.is_valid_type(type)):
            self.send_arena()    # Send Initial Arena
            self.server.lock.acquire()  # Acquire Lock
            pos = self.get_initial_position()   # Get initial position from the client
            self.id = self.server.game.init_player(pos, type) # Request to add player
            self.server.lock.release()  # Release the lock
            self.connected = True
            t = threading.Thread(target = self.start_listening)
            t.start()
            
            
    def send_arena(self):
        """
            send_arena(ClientThread) -> None
            Sends the arena to the client
        """
        self.server.lock.acquire()
        self.can_recieve_commands = False
        self.soc.send("__ARENA__" + str(len(str(self.server.game))))   # Send arena command
        if (not self.connected or self.from_listening):
            self.recieved = self.soc.recv(1024);
        while (self.recieved != "__READY__"):   # Wait to recieve ready
            continue    # Ready will be recieved by start_listening
        assert (self.recieved == "__READY__"), "Invalid Protocol: " + recieved
        self.recieved = ""  # Clear Recieved
        self.soc.send(str(self.server.game)) # Send the arena
        self.can_recieve_commands = True
        self.server.lock.release()
        
        
    def get_initial_position(self):
        """
            get_initial_positon(ClientThread) -> (int, int)
            Recieves the initial requested position from the client
        """
        self.soc.send("__POSITION__")    # Send position Command
        position = self.soc.recv(1024)   # Wait for position
        nums = filter(None, re.split("[(), ]", position))
        return (int(nums[0]), int(nums[1]))
    
    
    def start_listening(self):
        """
            start_listening(ClientThread) -> None
            Start listening for move requests
        """ 
        while True:
            if self.can_recieve_commands:
                command = self.soc.recv(1024)
                if command.startswith("__READY__"):
                    self.recieved = command
                    continue
                self.server.lock.acquire()
                self.server.game.move(self.id, command)
                self.server.lock.release()
                self.from_listening = True
                self.server.send_arena()
                self.from_listening = False
                
                    
                    
                    
if __name__ == "__main__":
    server = Server(8694)
    server.start_server()