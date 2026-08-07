%define base_name	simple_gettext

Name:		ocaml-%{base_name}
Version:	0.1
Release:	20
Summary:	OCaml wrapper for the gettext library
URL:		https://ocaml.org/
# Upstream (merd.net / pixel) is long dead; tarball from historic cooker SRPM
Source0:	ocaml-simple_gettext-%{version}.tar.bz2
License:	GPLv2+
Group:		Development/OCaml
BuildRequires:	make
BuildRequires:	perl
BuildRequires:	ocaml
BuildRequires:	ocaml-compiler
BuildRequires:	ocaml-findlib
# libintl is in glibc on Linux; gettext-devel for headers if split
BuildRequires:	gettext

%description
OCaml bindings to GNU gettext (bindtextdomain, textdomain, gettext,
dgettext) plus a small xgettext-ocaml helper. Upstream project is
defunct; this package keeps the historic 0.1 sources available for
legacy reverse dependencies.

%package devel
Summary:	Development files for %{name}
Group:		Development/OCaml
Requires:	%{name} = %{EVRD}

%description devel
Libraries and signature files for developing applications that use
%{name}.

%prep
%setup -q -n %{base_name}-%{version}
# OCaml 5 C API renames
find . -name '*.c' -print0 | xargs -0 -r perl -i -pe '
	for my $s (qw(
		raise_with_string raise_with_arg raise_out_of_memory raise_sys_error
		invalid_argument copy_string alloc_custom alloc_string string_length
		failwith alloc_small raise_constant raise_end_of_file
	)) {
		s/(?<![A-Za-z0-9_])$s\s*\(/caml_$s(/g;
	}
	s/caml_caml_/caml_/g;
'
# ML expects ocaml_simple_gettext_dcgettext; C only exported _dgettext
sed -i 's/ocaml_simple_gettext_dgettext/ocaml_simple_gettext_dcgettext/g' c_simple_gettext.c
# Prefer CAMLprim value for exports
sed -i 's/^value /CAMLprim value /' c_simple_gettext.c

%build
export CC=%{__cc}
export CFLAGS="$(echo "%{optflags}" | sed 's/-flto//g') -fPIC"
export LDFLAGS=
# Makefile hardcodes STDLIB/INSTALLBINDIR; findlib install uses env
make all \
	OCAMLC=ocamlc OCAMLOPT=ocamlopt OCAMLFIND=ocamlfind \
	CFLAGS="$CFLAGS" LDFLAGS=

%install
export OCAMLFIND_DESTDIR=%{buildroot}%{_libdir}/ocaml
export OCAMLFIND_LDCONF=ignore
export DESTDIR=%{buildroot}
mkdir -p "$OCAMLFIND_DESTDIR/stublibs" %{buildroot}%{_bindir}
# Install binary first
make install-bin DESTDIR=%{buildroot} INSTALLBINDIR=%{_bindir}
# Manual findlib install: avoid ld.conf write and place dll in stublibs
install -d "$OCAMLFIND_DESTDIR/%{base_name}"
install -m 644 META simple_gettext.cmi simple_gettext.mli \
	simple_gettext.cma simple_gettext.cmxa simple_gettext.a \
	libsimple_gettext.a \
	"$OCAMLFIND_DESTDIR/%{base_name}/"
# cmx is optional (not always produced as installable name)
if [ -f simple_gettext.cmx ]; then
	install -m 644 simple_gettext.cmx "$OCAMLFIND_DESTDIR/%{base_name}/"
fi
install -m 755 dllsimple_gettext.so "$OCAMLFIND_DESTDIR/stublibs/"
rm -f %{buildroot}%{_libdir}/ocaml/stublibs/*.owner

%files
%defattr(-,root,root)
%doc README
%license LICENSE
%dir %{_libdir}/ocaml/%{base_name}
%{_libdir}/ocaml/%{base_name}/META
%{_libdir}/ocaml/%{base_name}/*.cmi
%{_libdir}/ocaml/%{base_name}/*.cma
%{_libdir}/ocaml/stublibs/dllsimple_gettext.so*

%files devel
%defattr(-,root,root)
%{_bindir}/xgettext-ocaml
%{_libdir}/ocaml/%{base_name}/*.a
%{_libdir}/ocaml/%{base_name}/*.cmxa
%{_libdir}/ocaml/%{base_name}/*.mli
%{_libdir}/ocaml/%{base_name}/*.cmx
