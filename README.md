# ASV Unreal Simulation

UE 5.6 scene for ASV software-in-the-loop (HIL) with Jetson. Root map: `/Game/Main_Map`.

Part of the [asv-hil-platform](https://github.com/EnjunLiu/asv-hil-platform) stack. Sibling repos: training (`asv-vla-training`), Jetson runtime (`asv-jetson-ws`), ESP32 firmware (`asv-esp32-firmware`).

## Role

- Render the water scene, ego camera, and target boats
- Stream JPEG + JSON state to the Jetson ROS 2 bridge over TCP
- Apply body-frame kinematic setpoints from Jetson (`SceneExec`, typically port `8081`)

Online policy must not treat `/ue/entities` as privileged truth; that channel is for logging and offline supervision.

## Launch

Install UE 5.6 and required external plugins (`ObjectDeliverer` and others listed in project settings), then open `VLA.uproject`.

Example automated scene run (adjust slot / seed / log path as needed):

```text
UnrealEditor.exe VLA.uproject Main_Map -game -SceneAuto -Slot=RED_3M_TEST -Layout=L7B -Motion=S2 -Seed=231106 -SceneExecPort=8081 -MaxRuntimeSeconds=180 -YawFixWholeRun
```

Headless map-load check:

```text
UnrealEditor-Cmd.exe VLA.uproject -Map=/Game/Main_Map -unattended -RenderOffscreen -nosplash
```

`tools/export_ue_dependencies.py` runs inside the Unreal Editor Python environment and exports the Asset Registry dependency closure used to audit the minimal project.

## Repository boundaries

Ignored / not redistributed: `Binaries/`, `Intermediate/`, `Saved/`, DerivedDataCache, local editor state. Marketplace and third-party asset terms still apply before any public redistribution.

Operational handover for this machine lives in `WORKSPACE_CONTEXT.md` (local ops; not a substitute for the README).
