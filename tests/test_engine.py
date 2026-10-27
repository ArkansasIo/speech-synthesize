from pathlib import Path
import pytest
from speech_synthesize.engine import SynthesisOptions, synthesize_to_file


@pytest.mark.parametrize("text", ["", " ", "\n\t"])
def test_empty_text_rejected(tmp_path: Path, text: str) -> None:
    with pytest.raises(ValueError, match="non-empty"):
        synthesize_to_file(text, tmp_path / "speech.wav")


def test_oversized_text_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="100,000"):
        synthesize_to_file("x" * 100_001, tmp_path / "speech.wav")


@pytest.mark.parametrize("rate", [79, 401])
def test_invalid_rate_rejected(rate: int) -> None:
    with pytest.raises(ValueError, match="rate"):
        SynthesisOptions(rate=rate).validate()


@pytest.mark.parametrize("volume", [-0.01, 1.01])
def test_invalid_volume_rejected(volume: float) -> None:
    with pytest.raises(ValueError, match="volume"):
        SynthesisOptions(volume=volume).validate()
