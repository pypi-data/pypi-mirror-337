import pytest
from src.icinga.listener import icinga


@pytest.fixture
def icinga_instance():
    # metric_name = ".".join([self.current_test["suite"], self.current_test["test"]])
    icinga.current_keyword = {"suite": "testsuite", "test": "testtest", "keyword": "testkeyword"}
    return icinga()


def test_get_metric_name_keyword(icinga_instance):
    assert icinga_instance.get_metric_name(type="keyword") == "testsuite.testtest.testkeyword"
