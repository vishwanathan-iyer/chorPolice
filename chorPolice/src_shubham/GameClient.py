import socket
import re
import threading

class Client:
    """
        Class implementing the client for the game
    """
    
    def __init__(self, server_addr, server_port, type):
        """
            __init__(Client, str, int) -> None
            Initializes the client to connect to the specified server at the specified port
        """
        self.connected = False
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((server_addr, server_port))   # Connect to the server
        self.connected = True
        self.type = type    # "chor" or "police"
        self.init_game()    # Initialize the game on the client side
        t = threading.Thread(target = self.start_listening)
        t.start()
        self.start_game()
        
        
    def init_game(self):
        """
            init_game(Client) -> None
            Initializes the game for the client by following the protocol
        """
        assert self.connected, "Client is not connected"
        
        print "Waiting for Type Request"
        recieved = self.connection.recv(1024)
        assert (recieved == "__TYPE__"), "Invalid Protocol: " + recieved
        self.connection.send(self.type)
        print "Type sent"
        
        print "Waiting for Arena"
        arena = self.recieve_arena()
        print arena
        
        print "Waiting for position request"
        recieved = self.connection.recv(1024)
        assert (recieved == "__POSITION__"), "Invalid Protocol: " + recieved
        pos = input("Enter initial location (Eg. \"(2, 3)\"): ")
        self.connection.send(pos)
        print "Position sent"

        
    def start_listening(self):
        """
            __init__(Client) -> None
            Listens to the server for arena update
        """
        print "Listening"
        while True:
            print self.recieve_arena()
        
        
    def recieve_arena(self):
        """
            recieve_arena(Client) -> str
            Recieves and returns a string representation of the arena
        """
        recieved = self.connection.recv(1024)
        assert recieved.startswith("__ARENA__"), "Invalid Protocol: " + recieved
        length = int(filter(None, re.split("__ARENA__", recieved))[0])
        self.connection.send("__READY__")
        return self.connection.recv(length)
        
    
    def start_game(self):
        """
            start_game(Client) -> None
            Starts the game for the client
        """
        while True:
            dir = input("Enter Move (Eg: \"none\"): ")
            self.move(dir)
            
    
    
    def move(self, dir):
        """
            move(Client, str) -> None
            Moves the player in the specified direction if possible
            dir must be on of "left", "right", "up", "down"
        """
        self.connection.send(dir)
        
        
        
if __name__ == "__main__":
    client = Client("shubham-desktop", 8694, "police")