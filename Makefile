.PHONY: test

test:
	PYTHONPATH=. py.test --cov=rmotr_curriculum_tools tests/ -v --tb=short
