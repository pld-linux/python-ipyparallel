#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (some failures)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Interactive Parallel Computing with IPython
Summary(pl.UTF-8):	Interaktywne przetwarzanie równoległe z użyciem IPythona
Name:		python-ipyparallel
Version:	6.2.5
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/ipyparallel/
Source0:	https://files.pythonhosted.org/packages/source/i/ipyparallel/ipyparallel-%{version}.tar.gz
# Source0-md5:	102b6ab1577d2edef5767ee462f305ab
URL:		https://pypi.org/project/ipyparallel/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-dateutil >= 2.1
BuildRequires:	python-decorator
BuildRequires:	python-futures
BuildRequires:	python-ipykernel >= 4.4
BuildRequires:	python-ipython >= 4
BuildRequires:	python-ipython_genutils
BuildRequires:	python-jupyter_client
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
BuildRequires:	python-pyzmq >= 13
BuildRequires:	python-testpath
BuildRequires:	python-tornado >= 4
BuildRequires:	python-traitlets >= 4.3
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-dateutil >= 2.1
BuildRequires:	python3-decorator
BuildRequires:	python3-ipykernel >= 4.4
BuildRequires:	python3-ipython >= 4
BuildRequires:	python3-ipython_genutils
BuildRequires:	python3-jupyter_client
BuildRequires:	python3-mock
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pyzmq >= 13
BuildRequires:	python3-testpath
BuildRequires:	python3-tornado >= 4
BuildRequires:	python3-traitlets >= 4.3
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python-ipython
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Use multiple instances of IPython in parallel, interactively.

%description -l pl.UTF-8
Używanie wielu instancji IPythona równolegle, interaktywnie.

%package -n python3-ipyparallel
Summary:	Interactive Parallel Computing with IPython
Summary(pl.UTF-8):	Interaktywne przetwarzanie równoległe z użyciem IPythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-ipyparallel
Use multiple instances of IPython in parallel, interactively.

%description -n python3-ipyparallel -l pl.UTF-8
Używanie wielu instancji IPythona równolegle, interaktywnie.

%package apidocs
Summary:	API documentation for Python ipyparallel module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona ipyparallel
Group:		Documentation

%description apidocs
API documentation for Python ipyparallel module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona ipyparallel.

%prep
%setup -q -n ipyparallel-%{version}

%{__sed} -i -e "s,'etc/jupyter,'/etc/jupyter," setup.py

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for f in ipcluster ipcontroller ipengine ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
done

%py_postclean
%endif

%if %{with python3}
%py3_install

for f in ipcluster ipcontroller ipengine ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
	ln -s ${f}-3 $RPM_BUILD_ROOT%{_bindir}/$f
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/ipcluster-2
%attr(755,root,root) %{_bindir}/ipcontroller-2
%attr(755,root,root) %{_bindir}/ipengine-2
%{py_sitescriptdir}/ipyparallel
%{py_sitescriptdir}/ipyparallel-%{version}-py*.egg-info
%if 0
# shared with py3
%dir %{_datadir}/jupyter/nbextensions
%{_datadir}/jupyter/nbextensions/ipyparallel
%dir %{_sysconfdir}/jupyter
%dir %{_sysconfdir}/jupyter/jupyter_notebook_config.d
%{_sysconfdir}/jupyter/jupyter_notebook_config.d/ipyparallel-serverextension.json
%dir %{_sysconfdir}/jupyter/nbconfig
%dir %{_sysconfdir}/jupyter/nbconfig/tree.d
%{_sysconfdir}/jupyter/nbconfig/tree.d/ipyparallel-nbextension.json
%endif
%endif

%if %{with python3}
%files -n python3-ipyparallel
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/ipcluster
%attr(755,root,root) %{_bindir}/ipcluster-3
%attr(755,root,root) %{_bindir}/ipcontroller
%attr(755,root,root) %{_bindir}/ipcontroller-3
%attr(755,root,root) %{_bindir}/ipengine
%attr(755,root,root) %{_bindir}/ipengine-3
%{py3_sitescriptdir}/ipyparallel
%{py3_sitescriptdir}/ipyparallel-%{version}-py*.egg-info
%dir %{_datadir}/jupyter/nbextensions
%{_datadir}/jupyter/nbextensions/ipyparallel
%dir %{_sysconfdir}/jupyter
%dir %{_sysconfdir}/jupyter/jupyter_notebook_config.d
%{_sysconfdir}/jupyter/jupyter_notebook_config.d/ipyparallel-serverextension.json
%dir %{_sysconfdir}/jupyter/nbconfig
%dir %{_sysconfdir}/jupyter/nbconfig/tree.d
%{_sysconfdir}/jupyter/nbconfig/tree.d/ipyparallel-nbextension.json
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_images,_static,api,development,*.html,*.js}
%endif
