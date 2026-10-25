from janus.targets.workspace import Workspace


class MinimalTarget:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def read_note(self, note_id: str) -> str:
        return self.workspace.read_note(note_id)

    def search_notes(self, query: str) -> list[str]:
        return self.workspace.search_notes(query)

    