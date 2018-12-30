# tensorflow
version = 1.12.0
release = 1
name = tensorflow
full_name = $(name)-$(version)
download_url = "https://github.com/tensorflow/$(name)/archive/v$(version).tar.gz"

all: rpm

clean:
	rm -rf rpmbuild

mkdir: clean
	mkdir -p rpmbuild
	mkdir -p rpmbuild/BUILD
	mkdir -p rpmbuild/BUILDROOT
	mkdir -p rpmbuild/RPMS
	mkdir -p rpmbuild/SOURCES
	mkdir -p rpmbuild/SRPMS

download: mkdir
	curl -L -o rpmbuild/SOURCES/$(full_name).tar.gz $(download_url); 
	
rpm: download
	rpmbuild $(RPM_OPTS) \
	  --define "_topdir %(pwd)" \
	  --define "_builddir %{_topdir}/rpmbuild/BUILD" \
	  --define "_buildrootdir %{_topdir}/rpmbuild/BUILDROOT" \
	  --define "_rpmdir %{_topdir}/rpmbuild/RPMS" \
	  --define "_srcrpmdir %{_topdir}/rpmbuild/SRPMS" \
	  --define "_specdir %{_topdir}" \
	  --define "_sourcedir %{_topdir}/rpmbuild/SOURCES" \
	  --define "VERSION $(version)" \
 	  --define "RELEASE $(release)" \
	  -ba tensorflow.spec