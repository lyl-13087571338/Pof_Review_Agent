import os

from agent.run_agent import run_agent


def test_run_agent_callable():
    assert callable(run_agent)


def test_config_exists():
    assert os.path.exists("config/config.yaml")
