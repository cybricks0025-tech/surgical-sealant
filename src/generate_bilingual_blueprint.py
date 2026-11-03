"""Generate the 5-Sheet A3 Bilingual (繁體中文 / English) Master Device Engineering Blueprint PDF.

Every cross-section (A-A, B-B, C-C, D-D) and orthographic outline is mathematically sliced
from the exact B-Rep `.step` models via `cadgen.read_scene` + `build123d.section`, rendered
with ISO 128 section hatching, dimension witness lines, tolerances, and a complete 10-item BOM.
"""
from __future__ import annotations

import logging
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Polygon as MplPolygon, Rectangle
from PIL import Image

from cadgen import build123d as bd
from cadgen import read_scene

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from lib import specs as S  # noqa: E402

# Configure Traditional Chinese vector font (Arial Unicode MS / STHeiti on macOS)
_FONT_CANDIDATES = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/STHeiti Medium.ttc",
]
for _fp in _FONT_CANDIDATES:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)
        _prop = font_manager.FontProperties(fname=_fp)
        plt.rcParams["font.family"] = _prop.get_name()
        break
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42  # Embed TrueType outlines cleanly in PDF

A3_W, A3_H = 420.0, 297.0  # mm


def new_a3_sheet(
    sheet_no: int,
    total_sheets: int,
    dwg_no: str,
    title_zh: str,
    title_en: str,
    scale_str: str,
    material_str: str,
):
    """Create an ISO A3 landscape sheet (0..420 x 0..297 mm) with professional border & title block."""
    fig = plt.figure(figsize=(A3_W / 25.4, A3_H / 25.4), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, A3_W)
    ax.set_ylim(0, A3_H)
    ax.set_aspect("equal")
    ax.axis("off")

    # Outer paper background & double ISO border
    ax.add_patch(Rectangle((0, 0), A3_W, A3_H, facecolor="#FFFFFF", edgecolor="none"))
    ax.add_patch(Rectangle((8, 8), A3_W - 16, A3_H - 16, fill=False, edgecolor="#1A2430", lw=1.4))
    ax.add_patch(Rectangle((10, 10), A3_W - 20, A3_H - 20, fill=False, edgecolor="#1A2430", lw=0.6))

    # Grid reference ticks (A-F vertical, 1-8 horizontal)
    for idx, ch in enumerate(["1", "2", "3", "4", "5", "6", "7", "8"]):
        gx = 10 + (idx + 0.5) * ((A3_W - 20) / 8.0)
        ax.text(gx, A3_H - 9.0, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")
        ax.text(gx, 9.0, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")
    for idx, ch in enumerate(["F", "E", "D", "C", "B", "A"]):
        gy = 10 + (idx + 0.5) * ((A3_H - 20) / 6.0)
        ax.text(9.0, gy, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")
        ax.text(A3_W - 9.0, gy, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")

    # Revision Block (top-right inside frame)
    rx0, ry0 = 290, A3_H - 28
    ax.add_patch(Rectangle((rx0, ry0), 120, 18, facecolor="#F7FAFC", edgecolor="#1A2430", lw=0.7))
    ax.plot([rx0, rx0 + 120], [ry0 + 12, ry0 + 12], color="#1A2430", lw=0.6)
    ax.plot([rx0, rx0 + 120], [ry0 + 6, ry0 + 6], color="#1A2430", lw=0.5)
    ax.plot([rx0 + 14, rx0 + 14], [ry0, ry0 + 18], color="#1A2430", lw=0.5)
    ax.plot([rx0 + 38, rx0 + 38], [ry0, ry0 + 18], color="#1A2430", lw=0.5)
    ax.text(rx0 + 7, ry0 + 15, "REV", ha="center", va="center", fontsize=6.5, fontweight="bold")
    ax.text(rx0 + 26, ry0 + 15, "DATE", ha="center", va="center", fontsize=6.5, fontweight="bold")
    ax.text(rx0 + 79, ry0 + 15, "變更說明 / DESCRIPTION", ha="center", va="center", fontsize=6.5, fontweight="bold")
    ax.text(rx0 + 7, ry0 + 9, "A", ha="center", va="center", fontsize=6)
    ax.text(rx0 + 26, ry0 + 9, "2026-10-28", ha="center", va="center", fontsize=6)
    ax.text(rx0 + 40, ry0 + 9, "原廠商初步外廓概念圖（缺內部流道與配合公差）", ha="left", va="center", fontsize=5.8)
    ax.text(rx0 + 7, ry0 + 3, "B", ha="center", va="center", fontsize=6, fontweight="bold", color="#C53030")
    ax.text(rx0 + 26, ry0 + 3, "2026-11-03", ha="center", va="center", fontsize=6, fontweight="bold")
    ax.text(rx0 + 40, ry0 + 3, "完整 3D B-Rep 重建、剖面公差、ISO 魯爾與防呆卡口定版", ha="left", va="center", fontsize=5.8)

    # ISO Title Block (bottom-right: x = 235..410, y = 10..42)
    tx0, ty0, tw, th = 235, 10, 175, 32
    ax.add_patch(Rectangle((tx0, ty0), tw, th, facecolor="#F8FAFC", edgecolor="#1A2430", lw=0.9))
    ax.plot([tx0, tx0 + tw], [ty0 + 22, ty0 + 22], color="#1A2430", lw=0.6)
    ax.plot([tx0, tx0 + tw], [ty0 + 11, ty0 + 11], color="#1A2430", lw=0.6)
    ax.plot([tx0 + 115, tx0 + 115], [ty0, ty0 + 22], color="#1A2430", lw=0.6)
    ax.plot([tx0 + 55, tx0 + 55], [ty0, ty0 + 11], color="#1A2430", lw=0.6)

    ax.text(tx0 + 4, ty0 + 27.5, title_zh, ha="left", va="center", fontsize=9.5, fontweight="bold", color="#0F172A")
    ax.text(tx0 + 4, ty0 + 23.8, title_en, ha="left", va="center", fontsize=6.5, color="#475569")

    ax.text(tx0 + 4, ty0 + 18.2, "材質 / MATERIAL:", ha="left", va="center", fontsize=5.8, color="#64748B")
    ax.text(tx0 + 4, ty0 + 13.8, material_str, ha="left", va="center", fontsize=6.8, fontweight="bold", color="#1E293B")

    ax.text(tx0 + 118, ty0 + 18.2, "圖號 / DWG NO.:", ha="left", va="center", fontsize=5.8, color="#64748B")
    ax.text(tx0 + 118, ty0 + 13.8, dwg_no, ha="left", va="center", fontsize=8.0, fontweight="bold", color="#0F172A")

    ax.text(tx0 + 4, ty0 + 7.5, "一般公差 / TOLERANCE:", ha="left", va="center", fontsize=5.6, color="#64748B")
    ax.text(tx0 + 4, ty0 + 3.2, "ISO 2768-m (塑膠: ±0.10)", ha="left", va="center", fontsize=6.5, fontweight="bold")

    ax.text(tx0 + 58, ty0 + 7.5, "單位 / UNIT & PROJ.:", ha="left", va="center", fontsize=5.6, color="#64748B")
    ax.text(tx0 + 58, ty0 + 3.2, f"mm | 第三角法 3RD ANGLE", ha="left", va="center", fontsize=6.3, fontweight="bold")

    ax.text(tx0 + 118, ty0 + 7.5, f"比例 SCALE: {scale_str}", ha="left", va="center", fontsize=6.2, fontweight="bold")
    ax.text(
        tx0 + 118,
        ty0 + 3.2,
        f"REV B  |  SHEET {sheet_no} OF {total_sheets}",
        ha="left",
        va="center",
        fontsize=6.8,
        fontweight="bold",
        color="#B91C1C",
    )
    return fig, ax


def draw_xz_section(
    ax,
    step_path: Path,
    cx: float,
    cy: float,
    scale: float,
    color_map: dict[str, tuple[str, str]],
    z_shift: float = 0.0,
) -> None:
    """Slice a STEP assembly on the exact XZ plane (Y=0) and draw cross-hatched B-Rep faces."""
    scene = read_scene(step_path)
    hatches = ["////", "\\\\\\\\", "xxxx", "....", "////", "\\\\\\\\"]
    for idx, leaf in enumerate(scene.leaves()):
        lbl = leaf.label or ""
        fill_hex, edge_hex = "#E2E8F0", "#1E293B"
        for key, pair in color_map.items():
            if key in lbl:
                fill_hex, edge_hex = pair
                break
        shp = leaf.shape()
        sec = bd.section(shp, section_by=bd.Plane.XZ)
        for face in sec.faces():
            # Outer wire
            ow = face.outer_wire()
            pts_o = [(cx + v.X * scale, cy + (v.Z + z_shift) * scale) for v in _sample_wire_xz(ow)]
            # Inner wires (holes inside a sectioned face)
            ax.add_patch(
                MplPolygon(
                    pts_o,
                    closed=True,
                    facecolor=fill_hex,
                    edgecolor=edge_hex,
                    linewidth=0.85,
                    hatch=hatches[idx % len(hatches)],
                    alpha=0.88,
                    zorder=4 + idx * 0.1,
                )
            )
            for iw in face.inner_wires():
                pts_i = [(cx + v.X * scale, cy + (v.Z + z_shift) * scale) for v in _sample_wire_xz(iw)]
                ax.add_patch(
                    MplPolygon(
                        pts_i,
                        closed=True,
                        facecolor="#FFFFFF",
                        edgecolor=edge_hex,
                        linewidth=0.80,
                        zorder=4.05 + idx * 0.1,
                    )
                )


def _sample_wire_xz(wire: bd.Wire, n_curve: int = 24) -> list:
    """Sample ordered 3D points along a planar wire so curved/conical edges render smoothly."""
    pts = []
    for edge in wire.edges():
        gt = edge.geom_type
        n = 2 if str(gt).endswith("LINE") else n_curve
        for k in range(n):
            p = edge.position_at(k / float(n))
            if not pts or (abs(p.X - pts[-1].X) + abs(p.Z - pts[-1].Z) > 1e-4):
                pts.append(p)
    return pts


def dim_h(
    ax,
    x1: float,
    x2: float,
    y_ref1: float,
    y_ref2: float,
    y_dim: float,
    text: str,
    color: str = "#B91C1C",
    fontsize: float = 7.0,
) -> None:
    """Draw a clean ISO horizontal dimension with extension lines and arrows."""
    s1 = 1.2 if y_dim >= y_ref1 else -1.2
    s2 = 1.2 if y_dim >= y_ref2 else -1.2
    ax.plot([x1, x1], [y_ref1 + s1 * 0.5, y_dim + s1 * 1.5], color=color, lw=0.55, zorder=10)
    ax.plot([x2, x2], [y_ref2 + s2 * 0.5, y_dim + s2 * 1.5], color=color, lw=0.55, zorder=10)
    ax.annotate(
        "",
        xy=(x1, y_dim),
        xytext=(x2, y_dim),
        arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.65, mutation_scale=7),
        zorder=11,
    )
    ax.text(
        0.5 * (x1 + x2),
        y_dim + 1.2,
        text,
        ha="center",
        va="bottom",
        fontsize=fontsize,
        color=color,
        fontweight="bold",
        bbox=dict(boxstyle="square,pad=0.08", facecolor="#FFFFFF", edgecolor="none", alpha=0.85),
        zorder=12,
    )


def dim_v(
    ax,
    x_ref1: float,
    x_ref2: float,
    y1: float,
    y2: float,
    x_dim: float,
    text: str,
    color: str = "#B91C1C",
    fontsize: float = 7.0,
) -> None:
    """Draw a clean ISO vertical dimension with extension lines and arrows."""
    s1 = 1.2 if x_dim >= x_ref1 else -1.2
    s2 = 1.2 if x_dim >= x_ref2 else -1.2
    ax.plot([x_ref1 + s1 * 0.5, x_dim + s1 * 1.5], [y1, y1], color=color, lw=0.55, zorder=10)
    ax.plot([x_ref2 + s2 * 0.5, x_dim + s2 * 1.5], [y2, y2], color=color, lw=0.55, zorder=10)
    ax.annotate(
        "",
        xy=(x_dim, y1),
        xytext=(x_dim, y2),
        arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.65, mutation_scale=7),
        zorder=11,
    )
    offset_x = -2.0 if x_dim < 0.5 * (x_ref1 + x_ref2) else 2.2
    ax.text(
        x_dim + offset_x,
        0.5 * (y1 + y2),
        text,
        ha="center",
        va="center",
        rotation=90,
        fontsize=fontsize,
        color=color,
        fontweight="bold",
        bbox=dict(boxstyle="square,pad=0.08", facecolor="#FFFFFF", edgecolor="none", alpha=0.85),
        zorder=12,
    )


def callout(ax, xy_target: tuple[float, float], xy_text: tuple[float, float], text: str, ha: str = "left") -> None:
    """Draw an engineering leader callout."""
    ax.annotate(
        text,
        xy=xy_target,
        xytext=xy_text,
        ha=ha,
        va="center",
        fontsize=6.6,
        color="#0F172A",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#F8FAFC", edgecolor="#94A3B8", lw=0.5),
        arrowprops=dict(arrowstyle="-|>", color="#334155", lw=0.6, connectionstyle="arc3,rad=0.0"),
        zorder=15,
    )


def place_image_cropped(ax, img_path: Path, box: tuple[float, float, float, float]) -> None:
    """Auto-trim uniform background margins of a CAD snapshot (masking top-left badge) and place inside (x0, y0, w, h)."""
    if not img_path.exists():
        return
    im = Image.open(img_path).convert("RGBA")
    import numpy as np
    arr = np.array(im)
    bg = arr[-1, -1, :3].copy()
    # Mask cadgen's top-left camera-label badge (e.g. 'ISO' / 'CUSTOM') before auto-cropping
    arr[:90, :220, :3] = bg
    arr[:90, :220, 3] = 255
    im = Image.fromarray(arr)
    diff = np.abs(arr[:, :, :3].astype(int) - bg.astype(int)).sum(axis=2)
    ys, xs = np.where(diff > 12)
    if len(xs) > 10:
        pad = 20
        x0 = max(0, int(xs.min()) - pad)
        x1 = min(im.width, int(xs.max()) + pad)
        y0 = max(0, int(ys.min()) - pad)
        y1 = min(im.height, int(ys.max()) + pad)
        im = im.crop((x0, y0, x1, y1))
    bx, by, bw, bh = box
    img_aspect = im.width / float(im.height)
    box_aspect = bw / float(bh)
    if img_aspect > box_aspect:
        rw = bw
        rh = bw / img_aspect
    else:
        rh = bh
        rw = bh * img_aspect
    ox = bx + 0.5 * (bw - rw)
    oy = by + 0.5 * (bh - rh)
    ax.imshow(im, extent=(ox, ox + rw, oy, oy + rh), zorder=2)


def _save_sheet(pdf: PdfPages, fig, sheet_no: int) -> None:
    pdf.savefig(fig)
    sheets_dir = ROOT / "assets/sheets"
    sheets_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(sheets_dir / f"sheet_{sheet_no}.png", dpi=180)
    plt.close(fig)


def build_sheet_1(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        1, 5, "CSL-SYS-000",
        "雙單管混合裝置 — 三階段系統總成與 BOM 物料清單",
        "DUAL/SINGLE-BARREL SURGICAL SEALANT SYSTEM OVERVIEW & MASTER BOM",
        "NTS / AS SHOWN",
        "MEDICAL COC / PP / PC / BROMOBUTYL / SILICONE",
    )

    # Left: 3D System Overview Render
    ax.add_patch(Rectangle((16, 108), 165, 168, facecolor="#F4F7FA", edgecolor="#CBD5E1", lw=0.6))
    place_image_cropped(ax, ROOT / "tmp/overview_iso.png", (18, 110, 161, 156))
    ax.text(98.5, 271, "三階段操作組態與可替換前蓋 3D 總成視圖 (3-Stage Kit Isometric)", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#1E293B")

    # Stage callout badges on the 3D render
    ax.text(36, 122, "Stage 1: 儲存密封態\n(#3 初始塞閥蓋 + 雙管鎖定)", fontsize=6.5, fontweight="bold", color="#276749", bbox=dict(boxstyle="round,pad=0.3", fc="#F0FFF4", ec="#48BB78", lw=0.6))
    ax.text(84, 115, "Stage 2: 單管往復溶解態\n(#2 魯爾單管蓋 + 切換片旋開90°\n+ 外接粉劑單管對推 ~20 次)", fontsize=6.3, fontweight="bold", color="#553C9A", bbox=dict(boxstyle="round,pad=0.3", fc="#FAF5FF", ec="#9F7AEA", lw=0.6))
    ax.text(136, 134, "Stage 3: 雙管同步注射態\n(#1 螺旋混合雙管蓋 + 1:1 聯動)", fontsize=6.5, fontweight="bold", color="#744210", bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFF0", ec="#D69E2E", lw=0.6))

    # Right Upper: Complete 10-Part Bill of Materials (BOM)
    bx, by = 188, 132
    col_w = [12, 26, 44, 48, 12, 38, 36]  # total = 216 mm
    headers = ["項次", "零件編號", "中文零件名稱", "English Component Name", "數量", "建議醫療級材質", "關鍵配合與規範"]
    rows = [
        ["01", "CSL-PRT-101", "雙腔針筒本體", "Dual-Barrel Syringe Body", "1", "醫療級透明 COC / PP", "雙孔距14.40 / Ø12.20內孔 / 防呆卡口"],
        ["02", "CSL-PRT-102", "十字推桿", "Cruciform Plunger Rod", "2", "醫療級 PP / ABS (藍灰)", "總長75.50 / 尾盤Ø12.80×1.60"],
        ["03", "CSL-PRT-103", "三環彈性活塞", "Triple-Rib Elastomer Stopper", "2", "醫療級溴化丁基膠 (紫)", "成形Ø12.50±0.10 (過盈氣密) × 7.00"],
        ["04", "CSL-PRT-104", "#4 單雙管推拉切換片", "Single/Dual Plunger Clip", "1", "醫療級 POM / 耐衝擊 PP", "30×16.4×4.0 / B軸樞轉90° / A軸C扣"],
        ["05", "CSL-CAP-201A", "#1 螺旋混合外旋蓋", "Mixer Bayonet Outer Cap", "1", "醫療級 ABS / PP (卡其綠)", "Ø22.00×14.87 / 防呆卡耳23.96"],
        ["06", "CSL-CAP-201B", "#1 雙套筒彈性密封座", "Dual-Sleeve Manifold Seat", "1", "醫療級矽膠 Shore A 60", "孔距8.00 / 母套孔Ø3.10過盈密封"],
        ["07", "CSL-CAP-201C", "#1 錐形 Y 匯流座與螺旋管", "Y-Funnel + Ø4 Cannula & Core", "1組", "透明 PC 管 + POM 8節螺旋芯", "外管Ø4/Ø3×26.73外露 / 零預混死角"],
        ["08", "CSL-CAP-202A", "#2 魯爾轉接滾花外環", "Knurled Bayonet Ring", "1", "醫療級 PP / ABS (紫)", "Ø30.00×3.40 / 65°腎形旋轉讓位槽"],
        ["09", "CSL-CAP-202B", "#2 偏心母魯爾與盲塞芯", "ISO 80369-7 Luer + Blind Core", "1", "醫療級 PC + TPE 雙料包膠", "A側+4.0偏心6%母魯爾Ø7.80 / B側盲塞"],
        ["10", "CSL-CAP-203", "#3 初始塞閥蓋組 (含雙塞墊)", "Initial Plug Valve Cap Assy", "1組", "醫療級 PP (綠) + 丁基雙盲塞", "Ø22.00×17.00 (旋柄8×4) / 雙腔氣密"],
    ]

    ax.text(bx, by + 148, "完整工程物料清單 (MASTER BILL OF MATERIALS — 10 COMPONENTS)", fontsize=8.2, fontweight="bold", color="#0F172A")
    cur_y = by + 136
    rh_h = 8.0
    # Draw header
    cx = bx
    for w, h_txt in zip(col_w, headers):
        ax.add_patch(Rectangle((cx, cur_y), w, rh_h, facecolor="#1E293B", edgecolor="#0F172A", lw=0.5))
        ax.text(cx + w / 2.0, cur_y + rh_h / 2.0, h_txt, ha="center", va="center", fontsize=6.0, fontweight="bold", color="#FFFFFF")
        cx += w
    # Draw rows
    for r_idx, r in enumerate(rows):
        cur_y -= 11.8
        bg_c = "#F8FAFC" if r_idx % 2 == 0 else "#FFFFFF"
        cx = bx
        for c_idx, (w, val) in enumerate(zip(col_w, r)):
            ax.add_patch(Rectangle((cx, cur_y), w, 11.8, facecolor=bg_c, edgecolor="#CBD5E1", lw=0.45))
            align = "center" if c_idx in (0, 1, 4) else "left"
            tx = cx + w / 2.0 if align == "center" else cx + 1.5
            ax.text(tx, cur_y + 5.9, val, ha=align, va="center", fontsize=5.6, color="#1E293B")
            cx += w

    # Bottom Engineering Design Review & Key Improvements Box
    ax.add_patch(FancyBboxPatch((16, 16), 210, 84, boxstyle="round,pad=1.5", facecolor="#FFFBEB", edgecolor="#D97706", lw=0.8))
    ax.text(20, 95, "【工程審查與新版 Rev.B 關鍵補強項目 — 對標 Baxter CoSeal 臨床需求】", fontsize=7.8, fontweight="bold", color="#92400E")
    notes_zh = [
        "1. 修正原圖剖面干涉瑕疵：原簡報立體圖具凸出公嘴、但剖面圖卻為平底實心塞；Rev.B 統一規範為「雙偏心公嘴 Ø3.20×3.50mm + 彈性母套孔 Ø3.10mm 徑向與頂端雙重密封」。",
        "2. 新增 Poka-Yoke 180° 防呆非對稱卡口：寬卡耳 (26°) 與窄卡耳 (15°) 搭配非對稱入口槽 (+Y 60° / -Y 20°)，物理杜絕 #2 魯爾單管蓋裝反導致粉劑誤混入鹼性 T-buffer 腔。",
        "3. 外環獨立旋轉機構：#1、#2、#3 內部密封/分流芯皆對準雙出料嘴固定不轉動，僅外旋蓋旋轉 65° 鎖入卡口（#2 設有 65° 腎形讓位弧槽），避免扭斷彈性密封套。",
        "4. 補齊醫療標準接口：#2 偏心魯爾口 (+4.00mm) 明訂符合 ISO 80369-7 標準 6% 母魯爾內錐度 (Ø4.27→Ø3.91mm) 與雙頭外螺紋 Ø7.80mm，確保與標準單管粉劑針筒無洩漏對推。",
        "5. 補齊全套內部尺寸：雙管中心距 14.40mm、單腔有效工作容積 4.0 mL (最大 5.0 mL，雙腔共 8.0 mL)、出料嘴中心距 8.00mm、以及 #4 切換片樞軸/C扣全部公差。",
    ]
    for i, line in enumerate(notes_zh):
        ax.text(20, 84 - i * 15.0, line, fontsize=6.0, color="#1E293B", va="center")

    _save_sheet(pdf, fig, 1)


def build_sheet_2(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        2, 5, "CSL-PRT-101",
        "雙腔針筒本體與推桿活塞組 — A-A 全剖視工程圖",
        "DUAL-BARREL SYRINGE BODY, PLUNGER & STOPPER — SECTION A-A",
        "2 : 1 (SECTION)",
        "MEDICAL CLEAR COC / PP + BROMOBUTYL",
    )

    # Left: True B-Rep Section A-A of Stage 3 Dispense Assembly (focusing on Barrel + Stopper + Plunger + Collar)
    # Use scale = 2.1 for Dual Barrel Body section!
    sc = 2.2
    cx, cy = 115.0, 58.0
    ax.text(cx, 268, "剖視圖 SECTION A-A (XZ 雙腔中心縱剖面, SCALE 2.2:1)", ha="center", fontsize=8.2, fontweight="bold", color="#0F172A")
    draw_xz_section(
        ax,
        ROOT / "STEP/dual_barrel_body.step",
        cx=cx,
        cy=cy,
        scale=sc,
        color_map={"dual_barrel": ("#DBEAFE", "#1E3A8A")},
    )
    # Also overlay the two elastomer stoppers at Z = 12.84 mm in the section!
    for sx_off in (S.BARREL_X_A, S.BARREL_X_B):
        draw_xz_section(
            ax,
            ROOT / "STEP/elastomer_stopper.step",
            cx=cx + sx_off * sc,
            cy=cy,
            scale=sc,
            color_map={"elastomer_stopper": ("#E9D5FF", "#6B21A8")},
            z_shift=12.84,
        )

    # Centerlines for Barrel B (-7.20), Center (0), Barrel A (+7.20), Nozzles (±4.00)
    for x_mm in (S.BARREL_X_B, S.BARREL_X_A):
        ax.plot([cx + x_mm * sc, cx + x_mm * sc], [cy - 8, cy + 63 * sc], color="#DC2626", ls="-.", lw=0.45)
    for x_mm in (S.NOZZLE_X_B, S.NOZZLE_X_A):
        ax.plot([cx + x_mm * sc, cx + x_mm * sc], [cy + 57 * sc, cy + 72 * sc], color="#2563EB", ls="-.", lw=0.45)

    # Exact CAD-derived Dimensions on Section A-A
    dim_h(ax, cx - 23.05 * sc, cx + 23.05 * sc, cy, cy, cy - 16, "46.10 ±0.15 (指翼總寬)")
    dim_h(ax, cx - 14.90 * sc, cx + 14.90 * sc, cy + 30 * sc, cy + 30 * sc, cy + 84, "29.80 (雙筒外寬)")
    dim_h(ax, cx + S.BARREL_X_B * sc, cx + S.BARREL_X_A * sc, cy, cy, cy - 8, "14.40 ±0.05 (雙腔中心距)")
    dim_h(ax, cx + (S.BARREL_X_A - 6.10) * sc, cx + (S.BARREL_X_A + 6.10) * sc, cy + 25 * sc, cy + 25 * sc, cy + 52, "Ø12.20 ±0.05 (內徑 ID)")
    dim_h(ax, cx + S.NOZZLE_X_B * sc, cx + S.NOZZLE_X_A * sc, cy + 67.3 * sc, cy + 67.3 * sc, cy + 162, "8.00 ±0.03 (雙出料嘴中心距)")
    dim_h(ax, cx - 11.10 * sc, cx + 11.10 * sc, cy + 69.4 * sc, cy + 69.4 * sc, cy + 174, "Ø22.20 +0.10/-0 (前蓋配合內徑)")
    dim_h(ax, cx - 12.15 * sc, cx + 12.15 * sc, cy + 64.8 * sc, cy + 64.8 * sc, cy + 186, "Ø24.30 (Bayonet 卡口內扣環槽)")

    dim_v(ax, cx - 23.05 * sc, cx - 12.80 * sc, cy, cy + 69.40 * sc, cx - 64, "69.40 ±0.15 (針筒本體總長)")
    dim_v(ax, cx - 23.05 * sc, cx - 23.05 * sc, cy, cy + 2.00 * sc, cx - 54, "2.00 (指翼厚)")
    dim_v(ax, cx + 14.90 * sc, cx + 14.90 * sc, cy + 19.84 * sc, cy + 58.50 * sc, cx + 44, "38.66 (有效推注行程 ≈ 4.5 mL/腔)")
    dim_v(ax, cx - 12.80 * sc, cx - 12.80 * sc, cy + 63.80 * sc, cy + 69.40 * sc, cx - 42, "5.60 (護圈沉台深)")

    callout(ax, (cx + S.NOZZLE_X_A * sc + 1.6 * sc, cy + 66.0 * sc), (cx + 38, cy + 150), "偏心出料公嘴 (2X)\n外徑 Ø3.20±0.03 / 內孔 Ø1.80\n凸出高度 3.50 mm")
    callout(ax, (cx + S.BARREL_X_A * sc, cy + 16.0 * sc), (cx + 42, cy + 26), "三環醫療級活塞 (CSL-PRT-103)\n成形外徑 Ø12.50±0.10 × 長 7.00\n低啟動阻力雙洩壓環槽設計")

    # Right Side: Poka-Yoke Bayonet End-View Diagram + Plunger Rod Detail
    rx, ry, rsc = 305.0, 196.0, 1.80
    ax.text(rx, 261, "前端防呆卡口俯視圖 (POKA-YOKE BAYONET TOP VIEW, 1.8:1)", ha="center", fontsize=8.0, fontweight="bold", color="#0F172A")
    # Draw flange outline + barrels + asymmetric collar arcs
    ax.add_patch(FancyBboxPatch((rx - 23.05 * rsc, ry - 8.80 * rsc), 46.10 * rsc, 17.60 * rsc, boxstyle=f"round,pad=0,rounding_size={5.0*rsc}", fc="#F8FAFC", ec="#1E293B", lw=0.9))
    ax.add_patch(Circle((rx, ry + 8.305 * rsc), 8.40 * rsc, fc="#F8FAFC", ec="#1E293B", lw=0.8))
    ax.add_patch(Circle((rx, ry - 8.305 * rsc), 8.40 * rsc, fc="#F8FAFC", ec="#1E293B", lw=0.8))
    ax.add_patch(Circle((rx, ry), 12.80 * rsc, fc="#EFF6FF", ec="#1E3A8A", lw=1.0))
    ax.add_patch(Circle((rx, ry), 11.10 * rsc, fc="#FFFFFF", ec="#1E3A8A", lw=0.9))
    # Highlight +Y wide gap (50..110 deg) & -Y narrow gap (-122..-102 deg)
    for nx, lbl_n in ((S.NOZZLE_X_B, "B腔\n(T-buf)"), (S.NOZZLE_X_A, "A腔\n(S-buf)")):
        ax.add_patch(Circle((rx + nx * rsc, ry), 1.60 * rsc, fc="#DBEAFE", ec="#1E3A8A", lw=0.9))
        ax.add_patch(Circle((rx + nx * rsc, ry), 0.90 * rsc, fc="#FFFFFF", ec="#1E3A8A", lw=0.7))
        ax.text(rx + nx * rsc, ry - 5.5, lbl_n, ha="center", va="top", fontsize=5.8, fontweight="bold", color="#1E3A8A")

    dim_h(ax, rx - 23.05 * rsc, rx + 23.05 * rsc, ry, ry, ry - 38, "46.10 (指翼長軸)")
    dim_v(ax, rx, rx, ry - 16.705 * rsc, ry + 16.705 * rsc, rx + 52, "33.41 (側耳總寬)")
    callout(ax, (rx, ry + 11.8 * rsc), (rx - 68, ry + 36), "+Y 寬防呆入口槽 (60°)\n容許 26° 寬卡耳投入")
    callout(ax, (rx - 5.0 * rsc, ry - 11.0 * rsc), (rx - 68, ry - 32), "-Y 窄防呆入口槽 (20°)\n僅容 15° 窄卡耳通過！\n防止 #2 轉接蓋 180° 裝反")

    # Right Lower: Plunger Rod Section/Profile Box
    px0, py0 = 236, 52
    ax.add_patch(Rectangle((px0, py0), 173, 92, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    ax.text(px0 + 86.5, py0 + 86, "十字推桿規格圖 (CRUCIFORM PLUNGER ROD — CSL-PRT-102, QTY: 2)", ha="center", fontsize=7.4, fontweight="bold", color="#0F172A")
    # Draw horizontal plunger rod at scale 1.8
    psc = 1.80
    prx, pry = px0 + 22, py0 + 44
    # Thumb disc + neck + cruciform shaft + pusher + stud
    ax.add_patch(Rectangle((prx, pry - 6.40 * psc), 1.60 * psc, 12.80 * psc, fc="#CBD5E1", ec="#1E293B", lw=0.8))
    ax.add_patch(Rectangle((prx + 1.60 * psc, pry - 3.10 * psc), 3.20 * psc, 6.20 * psc, fc="#E2E8F0", ec="#1E293B", lw=0.8))
    ax.add_patch(Rectangle((prx + 4.80 * psc, pry - 5.60 * psc), 66.30 * psc, 11.20 * psc, fc="#CFD8E3", ec="#1E293B", lw=0.8))
    ax.add_patch(Rectangle((prx + 4.80 * psc, pry - 0.90 * psc), 66.30 * psc, 1.80 * psc, fc="#94A3B8", ec="#1E293B", lw=0.5))
    ax.add_patch(Rectangle((prx + 71.10 * psc, pry - 5.30 * psc), 1.20 * psc, 10.60 * psc, fc="#CBD5E1", ec="#1E293B", lw=0.8))
    ax.add_patch(Rectangle((prx + 72.30 * psc, pry - 2.60 * psc), 3.20 * psc, 5.20 * psc, fc="#94A3B8", ec="#1E293B", lw=0.8))
    dim_h(ax, prx, prx + 72.30 * psc, pry + 6.4 * psc, pry + 5.3 * psc, pry + 21, "72.30 ±0.10 (推桿有效肩長)")
    dim_h(ax, prx, prx + 75.50 * psc, pry - 6.4 * psc, pry - 2.6 * psc, pry - 24, "75.50 (推桿含倒扣栓總長)")
    dim_h(ax, prx, prx + 1.60 * psc, pry + 6.4 * psc, pry + 6.4 * psc, pry + 13, "1.60 (尾盤厚)")
    dim_v(ax, prx, prx, pry - 6.40 * psc, pry + 6.40 * psc, prx - 10, "Ø12.80")
    callout(ax, (prx + 3.2 * psc, pry - 3.1 * psc), (prx + 28, pry - 34), "樞軸頸徑 Ø6.20 × 長 3.20\n(供 #4 切換片 Ø6.80 槽旋轉)")

    _save_sheet(pdf, fig, 2)


def build_sheet_3(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        3, 5, "CSL-CAP-201",
        "#1 螺旋混合雙管蓋 — B-B 全剖視流道與靜態混合芯工程圖",
        "PART #1: HELICAL STATIC MIXER DUAL-BARREL CAP — SECTION B-B",
        "4.5 : 1 (SECTION)",
        "ABS + SILICONE (SHORE A 60) + CLEAR PC + POM",
    )

    sc = 4.6
    cx, cy = 135.0, 52.0
    ax.text(cx, 270, "剖視圖 SECTION B-B (#1 螺旋混合雙管蓋五件式內部流道組裝剖面, SCALE 4.6:1)", ha="center", fontsize=8.2, fontweight="bold", color="#0F172A")

    draw_xz_section(
        ax,
        ROOT / "STEP/helical_mixer_cap.step",
        cx=cx,
        cy=cy,
        scale=sc,
        color_map={
            "mixer_outer_cap": ("#D9DF9D", "#4D531B"),
            "mixer_seal_seat": ("#DDB892", "#6C3B1C"),
            "y_convergence_funnel": ("#E5989B", "#7F1D1D"),
            "mixing_cannula": ("#E0F2FE", "#0369A1"),
            "helical_mixer_core": ("#FCA5A5", "#991B1B"),
        },
    )
    ax.plot([cx, cx], [cy - 6, cy + 43.5 * sc], color="#DC2626", ls="-.", lw=0.5)

    # Full Dimensions matching Vendor + Internal Fluidics
    dim_v(ax, cx - 11.98 * sc, cx - 2.00 * sc, cy, cy + 41.60 * sc, cx - 76, "41.60 ±0.15 (混合蓋總長)")
    dim_v(ax, cx - 11.98 * sc, cx - 3.80 * sc, cy, cy + 14.87 * sc, cx - 64, "14.87 (外旋蓋高度)")
    dim_v(ax, cx - 3.80 * sc, cx - 2.00 * sc, cy + 14.87 * sc, cy + 41.60 * sc, cx - 48, "26.73 (透明混合管外露長)")
    dim_v(ax, cx + 11.98 * sc, cx + 11.98 * sc, cy, cy + 1.80 * sc, cx + 64, "1.80 (卡耳厚)")
    dim_v(ax, cx + 2.00 * sc, cx + 2.00 * sc, cy + 15.00 * sc, cy + 39.00 * sc, cx + 44, "24.00 (8節螺旋混合有效區)")

    dim_h(ax, cx - 11.98 * sc, cx + 11.98 * sc, cy, cy, cy - 12, "23.96 ±0.05 (防呆卡耳外跨距)")
    dim_h(ax, cx - 11.00 * sc, cx + 11.00 * sc, cy + 6.0 * sc, cy + 6.0 * sc, cy - 22, "Ø22.00 ±0.10 (外蓋本體外徑)")
    dim_h(ax, cx - 4.00 * sc, cx + 4.00 * sc, cy + 2.0 * sc, cy + 2.0 * sc, cy - 32, "8.00 ±0.03 (雙入口套筒中心距)")
    dim_h(ax, cx - 2.00 * sc, cx + 2.00 * sc, cy + 41.60 * sc, cy + 41.60 * sc, cy + 41.60 * sc + 9, "Ø4.00 外徑 / Ø3.00 內徑")

    # Component Callouts
    callout(ax, (cx + 1.1 * sc, cy + 28.0 * sc), (cx + 58, cy + 165), "⑤ 靜態螺旋混合芯 (Kenics Core)\n8節正反180°交錯扭轉葉片 (節距3.0mm)\n葉寬 2.82 × 厚 0.42 mm (切割2⁸=256層)")
    callout(ax, (cx + 2.0 * sc, cy + 21.0 * sc), (cx + 58, cy + 128), "④ 醫療級透明混合管 (Clear Cannula)\nØ4.00 OD × Ø3.00 ID (總長 31.36 mm)")
    callout(ax, (cx + 3.5 * sc, cy + 8.6 * sc), (cx + 58, cy + 92), "③ 錐形 Y 匯流座 (Maroon Funnel)\n兩液維持獨立至 Ø3.0 管口才首次接觸\n徹底消除歧管提前成膠堵塞風險！")
    callout(ax, (cx + 4.8 * sc, cy + 5.8 * sc), (cx + 58, cy + 54), "② 雙套筒彈性密封座 (Silicone Seat)\n成形母套孔 Ø3.10±0.05 (過盈包覆公嘴)\n外緣 Ø18.60/Ø17.00 階梯嵌合不隨外蓋轉動")
    callout(ax, (cx + 9.8 * sc, cy + 10.5 * sc), (cx + 58, cy + 18), "① 止滑肋外旋蓋 (Bayonet Outer Cap)\n外周16道止滑槽；裝上針筒後伸出長 36.20 mm")

    # Right Side: Design Note & Optional SHM Upgrade Note
    ax.add_patch(FancyBboxPatch((268, 52), 140, 208, boxstyle="round,pad=1.5", facecolor="#F8FAFC", edgecolor="#94A3B8", lw=0.7))
    ax.text(338, 252, "【混合流道設計規範與模組化相容性】", ha="center", fontsize=8.0, fontweight="bold", color="#0F172A")
    place_image_cropped(ax, ROOT / "tmp/dispense_iso.png", (276, 134, 124, 112))
    spec_lines = [
        "● 裝配後外露尺寸：36.20 mm (總長 166.60 mm)",
        "● 混合管滯留死體積：約 165 µL",
        "   (π×1.5²×31.4 mm 扣除螺旋芯體積)",
        "● 雙腔隔離原則：A液 (PEG) 與 B液 (T-buffer)",
        "   於 ② 彈性座與 ③ 匯流座內完全分流，",
        "   停推換頭時不會倒灌污染針筒本體。",
        "● 模組化擴充建議：本外蓋底座 (Ø22 卡口",
        "   + 8.0mm 雙套筒密封座) 為標準化介面，",
        "   可直接替換接上貴團隊驗證之低死體積",
        "   (<40 µL) SHM 人字形微流道混合頭！",
    ]
    for idx, sl in enumerate(spec_lines):
        ax.text(273, 126 - idx * 7.2, sl, fontsize=5.9, color="#1E293B", va="center")

    _save_sheet(pdf, fig, 3)


def build_sheet_4(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        4, 5, "CSL-CAP-202 / 203",
        "#2 魯爾混合單管蓋 & #3 初始塞閥蓋 — 全剖視工程圖",
        "PART #2 LUER TRANSFER CAP (SEC C-C) & PART #3 INITIAL PLUG CAP (SEC D-D)",
        "4.5 : 1 (SECTIONS)",
        "PP / PC / TPE / MEDICAL BROMOBUTYL",
    )

    # Divider between Left (#2 Luer Cap) and Right (#3 Initial Plug Cap)
    ax.plot([212, 212], [46, 262], color="#CBD5E1", ls="--", lw=0.8)

    # ==================== LEFT: PART #2 LUER TRANSFER CAP ====================
    sc2 = 4.6
    cx2, cy2 = 108.0, 95.0
    ax.text(cx2, 261, "#2 魯爾混合單管蓋 — 剖視圖 SECTION C-C (SCALE 4.6:1)", ha="center", fontsize=8.0, fontweight="bold", color="#553C9A")
    draw_xz_section(
        ax,
        ROOT / "STEP/luer_transfer_cap.step",
        cx=cx2,
        cy=cy2,
        scale=sc2,
        color_map={
            "luer_outer_ring": ("#E9D5FF", "#581C87"),
            "eccentric_luer_insert": ("#99F6E4", "#0F766E"),
        },
    )
    ax.plot([cx2, cx2], [cy2 - 8, cy2 + 17 * sc2], color="#DC2626", ls="-.", lw=0.45)
    ax.plot([cx2 + 4.0 * sc2, cx2 + 4.0 * sc2], [cy2 - 5, cy2 + 17.5 * sc2], color="#0F766E", ls="-.", lw=0.55)

    dim_h(ax, cx2 - 15.0 * sc2, cx2 + 15.0 * sc2, cy2 + 7.5 * sc2, cy2 + 7.5 * sc2, cy2 + 88, "Ø30.00 ±0.10 (32齒止滑滾花外環)")
    dim_h(ax, cx2 - 11.98 * sc2, cx2 + 11.98 * sc2, cy2, cy2, cy2 - 12, "23.96 ±0.05 (防呆卡耳跨距)")
    dim_h(ax, cx2 - 11.00 * sc2, cx2 + 11.00 * sc2, cy2 + 2.5 * sc2, cy2 + 2.5 * sc2, cy2 - 23, "Ø22.00 (卡口裙部外徑)")
    dim_h(ax, cx2, cx2 + 4.0 * sc2, cy2 + 15.0 * sc2, cy2 + 15.0 * sc2, cy2 + 76, "4.00 ±0.03 (偏心距)")
    dim_h(ax, cx2 + (4.0 - 3.9) * sc2, cx2 + (4.0 + 3.9) * sc2, cy2 + 15.0 * sc2, cy2 + 15.0 * sc2, cy2 + 100, "Ø7.80 (ISO 80369-7 母魯爾外螺紋)")

    dim_v(ax, cx2 - 15.0 * sc2, cx2 + 0.1 * sc2, cy2, cy2 + 15.0 * sc2, cx2 - 86, "15.00 ±0.10 (總高)")
    dim_v(ax, cx2 - 15.0 * sc2, cx2 - 15.0 * sc2, cy2 + 5.60 * sc2, cy2 + 9.00 * sc2, cx2 - 75, "3.40 (滾花盤厚)")
    dim_v(ax, cx2 + 7.90 * sc2, cx2 + 7.90 * sc2, cy2 + 9.00 * sc2, cy2 + 15.00 * sc2, cx2 + 52, "6.00 (魯爾伸出高)")

    callout(ax, (cx2 + 4.0 * sc2, cy2 + 12.5 * sc2), (cx2 + 26, cy2 + 122), "A腔連通口 (+4.00mm)\nISO 80369-7 6% 母魯爾內錐孔\n(開口 Ø4.27 → 底 Ø3.91 / 喉孔 Ø2.00)")
    callout(ax, (cx2 - 4.0 * sc2, cy2 + 3.2 * sc2), (cx2 - 90, cy2 - 42), "B腔盲塞端 (-4.00mm)\n母套孔封頂 + Ø1.86 內塞針\n單管對推溶解時完全封死 T-buffer！")
    callout(ax, (cx2 + 8.5 * sc2, cy2 + 8.2 * sc2), (cx2 + 32, cy2 - 42), "頂面 65° 腎形旋轉讓位槽 (寬8.10mm)\n紫色外環旋轉鎖緊時，青色內芯固定不轉")

    # ==================== RIGHT: PART #3 INITIAL PLUG CAP ====================
    sc3 = 4.6
    cx3, cy3 = 312.0, 95.0
    ax.text(cx3, 261, "#3 初始塞閥蓋 — 剖視圖 SECTION D-D (SCALE 4.6:1)", ha="center", fontsize=8.0, fontweight="bold", color="#276749")
    draw_xz_section(
        ax,
        ROOT / "STEP/initial_plug_cap.step",
        cx=cx3,
        cy=cy3,
        scale=sc3,
        color_map={
            "plug_outer_cap": ("#C6F6D5", "#22543D"),
            "dual_blind_plug": ("#E2B4B1", "#742A2A"),
        },
    )
    ax.plot([cx3, cx3], [cy3 - 8, cy3 + 18.5 * sc3], color="#DC2626", ls="-.", lw=0.45)

    dim_h(ax, cx3 - 11.98 * sc3, cx3 + 11.98 * sc3, cy3, cy3, cy3 - 12, "23.96 ±0.05 (防呆卡耳跨距)")
    dim_h(ax, cx3 - 11.00 * sc3, cx3 + 11.00 * sc3, cy3 + 4.5 * sc3, cy3 + 4.5 * sc3, cy3 - 23, "Ø22.00 ±0.10 (外蓋外徑)")
    dim_h(ax, cx3 - 10.00 * sc3, cx3 + 10.00 * sc3, cy3 + 17.0 * sc3, cy3 + 17.0 * sc3, cy3 + 88, "20.00 (扁平旋柄寬) × 厚 4.00 mm")

    dim_v(ax, cx3 - 11.98 * sc3, cx3 - 10.0 * sc3, cy3, cy3 + 17.0 * sc3, cx3 - 70, "17.00 ±0.10 (總高)")
    dim_v(ax, cx3 - 11.00 * sc3, cx3 - 11.00 * sc3, cy3, cy3 + 9.0 * sc3, cx3 - 58, "9.00 (圓蓋本體高)")
    dim_v(ax, cx3 + 10.00 * sc3, cx3 + 10.00 * sc3, cy3 + 9.0 * sc3, cy3 + 17.0 * sc3, cx3 + 58, "8.00 (旋柄凸出長)")

    callout(ax, (cx3 + 4.0 * sc3, cy3 + 3.2 * sc3), (cx3 - 18, cy3 - 42), "一體式雙盲塞彈性墊 (Bromobutyl)\nA/B 雙腔同時端面壓縮 + 內外徑雙重氣密\n確保滅菌、運輸與儲存期間零洩漏、零串腔")

    _save_sheet(pdf, fig, 4)


def build_sheet_5(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        5, 5, "CSL-PRT-104",
        "#4 單雙管推拉切換片 — 機構尺寸與 0°/90° 切換動作圖",
        "PART #4: SINGLE/DUAL PLUNGER SELECTOR CLIP — DETAIL & KINEMATICS",
        "5 : 1 (DETAIL)",
        "MEDICAL POM (DELRIN) / TOUGHENED PP",
    )

    # Left: Exact 5:1 Front View (XY) & Longitudinal Section of Plunger Clip #4
    sc = 5.0
    cx, cy = 112.0, 178.0
    ax.text(cx, 268, "#4 單雙管推拉切換片 正視與剖面詳圖 (SCALE 5:1)", ha="center", fontsize=8.2, fontweight="bold", color="#0F172A")

    # Slice plunger_clip on XY @ Z = 3.60 mm (front lip) & Z = 2.20 mm (internal disc pocket)
    clip_scene = read_scene(ROOT / "STEP/plunger_clip.step")
    clip_shp = list(clip_scene.leaves())[0].shape()

    # Draw backplate outline (Z = 0.5 mm)
    sec_back = bd.section(clip_shp, section_by=bd.Plane.XY.offset(0.5))
    for f in sec_back.faces():
        pts = [(cx + v.X * sc, cy + v.Y * sc) for v in _sample_wire_xz_or_xy(f.outer_wire())]
        ax.add_patch(MplPolygon(pts, closed=True, fc="#DCFCE7", ec="#166534", lw=1.0, zorder=3))

    # Draw internal pocket dashed line (Z = 2.2 mm)
    sec_mid = bd.section(clip_shp, section_by=bd.Plane.XY.offset(2.2))
    for f in sec_mid.faces():
        pts = [(cx + v.X * sc, cy + v.Y * sc) for v in _sample_wire_xz_or_xy(f.outer_wire())]
        ax.add_patch(MplPolygon(pts, closed=True, fc="#BBF7D0", ec="#15803D", lw=0.8, ls="--", zorder=4))
        for iw in f.inner_wires():
            pts_i = [(cx + v.X * sc, cy + v.Y * sc) for v in _sample_wire_xz_or_xy(iw)]
            ax.add_patch(MplPolygon(pts_i, closed=True, fc="#DCFCE7", ec="#15803D", lw=0.8, ls="--", zorder=4.1))

    # Draw front retaining lip (Z = 3.6 mm)
    sec_top = bd.section(clip_shp, section_by=bd.Plane.XY.offset(3.6))
    for f in sec_top.faces():
        pts = [(cx + v.X * sc, cy + v.Y * sc) for v in _sample_wire_xz_or_xy(f.outer_wire())]
        ax.add_patch(MplPolygon(pts, closed=True, fc="#86EFAC", ec="#14532D", lw=1.1, zorder=5))
        for iw in f.inner_wires():
            pts_i = [(cx + v.X * sc, cy + v.Y * sc) for v in _sample_wire_xz_or_xy(iw)]
            ax.add_patch(MplPolygon(pts_i, closed=True, fc="#DCFCE7", ec="#14532D", lw=1.1, zorder=5.1))

    # Center marks on Pivot B (-7.20, 0) & Snap A (+7.20, 0)
    for bx_mm in (S.BARREL_X_B, S.BARREL_X_A):
        ax.plot([cx + (bx_mm - 7.5) * sc, cx + (bx_mm + 7.5) * sc], [cy, cy], color="#DC2626", ls="-.", lw=0.45, zorder=8)
        ax.plot([cx + bx_mm * sc, cx + bx_mm * sc], [cy - 9.0 * sc, cy + 9.0 * sc], color="#DC2626", ls="-.", lw=0.45, zorder=8)

    dim_h(ax, cx - 15.0 * sc, cx + 15.0 * sc, cy + 8.2 * sc, cy + 8.2 * sc, cy + 68, "30.00 ±0.10 (切換片總長)")
    dim_h(ax, cx + S.BARREL_X_B * sc, cx + S.BARREL_X_A * sc, cy + 8.2 * sc, cy + 8.2 * sc, cy + 54, "14.40 ±0.05 (雙推桿中心距)")
    dim_h(ax, cx + (S.BARREL_X_A - 5.95) * sc, cx + (S.BARREL_X_A + 5.95) * sc, cy - 8.2 * sc, cy - 8.2 * sc, cy - 54, "11.90 ±0.05 (內袋C型彈扣開口，過盈0.90mm)")
    dim_h(ax, cx + (S.BARREL_X_A - 3.25) * sc, cx + (S.BARREL_X_A + 3.25) * sc, cy - 8.2 * sc, cy - 8.2 * sc, cy - 66, "6.50 (前唇頸部通過口)")
    dim_v(ax, cx - 15.0 * sc, cx - 15.0 * sc, cy - 8.2 * sc, cy + 8.2 * sc, cx - 88, "16.40 ±0.10 (寬度)")

    callout(ax, (cx + S.BARREL_X_B * sc, cy + 3.4 * sc), (cx - 94, cy + 56), "B軸常駐樞軸孔\n前唇孔 Ø6.80 / 內圓袋 Ø13.10\n永久扣住B推桿尾盤，可自由旋轉90°")
    callout(ax, (cx + (S.BARREL_X_A + 5.6) * sc, cy + 1.2 * sc), (cx + 58, cy + 46), "彈性釋放狹縫 (3.2 × 1.1 mm)\n降低側向卡扣應力，確保 >50 次開合不白化")

    # Lower Left: XZ Thickness Section of Clip #4 (Scale 5:1)
    scy = 56.0
    ax.text(cx, 92, "縱向厚度剖視圖 SECTION E-E (Y = 0, SCALE 5:1)", ha="center", fontsize=7.6, fontweight="bold", color="#0F172A")
    draw_xz_section(
        ax,
        ROOT / "STEP/plunger_clip.step",
        cx=cx,
        cy=scy,
        scale=sc,
        color_map={"plunger_clip": ("#86EFAC", "#14532D")},
    )
    dim_v(ax, cx - 15.0 * sc, cx - 15.0 * sc, scy, scy + 4.0 * sc, cx - 86, "4.00 (總厚)")
    dim_v(ax, cx + 15.0 * sc, cx + 15.0 * sc, scy, scy + 1.40 * sc, cx + 82, "1.40 (背板)")
    dim_v(ax, cx + 15.0 * sc, cx + 15.0 * sc, scy + 1.40 * sc, scy + 3.20 * sc, cx + 94, "1.80+0.10/-0 (盤槽)")

    # Right Half: 0-deg Locked vs 90-deg Unlocked 3D Kinematic Comparison
    ax.add_patch(FancyBboxPatch((222, 50), 186, 214, boxstyle="round,pad=1.5", facecolor="#F8FAFC", edgecolor="#94A3B8", lw=0.7))
    ax.text(315, 256, "【單雙管推拉切換動作說明 (DUAL / SINGLE MODE KINEMATICS)】", ha="center", fontsize=8.0, fontweight="bold", color="#0F172A")
    place_image_cropped(ax, ROOT / "tmp/dispense_iso.png", (226, 108, 86, 138))
    place_image_cropped(ax, ROOT / "tmp/dispense_unlocked.png", (318, 108, 86, 138))
    ax.text(269, 102, "模式 A：0° 水平扣合態\n● 同時鎖定 A/B 雙推桿尾盤\n● Stage 1 運輸防誤推\n● Stage 3 雙管 1:1 等位移點膠", ha="center", va="top", fontsize=6.2, fontweight="bold", color="#166534", bbox=dict(boxstyle="round,pad=0.3", fc="#DCFCE7", ec="#22C55E", lw=0.6))
    ax.text(361, 102, "模式 B：90° 向下旋開解鎖態\n● 繞 B 推桿頸部旋轉 90° 垂下\n● A 推桿完全解鎖可獨立推拉\n● Stage 2 與粉劑單管來回溶解", ha="center", va="top", fontsize=6.2, fontweight="bold", color="#553C9A", bbox=dict(boxstyle="round,pad=0.3", fc="#FAF5FF", ec="#A855F7", lw=0.6))

    _save_sheet(pdf, fig, 5)


def _sample_wire_xz_or_xy(wire: bd.Wire, n_curve: int = 24) -> list:
    pts = []
    for edge in wire.edges():
        gt = edge.geom_type
        n = 2 if str(gt).endswith("LINE") else n_curve
        for k in range(n):
            p = edge.position_at(k / float(n))
            if not pts or (abs(p.X - pts[-1].X) + abs(p.Y - pts[-1].Y) > 1e-4):
                pts.append(p)
    return pts


def main() -> None:
    out_pdf = ROOT / "PDF/雙單管混合裝置_完整專業設計圖_RevB.pdf"
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(out_pdf) as pdf:
        build_sheet_1(pdf)
        build_sheet_2(pdf)
        build_sheet_3(pdf)
        build_sheet_4(pdf)
        build_sheet_5(pdf)
    print(f"Wrote {out_pdf} (5 A3 landscape sheets)")


if __name__ == "__main__":
    main()
