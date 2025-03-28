.. _install:

Installing poezio
=================

.. warning:: Python 3.11 or above is **required**.
             To install it on a distribution that doesn't provide it, see :ref:`pyenv <pyenv-install>`.

poezio in the GNU/Linux distributions
-------------------------------------

As far as I know, Poezio is available in the following distributions, you just
have to install it by using the package manager of the distribution, if you're
using one of these.

- **Archlinux**: poezio_ and poezio-git_ packages are in the AUR
  (use your favourite AUR wrapper to install them)
- **Gentoo**:  `net-im/poezio`_
- **Fedora**: There is an `up-to-date package`_ in the repos since F19.
- **CentOS**: Poezio is available in EPEL repositories since CentOS 8.
- **Flatpak**: A stable package is provided on flathub_.
- **Debian**: A stable package is provided since buster_ thanks to debacle.
- **Nix** (and **NixOS**): The last stable version of poezio is availalble in
  the unstable branch of `nixpkgs`. Use ``nix-env -f "<nixpkgs>" -iA poezio``
  to install poezio for the current user.
- **OpenBSD**: a poezio port_ is available
- **Guix**: Poezio can be obtained with Guix on any GNU/Linux distribution.
  To install poezio in default user-profile: ``guix install poezio``.
  To try poezio without installation: ``guix environment --pure --ad-hoc poezio``.

(If another distribution provides a poezio package, please tell us and we will
add it to the list)

Thank to all the maintainers who took time to make and maintain those packages!

Install from source
-------------------

Stable version
~~~~~~~~~~~~~~

`Stable version`_ packages are available in standalone (dependencies provided)
and poezio-only packages (both with prebuilt html doc for convenience).

Those versions are also available on pypi_ (using uv, for example), and it is
recommended to install them this way if you absolutely want to **install** poezio
and your distribution provides no package.

Development version
~~~~~~~~~~~~~~~~~~~

The stable versions of poezio are more like snapshots of states of
development we deem acceptable. There is always an incentive to
use the development version, like new features, bug fixes, and more
support. Therefore, you might want to use the git version.

.. code-block:: bash

    git clone https://codeberg.org/poezio/poezio
    cd poezio

General
"""""""

Poezio is a python3.11 (and above)-only application, so you will first need that.

.. note:: If not building a package for a distribution, use of the ``uv`` tool
          is highly recommended.

Packages required for building poezio and deps:

- make
- gcc
- python3-devel (or equivalent)
- python3-setuptools
- (for slixmpp_) maturin and rustc/cargo

Poezio only needs slixmpp_ for its base functionality, and building slixmpp
from source requires the maturin build backend, as well as a rust compiler.

Users
"""""

uv takes care of everything, so building and installing all required packages is
simple as:

.. code-block::

    uv sync --all-groups --all-extras

Then you can just :ref:`run it <poezio-run-label>`.

.. note:: We provide an ``update.sh`` script that creates a virtualenv and
          downloads all the required and optional dependencies inside it.
          we recommend using it with the git version of poezio, in order
          to keep everything up-to-date.

Packagers
"""""""""

As long as you have a slixmpp_ packaged, it should be straightforward to
build a package for poezio using the standard facilities:

.. code-block:: bash

   python3 -m build


.. _poezio-run-label:

Running
~~~~~~~

If you didn’t install poezio, you can run it from the source directory
with:

.. code-block:: bash

    ./launch.sh
    # Or
    uv run poezio

Docker images
-------------

poezio is available on the docker hub in the `poezio/poezio`_ repository
in which ``poezio/poezio:latest`` is the latest built git version, and
stable versions are tagged with their numbers. The image is based off
alpine linux and we tried to keep the image size to a minimum (<100MiB).

You can therefore just fetch the images with docker pull:

.. code-block:: bash

    docker pull poezio/poezio

In order to run poezio with non-temporary config and logs, and to have
the right colors, you have to share the ``TERM`` env var and some directories
that should be created beforehand:

.. code-block:: bash

    mkdir -p ~/.config/poezio ~/.local/share/poezio
    docker run -it -e TERM -v ~/.config/poezio:/home/poezio-user/.config/poezio -v ~/.local/share/poezio:/home/poezio-user/.local/share/poezio poezio/poezio


If you don’t trust images distributed on the docker hub, you can rebuild the
image from the Dockerfile at the root of the git repository.

.. _slixmpp: https://codeberg.org/poezio/slixmpp
.. _aiodns: https://github.com/saghul/aiodns
.. _poezio: https://aur.archlinux.org/packages/poezio/
.. _poezio-git: https://aur.archlinux.org/packages/poezio-git/
.. _up-to-date package: https://apps.fedoraproject.org/packages/poezio
.. _pypi: https://pypi.python.org/pypi/poezio
.. _cython: http://cython.org
.. _bgo-overlay: https://bgo.zugaina.org/
.. _port: http://ports.su/net/poezio
.. _poezio/poezio: https://hub.docker.com/r/poezio/poezio/
.. _buster: https://packages.debian.org/buster/poezio
.. _net-im/poezio: https://packages.gentoo.org/packages/net-im/poezio
.. _flathub: https://flathub.org/apps/details/io.poez.Poezio
