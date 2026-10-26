import pytest

from janus.targets.minimal_target import MinimalTarget
from janus.targets.workspace import Workspace

@pytest.fixture
def target() -> MinimalTarget:
    workspace = Workspace()
    return MinimalTarget(workspace)

def test_target_reads_notes_from_workspace(target: MinimalTarget) -> None:
    result = target.read_note("note-001")

    assert result == "Janus is an AI agent security testing platform."


def test_target_returns_none_for_missing_note(target: MinimalTarget) -> None:
    result = target.read_note("note-999")

    assert result == "Note not found."


def test_target_searches_notes(target: MinimalTarget) -> None:
    result = target.search_notes("scenarios")

    assert "note-002" in result


def test_target_uses_injected_workspace() -> None:
    workspace = Workspace()
    target = MinimalTarget(workspace)

    assert target.workspace is workspace


def test_target_observes_changes_in_workspace(target: MinimalTarget) -> None:
    target.workspace.notes["note-004"] = "This is a new note."

    result = target.read_note("note-004")

    assert result == "This is a new note."

