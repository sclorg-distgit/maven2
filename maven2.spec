%global pkg_name maven2
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.2.1
Release:        47.13%{?dist}
Summary:        Java project management and project comprehension tool
License:        ASL 2.0 and MIT and BSD
URL:            http://maven.apache.org
BuildArch:      noarch

# export https://svn.apache.org/repos/asf/maven/maven-2/tags/maven-%{version}/ apache-maven-%{version}
# tar czvf %{pkg_name}-%{version}.tar.gz apache-maven-%{version}
Source0:        %{pkg_name}-%{version}.tar.gz

Patch4:         %{pkg_name}-%{version}-unshade.patch
Patch6:         %{pkg_name}-%{version}-strip-jackrabbit-dep.patch
Patch7:         %{pkg_name}-%{version}-classworlds.patch
Patch8:         %{pkg_name}-%{version}-migrate-to-plexus-containers-container-default.patch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)

%description
Apache Maven is a software project management and comprehension tool. Based on
the concept of a project object model (POM), Maven can manage a project's
build, reporting and documentation from a central piece of information.

%package -n %{?scl_prefix}maven-artifact
Summary:        Compatibility Maven artifact artifact

%description -n %{?scl_prefix}maven-artifact
Maven artifact manager artifact

%package -n %{?scl_prefix}maven-artifact-manager
Summary:        Compatibility Maven artifact manager artifact

%description -n %{?scl_prefix}maven-artifact-manager
Maven artifact manager artifact

%package -n %{?scl_prefix}maven-error-diagnostics
Summary:        Compatibility Maven error diagnostics artifact

%description -n %{?scl_prefix}maven-error-diagnostics
Maven error diagnostics artifact

%package -n %{?scl_prefix}maven-model
Summary:        Compatibility Maven model artifact

%description -n %{?scl_prefix}maven-model
Maven model artifact

%package -n %{?scl_prefix}maven-monitor
Summary:        Compatibility Maven monitor artifact

%description -n %{?scl_prefix}maven-monitor
Maven monitor artifact

%package -n %{?scl_prefix}maven-plugin-registry
Summary:        Compatibility Maven plugin registry artifact

%description -n %{?scl_prefix}maven-plugin-registry
Maven plugin registry artifact

%package -n %{?scl_prefix}maven-profile
Summary:        Compatibility Maven profile artifact

%description -n %{?scl_prefix}maven-profile
Maven profile artifact

%package -n %{?scl_prefix}maven-project
Summary:        Compatibility Maven project artifact

%description -n %{?scl_prefix}maven-project
Maven project artifact

%package -n %{?scl_prefix}maven-settings
Summary:        Compatibility Maven settings artifact

%description -n %{?scl_prefix}maven-settings
Maven settings artifact

%package -n %{?scl_prefix}maven-toolchain
Summary:        Compatibility Maven toolchain artifact

%description -n %{?scl_prefix}maven-toolchain
Maven toolchain artifact

%package -n %{?scl_prefix}maven-plugin-descriptor
Summary:        Maven Plugin Description Model

%description -n %{?scl_prefix}maven-plugin-descriptor
Maven toolchain artifact

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.


%prep
%setup -q -n apache-maven-2.2.1
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

%patch4 -b .unshade

# remove unneeded jackrabbit dependency
%patch6 -p1 -b .strip-jackrabbit-dep

%patch7 -p1 -b .classworlds

%patch8 -p1 -b .plexus-container

for nobuild in apache-maven maven-artifact-test \
               maven-compat maven-core maven-plugin-api \
               maven-plugin-parameter-documenter maven-reporting \
               maven-repository-metadata maven-script; do
    %pom_disable_module $nobuild
done

# Don't depend on backport-util-concurrent
%pom_remove_dep :backport-util-concurrent
%pom_remove_dep :backport-util-concurrent maven-artifact-manager
sed -i s/edu.emory.mathcs.backport.// `find -name DefaultArtifactResolver.java`

# PMD is not useful in RHEL
%pom_remove_plugin :maven-pmd-plugin maven-model

# Do not install parent POM
%mvn_package :maven __noinstall

# Install all artifacts in Maven 3 directory.
%mvn_file :"{*}" maven/@1

# these parts are compatibility versions which are available in
# maven-3.x as well. We default to maven-3, but if someone asks for
# 2.x we provide few compat versions
%mvn_compat_version :"maven-{artifact,model,settings}" 2.0.2 2.0.6 2.0.7 2.0.8 2.2.1
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build -s -f -- -P all-models
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -n %{?scl_prefix}maven-artifact -f .mfiles-maven-artifact
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-artifact-manager -f .mfiles-maven-artifact-manager
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-error-diagnostics -f .mfiles-maven-error-diagnostics
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-model -f .mfiles-maven-model
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-monitor -f .mfiles-maven-monitor
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-plugin-registry -f .mfiles-maven-plugin-registry
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-profile -f .mfiles-maven-profile
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-project -f .mfiles-maven-project
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-settings -f .mfiles-maven-settings
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-toolchain -f .mfiles-maven-toolchain
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files -n %{?scl_prefix}maven-plugin-descriptor -f .mfiles-maven-plugin-descriptor
%dir %{_mavenpomdir}/maven
%dir %{_javadir}/maven
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 2.2.1-47.13
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.2.1-47.12
- maven33 rebuild

* Fri Jan 16 2015 Michal Srb <msrb@redhat.com> - 2.2.1-47.11
- Fix directory ownership

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.10
- Install all POM files except parent POM

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.9
- Fix BR on maven-parent POM

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.2.1-47.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.2.1-47.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.5
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.4
- Rebuild to fix incorrect auto-requires

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.3
- SCL-ize build-requires
- SCL-ize subpackages

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-47.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.2.1-47
- Mass rebuild 2013-12-27

* Tue Oct  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-46
- Migrate from mvn-rpmbuild to %%mvn_build

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 2.2.1-45
- Add missing BR: maven-install-plugin (Resolves: #979504)
- Migrate to plexus-containers-container-default

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-45
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-44
- Don't depend on plexus-container-default
- Unset M2_HOME before calling mvn-rpmbuild
- Remove test dependencies

* Mon Mar 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-43
- Rebuild to generate mvn(*) versioned provides

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-41
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Nov 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-40
- Add license to javadoc subpackage

* Thu Nov 22 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-39
- Add license and notice files to packages
- Add javadoc subpackage

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-38
- Don't depend on backport-util-concurrent

* Mon Aug 20 2012 Michel Salim <salimma@fedoraproject.org> - 2.2.1-37
- Provide compatibility versions for maven-artifact and -settings

* Thu Jul 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-36
- Remove mistaken epoch use in requires

* Wed Jul 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-35
- Move artifacts together with maven-3 files
- Provide compatibility versions for maven-model

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-33
- Completely remove main package since it was just confusing

* Wed Jan 25 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-32
- Stip down maven 2 to bare minimum
- Remove scripts and most of home

* Mon Jan 23 2012 Tomas Radej <tradej@redhat.com> - 2.2.1-31
- Fixed Requires for plugin-descriptor

* Mon Jan 23 2012 Tomas Radej <tradej@redhat.com> - 2.2.1-30
- Moved plugin-descriptor into subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-28
- Provide mvn2 script instead of mvn (maven provides that now)

* Tue Jul 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-27
- Add maven-error-diagnostics subpackage
- Order subpackages according to alphabet

* Tue Jul 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-26
- Unown jars contained in subpackages (#723124)

* Mon Jun 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-25
- Add maven-toolchain subpackage

* Fri Jun 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-24
- Add few new subpackages
- Add several missing requires to new subpackages

* Fri Jun 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-23
- Split artifact-manager and project into subpackages
- Fix resolver to process poms and fragments from datadir
- No more need to update_maven_depmap after this update

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-22
- Fix jpp script to limit maven2.jpp.mode scope

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-20
- Add maven-artifact-test to installation

* Tue Jan 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-19
- Print plugin collector debug output only when maven2.jpp.debug mode is on

* Wed Dec 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-18
- Add xml-commons-apis to lib directory
- fixes NoClassDefFoundError org/w3c/dom/ElementTraversal

* Fri Dec 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-17
- Add conditional BRs to enable ff merge between f14 and f15
- Remove jackrabbit dependency from pom files

* Fri Dec 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-16
- Fix installation of pom files for artifact jars

* Mon Nov 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-15
- Add apache-commons-parent to BR/R
- Rename BRs from jakarta-commons to apache-commons

* Thu Nov 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-14
- Remove old depmaps from -depmap.xml file
- Fix argument quoting for mvn scripts (Resolves rhbz#647945)

* Mon Sep 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-13
- Create dangling symlinks during install (Resolves rhbz#613866)

* Fri Sep 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-12
- Update JPackageRepositoryLayout to handle "signature" packaging

* Mon Sep 13 2010 Yong Yang <yyang@redhat.com> 2.2.1-11
- Add -P all-models to generate maven model v3

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-10
- Remove buildnumber-maven-plugins deps now that is fixed.
- Use new package names in BR/R.
- Use global instead of define.

* Fri Aug 27 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-9
- Remove failing tests after maven-surefire 2.6 update

* Thu Aug 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-8
- Remove incorrect testcase failing with ant 1.8
- Cleanup whitespace

* Tue Jun 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-7
- Updated previous patch to only modify behaviour in JPP mode

* Mon Jun 28 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-6
- Disable parallel artifact resolution

* Wed Jun 23 2010 Yong Yang <yyang@redhat.com> 2.2.1-5
- Add Requires: maven-enforcer-plugin

* Fri Jun 18 2010 Deepak Bhole <dbhole@redhat.com> 2.2.1-4
- Final non-bootstrap build against non-bootstrap maven

* Fri Jun 18 2010 Deepak Bhole <dbhole@redhat.com> 2.2.1-3
- Added buildnumber plugin requirements
- Rebuild in non-bootstrap

* Thu Jun 17 2010 Deepak Bhole <dbhole@redhat.com> - 0:2.2.1-2
- Added support for dumping mapping info (in debug mode)
- Add a custom depmap
- Added empty-dep
- Added proper requirements
- Fixed classworlds jar name used at runtime
- Install individual components
- Install poms and mappings
- Remove non maven items from shaded uber jar
- Create dependency links in $M2_HOME/lib at install time

* Thu Nov 26 2009 Deepak Bhole <dbhole@redhat.com> - 0:2.2.1-1
- Initial bootstrap build
