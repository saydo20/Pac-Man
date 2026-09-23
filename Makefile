clean:
	@find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +
