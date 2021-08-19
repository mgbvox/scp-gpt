import pytest
import regex as re
from scp_gpt.models.scp_models import SCP_URL_PATTERN, SCPUrl, SCP
from pydantic import ValidationError


def test_scp_url_pattern(scp_urls, non_scp_urls):
    for url in scp_urls:
        assert re.search(SCP_URL_PATTERN, url)

    for url in non_scp_urls:
        assert re.search(SCP_URL_PATTERN, url) is None


def test_SCP_number_derivation_good_urls(scp_urls):
    for url in scp_urls:
        formatted_url = SCPUrl(raw_url=url)
        scp = SCP(url=formatted_url)
        assert isinstance(scp.number, int)
        assert scp.number > 0


def test_SCP_number_derivation_bad_urls(non_scp_urls):
    for url in non_scp_urls:
        with pytest.raises(ValidationError):
            """
            Expected to raise a KeyError, as derivation of SCP number will fail for bad urls.
            This, in turn, will cause values['url'] (for number validation) to fail.
            """
            formatted_url = SCPUrl(raw_url=url)

@pytest.mark.parametrize('valid_number', [1, '01', 1.00])
def test_SCP_valid_provided_number(valid_number):
    scp_001_url = SCPUrl(raw_url="https://scp-wiki.wikidot.com/scp-001")
    scp_w_valid_number = SCP(url=scp_001_url,
                             number=valid_number)
    assert scp_w_valid_number.number == int(valid_number)

@pytest.mark.parametrize('bad_number', ['one', 'taco', '0.01'])
def test_SCP_bad_provided_number(bad_number):
    scp_001_url = SCPUrl(raw_url="https://scp-wiki.wikidot.com/scp-001")
    with pytest.raises(ValidationError):
        scp_w_valid_number = SCP(url=scp_001_url,
                                 number=bad_number)
