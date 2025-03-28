import argparse
import ast
import os
import sys
import types
from tyger.discipline.sectypes.types import SecurityTypeSystem
from tyger.discipline.sectypes.ToAST import SecurityASTElaborator
from tyger.discipline.simple.ToAST import SimpleASTElaborator
from tyger.discipline.simple.types import SimpleTypeSystem
from tyger.driver import Driver
from tyger.parser import Parser
from tyger.phases.dependency_collection import DependencyCollectionPhase
from tyger.phases.elaboration import ElaborationPhase
from tyger.phases.type_check import TypingPhase


def setup_cli_parser() -> argparse.ArgumentParser:
    cli_parser = argparse.ArgumentParser(description="Tyger: a simple typechecker")
    cli_parser.add_argument("file_name", help="target file path")
    cli_parser.add_argument("-d", "--discipline", default="simple")
    cli_parser.add_argument("--elaborate", action="store_true",
                            help="Elaborate target source and dependencies for gradual typing")

    return cli_parser

def main():
    cli_parser = setup_cli_parser()
    cli_args = cli_parser.parse_args()

    file_name = cli_args.file_name

    file_dir, file_name = os.path.split(file_name)
    file_parser = Parser(file_dir)
    file_ast = file_parser.parse(file_name)

    discipline = cli_args.discipline

    if discipline == "simple":
        type_system = SimpleTypeSystem()
    elif discipline == "security":
        type_system = SecurityTypeSystem()
    else:
        print("Unsupported discipline")
        return 1

    phases = [DependencyCollectionPhase(file_dir), TypingPhase(type_system)]

    if cli_args.elaborate:
        if discipline == "simple":
            ast_elaborator = SimpleASTElaborator()
        elif discipline == "security":
            ast_elaborator = SecurityASTElaborator()
        phases.append(ElaborationPhase(ast_elaborator))

    driver = Driver(phases)

    target_module, deps_asts = driver.run(file_ast)

    if cli_args.elaborate:
        deps = {name: compile(ast.fix_missing_locations(code_ast), "<tyger>", "exec") for name, code_ast in
                deps_asts.items()}
        # We initialize the dependencies
        # We first add them to sys.modules
        for dep in deps:
            sys.modules[dep] = types.ModuleType(dep)

        # Then we add submodules to module namespace where necessary
        for dep in deps:
            name_tokens = dep.split('.')
            for i in range(len(name_tokens) - 1):
                to_update_name = '.'.join(name_tokens[:i + 1])
                to_update_module = sys.modules[to_update_name]
                to_add_name = name_tokens[i + 1]
                to_add_module = sys.modules[f"{to_update_name}.{to_add_name}"]
                if not hasattr(to_update_module, to_add_name):
                    setattr(to_update_module, to_add_name, to_add_module)
        exec(compile(ast.fix_missing_locations(target_module), '<ast>', 'exec'), globals())


if __name__ == "__main__":
    main()


