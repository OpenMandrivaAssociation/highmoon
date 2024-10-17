%define	name	highmoon
%define	version	1.2.4
%define release	5
%define	Summary	Artillery/Worms-like Game in Open Space

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{Summary}
Source0:	http://highmoon.gerdsmeier.net/%{name}-%{version}.tar.gz
Patch1:		highmoon-1.2.3-mdkconf.patch.bz2
URL:		https://highmoon.gerdsmeier.net/
Group:		Games/Arcade
License:	GPLv2
BuildRequires:	SDL-devel SDL_image-devel imagemagick
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
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
Name=HighMoon
Comment=%{Summary}
EOF

install -d $RPM_BUILD_ROOT{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert -size 16x16 icon.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
convert -size 32x32 icon.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -size 48x48 icon.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

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



%changelog
* Wed May 13 2009 Jérôme Brenier <incubusss@mandriva.org> 1.2.4-4mdv2010.0
+ Revision: 375064
- group/menu category fixed (#49515)
- license fixed (GPLv2)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.2.4-3mdv2009.0
+ Revision: 246860
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Jan 03 2008 Thierry Vignaud <tv@mandriva.org> 1.2.4-1mdv2008.1
+ Revision: 141863
- auto-convert XDG menu entry
- kill re-definition of %%buildroot on Pixel's request
- import highmoon

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Jérôme Soyer <saispo@mandriva.org>
    - New release


* Thu Feb 16 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.3-1mdk
- initial release based on suse package
