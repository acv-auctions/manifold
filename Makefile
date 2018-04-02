.PHONY: docs
docs:
	cd docs && make html

.PHONY: testlint
testlint:
	python3 runtests.py

.PHONY: deploy
deploy: testlint
	python setup.py bdist_wheel
	twine upload dist/*  --skip-existing
