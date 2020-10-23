AC_INIT([enigma2-po],[1.0.0],[https://github.com/opendreambox/enigma2-po])
AM_INIT_AUTOMAKE([foreign])

AC_PATH_PROG(MSGFMT, msgfmt)
AS_IF([test -z "$MSGFMT"],[AC_MSG_ERROR([Could not find msgfmt])])

AC_CONFIG_FILES([
Makefile
po/Makefile
])
AC_OUTPUT
