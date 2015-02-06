%define base_name   simple_gettext
%define name		ocaml-%{base_name}
%define version     0.1
%define release     17

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


%changelog
* Sun Jun 28 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.1-16mdv2010.0
+ Revision: 390305
- rebuild

* Mon Dec 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.1-15mdv2009.1
+ Revision: 320954
- move non-devel files in main package
- site-lib hierarchy doesn't exist anymore

* Tue Dec 09 2008 Pixel <pixel@mandriva.com> 0.1-14mdv2009.1
+ Revision: 312235
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 0.1-13mdv2009.0
+ Revision: 254356
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.1-11mdv2008.1
+ Revision: 136634
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 01 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.1-11mdv2008.0
+ Revision: 77686
- drop macro definition, now in rpm-mandriva-setup
  ship .cmi file in non-devel subpackage

* Tue May 29 2007 Pixel <pixel@mandriva.com> 0.1-10mdv2008.0
+ Revision: 32509
- rebuild with new ocaml
- versioned obsolete and versioned provide


* Wed Mar 21 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.1-9mdv2007.1
+ Revision: 147156
- devel package obsoletes non-devel one

* Thu Jan 25 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.1-8mdv2007.1
+ Revision: 113235
- this is actually a devel-only package
- Import ocaml-simple_gettext

* Tue Aug 29 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.1-7mdv2007.0
- rebuild

* Wed Apr 26 2006 Pixel <pixel@mandriva.com> 0.1-6mdk
- rebuild for new ocaml

* Mon Jan 23 2006 Pixel <pixel@mandriva.com> 0.1-5mdk
- rebuild for new ocaml

* Fri Nov 04 2005 Pixel <pixel@mandriva.com> 0.1-4mdk
- rebuild for new ocaml

* Sat May 07 2005 Pixel <pixel@mandriva.com> 0.1-3mdk
- do have files in lib64 on x86_64

* Sat May 07 2005 Pixel <pixel@mandriva.com> 0.1-2mdk
- don't _libdir since it doesn't get to lib64 on x86_64
- %%mkrel

* Tue Nov 09 2004 Pixel <pixel@mandrakesoft.com> 0.1-1mdk
- initial release

