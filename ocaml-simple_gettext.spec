%define base_name	simple_gettext

Name:		ocaml-%{base_name}
Version:	0.1
Release:	19
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
export DESTDIR=%{buildroot}
mkdir -p "$OCAMLFIND_DESTDIR" %{buildroot}%{_bindir}
# findlib install + binary
make findlib-install install-bin \
	OCAMLFIND=ocamlfind \
	DESTDIR=%{buildroot} \
	INSTALLBINDIR=%{_bindir}
rm -f %{buildroot}%{_libdir}/ocaml/stublibs/*.owner
# Ensure native bits land in the package dir if findlib put them there
ls -la "$OCAMLFIND_DESTDIR/%{base_name}/" || true

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
%{_libdir}/ocaml/%{base_name}/*.cmx
%{_libdir}/ocaml/%{base_name}/*.mli
