from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any
from unittest import mock

import prompt_toolkit.application
import prompt_toolkit.input
import prompt_toolkit.output
import pytest
from yarl import URL

import instawow._logging
import instawow.config
import instawow.config_ctx
import instawow.http
import instawow.http_ctx
from instawow.wow_installations import _DELECTABLE_DIR_NAMES, Flavour

from ._fixtures.http import ROUTES, ResponsesMockServer


def pytest_addoption(parser: pytest.Parser):
    parser.addoption('--iw-no-mock-http', action='store_true')


@pytest.fixture(autouse=True)
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def caplog(caplog: pytest.LogCaptureFixture):
    handler_id = instawow._logging.logger.add(
        caplog.handler,
        format='{message}',
        level=0,
        filter=lambda record: record['level'].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    instawow._logging.logger.remove(handler_id)


@pytest.fixture
async def iw_aresponses(
    monkeypatch: pytest.MonkeyPatch,
):
    async with ResponsesMockServer() as server:
        monkeypatch.setattr('aiohttp.TCPConnector', server.tcp_connector_class)
        monkeypatch.setattr('aiohttp.ClientRequest.is_ssl', mock.Mock(return_value=False))
        yield server


@pytest.fixture(params=['foo'])
def iw_global_config_values(request: pytest.FixtureRequest, tmp_path: Path):
    return {
        'config_dir': tmp_path / '__config__',
        'cache_dir': tmp_path / '__cache__',
        'state_dir': tmp_path / '__state__',
        'access_tokens': {
            'cfcore': request.param,
            'github': None,
            'wago_addons': request.param,
        },
    }


@pytest.fixture(params=[Flavour.Retail])
def iw_profile_config_values(request: pytest.FixtureRequest, tmp_path: Path):
    installation_dir = (
        tmp_path
        / '__game__'
        / next(
            (k for k, v in _DELECTABLE_DIR_NAMES.items() if v['flavour'] is request.param),
            '_unknown_',
        )
    )
    addon_dir = installation_dir / 'interface' / 'addons'
    addon_dir.mkdir(parents=True)
    return {
        'profile': '__default__',
        'addon_dir': addon_dir,
        'game_flavour': request.param,
        '_installation_dir': installation_dir,
    }


@pytest.fixture
def iw_global_config(iw_global_config_values: dict[str, Any]):
    return instawow.config.GlobalConfig.from_values(iw_global_config_values).write()


@pytest.fixture
def iw_profile_config(
    iw_profile_config_values: dict[str, Any], iw_global_config: instawow.config.GlobalConfig
):
    return instawow.config.ProfileConfig.from_values(
        {'global_config': iw_global_config, **iw_profile_config_values}
    ).write()


@pytest.fixture(autouse=True)
def _iw_global_config_defaults(
    monkeypatch: pytest.MonkeyPatch,
    iw_global_config_values: dict[str, Any],
):
    for key in ('config_dir', 'cache_dir', 'state_dir'):
        monkeypatch.setenv(f'INSTAWOW_{key.upper()}', str(iw_global_config_values[key]))


@pytest.fixture
async def _iw_config_ctx(iw_profile_config: instawow.config.ProfileConfig):
    @instawow.config_ctx.config.set
    def token():
        return iw_profile_config

    yield
    instawow.config_ctx.config.reset(token)


@pytest.fixture
async def iw_web_client(
    iw_global_config: instawow.config.GlobalConfig,
):
    async with instawow.http.init_web_client(iw_global_config.http_cache_dir) as web_client:
        yield web_client


@pytest.fixture
async def _iw_web_client_ctx(iw_web_client: instawow.http.CachedSession):
    token = instawow.http_ctx.web_client.set(iw_web_client)
    yield
    instawow.http_ctx.web_client.reset(token)


@pytest.fixture(autouse=True, params=['all'])
async def _iw_mock_aiohttp_requests(
    request: pytest.FixtureRequest, iw_aresponses: ResponsesMockServer
):
    if request.config.getoption('--iw-no-mock-http') or any(
        m.name == 'iw_no_mock_http' for m in request.node.iter_markers()
    ):
        await iw_aresponses.__aexit__(*((None,) * 3))
        return

    if request.param == 'all':
        routes = ROUTES.values()
    else:
        urls = set(map(URL, request.param))
        if not urls.issubset(ROUTES.keys()):
            raise ValueError('Supplied routes must be subset of all routes')

        routes = (ROUTES[k] for k in ROUTES.keys() & urls)

    iw_aresponses.add(*routes)


@pytest.fixture(scope='module')
def _iw_mock_pt_progress_bar():
    with pytest.MonkeyPatch.context() as context:
        context.setattr('prompt_toolkit.shortcuts.progress_bar.ProgressBar', mock.MagicMock())
        yield


@pytest.fixture
async def _iw_mock_asyncio_run(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr('asyncio.run', asyncio.get_running_loop().run_until_complete)


@pytest.fixture
def iw_pt_input():
    with (
        prompt_toolkit.input.create_pipe_input() as pipe_input,
        prompt_toolkit.application.create_app_session(
            input=pipe_input, output=prompt_toolkit.output.DummyOutput()
        ),
    ):
        yield pipe_input
