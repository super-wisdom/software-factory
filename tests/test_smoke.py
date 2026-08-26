from software_factory.core import healthcheck


def test_healthcheck():
    assert healthcheck() == "software-factory: ok"
