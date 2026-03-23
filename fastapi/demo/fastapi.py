from fastapi import FastAPI , Path
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()
    
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