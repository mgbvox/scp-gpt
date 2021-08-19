from pytest import fixture

@fixture
def scp_urls():
    return [
        "https://scp-wiki.wikidot.com/scp-001",
        "https://scp-wiki.wikidot.com/scp-10",
        "https://scp-wiki.wikidot.com/scp-1234",
    ]


@fixture
def non_scp_urls():
    return [
        "https://scp-wiki.wikidot.com/scp-series-5-tales-edition",
        "https://scp-wiki.wikidot.com/scp-ex",
        "https://scp-wiki.wikidot.com/scp-2615-j",
    ]
