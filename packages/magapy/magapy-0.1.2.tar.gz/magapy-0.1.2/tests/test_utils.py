import pytest
import tempfile
from pathlib import Path
import os
import json
from unittest.mock import patch, MagicMock

from ..utils.file_utils import safe_move, get_unique_filename
from ..utils.metadata_utils import read_metadata
from ..link_utils import is_qobuz_link, is_tidal_link

class TestFileUtils:
    def test_get_unique_filename(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file
            test_file = Path(temp_dir) / "test.txt"
            test_file.touch()
            
            # Get unique filename for existing file
            unique_file = get_unique_filename(test_file)
            assert unique_file != test_file
            assert unique_file.name == "test_1.txt"
            
            # Create the first unique filename
            unique_file.touch()
            
            # Get another unique filename
            another_unique = get_unique_filename(test_file)
            assert another_unique.name == "test_2.txt"
    
    def test_safe_move(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create source file
            source_dir = Path(temp_dir) / "source"
            source_dir.mkdir()
            source_file = source_dir / "test.txt"
            with open(source_file, "w") as f:
                f.write("test content")
            
            # Create destination directory
            dest_dir = Path(temp_dir) / "destination"
            
            # Test moving to non-existent directory
            dest_file = dest_dir / "test.txt"
            result = safe_move(source_file, dest_file)
            assert result is True
            assert dest_file.exists()
            assert not source_file.exists()
            
            # Create new source file
            source_file = source_dir / "test2.txt"
            with open(source_file, "w") as f:
                f.write("test content 2")
            
            # Create existing destination file
            with open(dest_dir / "test2.txt", "w") as f:
                f.write("existing content")
            
            # Test moving to existing file
            dest_file = dest_dir / "test2.txt"
            result = safe_move(source_file, dest_file)
            assert result is True
            assert not source_file.exists()
            duplicate_files = list(dest_dir.glob("test2_duplicate_*.txt"))
            assert len(duplicate_files) > 0

class TestLinkUtils:
    def test_is_qobuz_link(self):
        assert is_qobuz_link("https://play.qobuz.com/album/123456") is True
        assert is_qobuz_link("https://open.qobuz.com/track/789012") is True
        assert is_qobuz_link("https://www.qobuz.com/playlist/345678") is True
        assert is_qobuz_link("https://tidal.com/album/123456") is False
        assert is_qobuz_link("https://example.com") is False
        
    def test_is_tidal_link(self):
        assert is_tidal_link("https://tidal.com/browse/album/123456") is True
        assert is_tidal_link("https://tidal.com/track/789012") is True
        assert is_tidal_link("https://www.tidal.com/playlist/345678") is True
        assert is_tidal_link("https://play.qobuz.com/album/123456") is False
        assert is_tidal_link("https://example.com") is False

@patch('mutagen.flac.FLAC')
class TestMetadataUtils:
    def test_read_flac_metadata(self, mock_flac):
        # Setup mock
        flac_instance = MagicMock()
        flac_instance.get.side_effect = lambda key, default: {
            "artist": ["Test Artist"],
            "title": ["Test Title"],
            "album": ["Test Album"],
            "date": ["2023"],
            "genre": ["Rock"]
        }.get(key, default)
        flac_instance.info.bitrate = 1411000
        flac_instance.info.sample_rate = 44100
        flac_instance.info.length = 240
        mock_flac.return_value = flac_instance
        
        from ..utils.metadata_utils import read_flac_metadata
        
        # Test
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.flac"
            test_file.touch()
            
            metadata = read_flac_metadata(test_file)
            
            assert metadata["artist"] == "Test Artist"
            assert metadata["title"] == "Test Title"
            assert metadata["album"] == "Test Album"
            assert metadata["date"] == "2023"
            assert metadata["genre"] == "Rock"
            assert metadata["bitrate"] == 1411
            assert metadata["samplerate"] == 44100
            assert metadata["duration"] == 240
