Name:           tensorflow
Version:	%{VERSION}
Release:        %{RELEASE}%{?dist}
Summary:        An Open Source Machine Learning Framework for Everyone 
License:        Apache 2
Group:          Development/Libraries/C and C++
Url:            https://www.tensorflow.org/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  patch
BuildRequires:  python36

%description
TensorFlow is an open source software library for numerical computation using data flow graphs.

%package devel
Summary:    Development headers and library for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers for %{name}.

%prep
%setup -n %{name}-%{version}
cp %{_topdir}/.tf_configure.bazelrc %{_builddir}/tensorflow-%{version}

%build
bazel clean
bazel build --config=opt --define framework_shared_object=false //tensorflow:libtensorflow.so
bazel build --config=opt --define framework_shared_object=false //tensorflow:libtensorflow_cc.so

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/lib64
rm -f bazel-bin/tensorflow/*.params
cp -P bazel-bin/tensorflow/*.so* $RPM_BUILD_ROOT/usr/lib64

mkdir -p $RPM_BUILD_ROOT%{_includedir}/tensorflow

cp -r tensorflow/c $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r tensorflow/cc $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r tensorflow/core $RPM_BUILD_ROOT%{_includedir}/tensorflow

cp -r bazel-genfiles/tensorflow/c $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r bazel-genfiles/tensorflow/cc $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r bazel-genfiles/tensorflow/core $RPM_BUILD_ROOT%{_includedir}/tensorflow

find $RPM_BUILD_ROOT%{_includedir}/tensorflow -type f ! -name "*.h" -delete

tar -zxvf %{_topdir}/third_party.%{name}-%{version}.tar.gz --directory $RPM_BUILD_ROOT%{_includedir}/tensorflow/

%clean
rm -rf $RPM_BUILD_ROOT

%post
ldconfig

%postun
ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md AUTHORS ACKNOWLEDGMENTS
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/tensorflow/*
%{_libdir}/lib*.so

%changelog
