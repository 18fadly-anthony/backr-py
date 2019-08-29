PREFIX ?= ~/.local

all:
	@echo Run \'make install\' to install backr-py.

install:
	@mkdir -p $(DESTDIR)$(PREFIX)/bin
	@cp -p backr.py $(DESTDIR)$(PREFIX)/bin/backr.py
	@cp -p restor.py $(DESTDIR)$(PREFIX)/bin/restor.py

uninstall:
	@rm -rf $(DESTDIR)$(PREFIX)/bin/backr.py
	@rm -rf $(DESTDIR)$(PREFIX)/bin/restor.py
