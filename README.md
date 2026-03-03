# ai-agent-todo-list-handle

Dự án này là một hệ thống quản lý công việc (Todo List) thông minh được hỗ trợ bởi AI Agent. Thay vì sử dụng các thao tác CRUD truyền thống, bạn có thể tương tác với danh sách công việc của mình thông qua ngôn ngữ tự nhiên. 

Hệ thống sử dụng **FastAPI** làm backend, **LangGraph/LangChain** để xây dựng logic cho AI Agent, và **ChromaDB** làm cơ sở dữ liệu vector (Vector Database) để lưu trữ và tìm kiếm task theo ngữ nghĩa (semantic search).

## 🚀 Tính năng nổi bật

- **Quản lý Task bằng ngôn ngữ tự nhiên**: Thêm, xóa, cập nhật và tra cứu công việc chỉ bằng cách chat với AI.
- **Tính toán thời gian đến hạn**: AI có thể tự động hiểu và tính toán thời gian còn lại cho đến khi một công việc tới hạn so với thời gian thực tế.
- **Tìm kiếm theo ngữ nghĩa**: Nhờ sử dụng Vector Database (ChromaDB) và mô hình nhúng (Embeddings) của HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`), bạn không cần nhớ chính xác tên task để xóa hay tìm kiếm. Hệ thống có thể tự động tìm ra task phù hợp nhất dựa trên mô tả của bạn.
- **FastAPI Backend**: Cung cấp các API RESTful nhanh chóng và tiện lợi để giao tiếp với hệ thống frontend hoặc ứng dụng khác.

## 🛠️ Cấu trúc thư mục (Workspace)

```text
ai-agent-todo-list-handle/
├── cache/                  # Lưu trữ dữ liệu của ChromaDB và cache các model HuggingFace cục bộ
├── src/                    # Chứa mã nguồn chính
│   ├── agent/              # Logic của AI Agent (LangGraph, Prompts, LLM tools, Assistants)
│   ├── api/                # Các endpoint FastAPI (app.py)
│   ├── settings/           # Cấu hình dự án
│   ├── tools/              # Chứa các tool (function calling) cho Agent: add_task, list_tasks, vv.
│   ├── vectorstore/        # Logic kết nối và thao tác với ChromaDB
│   └── main.py             # Entrypoint khởi chạy server Uvicorn
├── requirements.txt        # Các thư viện phụ thuộc của dự án
└── README.md
```

## ⚙️ Cài đặt và Khởi chạy

### 1. Cài đặt môi trường
Bạn cần cài đặt Python (khuyến nghị 3.10+) và tạo một môi trường ảo (Virtual Environment).

```bash
# Tạo môi trường ảo (tuỳ chọn)
python -m venv .venv

# Kích hoạt môi trường ảo (ví dụ trên Windows)
.venv\Scripts\activate

# Cài đặt các thư viện yêu cầu
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường
Tạo file `.env` ở thư mục gốc và khai báo các khóa API cần thiết cho dự án. Tuỳ thuộc vào cấu hình model LLM trong `src/agent/llm.py` mà bạn sẽ cần các key như:
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- Hoặc các keys khác tương ứng.

### 3. Khởi chạy Server
Từ thư mục gốc, khởi chạy file `main.py` chạy qua môi trường Python:

```bash
python src/main.py
```
*Lưu ý: Server sẽ mặc định chạy trên địa chỉ `http://0.0.0.0:8000` thông qua Uvicorn.*

## 🔌 API Endpoints

Hệ thống hiện tại cung cấp các endpoint chính sau:

- **`GET /tasks`**: Lấy danh sách toàn bộ các task đang có trong ChromaDB vectorstore.
- **`POST /tasks`**: Thêm mới một task thủ công cung cấp `time`, `task_name` và `description`.
- **`POST /ask`**: 💬 Endpoint mạnh mẽ nhất để trò chuyện với AI Agent. Truyền một object JSON với key là `{"question": "Câu lệnh của bạn"}` và AI sẽ tự gọi tool phù hợp để xử lý tác vụ tương ứng.

## 🤖 Các công cụ Agent đang hỗ trợ (`src/tools/tasks.py`)
AI Agent được nạp các tool sau đây để gọi (Function Calling):
- `list_tasks`: Gọi ra tất cả các tasks đã lưu.
- `add_task`: Thêm task với thời gian cụ thể (định dạng `YYYY-MM-DD HH:MM:SS`), tên và mô tả.
- `update_task`: Cập nhật thông tin công việc dựa trên query.
- `delete_task`: Xoá bỏ một công việc thông qua tìm kiếm ngữ nghĩa.
- `time_until_task`: Báo cáo thời gian khả dụng (countdown) cho một sự kiện trong công việc.