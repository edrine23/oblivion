import pytest
from modules.utils.generator import Generator

@pytest.fixture
def generator():
    config = {"output_dir": "reports"}
    return Generator(config)

def test_password_generator_valid_input(generator):
    password, md5_hash, leet_text = generator.password_generator(12, "test")
    assert len(password) == 12
    assert len(md5_hash) == 32  # MD5 hash length
    assert leet_text == "73$7"  # Leet speak for "test"

def test_password_generator_invalid_length(generator):
    with pytest.raises(ValueError):
        generator.password_generator(0, "test")

def test_generate_payload_xss(generator):
    payload = generator.generate_payload("xss", "alert(1)")
    assert payload == "<script>alert(1)</script>"

def test_test_jwt_none_alg(generator):
    token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ."
    result = generator.test_jwt(token)
    assert result["vulnerable"] is True