import sys
from pathlib import Path

# Add the project root directory to the system path
sys.path.append(str(Path(__file__).resolve().parent))

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
