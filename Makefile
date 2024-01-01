#!/usr/bin/env -S make -f
.PHONY: clean clean-build pypi-build pypi-release
# Most commands copied from https://github.com/cookiecutter/cookiecutter/blob/main/Makefile

help: ## You are here
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc ## Remove ALL file artifacts

clean-build: ## Remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc: ## Remove python file artifacts
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

pypi-build: ## Prepare to upload to PyPI
	python3 setup.py sdist
	tar tzf dist/python_intensifies*
	twine check dist/*

pypi-release: dist ## Upload dist to PyPi
	twine upload dist/*

every_import.py:
	@grep -hIor --exclude={tags,.git} '^\(from [^\. ]*\|import [^\. ]*\)' * | sed -e 's/^from /import /' | sort -u > every_import.py

print-make-recipe-args:
	echo 'bwah' > $@
