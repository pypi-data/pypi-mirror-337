import os.path
import unittest
from tyger.discipline.simple.types import SimpleTypeSystem
from tyger.discipline.types import TypeException
from tyger.driver import Driver
from tyger.parser import Parser
from tyger.phases.dependency_collection import DependencyCollectionPhase
from tyger.phases.type_check import TypingPhase
import ast

class TestTyping(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        tests_dir = os.path.abspath(os.path.dirname(__file__))
        sources = os.path.join(tests_dir, "sources", "static")
        cls.parser = Parser(sources)
        cls.driver = Driver([DependencyCollectionPhase(sources), TypingPhase(SimpleTypeSystem())])

    def assertDoesNotFail(self, callback):
        try:
            callback()
        except Exception as e:
            self.fail(f"Callback failed with exception {e}")

    def typecheck(self, program: ast.Module):
        return self.driver.run(program)

    def read_source(self, loc: str) -> ast.Module:
        return self.parser.parse(loc)

    def test_assignments_fail(self):
        program = self.read_source("assignments_fail.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_assignments_ok(self):
        program = self.read_source("assignments_ok.py")
        self.assertDoesNotFail(lambda: self.typecheck(program))

    def test_ann_reassign_fail(self):
        program = self.read_source("ann_reassign_fail.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_unann_reassign_fail(self):
        program = self.read_source("unann_reassign_fail.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_assign_error(self):
        program = self.read_source("assign_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_ann_assign_fail_same_type(self):
        program = self.read_source("ann_assign_fail_same_type.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))


    def test_function(self):
        program = self.read_source("function.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_ho_function(self):
        program = self.read_source("ho_function.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_function_body_error(self):
        program = self.read_source("function_body_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_function_body_ok(self):
        program = self.read_source("function_body_ok.py")
        self.assertDoesNotFail(lambda: self.typecheck(program))

    def test_function_return_invalid(self):
        program = self.read_source("function_return_invalid.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_function_return_ok(self):
        program = self.read_source("function_return_ok.py")
        self.assertDoesNotFail(lambda: self.typecheck(program))

    def test_function_return_dyncheck(self):
        program = self.read_source("function_return_dyncheck.py")
        self.assertDoesNotFail(lambda: self.typecheck(program))

    def test_function_conditional(self):
        program = self.read_source("function_conditional.py")
        self.assertDoesNotFail(lambda: self.typecheck(program))

    def test_dict_key_error(self):
        program = self.read_source("dict_key_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_dict_value_error(self):
        program = self.read_source("dict_value_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_complex_tuple_assign_error(self):
        program = self.read_source("complex_tuple_assign_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_list_addition_error(self):
        program = self.read_source("list_addition_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_import_from_error(self):
        program = self.read_source("import_from_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_import_whole_module_error(self):
        program = self.read_source("import_whole_module_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_import_wildcard_error(self):
        program = self.read_source("import_wildcard_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_import_alias_namespace_error(self):
        program = self.read_source("import_alias_namespace_error.py")
        self.assertRaises(AttributeError, lambda: self.typecheck(program))

    def test_module_attribute_error(self):
        program = self.read_source("module_attribute_error.py")
        self.assertRaises(AttributeError, lambda: self.typecheck(program))

    def test_implicit_import_error(self):
        program = self.read_source("implicit_import_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_ifexpr_tuple_error(self):
        program = self.read_source("ifexpr_tuple_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_function_dom_error(self):
        program = self.read_source("function_dom_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_dict_assign_fail(self):
        program = self.read_source("dict_assign_fail.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_dict_return_error(self):
        program = self.read_source("dict_return_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))

    def test_dict_access_error(self):
        program = self.read_source("dict_access_error.py")
        self.assertRaises(TypeException, lambda: self.typecheck(program))