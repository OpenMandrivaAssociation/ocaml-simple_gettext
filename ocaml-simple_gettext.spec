%define base_name   simple_gettext
%define name		ocaml-%{base_name}
%define version     0.1
%define release     %mkrel 9

Name:		    %{name}
Version:	    %{version}
Release: 	    %{release}
Summary:	    OCaml wrapper for the gettext library
URL:		    http://merd.net/pixel/ocaml-simple_gettext
Source0:	    http://merd.sourceforge.net/pixel/ocaml-simple_gettext/%{name}-%{version}.tar.bz2
License:	    GPL
Group:		    Development/Other
BuildRequires:  ocaml
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
OCaml wrapper for the gettext library

%package devel
Summary:    OCaml wrapper for the gettext library
Group:		Development/Other
Obsoletes:  %{name}

%description devel
OCaml wrapper for the gettext library

%prep
%setup -q -n %{base_name}-%{version}

%build
make

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
%makeinstall_std OCAMLFIND= STDLIB=%{_libdir}/ocaml/site-lib

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
%doc README docs
%{_bindir}/*
%{_libdir}/ocaml/site-lib/%{base_name}


