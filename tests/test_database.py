from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from speech_synthesize.db_models import Base
from speech_synthesize.repositories import JobRepository, VoiceRepository
from speech_synthesize.models import SynthesisOptions, VoiceInfo


def test_repositories_round_trip_with_sqlite():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine, expire_on_commit=False)

    with sessions() as session:
        voice = VoiceRepository(session).upsert(
            VoiceInfo("voice-1", "English Test", ("en-US",), "neutral")
        )
        job = JobRepository(session).create(
            "Hello world", SynthesisOptions(language="en-US"), "pyttsx3"
        )
        session.commit()
        assert voice.language == "en-US"
        assert JobRepository(session).get(job.id).status == "queued"


def test_english_options_reject_non_english_language():
    options = SynthesisOptions(language="fr-FR")
    try:
        options.validate()
    except ValueError as exc:
        assert "en-*" in str(exc)
    else:
        raise AssertionError("non-English language should be rejected")
