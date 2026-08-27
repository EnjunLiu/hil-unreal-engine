from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
COMPRESSION_SOURCE = PROJECT / "Source/HILSimulation/Private/ImageCompressionLibrary.cpp"
AUTOMATION_SOURCE = PROJECT / "Source/HILSimulation/SceneAutomationSubsystem.cpp"


class CaptureColorContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compression = COMPRESSION_SOURCE.read_text(encoding="utf-8")
        cls.automation = AUTOMATION_SOURCE.read_text(encoding="utf-8")

    def test_jpeg_path_does_not_change_display_referred_pixels(self) -> None:
        forbidden = (
            "CaptureExposureScale",
            "CaptureExposureEv",
            "Exposed.ToFColor(true)",
            "ue5_exposure_ev",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, self.compression)

        self.assertIn("ReadFlags.SetLinearToGamma(false)", self.compression)
        self.assertIn("Pixel = Linear.ToFColor(true)", self.compression)
        self.assertIn("ERGBFormat::BGRA, 8", self.compression)

    def test_warmup_preserves_authored_capture_color_settings(self) -> None:
        forbidden = (
            "bOverride_AutoExposureBias = true",
            "AutoExposureBias = 2.0f",
            "RenderTargetFormat = RTF_RGBA8_SRGB",
            "TextureTarget->SRGB = true",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, self.automation)

        self.assertIn("CaptureSource = ESceneCaptureSource::SCS_FinalColorLDR", self.automation)
        self.assertIn("ShowFlags.SetPostProcessing(true)", self.automation)
        self.assertIn("ShowFlags.SetTonemapper(true)", self.automation)


if __name__ == "__main__":
    unittest.main()
