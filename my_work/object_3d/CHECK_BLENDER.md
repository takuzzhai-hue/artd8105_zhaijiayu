# Blender 校验（3D-Print Toolbox）

不要跑 bpy 来“代替”这一步。作业要的是你看见面板上的数字。也不要在 Blender 里修网格再导出覆盖 `output/object.stl`；`check_stl.py` 读过的字节才算数。

打印机：FDM，0.4 mm 喷嘴。导入后 **1 Blender 单位 = 1 mm**。

## 1. 导入

1. 打开 Blender **5.2 LTS**。若场景里已有 **Jar**（`build_jar.py` 生成的），可直接选它；否则 **File → Import → STL** 选 `output/object.stl`，缩放 1.0。
2. 启用 **3D-Print Toolbox**。删掉默认立方体，免得尺寸被它带偏。

## 2. 尺寸

选中物体，N 面板 → Item → **Dimensions**。

**通过：** 大约宽 110 mm、高 160 mm 量级，不是 0.11 那种被当成米的数。这件不是 ≤100 mm 的立方裁切件。

形体应像被手揉过：肚子鼓、腰被勒过、口沿高低不平，身子有一点拧和侧倾。口开着。壁是一整片，不是只在外面挖坑。

## 3. Check All

### Non-manifold / 非流形边

**通过：** 0。

### Intersecting faces / 自交

**通过：** 0。

### Zero faces / Zero edges

**通过：** 都是 0。

### Thickness / 壁厚

阈值设为 **1.6 mm**。

**通过：** 没有报出低于 1.6 mm 的面。名义壁 4 mm、底 3.6 mm；凹坑处被 clamp 到 ≥1.6。这是 Blender 的抽样；`check_stl.py` 的射线是另一次抽样。

### Overhang / 悬垂

约 45°。罐子外壁外倾处会有悬垂，**不算几何失败**。切片时再决定支撑。不要为了消悬垂去改网格。

## 4. 法线

Overlay → **Face Orientation**。实体朝外应是蓝：外壁蓝、罐内空腔看到的内皮也是蓝（法线指向空腔）。整件红则是翻面，`check_stl.py` 的有符号体积应已失败。不要手翻法线再导出。
