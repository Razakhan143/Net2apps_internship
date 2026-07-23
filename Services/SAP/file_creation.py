from pathlib import Path

file_init = "Manage_Recruiting_Email_Templates"

files_to_create = {
    "Config": [
        f"{file_init}_Run_All.py",
    ],
    "Models": [
        f"{file_init}_Models.py",
    ],
    "Controller": [
        f"{file_init}_Controllers.py",
    ],
    "TestCases": [
        f"{file_init}_Automate.py",
        f"{file_init}_Reverse.py",
        f"{file_init}_Validate.py",
    ],
}

for folder, files in files_to_create.items():
    folder_path = Path(folder)

    for file_name in files:
        file_path = folder_path / file_name

        # Create the file only if it doesn't already exist
        file_path.touch(exist_ok=True)
        print(f"Created: {file_path}")

print("All files created successfully.")