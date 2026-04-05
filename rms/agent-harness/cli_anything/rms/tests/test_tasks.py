"""Unit tests for tasks core module and CLI commands."""
from __future__ import annotations

import json
import os
from unittest.mock import patch

import pytest


# ── Core module tests ─────────────────────────────────────────────────


class TestTasksCore:
    """Tests for cli_anything.rms.core.tasks functions."""

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_tasks(self, mock_get):
        from cli_anything.rms.core.tasks import list_tasks

        mock_get.return_value = {"success": True, "data": [{"id": 1, "status": "completed"}]}
        result = list_tasks("tok")

        assert result["success"] is True
        args, kwargs = mock_get.call_args
        assert args[0] == "/devices/tasks"

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_tasks_with_pagination(self, mock_get):
        from cli_anything.rms.core.tasks import list_tasks

        mock_get.return_value = {"success": True, "data": []}
        list_tasks("tok", limit=10, offset=5)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["limit"] == 10
        assert kwargs["params"]["offset"] == 5

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_get_task(self, mock_get):
        from cli_anything.rms.core.tasks import get_task

        mock_get.return_value = {"success": True, "data": {"id": 42, "type": "firmware_update"}}
        result = get_task("tok", "42")

        assert result["data"]["id"] == 42
        args, _ = mock_get.call_args
        assert args[0] == "/devices/tasks/42"

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_task_logs(self, mock_get):
        from cli_anything.rms.core.tasks import list_task_logs

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        result = list_task_logs("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/tasks/logs"

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_get_task_log(self, mock_get):
        from cli_anything.rms.core.tasks import get_task_log

        mock_get.return_value = {"success": True, "data": {"id": 7, "message": "done"}}
        result = get_task_log("tok", "7")

        assert result["data"]["id"] == 7
        args, _ = mock_get.call_args
        assert args[0] == "/devices/tasks/logs/7"

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_task_groups(self, mock_get):
        from cli_anything.rms.core.tasks import list_task_groups

        mock_get.return_value = {"success": True, "data": [{"id": 1, "name": "batch1"}]}
        result = list_task_groups("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/tasks/groups"

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_get_task_group(self, mock_get):
        from cli_anything.rms.core.tasks import get_task_group

        mock_get.return_value = {"success": True, "data": {"id": 3}}
        result = get_task_group("tok", "3")

        assert result["data"]["id"] == 3
        args, _ = mock_get.call_args
        assert args[0] == "/devices/tasks/groups/3"

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_task_group_logs(self, mock_get):
        from cli_anything.rms.core.tasks import list_task_group_logs

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        result = list_task_group_logs("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/tasks/groups/logs"

    # ── Firmware updates ──

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_updates_pending(self, mock_get):
        from cli_anything.rms.core.tasks import list_updates_pending

        mock_get.return_value = {"success": True, "data": [{"device_id": 100}]}
        result = list_updates_pending("tok")

        assert result["success"] is True
        args, _ = mock_get.call_args
        assert args[0] == "/devices/updates/pending"

    @patch("cli_anything.rms.core.tasks.api_put")
    def test_set_updates(self, mock_put):
        from cli_anything.rms.core.tasks import set_updates

        mock_put.return_value = {"success": True}
        payload = {"devices": [100], "version": "7.6.10"}
        result = set_updates("tok", payload)

        assert result["success"] is True
        args, kwargs = mock_put.call_args
        assert args[0] == "/devices/updates/set"
        assert kwargs["data"] == payload

    @patch("cli_anything.rms.core.tasks.api_put")
    def test_cancel_updates(self, mock_put):
        from cli_anything.rms.core.tasks import cancel_updates

        mock_put.return_value = {"success": True}
        payload = {"devices": [100]}
        result = cancel_updates("tok", payload)

        assert result["success"] is True
        args, kwargs = mock_put.call_args
        assert args[0] == "/devices/updates/cancel"
        assert kwargs["data"] == payload

    # ── Device actions ──

    @patch("cli_anything.rms.core.tasks.api_post")
    def test_execute_action(self, mock_post):
        from cli_anything.rms.core.tasks import execute_action

        mock_post.return_value = {"success": True}
        payload = {"devices": [100], "action": "reboot"}
        result = execute_action("tok", payload)

        assert result["success"] is True
        args, kwargs = mock_post.call_args
        assert args[0] == "/devices/actions"
        assert kwargs["data"] == payload

    @patch("cli_anything.rms.core.tasks.api_post")
    def test_cancel_actions(self, mock_post):
        from cli_anything.rms.core.tasks import cancel_actions

        mock_post.return_value = {"success": True}
        payload = {"ids": [1, 2]}
        result = cancel_actions("tok", payload)

        assert result["success"] is True
        args, kwargs = mock_post.call_args
        assert args[0] == "/devices/actions/cancel"
        assert kwargs["data"] == payload

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_action_logs_by_device(self, mock_get):
        from cli_anything.rms.core.tasks import list_action_logs

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        result = list_action_logs("tok", device_id=2403606)

        assert result["success"] is True
        _, kwargs = mock_get.call_args
        assert kwargs["params"]["device_id"] == 2403606

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_list_action_logs_by_tag(self, mock_get):
        from cli_anything.rms.core.tasks import list_action_logs

        mock_get.return_value = {"success": True, "data": []}
        list_action_logs("tok", tag_id=5)

        _, kwargs = mock_get.call_args
        assert kwargs["params"]["tag_id"] == 5


# ── Commands core tests ──────────────────────────────────────────────


class TestCommandsCore:
    """Tests for cli_anything.rms.core.commands functions."""

    @patch("cli_anything.rms.core.commands.api_post")
    def test_execute_command(self, mock_post):
        from cli_anything.rms.core.commands import execute_command

        mock_post.return_value = {"success": True, "data": {"task_id": 99}}
        cmd_data = {"command": "reboot"}
        result = execute_command("tok", "2403606", cmd_data)

        assert result["success"] is True
        args, kwargs = mock_post.call_args
        assert args[0] == "/devices/2403606/command"
        assert kwargs["data"] == cmd_data


# ── CLI runner tests ──────────────────────────────────────────────────


class TestTasksCLI:
    """Click CliRunner tests for tasks commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_tasks_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["tasks", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "get" in result.output
        assert "logs" in result.output

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_tasks_list_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "tasks", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_tasks_get_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": {"id": 42}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "tasks", "get", "42"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["data"]["id"] == 42

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_tasks_logs_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "tasks", "logs"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_tasks_groups_list_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "tasks", "groups", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_tasks_updates_pending_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": []}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, ["--json", "tasks", "updates-pending"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    @patch("cli_anything.rms.core.tasks.api_get")
    def test_tasks_actions_logs_json(self, mock_get):
        from cli_anything.rms.rms_cli import cli

        mock_get.return_value = {"success": True, "data": [{"id": 1}]}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "tasks", "actions-logs",
                "--device-id", "2403606",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True


class TestCommandsCLI:
    """Click CliRunner tests for commands."""

    def setup_method(self):
        from click.testing import CliRunner
        self.runner = CliRunner()

    def test_commands_help(self):
        from cli_anything.rms.rms_cli import cli

        result = self.runner.invoke(cli, ["commands", "--help"])
        assert result.exit_code == 0
        assert "execute" in result.output

    @patch("cli_anything.rms.core.commands.api_post")
    def test_commands_execute_json(self, mock_post):
        from cli_anything.rms.rms_cli import cli

        mock_post.return_value = {"success": True, "data": {"task_id": 99}}
        with patch.dict(os.environ, {"RMS_API_TOKEN": "test-token"}):
            result = self.runner.invoke(cli, [
                "--json", "commands", "execute", "2403606",
                "--command", '{"command": "reboot"}',
                "--confirm",
            ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
