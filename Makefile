run: install
	@python3 pac-man.py $(ARG)

install:
	@uv sync

debug:
	@python3 -m pdb pac-man.py $(ARG)

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +
