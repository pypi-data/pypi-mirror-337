import textwrap

def print_project_structure():
    structure = textwrap.dedent("""
    📂 automation_project/
    │── bin/             # Executable scripts or helper tools
    │── ci_cd/           # CI/CD pipeline configs (GitHub Actions, Jenkins, etc.)
    │── config/          # Configuration settings (JSON, YAML, INI, etc.)
    │── data/            # Stores input/output files and datasets
    │── docker/          # Docker-related files for containerization
    │── docs/            # Documentation and API references
    │── logs/            # Log files for debugging
    │── migrations/      # Database migration scripts
    │── models/          # Machine learning models (if applicable)
    │── notebooks/       # Jupyter notebooks for debugging or prototyping
    │── scripts/         # Shell scripts for setup, deployment, or automation
    │── src/             # Main source code
    │   ├── core/        # Core logic and reusable modules
    │   ├── tasks/       # Automation scripts
    │   ├── main.py      # Entry point of the project (this file)
    │── tests/           # Unit tests for the project
    │── .env             # Environment variables file
    │── .gitignore       # Files to ignore in version control
    │── README.md        # Project documentation

    🚀 How to Use:
    1️⃣ Run the automation script:
        python src/main.py

    2️⃣ Run tests:
        python -m unittest discover tests

    3️⃣ Run inside Docker:
        docker build -t automation_project .
        docker run automation_project

    4️⃣ Modify configuration in config/config.json

    Happy coding! 🎉
    """)
    print(structure)

if __name__ == "__main__":
    print_project_structure()
