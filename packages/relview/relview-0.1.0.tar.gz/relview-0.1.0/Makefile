.PHONY: default
default:: install

.PHONY: all
all::

# Usage
# -----
# make prefix=<path> install           # Install git-cola
#
# make doc                             # Build documentation
# make prefix=<path> install-doc       # Install documentation
#
# Variables
# ---------
# prefix - Installation prefix.
# DESTDIR - Temporary staging directory.
#
# The external commands used by this Makefile are...

PIP = pip
PYTHON ?= python3
RM = rm -f
RM_R = rm -fr
RMDIR = rmdir
XARGS = xargs

# These values can be overridden on the command-line or via config.mak
# DESTDIR =
prefix = $(HOME)

install_args =
ifdef DESTDIR
	install_args += --root="$(DESTDIR)"
	export DESTDIR
endif
install_args += --prefix="$(prefix)"
install_args += --disable-pip-version-check
install_args += --ignore-installed
install_args += --no-deps
export prefix

PYTHON_DIRS = relview
PYTHON_DIRS += tests

ALL_PYTHON_DIRS = $(PYTHON_DIRS)

# User customizations
-include config.mak

all::

.PHONY: install
install:: all
	$(PIP) install $(install_args) .

.PHONY: tests

test::
	${PYTHON} -m pytest relview tests

# make check alias for make test
.PHONY: check
check:: test

.PHONY: wheel
wheel::
	${PYTHON} -m build -n .
