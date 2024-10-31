PY:=python3
PROJECT_ROOT:=$(shell pwd)
REQUIREMENTS:=$(PROJECT_ROOT)/requirements.txt

.ONESHELL:
.PHONY: venv
venv:
	@$(PY) -m venv .venv
	@. .venv/bin/activate
	@pip install -r $(REQUIREMENTS)

.PHONY: test
test:
	@PYTHONPATH=$(PROJECT_ROOT) python3 graphs/tests/test_simple_graph.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 hash_maps/tests/test_hash_map.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 lists/tests/test_array_list.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 lists/tests/test_doubly_linked_list.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 lists/tests/test_singly_linked_list.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 sorting/tests/test_merge_sort.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 trees/tests/test_binary_heap.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 trees/tests/test_binary_search_tree.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 trees/tests/test_binary_tree.py
	@PYTHONPATH=$(PROJECT_ROOT) python3 trees/tests/test_red_black_tree.py

.PHONY: fmt
fmt:
	@ruff format .
	@ruff check --fix .

.PHONY: check
check:
	@ruff check .
