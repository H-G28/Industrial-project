#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parent
    project_dir = base_dir / "DIAMONDAURAWEB()" / "DIAMONDAURAWEB()" / "DIAMONDAURAWEB"

    if not project_dir.exists():
        raise FileNotFoundError(f"Django project folder not found: {project_dir}")

    os.chdir(project_dir)
    sys.path.insert(0, str(project_dir))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
