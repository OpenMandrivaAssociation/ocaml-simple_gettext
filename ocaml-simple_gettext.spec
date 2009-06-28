%define base_name   simple_gettext
%define name		ocaml-%{base_name}
%define version     0.1
%define release     %mkrel 16

Name:		    %{name}
Version:	    %{version}
Release: 	    %{release}
Summary:	    OCaml wrapper for the gettext library
URL:		    http://merd.net/pixel/ocaml-simple_gettext
Source0:	    http://merd.sourceforge.net/pixel/ocaml-simple_gettext/%{name}-%{version}.tar.bz2
License:	    GPL
Group:		    Development/Other
BuildRequires:  ocaml >= 3.10
BuildRequires:  ocaml-findlib
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
OCaml wrapper for the gettext library

%package devel
Summary:    OCaml wrapper for the gettext library
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
OCaml wrapper for the gettext library

%prep
%setup -q -n %{base_name}-%{version}

%build
make

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}/ocaml/stublibs
%makeinstall_std OCAMLFIND_DESTDIR=%buildroot%{_libdir}/ocaml
rm -f %{buildroot}%{_libdir}/ocaml/stublibs/*.owner

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README docs
%dir %{_libdir}/ocaml/%{base_name}
%{_libdir}/ocaml/%{base_name}/*.cmi
%{_libdir}/ocaml/%{base_name}/*.cma
%{_libdir}/ocaml/%{base_name}/META
%{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/ocaml/%{base_name}/*.a
%{_libdir}/ocaml/%{base_name}/*.cmxa
%{_libdir}/ocaml/%{base_name}/*.mli
