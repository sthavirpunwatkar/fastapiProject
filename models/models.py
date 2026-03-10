# models are entities that are stored inside your database
from pydantic import BaseModel

class Product(BaseModel):
    id : int
    name : str
    description : str
    price : float
    quantity : int

    '''
    # after pydantic integrated, we dont need manual constructor here.
    
    def __init__(self, id, name, description, price, quantity):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
    '''