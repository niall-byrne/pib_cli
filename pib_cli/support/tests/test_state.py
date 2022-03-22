"""Tests for the State class."""

from unittest import TestCase
from unittest.mock import Mock, patch

from pib_cli.support.user_configuration import user_configuration_file
from pib_cli.support.user_configuration.bases import version_base

from .. import state


class TestRunningConfig(TestCase):
  """Test the RunningConfig monostate."""

  def setUp(self) -> None:
    state.State.clear()

  def test_instantiate(self) -> None:
    instance = state.State()
    self.assertIsNone(
        instance.user_config,
        version_base.UserConfigurationVersionBase,
    )
    self.assertIsNone(
        instance.user_config_file,
        user_configuration_file.UserConfigurationFile,
    )

  def test_mono_state_user_config(self) -> None:
    instance = state.State()
    instance.user_config = Mock()

    instance2 = state.State()
    self.assertEqual(instance.user_config, getattr(instance2, 'user_config'))

  def test_mono_state_clear(self) -> None:
    instance = state.State()
    instance.user_config = Mock()

    state.State.clear()

    instance2 = state.State()

    self.assertEqual(instance2.user_config, None)

  @patch(state.__name__ + ".user_configuration_file.UserConfigurationFile")
  def test_load_config(self, m_user_config_file: Mock) -> None:

    instance = state.State()
    instance.load()

    m_user_config_file.assert_called_once_with()
    m_user_config_file.return_value.parse.assert_called_once_with()
    self.assertEqual(instance.user_config_file, m_user_config_file.return_value)
    self.assertEqual(
        instance.user_config, m_user_config_file.return_value.parse.return_value
    )
