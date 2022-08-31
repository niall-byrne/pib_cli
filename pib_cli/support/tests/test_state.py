"""Tests for the State class."""

from unittest.mock import Mock, patch

from .. import state


class TestState:
  """Tests for the State class."""

  class TestInit:
    """Tests for initialization of the State class."""

    def setup_method(self) -> None:
      state.State.clear()

    def test__has_correct_properties(self) -> None:
      instance = state.State()

      assert instance.user_config is None
      assert instance.user_config_file is None

    def test__has_shared_state(self) -> None:
      instance1 = state.State()
      instance1.user_config = Mock()
      instance1.user_config_file = Mock()

      instance2 = state.State()

      assert instance1.user_config == instance2.user_config
      assert instance1.user_config_file == instance2.user_config_file

  class TestStateClear:
    """Tests for clear method of the State class."""

    def setup_method(self) -> None:
      state.State.clear()

    def test__restores_original_state(self) -> None:
      instance1 = state.State()
      instance1.user_config = Mock()
      instance1.user_config_file = Mock()

      state.State.clear()

      instance2 = state.State()
      assert instance2.user_config is None
      assert instance2.user_config_file is None

  class TestStateLoad:
    """Tests for load method of the State class."""

    def setup_method(self) -> None:
      state.State.clear()

    @patch(state.__name__ + ".user_configuration_file.UserConfigurationFile")
    def test__sets_user_config_file(
        self,
        m_user_config_file: Mock,
    ) -> None:
      instance = state.State()

      instance.load()

      m_user_config_file.assert_called_once_with()
      assert instance.user_config_file == m_user_config_file.return_value

    @patch(state.__name__ + ".user_configuration_file.UserConfigurationFile")
    def test__sets_parsed_user_config(
        self,
        m_user_config_file: Mock,
    ) -> None:
      m_parse = m_user_config_file.return_value.parse
      instance = state.State()

      instance.load()

      m_parse.assert_called_once_with()
      assert instance.user_config == m_parse.return_value

    @patch(state.__name__ + ".click.echo")
    @patch(state.__name__ + ".user_configuration_file.UserConfigurationFile")
    def test__with_non_default_config__does_not_echo_warning(
        self,
        m_user_config_file: Mock,
        m_echo: Mock,
    ) -> None:
      instance = state.State()

      instance.load()

      assert m_user_config_file.return_value.get_config_file_name() != \
             m_user_config_file.default_config
      m_echo.assert_not_called()

    @patch(state.__name__ + ".click.echo")
    @patch(state.__name__ + ".user_configuration_file.UserConfigurationFile")
    def test__with_default_config__echoes_warning(
        self,
        m_user_config_file: Mock,
        m_echo: Mock,
    ) -> None:
      m_user_config_file.return_value.default_config = \
        m_user_config_file.return_value.get_config_file_name.return_value
      instance = state.State()

      instance.load()

      assert instance.user_config_file.get_config_file_name() == \
             instance.user_config_file.default_config

      m_echo.assert_called_once_with("** PIB DEFAULT CONFIG IN USE **")
