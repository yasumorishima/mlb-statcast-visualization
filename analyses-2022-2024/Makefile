.PHONY: convert-notebooks

convert-notebooks:
	jupyter nbconvert --to script notebooks/*.ipynb
	jupyter nbconvert --to script notebooks/sql/*.ipynb
	@# nbconvert may output .txt instead of .py depending on kernel metadata
	@for f in notebooks/*.txt; do [ -f "$$f" ] && mv "$$f" "$${f%.txt}.py"; done 2>/dev/null; true
	@for f in notebooks/sql/*.txt; do [ -f "$$f" ] && mv "$$f" "$${f%.txt}.py"; done 2>/dev/null; true
	@echo "Notebooks converted to .py files."
