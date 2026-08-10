import unittest
from agents.creators.reading_creator import guard_mermaid_syntax

class TestMermaidGuard(unittest.TestCase):
    def test_markdown_mermaid_guard(self):
        input_text = """```mermaid
graph TD
    A[/Đầu vào: Repository Git ban đầu/] --> B[Tạo nhánh feature/catalog-service]
    C --> D{Thực hiện docker build thành công?}
    D -- Gặp lỗi build -- > C
    D -- Thành công --> E[Khởi chạy Container local]
```"""
        result = guard_mermaid_syntax(input_text)
        self.assertIn('D -->|Gặp lỗi build| C', result)
        self.assertIn('B["Tạo nhánh feature/catalog-service"]', result)
        self.assertIn('D{"Thực hiện docker build thành công?"}', result)

if __name__ == "__main__":
    unittest.main()
