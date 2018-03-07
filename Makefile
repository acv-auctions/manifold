.PHONY: testlint
testlint:
	python3 runtests.py

.PHONY: deploy
deploy:
	python setup.py bdist_wheel
	twine upload dist/*
