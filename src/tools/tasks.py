from langchain.tools import tool
from langgraph.func import task 

@tool 
def add_task(time : str, task_name : str, description : str = "") -> str :
    """Đây là tool để lưu lại các task. 
    - time: Thời gian của task (VD: '10h sáng mai')
    - task_name: Tên ngắn gọn của task (tự tạo nếu không có)
    - description: Mô tả chi tiết (có thể để trống)"""
    ##TODO: Implement the logic to add the task to a database or a file. For now, we will just return a confirmation message.
    return "taskid_123"

@tool
def list_tasks() -> str :
    """Đây la tool để liệt kê các task đã được lưu lại trong ChromaDB"""
    ###TODO: Implement the logic to retrieve the tasks from a database or a file. For now, we will just return a placeholder message.
    return "Here are your tasks: \n1. Task 1 at 10:00 - Description of task 1\n2. Task 2 at 14:00 - Description of task 2"

@tool 
def delete_task(task_id : int) -> str :
    """Đây là tool để xóa một task khỏi ChromaDB"""
    ###TODO: Implement the logic to delete the task from a database or a file. For now, we will just return a confirmation message.
    return f"Task with ID {task_id} has been deleted."

@tool
def update_task(task_id : int, time : str, task_name : str, description : str = "") -> str :
    """Đây là tool để cập nhật một task"""
    ###TODO: Implement the logic to update the task in a database or a file. For now, we will just return a confirmation message.
    return f"Task with ID {task_id} has been updated to '{task_name}' scheduled for {time} with description: {description}"

@tool
def time_until_task(task_id : int) -> str :
    """Đây là tool để tính toán thời gian còn lại cho đến khi một task được đến hạn"""
    ###TODO: Implement the logic to calculate the time remaining until the task is due. For now, we will just return a placeholder message.
    return f"Time remaining until task with ID {task_id} is due: 2 hours and 30 minutes."

tool_tasks = [add_task, list_tasks, delete_task, update_task, time_until_task]