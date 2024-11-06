# app/routes/__init__.py

# Import blueprints to make them available when the routes package is imported
from .health_check import health_bp
from .upload_file import upload_bp

# Optional: List all blueprints for easier import management
__all__ = ['health_bp', 'upload_bp']
