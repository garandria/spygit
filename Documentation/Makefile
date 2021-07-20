# Variables below are already defined in conf.py
# See lines 24 to 28 of conf.py
# PYTHONPATH=./src
# export PYTHONPATH
SPHINXBUILD=/usr/bin/sphinx-build
SPHINXAPIDOC=sphinx-apidoc
CONFIGPATH=.
SOURCEDOC=sourcedoc
DOC=doc

.PHONY: clean doc

clean:
	rm -f *~ */*~
	rm -rf __pycache__
	rm -rf $(DOC)

sourcedoc:
	$(SPHINXAPIDOC) -o $(SOURCEDOC) ../src --append-syspath

doc: sourcedoc
	$(SPHINXBUILD) -c $(CONFIGPATH) -b html $(SOURCEDOC) $(DOC)
