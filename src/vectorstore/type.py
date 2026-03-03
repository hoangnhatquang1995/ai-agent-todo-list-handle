from pydantic import BaseModel, Field 
from typing import Any, Optional

class Task(BaseModel):
    time: str = Field(description = "thời gian của task (định dạng 'YYYY-MM-DD HH:MM:SS')")
    task_name: str = Field(description = "Tên ngắn gọn của task")
    description: Optional[str] = Field(description = "Mô tả chi tiết của task", default="")

    def __str__(self) :
        return f" Time : {self.time} - Task Name: {self.task_name} - Description: {self.description}"
    