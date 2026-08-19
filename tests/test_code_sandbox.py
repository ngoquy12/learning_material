"""
tests/test_code_sandbox.py
Verifies the isolated Code Sandbox Executor:
- Clean python code runs and returns stdout.
- Runtime errors (ZeroDivisionError, NameError) are captured with error_type.
- Infinite loops or slow execution trigger TimeoutExpired.
- Non-python static syntax validation.
"""

import unittest
from core.sandbox.code_executor import CodeSandboxExecutor, execute_code_snippet

class TestCodeSandboxExecutor(unittest.TestCase):

    def setUp(self):
        self.sandbox = CodeSandboxExecutor(default_timeout_sec=2.0)

    def test_successful_python_execution(self):
        """Tests that valid python code executes and captures output."""
        code = "a = 10\nb = 20\nprint(f'Sum: {a + b}')"
        result = self.sandbox.execute_python_code(code)
        self.assertTrue(result.success)
        self.assertEqual(result.stdout, "Sum: 30")
        self.assertIsNone(result.error_type)
        self.assertGreaterEqual(result.execution_time_ms, 0.0)

    def test_runtime_error_capture(self):
        """Tests that ZeroDivisionError is cleanly caught and reported."""
        code = "x = 10 / 0"
        result = self.sandbox.execute_python_code(code)
        self.assertFalse(result.success)
        self.assertEqual(result.error_type, "ZeroDivisionError")
        self.assertIn("division by zero", result.error_message)

    def test_name_error_capture(self):
        """Tests that NameError is caught."""
        code = "print(undefined_variable)"
        result = self.sandbox.execute_python_code(code)
        self.assertFalse(result.success)
        self.assertEqual(result.error_type, "NameError")

    def test_timeout_expired_on_infinite_loop(self):
        """Tests that infinite loops are killed within timeout_sec."""
        code = "while True:\n    pass"
        result = self.sandbox.execute_python_code(code, timeout_sec=0.5)
        self.assertFalse(result.success)
        self.assertTrue(result.timeout_exceeded)
        self.assertEqual(result.error_type, "TimeoutExpired")

    def test_convenience_function_for_polyglot_check(self):
        """Tests the convenience functional interface with balanced and unbalanced brackets."""
        valid_js = "function test() { console.log('hello'); }"
        res1 = execute_code_snippet(valid_js, tech_stack="javascript")
        self.assertTrue(res1.success)

        invalid_js = "function test() { console.log('hello'); "
        res2 = execute_code_snippet(invalid_js, tech_stack="javascript")
        self.assertFalse(res2.success)
        self.assertEqual(res2.error_type, "SyntaxWarning")

if __name__ == "__main__":
    unittest.main()
