from pathlib import Path

file_init = "Manage_Recruiting_Email_Templates"

# Base directory (current project directory)
base_dir = Path.cwd()

# Files to create
files = {
    "Config": [
        f"{file_init}_Run_All.py",
    ],
    "Models": [
        f"{file_init}_Models.py",
    ],
    "Controller": [
        f"{file_init}_Models.py",
    ],
    "TestCases": [
        f"{file_init}_Automate.py",
        f"{file_init}_Reverse.py",
        f"{file_init}_Validate.py",
    ],
}


def create_python_file(file_path: Path):
    """Create a Python file with a class matching the filename."""
    class_name = file_path.stem

    content = f'''class {class_name}:
    pass
'''

    file_path.write_text(content, encoding="utf-8")
    print(f"Created: {file_path}")


for folder, filenames in files.items():
    folder_path = base_dir / folder

    for filename in filenames:
        file_path = folder_path / filename
        create_python_file(file_path)

print("All files created successfully.")