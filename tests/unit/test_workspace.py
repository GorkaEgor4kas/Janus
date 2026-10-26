import pytest

from janus.targets.workspace import Workspace

@pytest.fixture
def workspace() -> Workspace:
    return Workspace()


def test_read_existing_note_return_content(workspace: Workspace) -> None:
    result = workspace.read_note("note-001")

    assert result == "Janus is an AI agent security testing platform."


def test_read_missing_note_return_none(workspace: Workspace) -> None:
    result = workspace.read_note("note-999")

    assert result == "Note not found."

def test_search_notes_in_case_insensitive(workspace: Workspace) -> None:
    result = workspace.search_notes("SCENARIOS")

    assert "note-002" in result

def test_search_notes_return_empty_dict_for_no_matches(workspace: Workspace) -> None:
    result = workspace.search_notes("nonexistent query")

    assert result == {}

    
