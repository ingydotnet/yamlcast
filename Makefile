R := https://github.com/makeplus/makes
M := .cache/makes
$(shell [ -d '$M' ] || git clone -q $R '$M')

include $M/init.mk
include $M/go.mk
include $M/md2man.mk
include $M/ttyd.mk
include $M/uv.mk
include $M/yamlscript.mk
include $M/clean.mk

VHS-VERSION ?= 0.11.0
VHS-PKG := github.com/charmbracelet/vhs@v$(VHS-VERSION)
VHS := $(LOCAL-BIN)/vhs

VENV := $(LOCAL-PREFIX)/venv
CHAFA-PY-STAMP := $(VENV)/.chafa-py-installed

SHELL-DEPS += $(VHS) $(CHAFA-PY-STAMP)

include $M/shell.mk

export PATH := $(ROOT)/bin:$(PATH)

YAMLCAST := bin/yamlcast
MAN1 := man/man1/yamlcast.1
MAN1-SRC := man/yamlcast.1.md

test:
	$(YAMLCAST) --dry-run example.yaml

vhs-path: $(VHS) $(TTYD) $(CHAFA-PY-STAMP)
	@echo $(VHS)

man: $(MAN1)

$(MAN1): $(MAN1-SRC) $(MD2MAN)
	$Q mkdir -p $(dir $@)
	$(MD2MAN) < $< > $@

$(VHS): $(GO)
	@$(ECHO) "* Installing 'vhs' locally" >&2
	$Q GOBIN=$(LOCAL-BIN) go install $(VHS-PKG) 1>&2
	$Q touch $@

$(CHAFA-PY-STAMP): $(UV)
	@$(ECHO) "* Installing 'chafa.py' locally" >&2
	$Q UV_CACHE_DIR=$(LOCAL-CACHE)/uv $(UV) venv --quiet $(VENV) 1>&2
	$Q UV_CACHE_DIR=$(LOCAL-CACHE)/uv \
	  $(UV) pip install --quiet --python $(VENV)/bin/python chafa.py 1>&2
	$Q touch $@
