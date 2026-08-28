# 面向 ASV 仿真的硬件在环实验平台 - Unreal Engine 端

基于 UE 5.8 的海洋仿真平台。

## 功能接口

| 通道 | 方向 | 说明 |
| --- | --- | --- |
| TCP 8080 | UE → Jetson | CameraFrame 与 ASV / Entity 状态 |
| TCP 8081 | Jetson → UE | BodyFrame 下的二维期望位移指令|

- 输出：CameraFrame、ASVState、EntityState
- 输入：二维期望位移指令（包括停机等）

## 实现细节

- `HILSimulation` 模块中的 `USceneAutomationSubsystem` 按 Slot / Motion / Seed 布置目标与障碍
- CameraFrame 由 `UImageCompressionLibrary` 从 SceneCapture RenderTarget 压缩后经 ObjectDeliverer 发出

## 资产管理

ASV 在 Blender 中建模，发布为 USD，在 USD Composer 中核对后覆盖 UE 的 `SM_ASV` 网格体

<p align="center">
  <img src="docs/assets/blender_sm_asv.png" width="48%" alt="Blender SM_ASV" />
  <img src="docs/assets/usd_composer_sm_asv.png" width="48%" alt="USD Composer SM_ASV v007" />
</p>

## 测试环境

- Windows 11
- Unreal Engine 5.8 (ObjectDeliverer Plugin, Water Plugin)
- Blender 5.2
- USD Composer (Omniverse Kit)
