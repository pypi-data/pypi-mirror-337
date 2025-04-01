from bluer_ai.tests.test_env import test_bluer_ai_env

from bluer_objects import env


def test_required_env():
    test_bluer_ai_env()


def test_bluer_objects_env():
    assert env.VANWATCH_TEST_OBJECT

    assert env.DATABRICKS_WORKSPACE
    assert env.DATABRICKS_HOST
    assert env.DATABRICKS_TOKEN

    assert env.ABCLI_MLFLOW_EXPERIMENT_PREFIX
