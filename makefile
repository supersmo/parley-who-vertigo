all:
	@echo "Nothing to do"

clean:
	find . \( -type d -a -name __pycache__ \) -exec rm -rf {} +

.PHONY: all clean
