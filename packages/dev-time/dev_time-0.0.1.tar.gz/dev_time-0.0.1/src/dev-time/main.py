import typer
import os
import csv
from sqlmodel import create_engine, SQLModel, Session, select

from model import Project

from rich.console import Console
from rich.table import Table

app = typer.Typer()

console = Console()

err_console = Console(stderr=True, style="bold red")

db_url = os.getenv("DATABASE_DB", default="sqlite:///database.db")

db_engine = None


def init_db():
    """Inicialization of the database."""
    global db_engine
    db_engine = create_engine(db_url, echo = False) # añadir el DEBUG
    SQLModel.metadata.create_all(db_engine)


def get_project_if_exits(project_name: str, session: Session) -> Project | None:
    statement = select(Project).where(Project.name == project_name)
    return session.exec(statement).first()


@app.command()
def create_project(project_name: str) -> None:
    """Create a new project."""
    with Session(db_engine) as session:
        if get_project_if_exits(project_name, session):
            err_console.print("ERROR: It exists a project with the same name")
            raise typer.Exit(code=1)
        
        project = Project(name=project_name)
        session.add(project)
        session.commit()


@app.command()
def delete_project(project_name: str):
    """Delete a project"""
    with Session(db_engine) as session:
        if not get_project_if_exits(project_name, session):
            err_console.print("ERROR: It doen't exist a project with that name.")
            raise typer.Exit(code=1)
        
        statement = select(Project).where(Project.name == project_name)  
        result = session.exec(statement).first()
        
        session.delete(result)  
        session.commit()


@app.command()
def summary():
    """View a summary of all the projects and their total logged time."""
    with Session(db_engine) as session:
        projects = session.exec(select(Project)).all()
        
        
        table = Table()
        table.add_column("Project name", justify="right", style="cyan", no_wrap=True)
        table.add_column("Time logged", style="magenta")

        for project in projects:
            hours, minutes = divmod(project.total_time, 60)
            project_time = f"{hours}h {minutes}m" if hours else f"{minutes}m"
            table.add_row(project.name, project_time)


        console.print(table)


@app.command()
def log_time(project_name: str, time_project: str):
    """Logg time spent on a project."""
    with Session(db_engine) as session:

        if not get_project_if_exits(project_name, session):
            err_console.print("ERROR: It doesn't exist a project with that name")
            raise typer.Exit(code=1)

        statement = select(Project).where(Project.name == project_name)
        project = session.exec(statement).first()
        

        try:
            if time_project.endswith('h'):
                final_time = int(60 * float(time_project[:-1]))
            elif time_project.endswith('m'):
                final_time = int(float(time_project[:-1]))
            else:
                raise ValueError("Invalid format")
        except ValueError:
            err_console.print("ERROR: You must write a number followed by a character: 'h' or 'm' (i. e.: 2h, 30m)")
            raise typer.Exit(code=1)

        project.total_time = final_time
        print(f"OK! Logged {final_time} minutes for {project_name}")

        session.commit()


@app.command()
def snapshot(file: str) -> None:
    """Export the data project to a CSV file."""
    with Session(db_engine) as session:
        projects = session.exec(select(Project)).all()

        if not projects:
            err_console.print("ERROR: There isn't any project")
            typer.Exit(code=1)

        with open(file, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Project', 'Time'])
            for project in projects:
                spamwriter.writerow([project.name, project.total_time])
            print(f"OK! Snapshot saved to {file}")



if __name__ == "__main__":
    init_db()
    app()