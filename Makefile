.PHONY: docs
docs:
	cd docs && make html

.PHONY: test
test:
	py.test --cov-report html --cov-report term --cov=manifold --cov-config .coveragerc tests/

.PHONY: lint
lint:
	pylint manifold tests

.PHONY: check
check: test lint

.PHONY: check-travis
check-travis:
	pylint manifold tests
	py.test -c .coveragerc tests/

.PHONY: deploy
deploy: check
	python setup.py bdist_wheel
	twine upload dist/*  --skip-existing
