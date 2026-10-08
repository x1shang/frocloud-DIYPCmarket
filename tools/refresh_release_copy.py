# -*- coding: utf-8 -*-
"""
frocloud · DIYPCmarket —— refresh_release_copy.py

【机器写入 frocloud.xlsx 的唯一合法出口，且必须人工确认】

规则：仓库里的 `frocloud-DIYPCmarket/frocloud.xlsx` 是**纯手搓**的设计稿，
任何自动化流程都不许碰它。但发布用的 xlsx（Release 附件）必须是「说明 + 7 张数据表」
的那一份 —— 于是需要一个受控的、显式的动作来从手搓原件生成发布副本。

本脚本做的事：
    读 备份/frocloud-拆分前备份-YYYYMMDD.xlsx（人工维护的 9 表原件）
    → 生成 8 表的发布副本 → 覆盖仓库里的 frocloud.xlsx
    → 顺带把两张私有表单独归档

它**故意**要求显式确认，避免被人顺手跑：
    python tools/refresh_release_copy.py --i-am-human

日常月更流程（全在仓库里）：
    1. 人工在 WPS / Excel 里改 frocloud.xlsx（加月份列、改价格、调美化）—— 只动这一个文件
    2. python tools/export_csv.py          # xlsx → data/*.csv（单向，只读 xlsx）
    3. python tools/check_csv.py           # 校验

只有当你改了「工作簿的表结构」（增删工作表、改两张私有表）时，才需要跑本脚本。
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BUILDER = os.path.join(ROOT, ".work", "build_doc_sheet.py")
SRC_BAK = os.path.join(ROOT, "备份")
REPO_XLSX = os.path.join(ROOT, "frocloud-DIYPCmarket", "frocloud.xlsx")


def find_source_backup():
    if not os.path.isdir(SRC_BAK):
        return None
    cands = [f for f in os.listdir(SRC_BAK)
             if f.startswith("frocloud-拆分前备份-") and f.endswith(".xlsx")]
    if not cands:
        return None
    cands.sort()
    return os.path.join(SRC_BAK, cands[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-am-human", action="store_true",
                    help="必须显式声明：本次写入由人发起")
    args = ap.parse_args()

    print("=" * 74)
    print("⚠ 这个脚本会写入仓库里的 frocloud.xlsx")
    print("  规则：workbook 是纯手搓的，机器只准读。本脚本是唯一的例外，")
    print("  且必须在人工确认后运行。")
    print("=" * 74)

    if not args.i_am_human:
        print()
        print("已中止：没有 --i-am-human。")
        print("如果你**确实**要按人工维护的原件重建发布副本，请显式运行：")
        print("    python tools/refresh_release_copy.py --i-am-human")
        return 2

    src = find_source_backup()
    if not src:
        print("\n找不到人工维护的原件（备份/frocloud-拆分前备份-YYYYMMDD.xlsx）。")
        print("请先把它放好 —— 仓库里的 frocloud.xlsx 是它的产物，不能反过来当源。")
        return 1

    if not os.path.exists(BUILDER):
        print("\n找不到 %s（工作簿手术脚本在 .work/ 下，不入库）。" % BUILDER)
        return 1

    print("\n源（人工维护）：%s" % os.path.relpath(src, ROOT))
    print("目标（仓库）：  %s" % os.path.relpath(REPO_XLSX, ROOT))
    print()
    r = subprocess.run([sys.executable, BUILDER], cwd=os.path.dirname(BUILDER))
    if r.returncode != 0:
        return r.returncode

    print()
    print("接下来请务必跑一遍：")
    print("    python tools/export_csv.py")
    print("    python tools/check_csv.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
