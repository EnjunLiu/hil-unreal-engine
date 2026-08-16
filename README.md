# Minimal UE5 HIL Project

This is the dependency-reduced UE 5.6 project rooted at `/Game/Main_Map`.
Only the Asset Registry closure is included. `ObjectDeliverer` and the other
listed plugins remain external prerequisites and are not redistributed here.

## Launch

Install UE 5.6 and the required external plugins, then open `VLA.uproject`.
For a headless map-load check use `UnrealEditor-Cmd.exe` with the project and
`-Map=/Game/Main_Map -unattended -RenderOffscreen -nosplash`.

`tools/export_ue_dependencies.py` runs inside the Unreal Editor Python
environment and exports the Asset Registry dependency closure used to audit
the minimal project contents.

The project source and assets are an interview portfolio snapshot. Review
Marketplace and third-party asset redistribution terms before any public push.
