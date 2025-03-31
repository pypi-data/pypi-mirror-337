from sqlmodel import Session, SQLModel, create_engine, select
from dev_time.model import Project

import pytest


def test_create_project_with_defaults():
    """Test creating a Project with default values."""
    project = Project(name="Test Project")
    assert project.id is None
    assert project.name == "Test Project"
    assert project.total_time == 0

