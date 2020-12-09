#
# foris-controller-diagnostics-module
# Copyright (C) 2017, 2020 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
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
import pytest
import subprocess

from foris_controller_testtools.fixtures import (
    backend,
    infrastructure,
    uci_configs_init,
    lighttpd_restart_command,
    turris_os_version,
    device,
    cmdline_file,
)

from foris_controller_testtools.utils import lighttpd_restart_was_called


@pytest.fixture(scope="function")
def clear_diagnostics():
    process = subprocess.Popen(["rm", "-rf", "/tmp/diagnostics-*"])
    process.wait()
    yield process


@pytest.mark.parametrize("device,cmdline_file,turris_os_version", [("mox", "mox", "4.0")], indirect=True)
def test_diagnostics_list_modules(
    infrastructure, clear_diagnostics, device, cmdline_file, turris_os_version
):
    res = infrastructure.process_message(
        {"module": "diagnostics", "action": "list_modules", "kind": "request"}
    )
    assert res["data"].keys() == {"modules"}


@pytest.mark.parametrize("device,turris_os_version", [("mox", "4.0")], indirect=True)
def test_diagnostics_list_diagnostics(
    infrastructure, clear_diagnostics, device, turris_os_version
):
    res = infrastructure.process_message(
        {"module": "diagnostics", "action": "list_diagnostics", "kind": "request"}
    )
    assert isinstance(res["data"]["diagnostics"], list)


@pytest.mark.parametrize("device,turris_os_version", [("mox", "4.0")], indirect=True)
def test_diagnostics_prepare_diagnostic(
    infrastructure, clear_diagnostics, device, turris_os_version
):
    modules = ["15_processes"]
    res = infrastructure.process_message(
        {
            "module": "diagnostics",
            "action": "prepare_diagnostic",
            "kind": "request",
            "data": {"modules": modules},
        }
    )
    assert "diag_id" in res["data"]


@pytest.mark.parametrize("device,turris_os_version", [("mox", "4.0")], indirect=True)
def test_diagnostics_remove_diagnostic(
    infrastructure, clear_diagnostics, device, turris_os_version
):
    diag_id = "non-existing"
    res = infrastructure.process_message(
        {
            "module": "diagnostics",
            "action": "remove_diagnostic",
            "kind": "request",
            "data": {"diag_id": diag_id},
        }
    )
    assert "Incorrect input." in res["errors"][0]["description"]

    diag_id = "9999-99-99-99-99-99_ffffffff"
    res = infrastructure.process_message(
        {
            "module": "diagnostics",
            "action": "remove_diagnostic",
            "kind": "request",
            "data": {"diag_id": diag_id},
        }
    )
    assert res["data"] == {"result": False, "diag_id": diag_id}


@pytest.mark.parametrize("device,cmdline_file,turris_os_version", [("mox", "mox", "4.0")], indirect=True)
def test_diagnostics_complex(
    infrastructure, clear_diagnostics, device, cmdline_file, turris_os_version
):
    length = len(
        infrastructure.process_message(
            {"module": "diagnostics", "action": "list_diagnostics", "kind": "request"}
        )["data"]["diagnostics"]
    )
    # add a diagnostic
    modules = ["processes"]
    res = infrastructure.process_message(
        {
            "module": "diagnostics",
            "action": "prepare_diagnostic",
            "kind": "request",
            "data": {"modules": modules},
        }
    )
    diag_id = res["data"]["diag_id"]

    time.sleep(0.1)
    # check lenght
    new_length = len(
        infrastructure.process_message(
            {"module": "diagnostics", "action": "list_diagnostics", "kind": "request"}
        )["data"]["diagnostics"]
    )
    assert new_length == length + 1

    # remove diagnostic
    res = infrastructure.process_message(
        {
            "module": "diagnostics",
            "action": "remove_diagnostic",
            "kind": "request",
            "data": {"diag_id": diag_id},
        }
    )
    assert res["data"]["result"]

    time.sleep(0.1)
    # check lenght
    new_length = len(
        infrastructure.process_message(
            {"module": "diagnostics", "action": "list_diagnostics", "kind": "request"}
        )["data"]["diagnostics"]
    )
    assert new_length == length


@pytest.mark.parametrize("device,turris_os_version", [("mox", "4.0")], indirect=True)
def test_sentry(
    infrastructure,
    uci_configs_init,
    lighttpd_restart_command,
    device,
    turris_os_version,
):
    res = infrastructure.process_message(
        {"module": "diagnostics", "action": "get_sentry", "kind": "request"}
    )
    assert "dsn" in res["data"]

    filters = [("diagnostics", "set_sentry")]

    # successful generation
    notifications = infrastructure.get_notifications(filters=filters)

    # update dsn
    dsn = "https://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY@sentry.labs.nic.cz/40"
    res = infrastructure.process_message(
        {"module": "diagnostics", "action": "set_sentry", "kind": "request", "data": {"dsn": dsn}}
    )
    assert res["data"]["result"]

    notifications = infrastructure.get_notifications(notifications, filters=filters)
    assert notifications[-1] == {
        "module": "diagnostics",
        "action": "set_sentry",
        "kind": "notification",
        "data": {"dsn": dsn},
    }
    if infrastructure.backend_name != "mock":
        assert lighttpd_restart_was_called([])

    res = infrastructure.process_message(
        {"module": "diagnostics", "action": "get_sentry", "kind": "request"}
    )
    assert res["data"]["dsn"] == dsn
