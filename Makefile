.PHONY: test lint run clean

test:
	pytest tests/

lint:
	python -m py_compile **/*.py

run:
	uvicorn api.gateway.router:app --reload --port 8080

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
