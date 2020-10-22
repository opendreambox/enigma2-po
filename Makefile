DOMAIN=enigma2
GETTEXT=xgettext

PODIR=po

# The languages to build
languages := am ar ca cs ckb da de el en es et fi fa fr fy he hr hu is it lt lv nl no pl pt pt_BR ru sv sk sl sq sr tr uk

################################################## USAGE #################################################################
# First Time:
# - edit the E2 TARBALL Exports if needed.
# - make init
#
# Always:
# - make update
# - make merge
################################################# USAGE ##################################################################

.PHONY: init submodule_init submodule_update default update pull template merge msmgmerge

init : submodule_init submodule_update

submodule_init:
	git submodule init

submodule_update:
	git submodule update

default: update

update : submodule_update template

template:
	find ./enigma2 ./enigma2-skins -iname "*.py" | xargs $(GETTEXT) -L Python --from-code=UTF-8 --add-comments="TRANSLATORS:" -d enigma2 -s -o $(PODIR)/enigma2.pot
	find ./enigma2 -iname "*.xml" | xargs ./scripts/xml2po.py >> $(PODIR)/enigma2.pot
	find ./enigma2 ./enigma2-skins  -iname "plugin_*.xml" | xargs ./scripts/meta2po.py >> $(PODIR)/enigma2.pot
	find ./enigma2-skins -iname "skin_*.xml" | grep -v skin_default.* | xargs ./scripts/meta2po.py >> $(PODIR)/enigma2.pot
	msguniq -n --add-location -o $(PODIR)/enigma2.pot $(PODIR)/enigma2.pot

merge:
	for lang in $(languages); do \
		echo "merging catalog for $${lang}"; \
		msgmerge --add-location -s -N -U "$(PODIR)/$$lang.po" "$(PODIR)/enigma2.pot"; \
		msgattrib --output-file=$(PODIR)/$$lang.po --no-obsolete $(PODIR)/$$lang.po; \
	done
	rm -f $(PODIR)/*.po~
	rm -f $(PODIR)/*.pending
