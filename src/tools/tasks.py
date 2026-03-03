from langchain.tools import tool
from langgraph.func import task 
from vectorstore.type import Task
from vectorstore.chromadb import vectorstore_add_task, vectorstore_remove_task,vectorstore_get_list
@tool 
def add_task(time : str, task_name : str, description : str = "") -> str :
    """Đây là tool để lưu lại các task. 
    - time: Thời gian của task (Đúng định dạng time)
    - task_name: Tên ngắn gọn của task (tự tạo nếu không có)
    - description: Mô tả chi tiết (có thể để trống)"""
    task = Task(
        time = time,
        task_name= task_name,
        description= description
    )
    print(f"==> [Add Task] Add {str(task)}")
    result = vectorstore_add_task(task)
    return result

@tool
def list_tasks() -> str :
    """Đây la tool để liệt kê các task đã được lưu lại trong ChromaDB"""
    print(f"==> [List Task]")
    tasks = vectorstore_get_list()
    strs_task = [f"{i+1}. {str(task)}" for i, task in enumerate(tasks)]
    return "Danh sách:\n" + "\n".join(strs_task)

@tool 
def delete_task(task_name : str, time: str = "", description: str = "") -> str :
    """Đây là tool để xóa một task khỏi ChromaDB
    - task_name: Tên ngắn gọn của task
    - time: Thời gian của task (VD: '10h sáng mai', có thể để trống)
    - description: Mô tả chi tiết của task (có thể để trống)
    Nhập bất kỳ thông tin nào user cung cấp vào các tham số tương ứng. Nếu thiếu time hoặc description thì cứ để trống, tool sẽ tự động tìm kiếm ngữ nghĩa và xóa. ĐỪNG hỏi lại.
    """
    task = Task(
        time = time,
        task_name= task_name,
        description= description
    )
    print(f"==> [Delete Task] Delete {str(task)}")
    result = vectorstore_remove_task(task)
    return result

@tool
def update_task(time : str, task_name : str, description : str = "",
                 new_time: str = "", new_task_name: str = "", new_description: str = "") -> str :
    """Đây là tool để cập nhật một task
    - task_name: Tên ngắn gọn của task
    - time: Thời gian của task (VD: '10h sáng mai')
    - description: Mô tả chi tiết của task (có thể để trống)
    - new_task_name: Tên ngắn gọn mới của task (có thể để trống)
    - new_time: Thời gian mới của task (VD: '10h sáng mai', có thể để trống)
    - new_description: Mô tả chi tiết mới của task (có thể để trống)
    """
    ###TODO: Implement the logic to update the task in a database or a file. For now, we will just return a confirmation message.
    return f"[TODO] Task with time '{time}' has been updated to '{task_name}' with description: {description}"

@tool
def time_until_task(time : str, task_name : str, description : str = "") -> str :
    """Đây là tool để tính toán thời gian còn lại cho đến khi một task được đến hạn
    - task_name: Tên ngắn gọn của task
    - time: Thời gian của task (VD: '10h sáng mai')
    - description: Mô tả chi tiết của task (có thể để trống)
    """
    ###TODO: Implement the logic to calculate the time remaining until the task is due. For now, we will just return a placeholder message.
    return f"Time remaining until task with time '{time}' and description '{description}' is due: 2 hours and 30 minutes."

tool_tasks = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "delete_task": delete_task,
    "update_task": update_task,
    "time_until_task": time_until_task
}