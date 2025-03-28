from deepdiff import DeepDiff
import glob
import os
import pytest
from jarviscg.core import CallGraphGenerator
from jarviscg import formats

# Necessary because CallGraphGenerator expects to be running one directory
# up from shallowest module definitions
@pytest.fixture(autouse=True)
def change_directory():
    os.chdir("tests")
    yield
    os.chdir("../")

def test_call_graph_generator_includes_indexed_functions() -> None:
    # Fixture setup:
    # - `klass.py` imports `parse_into_list_of_expressions` from `_utils.parse`
    # - `Klass#method` invokes `parse.expr.parse_into_list_of_expressions`
    # - `_utils/parse/__init__.py` exports `parse_into_list_of_expressions`
    # using `__all__`

    entrypoints = [
            "./fixtures/__init__.py",
            "./fixtures/_utils/parse/expr.py",
            "./fixtures/_utils/__init__.py",
            "./fixtures/_utils/parse/__init__.py",
            "./fixtures/core/__init__.py",
            "./fixtures/core/nested/klass.py",
            "./fixtures/core/nested/__init__.py",
    ]
    expected = {"fixtures.core.nested": {"filename": "fixtures/core/nested/__init__.py", "methods": {"fixtures.core.nested": {"name": "fixtures.core.nested", "first": 0, "last": 0}}}, "fixtures.core.nested.klass": {"filename": "fixtures/core/nested/klass.py", "methods": {"fixtures.core.nested.klass": {"name": "fixtures.core.nested.klass", "first": 1, "last": 5}, "fixtures.core.nested.klass.Klass.method": {"name": "fixtures.core.nested.klass.Klass.method", "first": 4, "last": 5}}}, "fixtures._utils.parse": {"filename": "fixtures/_utils/parse/__init__.py", "methods": {"fixtures._utils.parse": {"name": "fixtures._utils.parse", "first": 1, "last": 8}, "fixtures._utils.parse.parse_into_list_of_expressions": {"name": "fixtures._utils.parse.parse_into_list_of_expressions", "first": None, "last": None}}}, "fixtures._utils.parse.expr": {"filename": "fixtures/_utils/parse/expr.py", "methods": {"fixtures._utils.parse.expr": {"name": "fixtures._utils.parse.expr", "first": 1, "last": 9}, "fixtures._utils.parse.expr.parse_into_list_of_expressions": {"name": "fixtures._utils.parse.expr.parse_into_list_of_expressions", "first": 1, "last": 6}, "fixtures._utils.parse.expr._parse_positional_inputs": {"name": "fixtures._utils.parse.expr._parse_positional_inputs", "first": 8, "last": 9}}}, "fixtures.core": {"filename": "fixtures/core/__init__.py", "methods": {"fixtures.core": {"name": "fixtures.core", "first": 0, "last": 0}}}, "fixtures._utils": {"filename": "fixtures/_utils/__init__.py", "methods": {"fixtures._utils": {"name": "fixtures._utils", "first": 0, "last": 0}}}, "fixtures": {"filename": "fixtures/__init__.py", "methods": {"fixtures": {"name": "fixtures", "first": 0, "last": 0}}}}
    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()

    internal_mods = cg.output_internal_mods()
    diff = DeepDiff(expected, internal_mods)

    assert diff == {}

def test_call_graph_generator_includes_refs_to_aliased_classes() -> None:
    caller_of_aliased_class = "fixtures.other_fixture_class.OtherFixtureClass.baz"
    entrypoints = [
        "./fixtures/__init__.py",
        "./fixtures/fixture_class.py",
        "./fixtures/other_fixture_class.py",
    ]

    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    assert "fixtures.fixture_class.FixtureClass.bar" in output[caller_of_aliased_class]
    assert "fixtures.fixture_class.FixtureClass.bar" in output.keys()

def test_call_graph_generator_default_builds_incomplete_graph_for_pytest_file() -> None:
    entrypoints = [
        "./fixtures/tests/__init__.py",
        "./fixtures/tests/example_test.py",
        "./fixtures/fixture_class.py",
    ]

    cg = CallGraphGenerator(entrypoints, None)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    test_function_callees = output["fixtures.tests.example_test.test_fixture_class_foo_sets_current_time"]
    assert test_function_callees == ["tests.fixtures.fixture_class.FixtureClass"]
    assert "tests.fixtures.fixture_class.FixtureClass" in output.keys()

def test_call_graph_generator_with_decy_true_builds_complete_graph_for_pytest_file() -> None:
    entrypoints = [
        "./fixtures/tests/__init__.py",
        "./fixtures/tests/example_test.py",
        "./fixtures/fixture_class.py",
    ]
    expected_callees = [
        "tests.fixtures.fixture_class.FixtureClass.__init__",
        "tests.fixtures.fixture_class.FixtureClass.foo",
    ]

    cg = CallGraphGenerator(entrypoints, None, decy=True)
    cg.analyze()
    formatter = formats.Simple(cg)
    output = formatter.generate()

    test_function_callees = output["fixtures.tests.example_test.test_fixture_class_foo_sets_current_time"]
    diff = DeepDiff(test_function_callees, expected_callees, ignore_order=True)
    assert diff == {}
    for callee in test_function_callees:
        assert callee in output.keys()
