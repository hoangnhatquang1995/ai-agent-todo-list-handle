from langchain.tools import tool
from langgraph.func import task 
from vectorstore.type import Task
from vectorstore.chromadb import vectorstore_add_task, vectorstore_remove_task,vectorstore_get_list,vectorstore_find_task
from datetime import datetime

@tool 
def add_task(time : str, task_name : str, description : str = "") -> str :
    """Đây là tool để lưu lại các task. 
    - time: Thời gian của task (định dạng 'YYYY-MM-DD HH:MM:SS')
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
    - time: Thời gian của task (định dạng 'YYYY-MM-DD HH:MM:SS', có thể để trống)
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
    - time: Thời gian của task (định dạng 'YYYY-MM-DD HH:MM:SS')
    - description: Mô tả chi tiết của task (có thể để trống)
    - new_task_name: Tên ngắn gọn mới của task (có thể để trống)
    - new_time: Thời gian mới của task (định dạng 'YYYY-MM-DD HH:MM:SS', có thể để trống)
    - new_description: Mô tả chi tiết mới của task (có thể để trống)
    """
    ###TODO: Implement the logic to update the task in a database or a file. For now, we will just return a confirmation message.
    return f"[TODO] Task with time '{time}' has been updated to '{task_name}' with description: {description}"

@tool
def time_until_task(time : str = "", task_name : str = "", description : str = "") -> str :
    """Đây là tool để tính toán thời gian còn lại cho đến khi một task được đến hạn
    - task_name: Tên ngắn gọn của task (Có thể để trống)
    - time: Thời gian của task (định dạng 'YYYY-MM-DD HH:MM:SS', có thể để trống)
    - description: Mô tả chi tiết của task (có thể để trống)
    Lưu ý : Nhập bất kỳ thông tin user cung cấp vào tham số tương ứng. Nếu không tìm được time hoặc task_name tương ứng thì bỏ chống. Đừng hỏi lại.
    """
    search_task = Task(
        time = time,
        task_name= task_name,
        description= description
    )
    store_task = vectorstore_find_task(search_task)
    if store_task is None:
        return f"Không tìm thấy task nào phù hợp với thông tin đã cho."
    try:
        print(f"==> [Time Until Task] Calculate time until task with time: {time}, task_name: {task_name}, description: {description}")
        task_time = datetime.strptime(store_task.time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        if task_time < now:
            return f"Task '{task_name}' đã quá hạn."
            
        diff = task_time - now
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        result = []
        if days > 0: result.append(f"{days} ngày")
        if hours > 0: result.append(f"{hours} giờ")
        if minutes > 0: result.append(f"{minutes} phút")
        print(f"==> Time until task: {' '.join(result)}")
        return f"Thời gian còn lại cho task '{task_name}': " + " ".join(result)
    except ValueError:
        return f"Lỗi định dạng thời gian. Vui lòng đảm bảo time là 'YYYY-MM-DD HH:MM:SS'."

tool_tasks = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "delete_task": delete_task,
    "update_task": update_task,
    "time_until_task": time_until_task
}