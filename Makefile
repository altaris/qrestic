DOCS_PATH 		= docs
SRC_PATH 		= qrestic
VENV			= ./venv

.ONESHELL:

all: format typecheck lint

.PHONY: build
build:
	cxfreeze --target-dir build/qrestic qrestic.py

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
	pyside6-rcc $(SRC_PATH)/ui/ressources.qrc \
		-o $(SRC_PATH)/ui/ressources_rc.py
	pyside6-uic --from-imports $(SRC_PATH)/ui/main_widget.ui \
		-o $(SRC_PATH)/ui/main_widget_ui.py
	pyside6-lupdate $(SRC_PATH)/**/*.py $(SRC_PATH)/**/*.ui \
		-ts $(SRC_PATH)/translations/translations.ts
	pyside6-lrelease $(SRC_PATH)/translations/translations.ts \
		-qm $(SRC_PATH)/translations/translations_fr.qm

.PHONY: run
run:
	python3 -m $(SRC_PATH) secrets/conf.json test/

.PHONY: typecheck
typecheck:
	mypy -p $(SRC_PATH)
