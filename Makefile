DOCS_PATH 		= docs
SRC_PATH 		= qrestic
VENV			= ./venv

.ONESHELL:

all: format typecheck lint

.PHONY: docs
docs:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	pdoc --output-directory $(DOCS_PATH) $(SRC_PATH)

.PHONY: docs-browser
docs-browser:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	pdoc $(SRC_PATH)

.PHONY: format
format:
	black --line-length 79 --target-version py310 $(SRC_PATH)

.PHONY: lint
lint:
	pylint $(SRC_PATH)

.PHONY: run
run:
	python3 -m $(SRC_PATH)

.PHONY: typecheck
typecheck:
	mypy -p $(SRC_PATH)

.PHONY: ui
ui:
	pyside6-rcc qrestic/ui/ressources.qrc -o qrestic/ui/ressources_rc.py
	pyside6-uic --from-imports qrestic/ui/main_widget.ui -o qrestic/ui/main_widget_ui.py
