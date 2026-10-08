# frocloud · DIYPCmarket

> **当前市场状况（导览）**

| 显卡 | CPU | 内存&存储 | 其他硬件 |
|---|---|---|---|
| NPC | 夯 | 拉完了 | NPC |
| 涨幅普遍在30%~100%之间，不给拉完了是因为可能还能涨 | 受显卡、存储等影响，DIY市场疲软，CPU价格基本已到底端，继续下探空间缩窄 | 涨价元凶，几大厂商默契不降价，尽管长江、长鑫等国产厂商入场，但是短期无法满产；AI需求仍在迅速增长，导致价格居高不下；DDR2345均涨价，DDR6距离进入消费级市场遥遥无期 | 价格见势跟风上涨（你说你凑啥热闹）|
| 高位缓升 | 跌转横 | 超高位横盘 | 中高位横盘 |

总结：非刚需不要入场。电子产品现在是理财产品。DIY市场更是风口浪尖，市场行情的风向标，比手机、笔记本市场更严重。

> 一份装机市场调研表。把显卡、CPU、内存与存储的价格与用料，
> 压成可以横向对比的「天梯图」—— 设计稿是一个 Excel 工作簿，机读的那一份是 `data/` 里的 CSV。

<img width="1173" height="885" alt="image" src="https://github.com/user-attachments/assets/96e8a09b-eedc-44a1-8a1d-e780eae4a4bf" />

---

## 📦 仓库里有什么

| 文件 | 说明 |
|---|---|
| `frocloud.xlsx` | **主体（手搓）**。8 张工作表 = 1 张「说明」+ 7 张数据表；2023-05 建档，持续更新（最近 2026-10-08） |
| `data/*.csv` | **由 xlsx 机器再生成的 7 个长表 CSV**，与 xlsx 一一对应；这是给机器读、给人 review 的那一份 |
| `tools/export_csv.py` | xlsx → CSV 的导出脚本（两行表头解析、派生列处理、覆盖报告） |
| `tools/check_csv.py` | CSV 校验脚本（相当于本仓库的 CI，失败返回非零退出码） |
| `tools/test_materialize.py` | 回归测试：合并单元格的标签必须物化到整段（用现造的小工作簿跑） |
| `tools/refresh_release_copy.py` | 唯一被允许写 xlsx 的脚本，需 `--i-am-human` 显式确认（见上面「铁律」） |
| `.githooks/commit-msg` | 改了 xlsx 却没带 `[handmade-xlsx]` 标记时拦下提交 |
| `.github/workflows/check-csv.yml` | CI：提交信息以 `(prerelease)` 结尾时自动跑导出 + 校验 + 同步检查（也可手动触发） |
| `LICENSE` | 数据用 CC BY 4.0，附第三方数据来源与免责声明 |
| `.gitignore` | 挡掉 Office/WPS 锁文件之类的噪声 |
| `README.md` | 你在这儿 |

**分工**：`frocloud.xlsx` 是手搓的设计稿，负责好看（合并单元格、配色、列宽、宽表横向对比），每个月的成品以 **Release 附件**形式发布（tag `data-YYYY-MM`）；`data/*.csv` 由脚本从 xlsx 生成，负责能被机器读、能被人 review。

⚠️ **两者不能各自手工维护** —— 一定会分叉。CSV 永远由脚本生成，改数据只改 xlsx。

---

## 🖐 铁律：`frocloud.xlsx` 只准手搓，机器禁碰

**这条比上面那条分工更重要。**

`frocloud.xlsx` 是纯手工设计稿 —— 合并单元格、配色、列宽、天梯排序，全是人一格一格调出来的。
**任何脚本、自动化流程、CI、AI 助手都不得写入它。** 脚本只准**读**它。

为什么写死这条：机器往 xlsx 里写一次（哪怕是"重建一份等价的工作簿"），就可能静默丢掉
字体、空字符串单元格、样式索引、单元格缓存值 —— 手工美化的成果是不可复现资产，
一旦走样就找不回来。（本仓库开发期实测过：一次整本重存把未显式设字体的单元格从宋体变成了 Calibri。）

| 谁 | 能对 xlsx 做什么 |
|---|---|
| 人（WPS / Excel 手工编辑） | 读写，随便改 |
| `tools/export_csv.py` | **只读** —— xlsx → CSV |
| `tools/check_csv.py` | **只读** —— 拿 xlsx 交叉验证 CSV |
| `tools/refresh_release_copy.py` | 唯一例外，且**必须带 `--i-am-human` 才会动** —— 从人工维护的原件重建发布副本 |
| CI / 其它任何脚本 | **只读** |

### 三条护栏

1. **commit-msg 钩子**（`.githooks/commit-msg`）—— 每个 clone 启用一次：

   ```powershell
   git config core.hooksPath .githooks
   ```

   改了 xlsx 但提交信息里没有 `[handmade-xlsx]` 标记，就拦下这次提交。
   （用 `commit-msg` 而不是 `pre-commit`：提交信息文件是作为参数传进钩子的，`-m` 和编辑器两条路都拿得到。）
2. **CI 守卫** —— `check-csv.yml` 第一步会对比本次 push 里的 `frocloud.xlsx`：
   有改动且提交信息不带 `[handmade-xlsx]`，直接让 CI 红掉。
3. **`.gitattributes`** —— 把 xlsx 声明为 binary，不让 Git 做行级 diff / 自动合并
   （它本质是个 zip，行级 diff 只会产生垃圾）。

于是日常月更变成：

```powershell
# 1) 人工在 WPS / Excel 里改 frocloud.xlsx —— 只动这一个文件
# 2) 导出 CSV（只读 xlsx）
python tools/export_csv.py
# 3) 校验
python tools/check_csv.py
# 4) 提交时带上标记（两个标记的先后顺序无所谓）
git commit -m "data-2026-11 (prerelease) [handmade-xlsx]"
```

---

## 📊 八张工作表

| # | 工作表 | 内容 | 对应 CSV |
|---|---|---|---|
| 0 | `说明` | 数据来源、价格口径、单位与币种、字段字典、工作表索引、授权与免责 | ——（说明不是数据） |
| 1 | `GPU天梯图` | 显卡性能分层，按 3DMark 的 TIME SPY / Port Royal / Steel Nomad 分项与总分排序 | `data/gpu-tier.csv` |
| 2 | `桌面端CPU天梯图` | 桌面 CPU 性能排序 | `data/cpu-tier.csv` |
| 3 | `笔记本CPU天梯图` | 移动端 CPU 排序（Ultra、AI Max、HX 系列等） | `data/laptop-cpu-tier.csv` |
| 4 | `显卡行情` | 在售显卡月度价格（2025-01 ~ 2026-10） | `data/gpu-prices.csv` |
| 5 | `CPU行情` | 在售 CPU 月度价格（2025-01 ~ 2026-10） | `data/cpu-prices.csv` |
| 6 | `内存行情` | 内存、固态、机械硬盘的每 GB 单价（2025-08 ~ 2026-10） | `data/memory-prices.csv` |
| 7 | `显卡品牌` | 品牌与产品线对照 | `data/gpu-brands.csv` |

另有两张**私有工作表**（`50系显卡用料`、`机箱散热电源`）不随本工作簿发布，单独归档，不计入上面的编号。归档位置（本机、不入库）：`../备份/frocloud-私有表-20261008.xlsx`；归档时保留了它们原本的「隐藏」状态，在 WPS / Excel 里右键工作表标签 →「取消隐藏」即可查看。拆分前的完整 9 表原件在 `../备份/frocloud-拆分前备份-20261008.xlsx`。

「天梯图」的写法不是堆跑分，而是一把五档的实用尺子：

```text
胜任  →  好用  →  能用  →  可运行  →  无法使用
```

不问跑分有多高，只问**能不能跑得动你要跑的东西**。

---

## 🗂 data/ 里有什么（CSV 字段字典）

CSV 是**长表**（一行一个事实，时间放字段），不是把 Excel 的宽表照搬过来 —— 这样每次月更只会新增几十行，**diff 本身就是变更日志**。

| 文件 | 行数 | 说明 |
|---|---|---|
| `gpu-tier.csv` | 120 | 显卡性能分层 |
| `cpu-tier.csv` | 54 | 桌面 CPU |
| `laptop-cpu-tier.csv` | 72 | 笔记本 CPU |
| `gpu-prices.csv` | 469 | 显卡月度价格（含 2026-07 下旬快照） |
| `cpu-prices.csv` | 774 | CPU 月度价格 |
| `memory-prices.csv` | 61 | 内存 / 固态 / 机械硬盘每 GB 单价 |
| `gpu-brands.csv` | 32 | 品牌 × 产品线 × 六档定位（AMD / Intel 分区各自的表头行已排除） |

### 价格类（`*-prices.csv`）

| 字段 | 含义 |
|---|---|
| `date` | `YYYY-MM`。**表头语义就是"月份"，年份写在 xlsx 的上一行**；`2026-07-下旬` 是「7 月下旬」那个非月份快照列 |
| `category` | `显卡` / `CPU` / `内存 DDR4` / `固态 PCIE5.0` / `机械硬盘 HDD` … |
| `model` | 型号。内存 / 存储类这里是大类（`内存`、`固态`、`机械硬盘`） |
| `spec` | 规格。显卡是核心代号（`RDNA4 TSMC 4nm 2025`）；内存 / 存储是容量或聚合标签（`16G×2`、`AVG`、`MAX`、`MIN`） |
| `price_cny` | 价格。显卡 / CPU 是**元/件**；内存 / 存储是**元每 GB**（1GB = 1000MB）。**不带货币符号**，纯数字 |
| `channel` | **目前一律留空**。原表里没有记录渠道（京东自营 / 淘宝 / 闲鱼…），这是已知缺口，见「已知局限」 |
| `note` | 备注。目前只用于标注 `7 月下半月快照` |

### 天梯图类

| 文件 | 字段 |
|---|---|
| `gpu-tier.csv` | `tier, vendor, series, model, score_timespy, score_portroyal, score_timespy_2, score_steelnomad, score_total` |
| `cpu-tier.csv` / `laptop-cpu-tier.csv` | `tier, vendor, platform, model, cores, threads, score_cpumark, score_single, note` |
| `gpu-brands.csv` | `vendor_group, tier, brand, 入门(丐版), 低端, 中端, 高端, 旗舰, 超旗舰` |

- `tier` 就是那五档（胜任 / 好用 / 能用 / 可运行 / 无法使用）—— **这是原创判断，是源数据**；`cpu-tier.csv` 的 `tier` 用的是桌面 CPU 表的档位（旗舰/顶级 → 高端 → 中高端 → 中端 → 入门）。笔记本 CPU 表原表没有档位列，故留空。
- `gpu-tier.csv` 的 `tier` **是稀疏的**：原表只在 9 行上写了档位（U8 `胜任`、U10 `好用`、U11 `能用`、U12 `可运行`、U13–U18 `无法使用`），其余行的档位由「该行以上最近的档位标签」决定 —— 也就是同一档位块的每一行都会拿到同一个标签。所以 115 行有档位、5 行为空（PRO6000 / 5090 / 5090D / 5090DV2 / 4090 位于第一个标签之前，原表确实没给档位）。**空就是空，不替它编一个档位。**
- `score_timespy_2` 对应 xlsx 里 NVIDIA 分区的第二个 TIME SPY 列（J 列），不是重复列。
- `series` / `platform` 来自 xlsx 的**两行表头**（第一行厂商、第二行产品线/世代），例如 `50系`、`ZEN5 9000系 · 2024`、`HX · Ultra200/Plus`。

### 几个约定

- 编码 **UTF-8 with BOM**（`utf-8-sig`），Windows 双击用 Excel 打开不会乱码。
- 文本不允许以 `=` `+` `-` `@` 开头（防公式注入）；含逗号的字段自动加引号。
- **派生列不进 CSV**：`涨幅`、`性能/价格`、内存的 `AVG / MAX / MIN` 都由脚本或校验脚本按原始价格现算。它们留在 xlsx 里。
- 原表里凡是空着的格，CSV 里也是空 —— 不补 0、不猜测、不用上一行的值填充。
- **唯一的例外是合并单元格的标签**：合并段的空白不是"缺数据"，而是"这个标签适用于整段"，导出时必须物化到该段每一行（例如「显卡品牌」的 `B3:B6 = 一线`，32 行里 26 行靠这个规则拿到分级）。
  合并段**锚点本身就是空的**（例如 Intel 区 `B32:B37` 没写分级），物化后仍然是空 —— 那才是真空白，如实留空。
  这条规则由 `tools/test_materialize.py` 守着（真实数据不依赖它，用现造的小工作簿回归）。

---

## 🧭 怎么用

1. 先在「天梯图」里定位目标档位 —— 比如"能跑 3A 中画质"或"够用就行"
2. 再去 `显卡行情` / `CPU行情` / `内存行情` 按预算挑具体型号
3. 同档位之间的差异，看 `显卡品牌`
4. 想用程序处理数据，直接读 `data/*.csv`（字段见上一节）

---

## 🔁 月更流程

```powershell
# 1) 手工美化 xlsx（流程完全不变）
# 2) 导出 CSV —— 遇到没登记过的表头列会直接报错并指出是哪一列，绝不静默丢弃
python tools/export_csv.py
# 3) 校验：列名 / 日期单调 / 价格是数字 / 无空行 / 表数 / 编码 / 公式
python tools/check_csv.py
# 4) 一次月更 = 一次提交；提交信息以 (prerelease) 结尾，CI 就会跑这一套
git add -A; git commit -m "data-2026-11 (prerelease)"
# 5) 打 tag 并把 xlsx 作为附件发 Release
git tag data-2026-11; git push --tags
```

`check_csv.py` 就是这套东西的 CI：失败会返回**非零退出码**。仓库里已挂好 `.github/workflows/check-csv.yml`：

- **触发**：提交信息**含 `(prerelease)`** 的 push（例如 `git commit -m "data-2026-11 (prerelease) [handmade-xlsx]"`），或在 Actions 页面手动 `Run workflow`。
- **跑什么**：**xlsx 守卫**（机器禁碰工作簿）→ 导出 → 合并单元格物化回归测试 → 校验 CSV → 检查 xlsx 与 CSV 是否同步（改了 xlsx 却没导出 CSV 会红）→ 数据新鲜度（超过 45 天未更新只给 warning，不红）。

**改了 xlsx 的表头怎么办？** `export_csv.py` 会停下并打印形如
`显卡行情：第 2 行出现未映射的表头列 AB=新列名 —— 请先在 export_csv.py 里显式登记`
的提示 —— 这是故意的：新列必须显式决定「进哪个字段 / 归为派生列 / 明确丢弃」，不允许它悄悄消失。

### 关于「涨幅」
`涨幅 =（当月价 − 表内历史最低价）÷ 表内历史最低价 × 100%`。历史上这张表的 17 条涨幅公式里，基准列取的是 N 列或 O 列（即"当年 8 月或 9 月价"），并不总是真正的历史最低价 —— 这两者不一致时 `check_csv.py` 会以 NOTE 提示。要不要把口径改成严格的"表内历史最低价"，见 ISSUE。

---

## ⚠️ 读者须知

### 数据截止日 2026.10.2
（各张表实际更新到的月份略有差异，以「说明」表里的工作表索引为准）

### 数据采集方式 
- 显卡、CPU、内存：个人搜索为主，使用b站up主“和微论件”《不能碰》系列“芝士华莱士”《显卡日报》频道的信息辅助验证。
- 和微论件b站链接：https://space.bilibili.com/297991412
- 芝士华莱士b站链接：https://space.bilibili.com/22697887
### 价格口径
全新卡，个人购买途径（电商平台等），取不同店铺在售最低价，**考虑**百亿补贴、618/双十一折扣、店家折扣，目的是贴合用户所花费的真实价格。
### 单位与币种
- 显卡、CPU：元（RMB）
- 内存、存储：元每GB（RMB，1GB=1000MB）
### 字段字典
- 涨幅计算方法：(当前月价格-表格中历史最低价)/表格中历史最低价*100%
- 用料来源：来自b站up“51972”“和微论件”的相关资料。本人为爱发电，无力购买各款显卡进行测试，如有错误敬请指正。
### 已知局限
本人为DIY发烧友，并非专业测试团队，跑分和用料数据均非自行测量，仅供参考，不建议以本仓库作为数据检索来源。如使用责任自负（见LICENSE）

- **没有渠道**：CSV 的 `channel` 一栏目前是空的 —— 原表只记了"取各店铺在售最低价"，没有区分京东自营 / 第三方 / 淘宝 / 闲鱼，也没区分是否含运费。这是当前最大的口径缺口，往后会补。
- **各表截止月不完全一致**：以「说明」表里的工作表索引为准。
- **型号名是手写的**：像 `U7285K`（Ultra 7 285K）、`R99950X3D`（Ryzen 9 9950X3D）这类简写沿用原表，CSV 未做规范化。

由于表格手搓，输入错误在所难免，修订也不免挂一漏万，烦请读者指正：请到 [Issues](https://github.com/x1shang/frocloud-DIYPCmarket/issues) 提，谢谢。
### 授权与免责
见 [LICENSE](LICENSE)（数据 CC BY 4.0；第三方跑分来源与免责声明同在其中）

> 价格随渠道时间波动，仅供装机参考，不构成购买建议

---

## 📄 更新日志

- **2026-10-08** —— 补齐数据层：
  - 新增 **`data/` 与 7 个长表 CSV**，由 `tools/export_csv.py` 从 xlsx 生成；新增 `tools/check_csv.py` 校验脚本。
  - 新增 **`说明` 工作表**（放在最前）：来源 / 口径 / 截止日 / 字段字典 / 工作表索引 / 授权与免责。
  - 原 9 张表中，`50系显卡用料`、`机箱散热电源` 两张**私有表移出**并单独归档，不再随工作簿发布。工作簿现为 **8 张表**。
  - 新增 `LICENSE`（CC BY 4.0 + 第三方数据来源 + 免责）。
  - 新增 `.github/workflows/check-csv.yml`：push / PR 自动跑导出与校验。
  - 修正 README 与文件不一致的表数、表名与列表。

