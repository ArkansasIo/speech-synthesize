"""Voice matching helpers."""
from .models import VoiceInfo
def find_voice(voices:list[VoiceInfo], query:str)->VoiceInfo|None:
    q=query.casefold()
    for v in voices:
        if v.id.casefold()==q or v.name.casefold()==q: return v
    for v in voices:
        if q in v.name.casefold() or any(q in lang.casefold() for lang in v.languages): return v
    return None
