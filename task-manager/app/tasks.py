from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# CREATE TASK
@router.post("/", response_model=TaskResponse)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):

    new_task = Task(
        title=data.title,
        description=data.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# GET ALL TASKS
@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):

    return db.query(Task).all()





# GET SINGLE TASK
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# UPDATE TASK
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskCreate, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = data.title
    task.description = data.description

    db.commit()
    db.refresh(task)

    return task


# DELETE TASK
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}


@router.get("/{task_id}/complete", response_model=TaskResponse)'
def complete_task(task_id: int, db: Session = Depends(get_db)):
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True

    db.commit()
    db.refresh(task)

    return task