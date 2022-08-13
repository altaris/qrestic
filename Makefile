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

.PHONY: qt
qt:
	pyside6-rcc qrestic/ui/ressources.qrc -o qrestic/ui/ressources_rc.py
	pyside6-uic --from-imports qrestic/ui/main_widget.ui -o qrestic/ui/main_widget_ui.py
	pyside6-lupdate qrestic/**/*.py qrestic/**/*.ui -ts qrestic/translations.ts
	pyside6-lrelease qrestic/translations/translations.ts -qm qrestic/translations/translations_fr.qm

.PHONY: run
run:
	python3 -m $(SRC_PATH) secrets/conf.json test/

.PHONY: typecheck
typecheck:
	mypy -p $(SRC_PATH)
