%define base_name   simple_gettext
%define name		ocaml-%{base_name}
%define version     0.1
%define release     %mkrel 13

Name:		    %{name}
Version:	    %{version}
Release: 	    %{release}
Summary:	    OCaml wrapper for the gettext library
URL:		    http://merd.net/pixel/ocaml-simple_gettext
Source0:	    http://merd.sourceforge.net/pixel/ocaml-simple_gettext/%{name}-%{version}.tar.bz2
License:	    GPL
Group:		    Development/Other
BuildRequires:  ocaml >= 3.10
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
%makeinstall_std OCAMLFIND= STDLIB=%{ocaml_sitelib}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README docs
%dir %{ocaml_sitelib}/%{base_name}
%{ocaml_sitelib}/%{base_name}/*.cmi

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{ocaml_sitelib}/%{base_name}/*
%exclude %{ocaml_sitelib}/%{base_name}/*.cmi
