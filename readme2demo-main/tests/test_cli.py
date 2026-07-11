"""Tests for CLI input resolution: repo is optional, -gr flag, guide-only runs.

Pure — no typer runtime, no docker, no network. Exercises the ``_resolve_repo``
helper that reconciles the positional repo, ``-gr/--github-repo``, and the
``-s/--step-by-step`` guide.
"""

from pathlib import Path


import typer

from readme2demo.cli import _resolve_repo
from typer.testing import CliRunner
from readme2demo.cli import app

_URL = "https://github.com/owner/repo"

from typer.testing import CliRunner
from readme2demo.cli import app  # Ή όπως ονομάζεται το Typer app σου

runner = CliRunner()

runner = CliRunner()

def test_positional_repo_only() -> None:
    assert _resolve_repo(_URL, None, None) == _URL


def test_gr_flag_only() -> None:
    assert _resolve_repo(None, _URL, None) == _URL


def test_both_spellings_agree() -> None:
    assert _resolve_repo(_URL, _URL, None) == _URL


def test_conflicting_repo_spellings_raise() -> None:
    with pytest.raises(typer.BadParameter):
        _resolve_repo(_URL, "https://github.com/other/repo", None)


def test_guide_only_returns_none() -> None:
    # No repo, guide supplied -> guide-only run.
    assert _resolve_repo(None, None, Path("guide.md")) is None


def test_neither_repo_nor_guide_raises() -> None:
    with pytest.raises(typer.BadParameter):
        _resolve_repo(None, None, None)


def test_repo_and_guide_both_returns_repo() -> None:
    # "both" case: the repo is returned; the guide flows through cfg.step_by_step
    # separately, so both are taken into account downstream.
    assert _resolve_repo(_URL, None, Path("g.md")) == _URL
    assert _resolve_repo(None, _URL, Path("g.md")) == _URL


def test_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip() != ""

def test_report_json_output():
    # 1. Αν η εντολή χρειάζεται mock δεδομένα ή κάποιο υπαρκτό run_dir, 
    # θα πρέπει να το προετοιμάσεις εδώ (π.χ. δημιουργώντας ένα temp directory).
    
    # 2. Εκτέλεση της εντολής μέσω του CliRunner
    result = runner.invoke(app, ["report", "path/to/run_dir", "--json"])
    
    # 3. Επαλήθευση (Assertions)
    assert result.exit_code == 0  # Επιβεβαιώνεις ότι βγαίνει με exit code 0
    assert "stages" in result.stdout  # Επιβεβαιώνεις ότι το output περιέχει JSON data