import click
import os
import shutil
import subprocess
from pathlib import Path
import sys

def create_project_structure(project_name):
    """Create the project structure with all necessary files"""
    # Create main project directory
    os.makedirs(project_name, exist_ok=True)
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env

# Knowledge directory
knowledge/
"""
    with open(os.path.join(project_name, '.gitignore'), 'w') as f:
        f.write(gitignore_content)

    # Create pyproject.toml
    pyproject_content = f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "A project created with mycommand"
requires-python = ">=3.8"
dependencies = [
    "click>=8.0.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/{project_name}"]
"""
    with open(os.path.join(project_name, 'pyproject.toml'), 'w') as f:
        f.write(pyproject_content)

    # Create README.md
    readme_content = f"""# {project_name}

This project was created using mycommand.
## Installation
```bash
uv pip install -e .
```
## Usage
Add your usage instructions here.
## License
MIT License
"""
    with open(os.path.join(project_name, 'README.md'), 'w') as f:
        f.write(readme_content)
    # Create .env
    env_content = """# Add your environment variables here"""
    with open(os.path.join(project_name, '.env'), 'w') as f:
        f.write(env_content)
    # Create knowledge directory
    os.makedirs(os.path.join(project_name, 'knowledge'), exist_ok=True)
    # Create src directory structure
    src_path = os.path.join(project_name, 'src', project_name)
    os.makedirs(src_path, exist_ok=True)
    # Create __init__.py
    with open(os.path.join(src_path, '__init__.py'), 'w') as f:
        f.write('"""Main package initialization."""\n')
    # Create main.py
    main_content = """def main():
    print("Hello from mycommand!")

if __name__ == "__main__":
    main()
"""
    with open(os.path.join(src_path, 'main.py'), 'w') as f:
        f.write(main_content)
    # Create crew.py
    crew_content = """# Add your crew configuration here"""
    with open(os.path.join(src_path, 'crew.py'), 'w') as f:
        f.write(crew_content)
    # Create tools directory
    tools_path = os.path.join(src_path, 'tools')
    os.makedirs(tools_path, exist_ok=True)
    # Create tools/__init__.py
    with open(os.path.join(tools_path, '__init__.py'), 'w') as f:
        f.write('"""Tools package initialization."""\n')
    # Create custom_tool.py
    custom_tool_content = """class CustomTool:
    def __init__(self):
        pass
    def execute(self):
        pass"""
    with open(os.path.join(tools_path, 'custom_tool.py'), 'w') as f:
        f.write(custom_tool_content)
    # Create config directory
    config_path = os.path.join(src_path, 'config')
    os.makedirs(config_path, exist_ok=True)
    # Create agents.yaml
    agents_content = """agents:
  - name: default_agent
    role: default
    goals:
      - Complete assigned tasks"""
    with open(os.path.join(config_path, 'agents.yaml'), 'w') as f:
        f.write(agents_content)

    # Create tasks.yaml
    tasks_content = """tasks:
  - name: default_task
    description: Default task
    agent: default_agent
"""
    with open(os.path.join(config_path, 'tasks.yaml'), 'w') as f:
        f.write(tasks_content)

def create_flow_project_structure(project_name):
    """Create the 'flow' specific project structure"""
    flow_path = Path(project_name)
    flow_path.mkdir(parents=True, exist_ok=True)

    # Create directories
    (flow_path / "crews/poem_crew/config").mkdir(parents=True, exist_ok=True)
    (flow_path / "tools").mkdir(parents=True, exist_ok=True)

    # Create configuration files
    (flow_path / "crews/poem_crew/config/agents.yaml").write_text("""agents:
  - name: poem_writer
    role: writer
    goals:
      - Write creative poetry
""")
    (flow_path / "crews/poem_crew/config/tasks.yaml").write_text("""tasks:
  - name: write_poem
    description: Generate a poem based on a given theme
    agent: poem_writer
""")

    # Create core scripts
    (flow_path / "crews/poem_crew/poem_crew.py").write_text("# Poem crew logic goes here\n")
    (flow_path / "tools/custom_tool.py").write_text("# Custom tool logic goes here\n")

def check_package_manager():
    """Check which package manager is available"""
    try:
        subprocess.run(['uv', '--version'], check=True, capture_output=True)
        return 'uv'
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(['pip', '--version'], check=True, capture_output=True)
            return 'pip'
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

def create_venv(project_dir):
    """Create virtual environment using available package manager"""
    package_manager = check_package_manager()
    
    if package_manager == 'uv':
        try:
            subprocess.run(['uv', 'venv'], check=True, cwd=project_dir)
            return True
        except subprocess.CalledProcessError:
            click.echo("Warning: Failed to create virtual environment with uv, falling back to venv module")
    
    # Fallback to venv module
    try:
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True, cwd=project_dir)
        return True
    except subprocess.CalledProcessError as e:
        click.echo(f"Error creating virtual environment: {str(e)}", err=True)
        return False

def install_package(project_dir):
    """Install package in editable mode using available package manager"""
    package_manager = check_package_manager()
    
    if package_manager == 'uv':
        try:
            subprocess.run(['uv', 'pip', 'install', '-e', '.'], check=True, cwd=project_dir)
            return True
        except subprocess.CalledProcessError:
            click.echo("Warning: Failed to install with uv, falling back to pip")
    
    # Fallback to pip
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.'], check=True, cwd=project_dir)
        return True
    except subprocess.CalledProcessError as e:
        click.echo(f"Error installing package: {str(e)}", err=True)
        return False

@click.group()
def cli():
    """Mycommand tool - A command line interface for project management"""
    pass

@cli.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new project with standard structure"""
    click.echo(f"Initializing project: {project_name}")
    try:
        # Create project structure
        create_project_structure(project_name)
        
        # Change to project directory
        os.chdir(project_name)
        
        # Create virtual environment
        click.echo("Creating virtual environment...")
        if not create_venv(project_name):
            raise click.Abort()
        
        # Get the path to the virtual environment's activate script
        if os.name == 'nt':  # Windows
            activate_script = os.path.join('.venv', 'Scripts', 'activate')
        else:  # Unix/Linux/MacOS
            activate_script = os.path.join('.venv', 'bin', 'activate')
        
        # Install the package in editable mode
        click.echo("Installing package in editable mode...")
        if not install_package(project_name):
            raise click.Abort()
        
        click.echo(f"\nSuccessfully initialized project: {project_name}")
        click.echo("\nTo activate the virtual environment, run:")
        if os.name == 'nt':  # Windows
            click.echo(f"    {activate_script}")
        else:  # Unix/Linux/MacOS
            click.echo(f"    source {activate_script}")
            
    except Exception as e:
        click.echo(f"Error initializing project: {str(e)}", err=True)
        raise click.Abort()

@cli.command()
@click.argument("library_name")
def add(library_name):
    """Add a new dependency to the project"""
    package_manager = check_package_manager()
    click.echo(f"Adding library: {library_name}...")
    
    try:
        if package_manager == 'uv':
            subprocess.run(["uv", "pip", "install", library_name], check=True)
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", library_name], check=True)
        click.echo(f"Successfully added {library_name}.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error adding {library_name}: {str(e)}", err=True)

@cli.group()
def create():
    """Create different types of projects"""
    pass

@create.command()
@click.argument('project_name')
def flow(project_name):
    """Create a new flow project"""
    click.echo(f"Creating flow project: {project_name}")
    try:
        create_flow_project_structure(project_name)
        click.echo(f"Successfully created flow project: {project_name}")
    except Exception as e:
        click.echo(f"Error creating flow project: {str(e)}", err=True)

def main():
    cli()

if __name__ == '__main__':
    main() 