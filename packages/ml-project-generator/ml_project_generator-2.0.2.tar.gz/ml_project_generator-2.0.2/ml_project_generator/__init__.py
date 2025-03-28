"""
ML Project Generator - A tool to generate structured ML project templates
"""

__version__ = "2.0.2"

from .project_creator import (
    ProjectTemplate,
    create_ml_project_structure,
    create_virtual_environment,
    get_template_dependencies,
    get_template_files
)
from .utils import get_docstring_template, get_example_code, get_config_template, get_test_template

__all__ = [
    "ProjectTemplate",
    "create_ml_project_structure",
    "create_virtual_environment",
    "get_template_dependencies",
    "get_template_files",
    "get_docstring_template",
    "get_example_code",
    "get_config_template",
    "get_test_template",
]
