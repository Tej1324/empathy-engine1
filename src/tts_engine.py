import os
import time
from ctypes import COMError

import pyttsx3


def _patch_pyttsx3_sapi5():
    """
    Work around a Windows SAPI issue seen with newer Python builds where
    reading SPVoice.Voice.Id raises COMError even though voices are available.
    """
    try:
        from pyttsx3.drivers import sapi5
    except Exception:
        return

    if getattr(sapi5.SAPI5Driver, "_empathy_engine_patched", False):
        return

    original_init = sapi5.SAPI5Driver.__init__
    original_get_property = sapi5.SAPI5Driver.getProperty
    original_set_property = sapi5.SAPI5Driver.setProperty

    def _safe_current_voice_id(driver):
        voice_id = getattr(driver, "_current_voice_id", None)
        if voice_id:
            return voice_id
        try:
            voice_id = driver._tts.Voice.Id
        except COMError:
            tokens = driver._tts.GetVoices()
            if tokens.Count == 0:
                raise
            token = tokens.Item(0)
            driver._tts.Voice = token
            voice_id = token.Id
        driver._current_voice_id = voice_id
        return voice_id

    def patched_init(self, proxy):
        try:
            original_init(self, proxy)
        except COMError:
            self._tts = sapi5.comtypes.client.CreateObject("SAPI.SPVoice")
            self._tts.EventInterests = 33790
            self._event_sink = sapi5.SAPI5DriverEventSink()
            self._event_sink.setDriver(sapi5.weakref.proxy(self))
            self._advise = sapi5.comtypes.client.GetEvents(self._tts, self._event_sink)
            self._proxy = proxy
            self._looping = False
            self._speaking = False
            self._stopping = False
            self._current_text = ""
            self._rateWpm = 200
            tokens = self._tts.GetVoices()
            if tokens.Count == 0:
                raise
            token = tokens.Item(0)
            self._tts.Voice = token
            self._current_voice_id = token.Id
            self.setProperty("voice", self._current_voice_id)

    def patched_get_property(self, name):
        if name == "voice":
            return _safe_current_voice_id(self)
        return original_get_property(self, name)

    def patched_set_property(self, name, value):
        if name == "voice":
            token = self._tokenFromId(value)
            self._tts.Voice = token
            self._current_voice_id = token.Id
            a, b = sapi5.E_REG.get(value, sapi5.E_REG[sapi5.MSMARY])
            self._tts.Rate = int(sapi5.math.log(self._rateWpm / a, b))
            return
        if name == "rate":
            voice_id = _safe_current_voice_id(self)
            a, b = sapi5.E_REG.get(voice_id, sapi5.E_REG[sapi5.MSMARY])
            self._tts.Rate = int(sapi5.math.log(value / a, b))
            self._rateWpm = value
            return
        return original_set_property(self, name, value)

    sapi5.SAPI5Driver.__init__ = patched_init
    sapi5.SAPI5Driver.getProperty = patched_get_property
    sapi5.SAPI5Driver.setProperty = patched_set_property
    sapi5.SAPI5Driver._empathy_engine_patched = True

def generate_speech(text, rate, volume, pitch, emotion):
    """
    Generates a speech audio file using pyttsx3.

    I initialize the TTS engine per request to avoid
    blocking issues when used inside a Flask app
    (especially on Windows / SAPI5).
    """
    _patch_pyttsx3_sapi5()
    engine = pyttsx3.init()

    # Apply voice parameters derived from emotion
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    # Pitch support is platform-dependent (best-effort)
    try:
        engine.setProperty("pitch", pitch)
    except Exception:
        # Windows SAPI5 often ignores pitch changes
        pass

    # Audio files are stored under static/ so Flask can serve them
    os.makedirs("static/audio", exist_ok=True)

    # Timestamped filenames prevent overwriting during multiple requests
    filename = f"static/audio/output_{emotion}_{int(time.time())}.wav"

    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()

    return filename
