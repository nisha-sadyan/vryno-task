
from fastapi import FastAPI,Path
from enum import Enum
from pydantic import BaseModel

app= FastAPI()

# @app.get("/hello/{name}")
# async def hello(name):
#     return f"welcome to my 1st app created using fastapi {name}"

#class to validate the products
class availableproducts(str,Enum): 
    laptop='laptop'
    TV='TV' 
    phone= 'phone'

product_item={
    availableproducts.laptop :['hp','lenova','dell'],
    'phone':['samsung','MI','mototrola'],
    'TV':['samsung','LG','videocon']
}
valid_product= product_item.keys()


@app.get("/get_item/{product}")
async def get_item(product:availableproducts):
    return product_item.get(product)

students={
    1:
    {"Fname":"Nisha",
    "Lname":"Sadyan",
    "Phone":45678945678

    }
}
@app.get("/get-student/{student_id}")
async def get_student(student_id:int= Path(None, description="The id you want to view")):
    # other attrbutes available are gt= greater than, lt= less than, ge=greater than equal, le= less than equal
    return students[student_id]

# query parameters
@app.get("/get-by-name")
def get_student(name:str):# if we make str= none,then it willnot be 
    # compulsory to enter the name or optional[str]=none but for this need to import optional
    for student_id in students:
        if students[student_id]["Fname"] == name:
            return students[student_id]
    return {"Data":"NOt Found"}

# Request body and post method
class student(BaseModel):
    Fname:str 
    Lname:str
    phone:int

@app.post("/create-student/{student_id}")
async def create_student(student_id:int, s1:student):
    if student_id in students:
        return {"error":"student exist"}
    students[student_id]= s1
    return students[student_id]
