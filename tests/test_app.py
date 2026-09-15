import tempfile
import unittest
from pathlib import Path
from app import create_app
from export_static import export


class AppTests(unittest.TestCase):
    def test_page_and_assets(self):
        with create_app().test_client() as client:
            self.assertEqual(client.get('/').status_code, 200)
            for asset in ('app.js', 'math.mjs', 'styles.css'):
                with client.get('/static/' + asset) as response:
                    self.assertEqual(response.status_code, 200)

    def test_portable_export(self):
        with tempfile.TemporaryDirectory() as temp:
            site = export(Path(temp) / 'CS_Math')
            html = (site / 'index.html').read_text()
            self.assertIn('./static/styles.css', html)
            self.assertIn('./static/app.js', html)
            self.assertTrue((site / 'static/math.mjs').is_file())
            self.assertNotIn('{{', html)
