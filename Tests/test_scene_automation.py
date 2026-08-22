from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = (PROJECT / "Source/EDGE/SceneAutomationSubsystem.cpp").read_text(
    encoding="utf-8"
)
HEADER = (PROJECT / "Source/EDGE/SceneAutomationSubsystem.h").read_text(
    encoding="utf-8"
)


def test_expert_follow_mode_is_opt_in_and_bounded() -> None:
    assert "ExpertFollowColor" in SOURCE
    assert "ExpertStandoffM" in SOURCE
    assert "ExpertFollow" in HEADER
    assert "SCENE_EXPERT_APPLY" in SOURCE
    assert "ExpertMaxStepCm" in SOURCE
    assert "ExpertMaxAccelerationCmPerSec2" in SOURCE


def test_expert_mode_does_not_change_normal_scene_without_flag() -> None:
    assert "FParse::Value(CommandLine, TEXT(\"ExpertFollowColor=\")" in SOURCE
    assert "if (bExpertFollowEnabled)" in SOURCE
