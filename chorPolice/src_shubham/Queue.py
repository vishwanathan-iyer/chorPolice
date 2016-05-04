class Queue:
    """
        Queue Data Structure
    """
    def __init__(self):
        """
            __init__(Queue) -> None
            Initializes the queue
        """
        self.data = []
        self.num_items = 0
        
    def enqueue(self, item):
        """
            enqueue(Queue, item) -> None
            Adds the item to the end of the queue
        """
        self.num_items += 1
        self.data.append(item)
    
    def dequeue(self):
        """
            dequeue(Queue) -> item
            Returns the item at the front of the queue.
            Throws an error if queue is empty
        """
        assert (self.num_items > 0), "Empty Queue"
        self.num_items -= 1
        return self.data.pop(0) # Pop the first item
    
    def isempty(self):
        """
            isempty(Queue) -> bool
            Returns True if the queue is empty and False otherwise
        """
        return (self.num_items == 0)
    
    def get_count(self):
        """
            get_count(Queue) -> int
            Returns the number of elements in the list
        """
        return self.num_items