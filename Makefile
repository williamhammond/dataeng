dataset:
	python nycevents/make_dataset.py
lint:
	find . -iname "*.py" | xargs pylint 
graphs:
	python nycevents/visualize.py