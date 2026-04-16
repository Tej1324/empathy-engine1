import os
import unittest
from unittest.mock import patch

from src.emotion_analyzer import detect_emotion
from src.tts_engine import generate_speech
from src.voice_mapper import (
    BASE_PITCH,
    BASE_RATE,
    BASE_VOLUME,
    map_emotion_to_voice,
)


class EmotionAnalyzerTests(unittest.TestCase):
    def test_detects_enthusiastic_for_excited_text(self):
        emotion, intensity = detect_emotion("This is AMAZING news!")
        self.assertEqual(emotion, "enthusiastic")
        self.assertGreaterEqual(intensity, 0.6)

    def test_detects_frustrated_for_negative_text(self):
        emotion, intensity = detect_emotion("I am really disappointed with the service.")
        self.assertEqual(emotion, "frustrated")
        self.assertLessEqual(intensity, -0.5)

    def test_detects_inquisitive_for_question(self):
        emotion, intensity = detect_emotion("Why is this taking so long?")
        self.assertEqual(emotion, "inquisitive")
        self.assertLess(intensity, 0.05)

    def test_detects_neutral_for_plain_statement(self):
        emotion, intensity = detect_emotion("The meeting is at 4 PM.")
        self.assertEqual(emotion, "neutral")
        self.assertGreaterEqual(intensity, -0.05)
        self.assertLessEqual(intensity, 0.05)


class VoiceMapperTests(unittest.TestCase):
    def test_positive_voice_mapping_increases_energy(self):
        rate, volume, pitch = map_emotion_to_voice("positive", 0.6)
        self.assertGreater(rate, BASE_RATE)
        self.assertGreater(volume, BASE_VOLUME)
        self.assertGreater(pitch, BASE_PITCH)

    def test_negative_voice_mapping_decreases_energy(self):
        rate, volume, pitch = map_emotion_to_voice("negative", -0.6)
        self.assertLess(rate, BASE_RATE)
        self.assertLess(volume, BASE_VOLUME)
        self.assertLess(pitch, BASE_PITCH)

    def test_inquisitive_voice_mapping_uses_fixed_offsets(self):
        rate, volume, pitch = map_emotion_to_voice("inquisitive", 0.2)
        self.assertEqual(rate, BASE_RATE + 10)
        self.assertEqual(volume, BASE_VOLUME)
        self.assertEqual(pitch, BASE_PITCH + 5)

    def test_neutral_voice_mapping_keeps_baseline(self):
        rate, volume, pitch = map_emotion_to_voice("neutral", 0.0)
        self.assertEqual(rate, BASE_RATE)
        self.assertEqual(volume, BASE_VOLUME)
        self.assertEqual(pitch, BASE_PITCH)


class GenerateSpeechTests(unittest.TestCase):
    @patch("src.tts_engine._patch_pyttsx3_sapi5")
    @patch("src.tts_engine.time.time", return_value=1234567890)
    @patch("src.tts_engine.os.makedirs")
    @patch("src.tts_engine.pyttsx3.init")
    def test_generate_speech_configures_engine_and_returns_expected_path(
        self, mock_init, mock_makedirs, mock_time, mock_patch
    ):
        engine = mock_init.return_value

        output_file = generate_speech(
            text="Hello there",
            rate=175,
            volume=0.95,
            pitch=55,
            emotion="positive",
        )

        self.assertEqual(
            output_file,
            os.path.join("static", "audio", "output_positive_1234567890.wav").replace("\\", "/"),
        )
        mock_patch.assert_called_once_with()
        mock_makedirs.assert_called_once_with("static/audio", exist_ok=True)
        engine.setProperty.assert_any_call("rate", 175)
        engine.setProperty.assert_any_call("volume", 0.95)
        engine.setProperty.assert_any_call("pitch", 55)
        engine.save_to_file.assert_called_once_with(
            "Hello there",
            "static/audio/output_positive_1234567890.wav",
        )
        engine.runAndWait.assert_called_once_with()
        engine.stop.assert_called_once_with()

    @patch("src.tts_engine._patch_pyttsx3_sapi5")
    @patch("src.tts_engine.pyttsx3.init")
    def test_generate_speech_ignores_pitch_errors(self, mock_init, mock_patch):
        engine = mock_init.return_value

        def set_property(name, value):
            if name == "pitch":
                raise RuntimeError("pitch unsupported")

        engine.setProperty.side_effect = set_property

        output_file = generate_speech(
            text="Hello there",
            rate=150,
            volume=0.9,
            pitch=50,
            emotion="neutral",
        )

        self.assertTrue(output_file.startswith("static/audio/output_neutral_"))
        engine.save_to_file.assert_called_once()
        engine.runAndWait.assert_called_once_with()
        engine.stop.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
