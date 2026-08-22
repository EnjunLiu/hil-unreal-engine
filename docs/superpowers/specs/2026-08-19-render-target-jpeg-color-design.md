# Render Target JPEG Color Design

## Goal

Export the `SceneCaptureComponent2D` image to JPEG with the same display-referred appearance shown by the Render Target asset editor. JPEG compression error is acceptable; additional exposure, gamma, contrast, or Jetson-side preprocessing is not.

## Root Cause

The current path altered the authored image twice and then omitted the required display transfer:

1. `WarmupSceneCaptures()` overrode the capture exposure with `AutoExposureBias = 2.0f` and changed the Render Target format and `SRGB` property.
2. `ReadRenderTargetPixels()` treated the linear readback as display bytes, multiplied it by two, and called `ToFColor(true)`, applying an exposure increase on top of an incorrect color-space assumption.
3. Removing the exposure loop without restoring the single linear-to-sRGB transfer produced a dark JPEG. A controlled offline conversion matched the Render Target preview, proving that the missing transfer, not missing exposure, was the remaining issue.

This clips highlights and changes midtones before JPEG encoding. JPEG quality cannot correct that transformation.

## Selected Design

- Keep `SCS_FinalColorLDR`, post processing, and the tonemapper so the capture remains display-referred.
- Preserve the Scene Capture and Render Target properties authored in UE5 instead of overriding exposure, format, or `SRGB` during warmup.
- Read the authored Render Target without an implicit readback transfer, then
  convert each normalized linear RGB value once with UE's standard sRGB
  transfer. Do not multiply RGB by an exposure scale.
- Pass the resulting `FColor` array directly to the JPEG wrapper as `ERGBFormat::BGRA`, 8 bits per channel.
- Retain warmup, pixel statistics, black-frame diagnostics, and optional JPEG dumping.
- Do not add brightness, gamma, or contrast preprocessing on Jetson.

## Acceptance Criteria

1. Source contract test proves there are no exposure constants, per-pixel exposure scaling, Scene Capture exposure override, or forced Render Target color properties in this path, and requires exactly one explicit sRGB transfer.
2. UE5 project compiles with Unreal Engine 5.6.
3. A newly generated diagnostic JPEG is visually inspected and compared with a same-source uncompressed readback or Render Target reference.
4. Pixel differences are attributable to the single standard sRGB transfer and JPEG compression; no artificial exposure increase or new highlight clipping is present.

## Repository Note

`D:\asv-hil-validation-20260816` is not a Git repository. This work therefore records source, test, build, and runtime evidence without commit steps.
