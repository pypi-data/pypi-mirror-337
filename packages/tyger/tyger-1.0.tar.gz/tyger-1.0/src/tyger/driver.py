import ast
from tyger.phase import Phase


class Driver:
    def __init__(self, phases: list[Phase]):
        self.phases = phases

    def run(self, tree: ast.Module) -> tuple[ast.Module, dict[str, ast.Module]]:
        new_tree = tree
        kwargs = {}
        for phase in self.phases:
            new_tree, kwargs = phase.run(new_tree, **kwargs)
        return new_tree, kwargs.get("dependencies", {})


