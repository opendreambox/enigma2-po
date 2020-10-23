LANGS = ar ca cs da de el en es et fa fi fr fy he hr hu is it lt lv nl no pl pt pt_BR ru sv sk sl sr tr uk
MO_NAME = enigma2

LANGMO = $(LANGS:=.mo)
LANGPO = $(LANGS:=.po)

BUILT_SOURCES = $(LANGMO)
CLEANFILES = $(LANGMO)

.po.mo:
	$(MSGFMT) -o $@ $<

dist-hook: $(LANGPO)

install-data-local: $(LANGMO)
	for lang in $(LANGS); do \
		$(mkinstalldirs) $(DESTDIR)${datadir}/enigma2/po/$$lang/LC_MESSAGES; \
		$(INSTALL_DATA) $$lang.mo $(DESTDIR)${datadir}/enigma2/po/$$lang/LC_MESSAGES/$(MO_NAME).mo; \
	done

uninstall-local:
	for lang in $(LANGS); do \
		$(RM) $(DESTDIR)${datadir}/enigma2/po/$$lang/LC_MESSAGES/$(MO_NAME).mo; \
	done
