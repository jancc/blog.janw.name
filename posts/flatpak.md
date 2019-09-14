I've switched to using [Flatpak](https://www.flatpak.org) on my desktop Linux
computers. Here's why I've made that switch and how I made it work on an Arch
install with an i3-based desktop.

===ENDPREVIEW===

Flatpak is IMHO the way to go for desktop applications in Linux. In a perfect
world we could just always compile everything from source and fit it snuggily
into the base-system. But that ship has long sailed. Somewhere between
dependency hell and software only shipping in binary form, there need to be a
solution to all these problems.

Several projects have tried tackling that. Canonical's
[Snaps](https://snapcraft.io) or [AppImages](https://appimage.org) come to
mind. Snaps contain a full base system for each application. Thus each
installation needs to carry the weight of a full userland. This wastes a lot of
space. AppImages are slighly more lenitent. They just give you a way of putting
your necessary libraries into the package, while still relying on certain
functionality from the main system.

There is also the thing that Valve's Steam does, where they simply ship an
outdated Ubuntu userland and have everyone target that.

Flatpak combines these approaches. Applications still use a seperate userland
from the main system, but there is the concept of _runtimes_. If an application
needs functionality provided by KDE, it can use a KDE-based runtime. If,
however, another application also needs this base system, the runtimes needs
only be present once. Effectively this solves the immense space bloat problem
posed by Snaps. It also solves a security problem, because runtimes can be
updated independently from the programs. Thus outdated, flawed libraries can
be patched. Provided they are still compatible with their previous version.

This is why I wanted to make use of Flatpak on my desktop system. It is based
on Arch Linux and I use a simple i3 based desktop.

In fact, installing Flatpak itself is not hard. There is the
[flatpak](https://www.archlinux.org/packages/?name=flatpak) package available
in the "Extra" repository of Arch. The `flatpak` commandline tool is enough to
manage the installations of flatpak based programs. Though, without a
pre-configured DE, this is only half of the way.

You'll need to tell your environment about the presence of Flatpak. This is
done by extending the value of the `XDG_DATA_DIRS` environment variable. In my
`~/.xinitrc` file I added the following line:

    export XDG_DATA_DIRS="/usr/share:/usr/local/share:$HOME/.local/share/applications:/var/lib/flatpak/exports/share:$HOME/.local/share/flatpak/exports/share"

Now, when starting X, it knows about Flatpak's data directory.

Flatpak applications are not placed in the regular PATH. They are expected to
be run using some sort of start-menu. So using plain old `dmenu_run` is out of
the question. Luckily there exists a project called
[j4-dmenu-desktop](https://github.com/enkore/j4-dmenu-desktop). It implements
a dmenu based application launcher that actually parses the `.desktop` files
provided by FreeDesktop compliant programs.

Replace the call of `dmenu_run` with a call to `j4-dmenu-desktop` in your i3
config. In my setup the line looks like this:

    bindsym Mod4+d exec j4-dmenu-desktop --term="urxvt" --no-generic

I'd highly recommend adding the `--no-generic` option. Otherwise the launcher
would use generic application names such as "Web Browser". This is especially
annoying if you have multiple browsers installed :)

And now you're good to go to use Flatpak in a minimal WM-based setup! It does
not need to be i3 of course, but the general steps are similar.
