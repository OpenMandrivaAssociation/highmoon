%define	name	highmoon
%define	version	1.2.4
%define	release	%mkrel	1
%define	Summary	Artillery/Worms-like Game in Open Space

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
Source0:	http://highmoon.gerdsmeier.net/%{name}-%{version}.tar.gz
Patch1:		highmoon-1.2.3-mdkconf.patch.bz2
URL:		http://highmoon.gerdsmeier.net/
Group:		Games/Strategy
License:	GPL
BuildRequires:	SDL-devel SDL_image-devel ImageMagick
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
HighMoon is an Artillery/Worms-like duel game in which two spaceships fight
each other in open space. All shots are deflected by the gravitation of
planets and moons, so be careful not to destroy your own UFO.

%prep
%setup -q -n HighMoon
%patch1 -b .mdkconf
find -type f| xargs chmod 644

%build
%make	OPTFLAGS="$RPM_OPT_FLAGS -O3" \
	INSTALLPATH="%{_gamesdatadir}/%{name}" \
	INSTALLBIN="%{_gamesbindir}"

%install
rm -rf $RPM_BUILD_ROOT
make	INSTALLPATH="$RPM_BUILD_ROOT%{_gamesdatadir}/%{name}" \
	INSTALLBIN="$RPM_BUILD_ROOT%{_gamesbindir}" \
	install

cat<<EOF > $RPM_BUILD_ROOT%{_gamesbindir}/highmoon
#!/bin/sh
cd %{_gamesdatadir}/%{name}
./ufo \$@
EOF
chmod 755 $RPM_BUILD_ROOT%{_gamesbindir}/highmoon

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Categories=Game;StrategyGame;
Name=HighMoon
Comment=%{Summary}
EOF

install -d $RPM_BUILD_ROOT{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert -size 16x16 icon.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
convert -size 32x32 icon.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -size 48x48 icon.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%defattr(-,root,root)
%{_gamesbindir}/highmoon
%dir %{_gamesdatadir}/highmoon
%dir %{_gamesdatadir}/highmoon/gfx
%{_gamesdatadir}/highmoon/gfx/*
%dir %{_gamesdatadir}/highmoon/snd
%{_gamesdatadir}/highmoon/snd/*
%{_gamesdatadir}/highmoon/ufo
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

