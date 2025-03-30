import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--db-host",
        action="store",
        default="raspi.thepmsquare.com",
        help="Database host",
    )
    parser.addoption(
        "--db-port",
        action="store",
        type=int,
        default=15432,
        help="Database port",
    )
    parser.addoption(
        "--db-user",
        action="store",
        default="postgres",
        help="Database user",
    )
    parser.addoption(
        "--db-password",
        action="store",
        default="testing",
        help="Database password",
    )


@pytest.fixture(scope="session")
def db_credentials(request):
    return {
        "host": request.config.getoption("--db-host"),
        "port": request.config.getoption("--db-port"),
        "user": request.config.getoption("--db-user"),
        "password": request.config.getoption("--db-password"),
    }
