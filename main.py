import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from reportgen.cli import app

if __name__ == "__main__":
    app()
