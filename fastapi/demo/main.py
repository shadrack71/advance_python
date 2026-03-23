from fastapi import FastAPI , Path ,Query
from typing import Optional
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
# to run the app fastapi dev main.py  
# source d:/SOFTWARE_DEVELOPMENT_PROJ/advanced_learning_python/.venv/Scripts/activate
students =  {
    1:{
    "name": "John Doe",
    "age": 20,
    "grade": "A",
    "courses": ["Math", "Science", "History"]
    }
}

class studentModel(BaseModel):
    name: str 
    age: int 
    grade: str
    courses: list[str] 
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None 
    age: Optional[int] = None  
    grade: Optional[str] = None 
    courses: Optional[list[str]] = None   

@app.get("/student/{student_id}/}")
def read_root(student_id:int ):
    return students.get(student_id, {"message": "Student not found"})


@app.get("/student/{student_id}")
def read_all_students(student_id:int,name:str):
    for student_id in students:
        if students[student_id]["name"].lower() == name.lower():
            return students[student_id]

@app.post("/post-student/{student_id}")
def post_student(student_id: int, student: studentModel):
    if student_id in student:
        return {"message": "Student ID already exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/put-student/{student_id}")
def put_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"message": "Student ID does not exist"}
    students[student_id] = student
    return students[student_id]
    
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"message": "Student ID does not exist"}
    del students[student_id]
    return {"message": "Student deleted successfully"}


#Query Parameters and String Validations

@app.get("/items/")
def read_items(q: Annotated[list[str] | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results