import pytest
from pathlib import Path
import os
from unittest.mock import patch, MagicMock
from ..audio_utils import determine_quality, validate_flac_file, extract_id_from_path, quality_rank

def test_extract_id_from_path():
    # Test Tidal ID extraction
    tidal_path = Path("/music/downloads/Artist - Album [1234567890]")
    service, id = extract_id_from_path(tidal_path)
    assert service == "tidal"
    assert id == "1234567890"
    
    # Test Qobuz ID extraction
    qobuz_path = Path("/music/downloads/qobuz_12345678")
    service, id = extract_id_from_path(qobuz_path)
    assert service == "qobuz"
    assert id == "12345678"
    
    # Test no ID
    no_id_path = Path("/music/downloads/Artist - Album")
    service, id = extract_id_from_path(no_id_path)
    assert service is None
    assert id is None

@patch('mutagen.flac.FLAC')
def test_determine_quality(mock_flac):
    # Setup mock for hi-res
    hires_mock = MagicMock()
    hires_mock.info.bitrate = 3000 * 1000  # 3000kbps
    hires_mock.info.sample_rate = 96000
    mock_flac.return_value = hires_mock
    
    assert determine_quality(Path("test.flac")) == "hires"
    
    # Setup mock for standard
    standard_mock = MagicMock()
    standard_mock.info.bitrate = 1000 * 1000  # 1000kbps
    standard_mock.info.sample_rate = 44100
    standard_mock.pprint.return_value = "standard info"
    mock_flac.return_value = standard_mock
    
    assert determine_quality(Path("test.flac")) == "standard"
    
    # Setup mock for MQA
    mqa_mock = MagicMock()
    mqa_mock.info.bitrate = 1500 * 1000
    mqa_mock.info.sample_rate = 48000
    mqa_mock.pprint.return_value = "MQA info"
    mock_flac.return_value = mqa_mock
    
    assert determine_quality(Path("test.flac")) == "mqa"

@patch('mutagen.flac.FLAC')
def test_validate_flac_file(mock_flac):
    # Valid FLAC
    mock_flac.return_value = MagicMock()
    assert validate_flac_file(Path("valid.flac")) is True
    
    # Invalid FLAC
    mock_flac.side_effect = Exception("Invalid FLAC")
    assert validate_flac_file(Path("invalid.flac")) is False

def test_quality_rank():
    assert quality_rank("hires") == 3
    assert quality_rank("mqa") == 2
    assert quality_rank("standard") == 1
    assert quality_rank("unknown") == 0
