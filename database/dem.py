from fastapi import FastAPI

from models.models import Product

app = FastAPI()   # this is fastapi object after import



@app.get("/")
def greet():
    return "welcome to my app"


products = [

    #Product(1, "HP", "Budget Laptop", 40000, 1),   # object of Product entity
    #Product(2, "ACER", "Budget Laptop", 25000, 3)   # each object will refer to one product entity in your DB


    Product(id = 1, name = "Dell", description = "Dell Laptop", price = 50000, quantity = 50000),
    Product(id = 2, name = "acer", description= "acer laptop", price = 40000, quantity = 2),

]


@app.get("/products")    # this is for getting all the data
def get_all_products():
    return products

@app.get("/products/{id}")
def get_product_by_id(id:int):
    return products[id-1]



