# 面向 ASV 仿真的硬件在环实验平台 - Unreal Engine 端

UE 5.8 水面场景与运动学执行器。

## 功能接口

| 通道 | 方向 | 说明 |
| --- | --- | --- |
| TCP `:8080`（ObjectDeliverer） | UE → Jetson | 相机 JPEG 与 ASV / Entity 状态 |
| TCP `:8081`（SceneExec） | Jetson → UE | BodyFrame 二维期望位移|

- 输出：相机帧、ASVState、EntityState（由 Jetson `bridge` 转为 `/ue/camera_frame`、`/ue/asv_state`）
- 输入：二维期望位移（`Delta_X_Cm` / `Delta_Y_Cm` / `Valid` / `Hold_Position`），对应 Jetson `/control/desired_displacement`

## 实现细节

- `HILSimulation` 模块中的 `USceneAutomationSubsystem` 在命令行带 `-SceneAuto` 时创建，按 Slot / Layout / Motion / Seed 布置目标与障碍
- 相机 JPEG 由 `UImageCompressionLibrary` 从 SceneCapture RenderTarget 压缩后经 ObjectDeliverer 发出


## 资产管线

ASV 在 Blender 中建模，发布为版本化 USD，在 USD Composer 中核对后覆盖 UE 的 `SM_ASV`。

<p align="center">
  <img src="docs/assets/blender_sm_asv.png" width="48%" alt="Blender SM_ASV" />
  <img src="docs/assets/usd_composer_sm_asv.png" width="48%" alt="USD Composer SM_ASV v007" />
</p>

- `tools/blender_export_usd.py`：合成可见网格，写入 `published/vNNN/` 与 `asset_manifest.json`
- `tools/import_usd_manifest.py`：按清单覆盖 `/Game/ASVModel/SM_ASV`
- `Plugins/AssetPipelineMCP`：在已打开的编辑器里通过 MCP 调用导入
- USD Composer 菜单 `Tools → Asset Pipeline` 调用上述脚本

## 测试环境

- Windows 11
- Unreal Engine 5.8
- ObjectDeliverer Plugin
- Water Plugin
- Blender 5.2
- USD Composer / Omniverse Kit
