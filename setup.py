#!/usr/bin/env python

#
# foris-controller-diagnostics-module
# Copyright (C) 2017-2020 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#

from setuptools import setup

from foris_controller_diagnostics_module import __version__

DESCRIPTION = """
Diagnostics module for foris-controller (wrapper around diagnostics cmd)
"""

setup(
    name="foris-controller-diagnostics-module",
    version=__version__,
    author="CZ.NIC, z.s.p.o. (http://www.nic.cz/)",
    author_email="packaging@turris.cz",
    packages=[
        "foris_controller_diagnostics_module",
        "foris_controller_backends",
        "foris_controller_backends.diagnostics",
        "foris_controller_modules",
        "foris_controller_modules.diagnostics",
        "foris_controller_modules.diagnostics.handlers",
    ],
    package_data={"foris_controller_modules.diagnostics": ["schema", "schema/*.json"]},
    namespace_packages=["foris_controller_modules", "foris_controller_backends"],
    scripts=[],
    url="https://gitlab.nic.cz/turris/foris-controller/foris-controller-diagnostics-module",
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    license="GPLv3",
    install_requires=[
        "foris-controller @ git+https://gitlab.nic.cz/turris/foris-controller/foris-controller.git#egg=foris-controller"
    ],
    setup_requires=[
        "pytest-runner",
        "flake8",
    ],
    tests_require=["pytest", "foris-controller-testtools", "foris-client", "ubus", "paho-mqtt"],
    dependency_links=[
        "git+https://gitlab.nic.cz/turris/foris-controller/foris-controller-testtools.git#egg=foris-controller-testtools",
        "git+https://gitlab.nic.cz/turris/foris-controller/foris-client.git#egg=foris-client",
    ],
    include_package_data=True,
    zip_safe=False,
)
