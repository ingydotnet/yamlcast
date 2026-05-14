R := https://github.com/makeplus/makes
M := .cache/makes
$(shell [ -d '$M' ] || git clone -q $R '$M')

include $M/init.mk
include $M/go.mk
include $M/clean.mk
include $M/shell.mk
include .cache/makes/init.mk

include $(MAKES)/yamlscript.mk

export PATH := $(ROOT)/bin:$(PATH)

YAMLCAST := bin/yamlcast

test:
	$(YAMLCAST) --dry-run example.yaml
