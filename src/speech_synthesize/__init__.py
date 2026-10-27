"""Speech Synthesize: a small, extensible text-to-speech toolkit."""

from .engine import SynthesisError, SynthesisOptions, list_voices, synthesize_to_file

__all__ = ["SynthesisError", "SynthesisOptions", "list_voices", "synthesize_to_file"]
__version__ = "0.1.0"
