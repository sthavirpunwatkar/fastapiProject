from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from models.models import Product
from database import database_models
from database.db import session, engine
from sqlalchemy.orm import Session
app = FastAPI()# this is fastapi object after import

# for cors permission
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,

    
)
database_models.Base.metadata.create_all(engine)


@app.get("/")
def greet():
    return "welcome to my app"


products = [

    #Product(1, "HP", "Budget Laptop", 40000, 1),   # object of Product entity
    #Product(2, "ACER", "Budget Laptop", 25000, 3)   # each object will refer to one product entity in your DB


    Product(id = 1, name = "Dell", description = "Dell Laptop", price = 50000, quantity = 50000),
    Product(id = 2, name = "acer", description= "acer laptop", price = 40000, quantity = 2),


]

def init_db():
    db = session()
    count =  db.query(database_models.Product).count()  #this query is used to check the count of data present
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))  #Here we are taking the product object and serializing it to dictionary by modeldump and later unpacking it to db
    db.commit() # commit for the transaction

init_db()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")    # this is for getting all the data
def get_all_products(db: Session = Depends(get_db)):   #injected get_db session creator to this function

    db_products = db.query(database_models.Product).all()   ## .all( is an orm method to get all data
    return db_products

    # return products


@app.get("/products/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    # for p in products:
    #     if p.id == id:
    #         return p
    # return  "product not found"
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product

    return "product not found"


@app.post("/products")
def add_product(product:Product,db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

    '''
    products.append(product)
    return product
    '''

@app.put("/products/{id}")
def update_product(id:int, product:Product,db: Session = Depends(get_db)):   #updating the content by id, but we are sending id also to update, but id must not be changed
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description  = product.description
        db_product.price    = product.price
        db_product.quantity = product.quantity
        db.commit()
        return  "product updated"
    else:
        return "product not found"



    '''
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "product updated successfully"

    return "product not found"
    '''
@app.delete("/products/{id}")
def delete_product(id:int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return  "Product Deleted"
    else:
        "Product not Found"



    '''
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted successfully"

    return "product not found"
    '''


