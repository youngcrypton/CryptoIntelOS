from unittest.mock import patch

from src.core.app import run


@patch("src.core.app.browser_manager.stop")
@patch("src.core.app.scheduler.run")
@patch("src.core.app.browser_manager.start")
@patch("src.core.app.database.create_tables")
@patch("src.core.app.database.connect")
@patch("src.core.app.config.verify_directories")
@patch("src.core.app.initialize_logger")
@patch("src.core.app.show_banner")
@patch("src.core.app.project_service.list_projects", return_value=[])
@patch("src.core.app.event_service.list_events", return_value=[])
@patch("src.core.app.logger.info")
@patch("src.core.app.database.close")
def test_run_starts_application(
    mock_close,
    mock_logger,
    mock_events,
    mock_projects,
    mock_banner,
    mock_logger_init,
    mock_verify,
    mock_connect,
    mock_tables,
    mock_browser_start,
    mock_scheduler,
    mock_browser_stop,
):
    run()

    mock_banner.assert_called_once()
    mock_logger_init.assert_called_once()
    mock_verify.assert_called_once()
    mock_connect.assert_called_once()
    mock_tables.assert_called_once()
    mock_browser_start.assert_called_once()
    mock_scheduler.assert_called_once()
    mock_browser_stop.assert_called_once()
    mock_close.assert_called_once()