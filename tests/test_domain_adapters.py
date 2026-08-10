# tests/test_domain_adapters.py
import unittest
import os
from pathlib import Path
from core.domain_adapters import (
    get_domain_rules,
    get_enterprise_domain_prompt,
    resolve_slm_endpoint,
    DOMAIN_RULES,
    ENTERPRISE_SCENARIOS
)
from scripts.build_slm_fine_tune_dataset import (
    generate_fine_tune_pairs,
    build_dataset_file
)

class TestDomainAdaptersEngine(unittest.TestCase):

    def test_get_domain_rules(self):
        """Verify domain rule extraction per tech stack."""
        rules_python = get_domain_rules("python/core")
        self.assertIn("PEP 8 Compliance", rules_python)

        rules_fastapi = get_domain_rules("fastapi/backend")
        self.assertIn("WEB FRAMEWORK & RESTFUL BACKEND", rules_fastapi)

        rules_react = get_domain_rules("react/frontend")
        self.assertIn("WEB FRONTEND", rules_react)

        rules_empty = get_domain_rules("")
        self.assertEqual(rules_empty, "")

    def test_get_enterprise_domain_prompt(self):
        """Verify enterprise domain scenario injection."""
        prompt_payment = get_enterprise_domain_prompt("python/core", "xử lý thanh toán webhook")
        self.assertIn("PAYMENT GATEWAY WEBHOOK INTEGRATION", prompt_payment)
        self.assertIn("PEP 8 Compliance", prompt_payment)

        prompt_auth = get_enterprise_domain_prompt("fastapi/backend", "bảo mật JWT Auth và phân quyền RBAC")
        self.assertIn("ENTERPRISE AUTH & RBAC GUARD", prompt_auth)

    def test_resolve_slm_endpoint(self):
        """Verify SLM endpoint resolver returns string or None gracefully."""
        endpoint = resolve_slm_endpoint()
        # Should either be a valid URL string (http://...) or None if no local server is listening
        if endpoint is not None:
            self.assertTrue(endpoint.startswith("http"))

    def test_dataset_generator(self):
        """Verify JSONL fine-tuning dataset generator produces valid items."""
        pairs = generate_fine_tune_pairs()
        self.assertGreater(len(pairs), 5)
        for item in pairs:
            self.assertIn("instruction", item)
            self.assertIn("input", item)
            self.assertIn("output", item)
            self.assertTrue(len(item["output"]) > 0)

        test_out = Path("storage") / "test_slm_dataset.jsonl"
        built_file = build_dataset_file(test_out)
        self.assertTrue(built_file.exists())
        # Clean up temporary test file
        if built_file.exists():
            os.remove(built_file)


if __name__ == "__main__":
    unittest.main()
