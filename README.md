# 面向 ASV 仿真的硬件在环实验平台 - Unreal Engine 端

UE 5.8 水面场景与运动学执行器。工程入口：`HILPlatform.uproject`，主关卡：`/Game/Main_Map`。

## 功能接口

| 通道 | 方向 | 说明 |
| --- | --- | --- |
| TCP `:8080`（ObjectDeliverer） | UE → Jetson | 相机 JPEG 与 ASV / 实体 JSON 状态 |
| TCP `:8081`（SceneExec） | Jetson → UE | BodyFrame 二维期望位移（cm） |

- 输出：第一人称相机帧、ASV 位姿、场景实体状态（由 Jetson `bridge` 转为 `/ue/camera_frame`、`/ue/asv_state`）
- 输入：二维期望位移 JSON（`Delta_X_Cm` / `Delta_Y_Cm` / `Valid` / `Hold_Position`），对应 Jetson `/control/desired_displacement`
- 在线策略不得把 `/ue/entities` 当作特权真值；该通道仅用于记录与离线监督

## 实现细节

- `HILSimulation` 模块中的 `USceneAutomationSubsystem` 仅在命令行带 `-SceneAuto` 时创建，按 Slot / Layout / Motion / Seed 布置目标与障碍
- 相机 JPEG 由 `UImageCompressionLibrary` 从 SceneCapture RenderTarget 压缩后经 ObjectDeliverer 发出
- `-SceneExecPort=8081` 时，C++ 运动学执行器直接移动 `BP_ASV`（headless 下 Blueprint 不落地 setpoint）
- 船体网格位于 `Content/ASVModel/`（`SM_ASV`、`SM_Target`）

示例闭环场景：

```text
UnrealEditor.exe HILPlatform.uproject Main_Map -game -SceneAuto -Slot=RED_3M_TEST -Layout=L7B -Motion=S2 -Seed=231106 -SceneExecPort=8081 -MaxRuntimeSeconds=180 -YawFixWholeRun
```

## 测试环境

- Windows 10 / 11
- Unreal Engine 5.8
- ObjectDeliverer（Marketplace）
- Water 插件
