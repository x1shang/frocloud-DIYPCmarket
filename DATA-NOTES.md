# 数据说明 · DATA NOTES

> 这一页讲**数据本身怎么读**（空值口径、合并单元格语义），**不是许可证条款**。
> 授权见 [`LICENSE`](LICENSE)，免责见 [`DISCLAIMER.md`](DISCLAIMER.md)，
> 每个 CSV 有哪些列、什么含义见 [`README.md`](README.md) 的「CSV 字段字典」。

数据部分的 SPDX 标识：

```text
SPDX-License-Identifier: CC-BY-4.0
SPDX-FileCopyrightText: 2023-2026 x1shang
```

## 数据文件里的「空」是什么意思

- 空单元格 / 空字段 = **原表里就没有这个数据**，不补 0、不猜测、不用别的值顶上。
- 唯一的例外是**合并单元格的标签**（例如「显卡品牌」里 `B3:B6 = 一线`）：
  这种空白不是「缺数据」，而是「这个标签适用于整段」，导出 CSV 时会物化到该段的每一行。
  合并段的锚点本身是空的（例如 Intel 区没写分级），物化后仍然是空 —— 那才是真空白。

这条规则由 `tools/test_materialize.py` 守着；改动导出逻辑后必须让它保持全绿。

## 两个别踩的坑

- **CSV 是机器生成的**（`python tools/export_csv.py`），不得手改，也不要在 CSV 里加注释行：
  CI 会逐字节对比「重新导出的结果」与仓库里的 `data/*.csv`。
- **CSV 与 xlsx 不一致时**，`tools/check_csv.py` 会报错 —— 正确反应是**告诉维护者**，
  而不是自己动手改其中任何一边（改数据只能由人改 xlsx 后重新导出）。

---

本文件更新：2026-10-08
