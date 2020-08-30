Summary:	A tool for capturing and visualizing network traffic
Summary(pl.UTF-8):	Narzędzie do przechwytywania i wizualizacji ruchu sieciowego
Name:		jpcap
Version:	0.01.16
Release:	2
License:	MPL v1.1
Group:		Development/Languages/Java
Source0:	http://downloads.sourceforge.net/jpcap/%{name}-%{version}.tar.gz
# Source0-md5:	2307e2956dc2d4da1e9891bf22e8f7b4
URL:		http://jpcap.sourceforge.net/
BuildRequires:	jpackage-utils
BuildRequires:	jdk >= 1.2
BuildRequires:	libpcap-devel >= 0.4
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jpcap captures network packets and allows the visualization of traffic
patterns in real-time. Users can define filter expressions, examine
packet data and manipulate graphical representations of hosts and
network communications.

Included is a jar file containing the jpcap packet capture library
which can be used by Java developers who wish to create their own
packet capture applications.

Internally, jpcap provides Java-native bindings to and relies on
libpcap.

%description -l pl.UTF-8
Jpcap przechwytuje pakiety sieciowe i pozwala wizualizować wzorce
ruchu w czasie rzeczywistym. Użytkownik może definiować wyrażenia
filtrów, badać dane pakietów oraz strerować reprezentacją graficzną
hostów i komunikacji sieciowej.

Załączony jest plik jar zawierający bibliotekę jpcap do
przechwytywania pakietów, którą programiści Javy mogą wykorzystać do
tworzenia własnych aplikacji przechwytujących pakiety.

Wewnętrznie jpcap zawiera natywne wiązania Javy do biblioteki libpcap.

%prep
%setup -q
%{__sed} -e 's|-lnsl /usr/lib/libpcap.a|-lpcap|' -i src/java/net/sourceforge/jpcap/capture/makefile
%{__sed} -e 's|for(;ifr < last; (char\*)ifr += ifrSize) {|for(;ifr < last; ifr = (ifreq*)((char*)ifr + ifrSize)) {|' -i src/java/net/sourceforge/jpcap/capture/jpcap.c

# "error: unknown tag @..."
%{__sed} -e '/@lastModified\(By\|At\)/d' -i src/java/net/sourceforge/jpcap/{capture,client,net,simulator,util}/*.java
# "error: bad use of '>'"
%{__sed} -e 's/-1 -> "ff"/-1 -\&gt; "ff"/' -i src/java/net/sourceforge/jpcap/util/HexHelper.java

find . -type d -name CVS | xargs %{__rm} -r
%{__rm} lib/libjpcap.so

%build
MAKE_HOME=`pwd`/make
CLASSPATH=`pwd`/src/java:`pwd`/thirdParty/jars/junit.jar:`pwd`/thirdParty/jars/fooware_CommandLine-1.0.jar:`pwd`/thirdParty/jars/dev-classes_net.ultrametrics-0.03.jar
OSTYPE=linux
export OSTYPE MAKE_HOME CLASSPATH
%{__make} clean
%{__make} -j1

export RELEASE_HOME=`pwd`
%{__make} -C src/java/net/sourceforge/jpcap -j1 release

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

MAKE_HOME=`pwd`/make
RELEASE_HOME=`pwd`
export RELEASE_HOME MAKE_HOME
%{__make} setup_pkgroot \
	PKG_ROOT=$RPM_BUILD_ROOT%{_prefix}

[ "%{_lib}" != 'lib' ] && %{__mv} $RPM_BUILD_ROOT{%{_prefix}/lib/libjpcap.so,%{_libdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README docs/{ethernet,html,images,CREDITS,FAQ,PROJECTS,RELEASE_NOTES}
# src/java/net/sourceforge/jpcap/{tutorial,README}
%attr(755,root,root) %{_bindir}/jpcap
%attr(755,root,root) %{_libdir}/libjpcap.so
%{_exec_prefix}/lib/%{name}-%{version}
