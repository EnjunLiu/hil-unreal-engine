# Render Target JPEG Color Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make UE5 JPEG output preserve the Render Target preview appearance without artificial exposure or export-stage exposure scaling.

**Architecture:** Preserve the authored Scene Capture and Render Target color settings, capture `FinalColorLDR`, read the target without an implicit transfer, apply one explicit standard linear-to-sRGB conversion with no exposure scaling, and encode those BGRA8 bytes directly as JPEG. Keep existing warmup and diagnostics so startup and runtime failures remain observable.

**Tech Stack:** Unreal Engine 5.6, C++, Python `unittest`, ImageWrapper JPEG

---

### Task 1: Add the color-path regression contract

**Files:**
- Create: `Tests/test_capture_color_contract.py`
- Test: `Tests/test_capture_color_contract.py`

- [x] **Step 1: Write a source contract test**

The test rejects exposure constants, per-pixel gamma conversion, Scene Capture exposure overrides, and forced Render Target color properties. It also requires `FinalColorLDR`, direct readback, and BGRA JPEG input.

- [x] **Step 2: Run the test and verify RED**

Run: `python -m unittest Tests.test_capture_color_contract -v`

Expected: failures identifying the current `CaptureExposure*`, `ToFColor(true)`, `AutoExposureBias`, and forced `RTF_RGBA8_SRGB` code.

### Task 2: Preserve capture settings and remove runtime target overrides

**Files:**
- Modify: `Source/EDGE/SceneAutomationSubsystem.cpp`
- Test: `Tests/test_capture_color_contract.py`

- [x] **Step 1: Keep capture behavior but remove color overrides**

Keep `SCS_FinalColorLDR`, post processing, tonemapper, `CaptureScene()`, and render-command synchronization. Remove runtime exposure override and Render Target format/`SRGB` mutation so the UE5-authored capture settings remain authoritative.

### Task 3: Encode readback bytes without exposure or gamma changes

**Files:**
- Modify: `Source/EDGE/Private/ImageCompressionLibrary.cpp`
- Test: `Tests/test_capture_color_contract.py`

- [x] **Step 1: Remove artificial pixel conversion and use one display transfer**

Delete `CaptureExposureEv`, `CaptureExposureScale`, and exposure-specific log fields. Keep `ReadPixels` with `SetLinearToGamma(false)`, convert normalized linear RGB once with `Linear.ToFColor(true)` without multiplication, and keep diagnostics, warmup handling, and `SetRaw(... ERGBFormat::BGRA, 8)`.

- [x] **Step 2: Run the test and verify GREEN**

Run: `python -m unittest Tests.test_capture_color_contract -v`

Expected: all contract tests pass.

### Task 4: Compile and perform runtime image acceptance

**Files:**
- Verify: `VLA.uproject`
- Runtime output: `Saved/CaptureDiagnostics/capture_*.jpg`

- [x] **Step 1: Compile the editor target**

Run Unreal Build Tool for the UE 5.6 Win64 Development Editor target. Expected: exit code 0 and no C++ compile errors.

- [x] **Step 2: Generate a fresh JPEG**

Start the project with `edge.ImageCompression.DumpFrames` enabled and trigger the live capture path. Expected: a new timestamped diagnostic JPEG and matching current-run log entry.

- [x] **Step 3: Compare appearance and pixels**

Visually inspect the new JPEG and the Render Target reference. Compare mean RGB/luminance, histogram shape, and clipped-channel ratio. Acceptance requires no systematic exposure offset; remaining local differences should have JPEG compression characteristics.

## Plan Self-Review

- Spec coverage: source, test, build, runtime capture, pixel statistics, and visual inspection are included.
- Placeholder scan: no deferred implementation steps remain.
- Scope: only the two identified C++ color-path files plus test and documentation are changed.
- Git: omitted because the project is not a Git repository.
