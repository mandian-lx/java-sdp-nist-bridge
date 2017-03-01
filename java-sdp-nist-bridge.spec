%{?_javapackages_macros:%_javapackages_macros}

Summary:	An SdpFactory binding the free OpenTelecoms javax.sdp API
Name:		java-sdp-nist-bridge
Version:	1.2
Release:	1
License:	ASL 2.0
Group:		Development/Java
Url:		http://opentelecoms.org/
Source0:	https://github.com/opentelecoms-org/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:	mvn(org.jitsi:jain-sip-ri-ossonly)
BuildRequires:	mvn(org.opentelecoms.sdp:sdp-api)

%description
# from the hompage
This little project provides a free, Apache 2.0 licensed, implementation
of the JSR 141 SdpFactory interface against NIST's public domain reference
implementation of the JSR 141 classes and interfaces.

The entire javax.sdp package, including the SdpFactory class of the NIST RI
cannot be used because:

  * it has a non-free, non-OSI approved, expired, proprietary license
  * the interface references the implementation and vice-versa

%files -f .mfiles
%doc README.md
%doc LICENSE

#----------------------------------------------------------------------------

%package		javadoc
Summary:		Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build

%install
%mvn_install

