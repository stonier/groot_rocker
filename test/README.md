# Executing Tests

```bash
# run all tests in the current directory
$ pytest .
$ nosetests .

# run all tests with full stdout (-s / --capture=no)
$ pytest -s
$ nosetests -s .

# run a test module
$ pytest -s test_yaml.py
$ nosetests -s test_yaml.py

# run a single test
$ pytest -s test_yaml.py::ExtensionTestCase::test_defaults_from_yaml
$ nosetests -s test_yaml.py:ExtensionTestCase.test_defaults_from_yaml

# run a set of tests (filtered by keywords)
$ pytest -s -k "ExtensionTestCase and test_defaults_from_yaml"
```
