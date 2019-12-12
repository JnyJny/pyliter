
TARGET=pyliter

VERSION_FILE= $(TARGET)/__version__.py

.PHONY: $(VERSION_FILE) tag bump push update_pyproject

all:
	@echo bump  - updates version minor number and tags in git
	@echo push  - pushes commits and tags to origin/master
	@echo clean - cleans up report files and/or directories

bump:
	@poetry version
	@awk '/^version/ {print $$0}' pyproject.toml | sed "s/version/__version__/" > $(VERSION_FILE)
	@git add pyproject.toml $(VERSION_FILE)
	@awk '{print $$3}' $(VERSION_FILE) | xargs git commit -m
	@awk '{print $$3}' $(VERSION_FILE) | xargs git tag


push:
	@git push --tags origin master

clean:
	@/bin/rm -rf report?* report.???*
