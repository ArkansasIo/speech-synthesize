"""Speech synthesis exception hierarchy."""
class SpeechSynthesizeError(RuntimeError): pass
class ConfigurationError(SpeechSynthesizeError): pass
class BackendUnavailableError(SpeechSynthesizeError): pass
class SynthesisError(SpeechSynthesizeError): pass
class VoiceNotFoundError(SpeechSynthesizeError): pass
