Summary:	Generating Rust FFI bindings to C (and some C++) libraries
Summary(pl.UTF-8):	Generowanie wiązań Rust FFI do bibliotek C (i niektórych C++)
Name:		rust-bindgen
Version:	0.73.2
Release:	1
License:	BSD
Group:		Development/Tools
Source0:	https://github.com/rust-lang/rust-bindgen/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	baefc3f7d25a22d9b6b9113a2db39649
# cd rust-bindgen-%{version}
# cargo vendor
# cd ..
# tar cJf rust-bindgen-crates-%{version}.tar.xz cbindgen-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-crates-%{version}.tar.xz
# Source1-md5:	551679a7e17f02ed3287ab07ac52b3e2
URL:		https://rust-lang.github.io/rust-bindgen/
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.71.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
# dynamically loaded
Requires:	clang-libs
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bindgen automatically generates Rust FFI bindings to C (and some C++)
libraries.

%description -l pl.UTF-8
bindgen automatycznie generuje wiązania Rust FFI do bibliotek C (i
niektórych C++).

%prep
%setup -q -a1

%{__mv} %{name}-%{version}/* .

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD/bindgen-cli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTING.md README.md
%attr(755,root,root) %{_bindir}/bindgen
