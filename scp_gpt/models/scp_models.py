from typing import Optional, List
from pydantic import BaseModel, validator, root_validator
import regex as re

SCP_URL_PATTERN = re.compile(r"http[s].*/scp-\d{1,}$")

SCP_NUMBER_PATTERN = re.compile(r"-(\d{1,})$")


class SCPUrl(BaseModel):
    raw_url: str

    @validator("raw_url")
    def ensure_url_points_to_an_scp(cls, v):
        is_valid = re.match(SCP_URL_PATTERN, v)
        assert is_valid
        assert is_valid.string == v
        return v


class SCP(BaseModel):
    url: SCPUrl

    number: Optional[int]

    @validator("number", always=True)
    def derive_scp_number(cls, v, values):
        if v:
            if isinstance(v, int):
                return v
            else:
                try:
                    as_int = int(v)
                    return as_int
                except:
                    raise ValueError(f"Could not parse provided number to int: {v}.")
        else:
            raw_url = values["url"].raw_url
            match = re.search(SCP_NUMBER_PATTERN, raw_url)
            if match:
                detected_number = match.group(1)
                if detected_number:
                    return int(detected_number)
                else:
                    raise ValueError(
                        f"Number detected in url {raw_url} but could not be parsed."
                    )
            else:
                raise ValueError(
                    f"Could not find an valid scp number in the url {raw_url}"
                )
