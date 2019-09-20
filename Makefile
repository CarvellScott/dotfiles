every_import.py:
	@grep -hIor --exclude={tags,.git} '^\(from [^\. ]*\|import [^\. ]*\)' * | sed -e 's/^from /import /' | sort -u > every_import.py

tags:
	ctags -R --fields=+l --languages=python --python-kinds=-iv -f ./tags ./
