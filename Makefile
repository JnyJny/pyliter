
TARGET=pyliter

VERSION_FILE= $(TARGET)/__version__.py

.PHONY: $(VERSION_FILE) tag bump push update_pyproject

all:
	@echo major  - updates version major number 
	@echo minor  - updates version minor number
	@echo patch  - updates version patch number
	@echo update - updates __version__.py and tags version git
	@echo push  - pushes commits and tags to origin/master
	@echo clean - cleans up report files and/or directories

MAJOR:
	@poetry version major

MINOR:
	@poetry version minor

PATCH:
	@poetry version patch

major: MAJOR update

minor: MINOR update

patch: PATCH update

update:
	@awk '/^version/ {print $$0}' pyproject.toml | sed "s/version/__version__/" > $(VERSION_FILE)
	@git add pyproject.toml $(VERSION_FILE)
	@awk '{print $$3}' $(VERSION_FILE) | xargs git commit -m
	@awk '{print $$3}' $(VERSION_FILE) | xargs git tag


push:
	@git push --tags origin master

clean:
	@/bin/rm -rf report?* report.???*
