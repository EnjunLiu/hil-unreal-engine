# 面向 ASV 仿真的硬件在环实验平台 - Unreal Engine 端

UE 5.8 水面场景与运动学执行器。工程入口：`HILPlatform.uproject`，主关卡：`/Game/Main_Map`。

## 功能接口

| 通道 | 方向 | 说明 |
| --- | --- | --- |
| TCP `:8080`（ObjectDeliverer） | UE → Jetson | 相机 JPEG 与 ASV / 实体 JSON 状态 |
| TCP `:8081`（SceneExec） | Jetson → UE | BodyFrame 二维期望位移（cm） |

- 输出：第一人称相机帧、ASV 位姿、场景实体状态（由 Jetson `bridge` 转为 `/ue/camera_frame`、`/ue/asv_state`）
- 输入：二维期望位移 JSON（`Delta_X_Cm` / `Delta_Y_Cm` / `Valid` / `Hold_Position`），对应 Jetson `/control/desired_displacement`

## 实现细节

- `HILSimulation` 模块中的 `USceneAutomationSubsystem` 仅在命令行带 `-SceneAuto` 时创建，按 Slot / Layout / Motion / Seed 布置目标与障碍
- 相机 JPEG 由 `UImageCompressionLibrary` 从 SceneCapture RenderTarget 压缩后经 ObjectDeliverer 发出
- `-SceneExecPort=8081` 时，C++ 运动学执行器直接移动 `BP_ASV`
- 船体网格位于 `Content/ASVModel/`（`SM_ASV`、`SM_Target`）

示例闭环场景：

```text
UnrealEditor.exe HILPlatform.uproject Main_Map -game -SceneAuto -Slot=RED_3M_TEST -Layout=L7B -Motion=S2 -Seed=231106 -SceneExecPort=8081 -MaxRuntimeSeconds=180 -YawFixWholeRun
```

## 资产管线

船体在 Blender 中建模，发布为版本化 USD，在 USD Composer 中核对后覆盖 UE 的 `SM_ASV`。NVIDIA Kit 模板本身不入库；本仓只保留原创脚本。

<p align="center">
  <img src="docs/assets/blender_sm_asv.png" width="48%" alt="Blender SM_ASV" />
  <img src="docs/assets/usd_composer_sm_asv.png" width="48%" alt="USD Composer SM_ASV v007" />
</p>

- `tools/blender_export_usd.py`：合成可见网格，写入 `published/vNNN/` 与 `asset_manifest.json`
- `tools/import_usd_manifest.py`：按清单覆盖 `/Game/ASVModel/SM_ASV`（不保存 `Main_Map`）
- `Plugins/AssetPipelineMCP`：在已打开的编辑器里通过 MCP 调用导入
- USD Composer 菜单 `Tools → Asset Pipeline` 调用上述脚本

```text
blender --background --python tools/blender_export_usd.py -- --source-blend SM_ASV.blend --asset-root <asset-root> --asset-name SM_ASV
```

## 测试环境

- Windows 11
- Unreal Engine 5.8
- ObjectDeliverer Plugin
- Water Plugin
- Blender 5.2（仅资产发布）
- USD Composer / Omniverse Kit（仅资产核对，可选）
