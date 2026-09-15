"""Export the Flask page and browser assets for GitHub Pages."""
from pathlib import Path
from shutil import copytree
from app import create_app

ROOT = Path(__file__).resolve().parent


def export(destination=None):
    destination = Path(destination) if destination else ROOT / '_site'
    destination.mkdir(parents=True, exist_ok=True)
    with create_app().test_client() as client:
        response = client.get('/')
        if response.status_code != 200:
            raise RuntimeError('Flask page failed to render')
        (destination / 'index.html').write_bytes(response.data)
    copytree(ROOT / 'static', destination / 'static', dirs_exist_ok=True)
    (destination / '.nojekyll').touch()
    return destination


if __name__ == '__main__':
    print(export())
