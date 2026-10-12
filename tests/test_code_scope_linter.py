import unittest

from core.validators.code_scope_linter import (
    find_js_scope_violations,
    find_py_scope_violations,
    find_signature_drift,
    mask_lines,
    provided_code_lines,
)

CLOSURE_JS = """
function createShopClient({ token = null } = {}) {
  const state = { token };
  const http = axios.create({ baseURL: "x" });
  const setToken = (t) => { state.token = t; };
  const getProduct = async (id) => http.get("/products/" + id);
  return { setToken, getProduct };
}
"""

MODULE_STATE_JS = """
const shopSession = { token: null };
function createShopHttp(timeoutMs = 5000) {
  const http = axios.create({ baseURL: "x", timeout: timeoutMs });
  http.interceptors.request.use((config) => {
    if (shopSession.token) config.headers.Authorization = "Bearer " + shopSession.token;
    return config;
  });
  return http;
}
async function getProduct(id) {
  const http = createShopHttp();
  return http.get("/products/" + id);
}
"""


class TestJsScope(unittest.TestCase):
    def test_closure_tra_ve_ham_dung_lai_bien_cuc_bo_bi_bat(self):
        found = find_js_scope_violations(CLOSURE_JS, ["closure"])
        self.assertTrue(found)
        self.assertEqual({f.construct for f in found}, {"closure"})

    def test_trang_thai_o_pham_vi_module_khong_bi_bat(self):
        self.assertEqual(find_js_scope_violations(MODULE_STATE_JS, ["closure", "class", "this"]), [])

    def test_class_this_module(self):
        code = "class A {}\nconst o = { f() { return this.x; } };\nimport x from 'y';\nexport const z = 1;\n"
        kinds = {f.construct for f in find_js_scope_violations(code, ["class", "this", "module"])}
        self.assertEqual(kinds, {"class", "this", "module"})

    def test_chu_thich_va_chuoi_khong_gay_bao_dong_gia(self):
        code = '// this la class closure\nconst s = "this class import x";\nconst t = `this ${1}`;\n'
        self.assertEqual(find_js_scope_violations(code, ["class", "this", "module", "closure"]), [])

    def test_chi_bao_cau_truc_bi_cam(self):
        self.assertEqual(find_js_scope_violations("class A {}", ["this"]), [])

    def test_khong_bao_trung_dong(self):
        code = "const o = { f() { return this.a + this.b; } };"
        self.assertEqual(len(find_js_scope_violations(code, ["this"])), 1)


class TestPyScope(unittest.TestCase):
    def test_lambda_class_decorator(self):
        code = "class A:\n    pass\n@dec\ndef f():\n    return list(map(lambda x: x, [1]))\n"
        kinds = {f.construct for f in find_py_scope_violations(code, ["class", "lambda", "decorator"])}
        self.assertEqual(kinds, {"class", "lambda", "decorator"})

    def test_comprehension(self):
        self.assertTrue(find_py_scope_violations("a = [x for x in range(3)]", ["comprehension"]))
        self.assertFalse(find_py_scope_violations("for x in range(3):\n    print(x)", ["comprehension"]))


class TestProvidedCode(unittest.TestCase):
    def test_ma_nen_bi_che(self):
        code = "// ===== Mã nền (không sửa) =====\nfunction a() { return this.x; }\n// ===== HẾT MÃ NỀN =====\nfunction b() { return 1; }\n"
        masked = mask_lines(code, provided_code_lines(code))
        self.assertEqual(find_js_scope_violations(masked, ["this"]), [])
        self.assertEqual(len(find_js_scope_violations(code, ["this"])), 1)


class TestSignatureDrift(unittest.TestCase):
    def test_lech_hinh_dang_tham_so(self):
        files = {"b3.js": "function loadDashboard(id) {}", "b5.js": "function loadDashboard({a = 1} = {}) {}"}
        self.assertEqual([d.name for d in find_signature_drift(files)], ["loadDashboard"])

    def test_chi_khac_ten_tham_so_thi_bo_qua(self):
        files = {"b3.js": "function loadDashboard(id) {}", "b4.js": "function loadDashboard(studentId) {}"}
        self.assertEqual(find_signature_drift(files), [])

    def test_cung_chu_ky_khong_bao(self):
        files = {"a.js": "const f = (x, y) => { return x; };", "b.js": "function f(x, y) { return y; }"}
        self.assertEqual(find_signature_drift(files), [])


if __name__ == "__main__":
    unittest.main()
