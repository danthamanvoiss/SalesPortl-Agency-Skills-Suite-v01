import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_catalog.py"

spec = importlib.util.spec_from_file_location("validate_catalog", MODULE_PATH)
validate_catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_catalog)


class ValidateCatalogTests(unittest.TestCase):
    def test_invalid_frontmatter_returns_empty(self):
        text = "name: bad-frontmatter\n## Purpose\n..."
        self.assertEqual(validate_catalog.parse_frontmatter(text), {})

    def test_missing_required_headings_detected(self):
        text = """---
name: sample
description: test
version: 0.1.0
tags: [a, b]
---

## Purpose
ok

```
## Use when
inside code block only
```
"""
        headings = validate_catalog.extract_h2_headings(text)
        self.assertIn("## Purpose", headings)
        self.assertNotIn("## Use when", headings)

    def test_catalog_path_is_valid_json(self):
        self.assertTrue(validate_catalog.CATALOG_PATH.exists())
        data = json.loads(validate_catalog.CATALOG_PATH.read_text(encoding="utf-8"))
        self.assertIn("skills", data)
        self.assertEqual(data.get("total_skills"), len(data.get("skills", [])))


if __name__ == "__main__":
    unittest.main()
