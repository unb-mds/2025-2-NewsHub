from unittest.mock import patch, MagicMock
import runpy

def test_main_py_creates_and_runs_app():
    with patch('app.create_app') as mock_create_app:
        mock_app_instance = MagicMock()
        mock_create_app.return_value = mock_app_instance

        runpy.run_module('app.main', run_name='__main__')

    mock_create_app.assert_called_once()
    mock_app_instance.run.assert_called_once_with(debug=True)