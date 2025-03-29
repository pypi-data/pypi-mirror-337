# solutionmaker/cli.py
import os
import shutil
import sys
from pathlib import Path

def create_project(project_name):
    # Путь к шаблону
    template_dir = Path(__file__).parent / "templates"
    # Путь к новому проекту
    project_dir = Path.cwd() / project_name

    if project_dir.exists():
        print(f"Error: Directory '{project_name}' already exists.")
        sys.exit(1)

    # Копируем шаблон в новую директорию
    shutil.copytree(template_dir, project_dir)
    print(f"Project '{project_name}' created successfully at {project_dir}")

def main():
    if len(sys.argv) != 2:
        print("Usage: solutionmaker <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    create_project(project_name)

if __name__ == "__main__":
    main()