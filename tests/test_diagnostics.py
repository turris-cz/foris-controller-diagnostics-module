#
# foris-controller
# Copyright (C) 2017 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
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

import time

from .fixtures import backend, clear_diagnostics, infrastructure, ubusd_test


def test_diagnostics_list_modules(infrastructure, ubusd_test, clear_diagnostics):
    res = infrastructure.process_message({
        "module": "diagnostics",
        "action": "list_modules",
        "kind": "request",
    })
    assert res["data"].keys() == [
        u"modules",
    ]


def test_diagnostics_list_diagnostics(infrastructure, ubusd_test, clear_diagnostics):
    res = infrastructure.process_message({
        "module": "diagnostics",
        "action": "list_diagnostics",
        "kind": "request",
    })
    assert isinstance(res["data"]["diagnostics"], list)


def test_diagnostics_prepare_diagnostic(infrastructure, ubusd_test, clear_diagnostics):
    modules = ["processes"]
    res = infrastructure.process_message({
        "module": "diagnostics",
        "action": "prepare_diagnostic",
        "kind": "request",
        "data": {"modules": modules},
    })
    assert "diag_id" in res["data"]


def test_diagnostics_remove_diagnostic(infrastructure, ubusd_test, clear_diagnostics):
    diag_id = "non-existing"
    res = infrastructure.process_message({
        "module": "diagnostics",
        "action": "remove_diagnostic",
        "kind": "request",
        "data": {"diag_id": diag_id},
    })
    assert res["data"] == {"result": False, "diag_id": diag_id}


def test_diagnostics_complex(infrastructure, ubusd_test, clear_diagnostics):
    length = len(infrastructure.process_message({
        "module": "diagnostics",
        "action": "list_diagnostics",
        "kind": "request",
    })["data"]["diagnostics"])
    # add a diagnostic
    modules = ["processes"]
    res = infrastructure.process_message({
        "module": "diagnostics",
        "action": "prepare_diagnostic",
        "kind": "request",
        "data": {"modules": modules},
    })
    diag_id = res["data"]["diag_id"]

    time.sleep(0.1)
    # check lenght
    new_length = len(infrastructure.process_message({
        "module": "diagnostics",
        "action": "list_diagnostics",
        "kind": "request",
    })["data"]["diagnostics"])
    assert new_length == length + 1

    # remove diagnostic
    res = infrastructure.process_message({
        "module": "diagnostics",
        "action": "remove_diagnostic",
        "kind": "request",
        "data": {"diag_id": diag_id},
    })
    assert res["data"]["result"]

    time.sleep(0.1)
    # check lenght
    new_length = len(infrastructure.process_message({
        "module": "diagnostics",
        "action": "list_diagnostics",
        "kind": "request",
    })["data"]["diagnostics"])
    assert new_length == length
