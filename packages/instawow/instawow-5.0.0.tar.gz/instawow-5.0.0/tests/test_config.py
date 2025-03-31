from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import cattrs
import pytest

from instawow.config import GlobalConfig, ProfileConfig, UninitialisedConfigError
from instawow.wow_installations import Flavour


def test_env_vars_always_take_precedence(
    monkeypatch: pytest.MonkeyPatch,
    iw_global_config_values: dict[str, Any],
    iw_profile_config_values: dict[str, Any],
):
    monkeypatch.setenv('INSTAWOW_AUTO_UPDATE_CHECK', '1')
    monkeypatch.setenv('INSTAWOW_GAME_FLAVOUR', 'classic')

    global_config = GlobalConfig.from_values(
        {**iw_global_config_values, 'auto_update_check': False}, env=True
    )
    profile_config = ProfileConfig.from_values(
        {'global_config': global_config, **iw_profile_config_values, 'game_flavour': 'retail'},
        env=True,
    )
    assert global_config.auto_update_check is True
    assert profile_config.game_flavour is Flavour.Classic


def test_read_profile_from_nonexistent_config_dir_raises(
    iw_global_config_values: dict[str, Any],
):
    global_config = GlobalConfig(config_dir=iw_global_config_values['config_dir'])
    with pytest.raises(UninitialisedConfigError):
        ProfileConfig.read(global_config, '__default__')


def test_init_with_nonexistent_addon_dir_raises(
    iw_global_config_values: dict[str, Any],
    iw_profile_config_values: dict[str, Any],
):
    global_config = GlobalConfig.from_values(iw_global_config_values).write()

    values = dict(iw_profile_config_values)
    del values['_installation_dir']

    with pytest.raises(ValueError, match='not a writable directory'):
        ProfileConfig(**{**values, 'global_config': global_config, 'addon_dir': '#@$foo'})


def test_default_config_dir(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.delenv('XDG_CONFIG_HOME', False)

    with monkeypatch.context() as patcher:
        patcher.setattr(sys, 'platform', 'linux')

        config_dir = GlobalConfig().config_dir
        assert config_dir == Path.home() / '.config/instawow'

        patcher.setenv('XDG_CONFIG_HOME', '/foo')
        config_dir = GlobalConfig().config_dir
        assert config_dir == Path('/foo/instawow').resolve()

    with monkeypatch.context() as patcher:
        patcher.setattr(sys, 'platform', 'darwin')

        config_dir = GlobalConfig().config_dir
        assert config_dir == Path.home() / 'Library/Application Support/instawow'

    with monkeypatch.context() as patcher:
        patcher.setattr(sys, 'platform', 'win32')

        patcher.delenv('APPDATA', False)
        assert GlobalConfig().config_dir == Path.home() / '.config' / 'instawow'

        patcher.setenv('APPDATA', '/foo')
        assert GlobalConfig().config_dir == Path('/foo/instawow').resolve()


def test_config_dir_xdg_env_var_is_respected_on_all_plats(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    config_parent_dir = tmp_path / 'instawow_config_parent_dir'
    monkeypatch.setenv('XDG_CONFIG_HOME', str(config_parent_dir))
    global_config = GlobalConfig()
    assert global_config.config_dir == config_parent_dir / 'instawow'


def test_config_dir_instawow_specific_env_var_takes_precedence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    test_config_dir_xdg_env_var_is_respected_on_all_plats(monkeypatch, tmp_path)

    config_dir = tmp_path / 'instawow_config_dir'
    monkeypatch.setenv('INSTAWOW_CONFIG_DIR', str(config_dir))
    global_config = GlobalConfig.from_values(env=True)
    assert global_config.config_dir == config_dir


def test_default_state_dir(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.delenv('XDG_STATE_HOME', False)

    with monkeypatch.context() as patcher:
        patcher.setattr(sys, 'platform', 'linux')

        assert GlobalConfig().state_dir == Path.home() / '.local' / 'state' / 'instawow'

    for platform in {'darwin', 'win32'}:
        with monkeypatch.context() as patcher:
            patcher.setattr(sys, 'platform', platform)

            global_config = GlobalConfig()
            assert global_config.config_dir == global_config.state_dir


def test_state_dir_xdg_env_var_is_respected_on_all_plats(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    state_parent_dir = tmp_path / 'instawow_state_parent_dir'
    monkeypatch.setenv('XDG_STATE_HOME', str(state_parent_dir))
    global_config = GlobalConfig()
    assert global_config.state_dir == state_parent_dir / 'instawow'


def test_state_dir_instawow_specific_env_var_takes_precedence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    test_state_dir_xdg_env_var_is_respected_on_all_plats(monkeypatch, tmp_path)

    state_dir = tmp_path / 'instawow_state_dir'
    monkeypatch.setenv('INSTAWOW_STATE_DIR', str(state_dir))
    global_config = GlobalConfig.from_values(env=True)
    assert global_config.state_dir == state_dir


def test_access_tokens_file_takes_precedence():
    global_config = GlobalConfig.read().write()
    assert global_config.access_tokens.cfcore is None
    global_config.config_dir.joinpath('config.access_tokens.json').write_text(
        json.dumps({'cfcore': 'abc'})
    )
    assert GlobalConfig.read().access_tokens.cfcore == 'abc'


def test_can_list_profiles(
    iw_profile_config_values: dict[str, Any],
):
    global_config = GlobalConfig.read()
    assert set(global_config.iter_profiles()) == set()

    ProfileConfig.from_values({'global_config': global_config, **iw_profile_config_values}).write()
    ProfileConfig.from_values(
        {'global_config': global_config, **iw_profile_config_values, 'profile': 'foo'}, env=False
    ).write()
    assert set(global_config.iter_profiles()) == {'__default__', 'foo'}


def test_can_list_installations(
    iw_profile_config_values: dict[str, Any],
):
    global_config = GlobalConfig.read()
    assert set(global_config.iter_installations()) == set()

    ProfileConfig.from_values({'global_config': global_config, **iw_profile_config_values}).write()
    assert set(global_config.iter_installations()) == {
        iw_profile_config_values['_installation_dir']
    }


def test_profile_dirs_are_populated(
    iw_global_config_values: dict[str, Any],
    iw_profile_config_values: dict[str, Any],
):
    global_config = GlobalConfig.from_values(iw_global_config_values)
    profile_config = ProfileConfig.from_values(
        {'global_config': global_config, **iw_profile_config_values}
    ).write()
    assert {i.name for i in profile_config.config_dir.iterdir()} <= {'config.json'}
    assert {i.name for i in profile_config.state_dir.iterdir()} <= {'logs', 'plugins'}


def test_can_delete_profile(
    iw_global_config_values: dict[str, Any],
    iw_profile_config_values: dict[str, Any],
):
    global_config = GlobalConfig.from_values(iw_global_config_values).write()
    profile_config = ProfileConfig.from_values(
        {'global_config': global_config, **iw_profile_config_values}
    ).write()
    assert profile_config.config_dir.exists()
    profile_config.delete()
    assert not profile_config.config_dir.exists()


def test_validate_profile_name(
    iw_global_config_values: dict[str, Any],
    iw_profile_config_values: dict[str, Any],
):
    global_config = GlobalConfig.from_values(iw_global_config_values)

    with pytest.raises(cattrs.ClassValidationError) as exc_info:
        ProfileConfig.from_values(
            {'global_config': global_config, **iw_profile_config_values, 'profile': ''}
        )

    (value_error,) = exc_info.value.exceptions
    assert value_error.args == ('Value must have a minimum length of 1',)

    (note,) = value_error.__notes__
    assert note == 'Structuring class ProfileConfig @ attribute profile'
    assert type(note) is cattrs.AttributeValidationNote
    assert note.name == 'profile'


@pytest.mark.skipif(
    sys.platform == 'win32',
    reason='chmod has no effect on Windows',
)
def test_validate_addon_dir(
    tmp_path: Path,
    iw_global_config_values: dict[str, Any],
    iw_profile_config_values: dict[str, Any],
):
    global_config = GlobalConfig.from_values(iw_global_config_values)

    non_writeable_dir = tmp_path / 'non-writeable-dir'
    non_writeable_dir.mkdir(0o400)

    with pytest.raises(cattrs.ClassValidationError) as exc_info:
        ProfileConfig.from_values(
            {
                'global_config': global_config,
                **iw_profile_config_values,
                'addon_dir': non_writeable_dir,
            }
        )

    (value_error,) = exc_info.value.exceptions
    assert value_error.args == (f'"{non_writeable_dir}" is not a writable directory',)

    (note,) = value_error.__notes__
    assert note == 'Structuring class ProfileConfig @ attribute addon_dir'
    assert type(note) is cattrs.AttributeValidationNote
    assert note.name == 'addon_dir'
