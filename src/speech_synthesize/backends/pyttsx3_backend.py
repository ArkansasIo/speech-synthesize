"""pyttsx3 backend."""
from __future__ import annotations
from pathlib import Path
from ..exceptions import BackendUnavailableError, SynthesisError
from ..models import SynthesisOptions, VoiceInfo
class Pyttsx3Backend:
    name = "pyttsx3"
    def _engine(self):
        try:
            import pyttsx3
            return pyttsx3.init()
        except Exception as exc: raise BackendUnavailableError("Unable to initialize pyttsx3/system speech support") from exc
    def list_voices(self) -> list[VoiceInfo]:
        engine = self._engine()
        try:
            result=[]
            for v in engine.getProperty("voices") or []:
                langs=tuple(str(x) for x in (getattr(v,"languages",[]) or []))
                result.append(VoiceInfo(str(getattr(v,"id","")), str(getattr(v,"name","")), langs))
            return result
        finally: engine.stop()
    def synthesize(self, text: str, output_path: Path, options: SynthesisOptions) -> None:
        engine=self._engine()
        try:
            engine.setProperty("rate", options.rate); engine.setProperty("volume", options.volume)
            if options.voice_id: engine.setProperty("voice", options.voice_id)
            engine.save_to_file(text.strip(), str(output_path)); engine.runAndWait()
        except Exception as exc: raise SynthesisError("pyttsx3 synthesis failed") from exc
        finally: engine.stop()
        if not output_path.exists() or output_path.stat().st_size == 0: raise SynthesisError("speech backend produced no audio")
