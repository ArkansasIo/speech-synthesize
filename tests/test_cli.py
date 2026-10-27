from pathlib import Path
import pytest
from speech_synthesize.cli import main


def test_cli_requires_source() -> None:
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2


def test_cli_reads_utf8_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    source = tmp_path / "input.txt"
    source.write_text("Bonjour", encoding="utf-8")
    output = tmp_path / "speech.wav"
    observed: dict[str, object] = {}

    def fake_synthesize(text, output_path, options):
        observed["text"] = text
        observed["output_path"] = output_path
        observed["options"] = options
        output.touch()
        return output

    monkeypatch.setattr("speech_synthesize.cli.synthesize_to_file", fake_synthesize)
    assert main(["--input", str(source), "--output", str(output)]) == 0
    assert observed["text"] == "Bonjour"
    assert observed["output_path"] == output
