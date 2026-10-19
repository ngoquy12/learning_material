"""
tests/test_polyglot_sandbox.py
Unit and integration tests for the Polyglot Sandbox Runner:
- Python execution and runtime error capture.
- SQL In-Memory SQLite execution (DDL, DML, SELECT queries, syntax errors).
- JavaScript execution and bracket syntax validation.
- Polyglot language detection and normalization.
- Backward compatibility of execute_code_safely.
"""

import unittest
from core.sandbox.polyglot_runner import (
    detect_language,
    normalize_language,
    execute_polyglot_code,
    SqlRunner,
    PythonRunner,
    NodeJSRunner
)
from core.sandbox import execute_code_safely


class TestPolyglotSandbox(unittest.TestCase):

    def test_language_normalization(self):
        """Tests that common aliases resolve to canonical names."""
        self.assertEqual(normalize_language("py"), "python")
        self.assertEqual(normalize_language("PYTHON3"), "python")
        self.assertEqual(normalize_language("js"), "javascript")
        self.assertEqual(normalize_language("nodejs"), "javascript")
        self.assertEqual(normalize_language("ts"), "typescript")
        self.assertEqual(normalize_language("sqlite"), "sql")
        self.assertEqual(normalize_language("postgres"), "sql")
        self.assertEqual(normalize_language("golang"), "go")
        self.assertEqual(normalize_language("c++"), "cpp")
        self.assertEqual(normalize_language("sh"), "bash")

    def test_language_detection_heuristics(self):
        """Tests automatic language inference from code heuristics."""
        sql_code = "CREATE TABLE users (id INT, name TEXT);"
        self.assertEqual(detect_language(sql_code), "sql")

        java_code = "public class StudentService { public static void main(String[] args) {} }"
        self.assertEqual(detect_language(java_code), "java")

        go_code = "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello\") }"
        self.assertEqual(detect_language(go_code), "go")

        js_code = "const sum = (a, b) => { console.log(a + b); return a + b; };"
        self.assertEqual(detect_language(js_code), "javascript")

        py_code = "def calculate_discount(price, rate):\n    return price * (1 - rate)"
        self.assertEqual(detect_language(py_code), "python")

    def test_sql_in_memory_execution_success(self):
        """Tests executing DDL, INSERT, and SELECT queries in SQLite in-memory."""
        sql_script = """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL
        );
        INSERT INTO products (id, name, price) VALUES (1, 'Bánh Mì', 25000);
        INSERT INTO products (id, name, price) VALUES (2, 'Cà Phê Sữa', 30000);
        SELECT name, price FROM products WHERE price > 20000 ORDER BY price DESC;
        """
        runner = SqlRunner()
        result = runner.run(sql_script, timeout_sec=2.0)
        self.assertTrue(result.success)
        self.assertIn("Cà Phê Sữa", result.stdout)
        self.assertIn("Bánh Mì", result.stdout)
        self.assertIn("name | price", result.stdout)
        self.assertEqual(result.engine, "sqlite_in_memory")

    def test_sql_in_memory_syntax_error(self):
        """Tests that invalid SQL syntax is cleanly caught and reported."""
        bad_sql = "SELCT * FROM non_existent_table WHERE;"
        runner = SqlRunner()
        result = runner.run(bad_sql, timeout_sec=2.0)
        self.assertFalse(result.success)
        self.assertIn("OperationalError", result.error_type)
        self.assertIn("Lỗi SQL", result.error_message)

    def test_python_runner_execution(self):
        """Tests standard Python runner execution and output capture."""
        py_code = "items = [10, 20, 30]\nprint(f'Total: {sum(items)}')"
        runner = PythonRunner()
        result = runner.run(py_code, timeout_sec=2.0)
        self.assertTrue(result.success)
        self.assertEqual(result.stdout, "Total: 60")

    def test_polyglot_dispatcher(self):
        """Tests the unified execute_polyglot_code dispatcher with SQL and Python."""
        res_sql = execute_polyglot_code(
            "CREATE TABLE t (x INT); INSERT INTO t VALUES (42); SELECT * FROM t;",
            language="sql"
        )
        self.assertTrue(res_sql.success)
        self.assertIn("42", res_sql.stdout)

        res_py = execute_polyglot_code(
            "print('Hello from Polyglot Runner')",
            language="python"
        )
        self.assertTrue(res_py.success)
        self.assertIn("Hello from Polyglot Runner", res_py.stdout)

    def test_execute_code_safely_backward_compatibility(self):
        """Tests execute_code_safely without language defaults to Python."""
        res = execute_code_safely("a = 5\nb = 7\nprint(a * b)")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("35", res["output"])

    def test_execute_code_safely_with_sql(self):
        """Tests execute_code_safely with language='sql'."""
        res = execute_code_safely(
            "CREATE TABLE orders (id INT, total REAL); INSERT INTO orders VALUES (101, 150000); SELECT * FROM orders;",
            language="sql"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("150000", res["output"])

    def test_execute_code_safely_with_html_and_css(self):
        """Tests execute_code_safely with HTML and CSS."""
        html_code = "<div class='container'><p>Hello Web</p></div>"
        res_html = execute_code_safely(html_code, language="html")
        self.assertEqual(res_html["status"], "SUCCESS")
        self.assertIn("HTML markup verified successfully", res_html["output"])

        css_code = ".container { display: flex; justify-content: center; }"
        res_css = execute_code_safely(css_code, language="css")
        self.assertEqual(res_css["status"], "SUCCESS")
        self.assertIn("CSS stylesheet syntax verified successfully", res_css["output"])


class TestSandboxSafety(unittest.TestCase):
    def test_bash_khong_bao_gio_thuc_thi(self):
        import os
        import tempfile

        from core.sandbox.polyglot_runner import execute_polyglot_code

        marker = os.path.join(tempfile.gettempdir(), "polyglot_bash_must_not_run.txt")
        if os.path.exists(marker):
            os.remove(marker)
        res = execute_polyglot_code(f'touch "{marker}"', language="bash")
        self.assertFalse(os.path.exists(marker), "lệnh bash đã bị thực thi trên máy chủ")
        self.assertTrue(res.success)
        self.assertIn("NOT executed", res.stdout)

    def test_bash_loi_cu_phap_bi_bat(self):
        from core.sandbox.polyglot_runner import execute_polyglot_code

        res = execute_polyglot_code("if then fi fi (", language="bash")
        if res.engine == "bash_unavailable":
            self.skipTest("không có bash")
        self.assertFalse(res.success)

    def test_tien_trinh_con_khong_chay_trong_thu_muc_du_an(self):
        import os

        from core.sandbox.polyglot_runner import execute_polyglot_code

        res = execute_polyglot_code("import os; print(os.getcwd())", language="python")
        self.assertTrue(res.success)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.assertNotEqual(os.path.normcase(res.stdout.strip()), os.path.normcase(project_root))


if __name__ == "__main__":
    unittest.main()
