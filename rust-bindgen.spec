Summary:	Automatically generates Rust FFI bindings to C (and some C++) libraries
Name:		rust-bindgen
Version:	0.68.1
Release:	1
License:	BSD
Group:		Development/Tools
Source0:	https://github.com/rust-lang/rust-bindgen/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	64b5f012317e7152cf13f8ee4fee2555
# cd rust-bindgen-%{version}
# cargo vendor
# cd ..
# tar cJf rust-bindgen-crates-%{version}.tar.xz cbindgen-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-crates-%{version}.tar.xz
# Source1-md5:	a2b65da1bb62eae712eb2d369b1a290b
URL:		https://rust-lang.github.io/rust-bindgen/
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust >= 1.57.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# dynamically loaded
Requires:	clang-libs
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bindgen automatically generates Rust FFI bindings to C (and some C++)
libraries.

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

%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTING.md README.md
%attr(755,root,root) %{_bindir}/bindgen
