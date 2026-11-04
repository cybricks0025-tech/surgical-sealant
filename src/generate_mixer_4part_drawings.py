"""Generate the 5-Sheet A3 Bilingual Detail Engineering Drawing Set for Part #1's 4 Sub-Parts:
`PDF/螺旋混合頭_四件式零件拆解設計圖_RevC.pdf` (+ `assets/mixer_sheets/mixer_sheet_1..5.png`).

Sheets:
1. `CSL-CAP-201-ASSY` : #1 螺旋混合雙管蓋 — 四件式結構爆炸圖、B-B 組裝剖視圖與無膠夾持防脫出規範
2. `CSL-CAP-201-1`    : 零件 1-1 外旋卡口壓蓋 (Mixer Bayonet Retaining Outer Cap) 單件製造圖
3. `CSL-CAP-201-2`    : 零件 1-2 雙流道分流密封內座 (Dual-Channel Manifold Seal Seat) 單件製造圖
4. `CSL-CAP-201-3`    : 零件 1-3 一體式喇叭口透明混合外管 (One-Piece Bell-Mouth Mixing Cannula) 單件製造圖
5. `CSL-CAP-201-4`    : 零件 1-4 防脫出底座靜態螺旋混合芯 (9-Element Kenics Helical Core) 單件製造圖
"""
from __future__ import annotations

import logging
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Polygon as MplPolygon, Rectangle, Wedge
from PIL import Image

from cadgen import build123d as bd
from cadgen import read_scene, read_step

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from lib import specs as S  # noqa: E402

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
plt.rcParams["pdf.fonttype"] = 42

A3_W, A3_H = 420.0, 297.0


def new_a3_sheet(
    sheet_no: int,
    total_sheets: int,
    dwg_no: str,
    title_zh: str,
    title_en: str,
    scale_str: str,
    material_str: str,
):
    fig = plt.figure(figsize=(A3_W / 25.4, A3_H / 25.4), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, A3_W)
    ax.set_ylim(0, A3_H)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), A3_W, A3_H, facecolor="#FFFFFF", edgecolor="none"))
    ax.add_patch(Rectangle((8, 8), A3_W - 16, A3_H - 16, fill=False, edgecolor="#1A2430", lw=1.4))
    ax.add_patch(Rectangle((10, 10), A3_W - 20, A3_H - 20, fill=False, edgecolor="#1A2430", lw=0.6))

    for idx, ch in enumerate(["1", "2", "3", "4", "5", "6", "7", "8"]):
        gx = 10 + (idx + 0.5) * ((A3_W - 20) / 8.0)
        ax.text(gx, A3_H - 9.0, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")
        ax.text(gx, 9.0, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")
    for idx, ch in enumerate(["F", "E", "D", "C", "B", "A"]):
        gy = 10 + (idx + 0.5) * ((A3_H - 20) / 6.0)
        ax.text(9.0, gy, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")
        ax.text(A3_W - 9.0, gy, ch, ha="center", va="center", fontsize=6.5, color="#4A5568")

    # Revision Block (top-right: x = 282..410, y = 266..287)
    rx0, ry0 = 282, A3_H - 31
    ax.add_patch(Rectangle((rx0, ry0), 128, 21, facecolor="#F7FAFC", edgecolor="#1A2430", lw=0.7))
    for dy in (15.5, 10.2, 5.1):
        ax.plot([rx0, rx0 + 128], [ry0 + dy, ry0 + dy], color="#1A2430", lw=0.5)
    ax.plot([rx0 + 13, rx0 + 13], [ry0, ry0 + 21], color="#1A2430", lw=0.5)
    ax.plot([rx0 + 36, rx0 + 36], [ry0, ry0 + 21], color="#1A2430", lw=0.5)
    ax.text(rx0 + 6.5, ry0 + 18.2, "REV", ha="center", va="center", fontsize=6.0, fontweight="bold")
    ax.text(rx0 + 24.5, ry0 + 18.2, "DATE", ha="center", va="center", fontsize=6.0, fontweight="bold")
    ax.text(rx0 + 82, ry0 + 18.2, "變更說明 / REVISION HISTORY", ha="center", va="center", fontsize=6.0, fontweight="bold")
    ax.text(rx0 + 6.5, ry0 + 12.8, "A", ha="center", va="center", fontsize=5.5)
    ax.text(rx0 + 24.5, ry0 + 12.8, "2026-10-28", ha="center", va="center", fontsize=5.5)
    ax.text(rx0 + 38, ry0 + 12.8, "原廠商簡報概念剖面圖 (混合頭.png)", ha="left", va="center", fontsize=5.4)
    ax.text(rx0 + 6.5, ry0 + 7.6, "B", ha="center", va="center", fontsize=5.5)
    ax.text(rx0 + 24.5, ry0 + 7.6, "2026-11-03", ha="center", va="center", fontsize=5.5)
    ax.text(rx0 + 38, ry0 + 7.6, "全系統 3D 重建與防呆卡口規範", ha="left", va="center", fontsize=5.4)
    ax.text(rx0 + 6.5, ry0 + 2.5, "C", ha="center", va="center", fontsize=5.8, fontweight="bold", color="#B91C1C")
    ax.text(rx0 + 24.5, ry0 + 2.5, "2026-11-04", ha="center", va="center", fontsize=5.6, fontweight="bold")
    ax.text(rx0 + 38, ry0 + 2.5, "考證確認四件式結構：一體式喇叭外管 + 防脫螺旋芯單件圖", ha="left", va="center", fontsize=5.4, fontweight="bold", color="#991B1B")

    # ISO Title Block (bottom-right: x = 235..410, y = 10..42)
    tx0, ty0, tw, th = 235, 10, 175, 32
    ax.add_patch(Rectangle((tx0, ty0), tw, th, facecolor="#F8FAFC", edgecolor="#1A2430", lw=0.9))
    ax.plot([tx0, tx0 + tw], [ty0 + 22, ty0 + 22], color="#1A2430", lw=0.6)
    ax.plot([tx0, tx0 + tw], [ty0 + 11, ty0 + 11], color="#1A2430", lw=0.6)
    ax.plot([tx0 + 115, tx0 + 115], [ty0, ty0 + 22], color="#1A2430", lw=0.6)
    ax.plot([tx0 + 55, tx0 + 55], [ty0, ty0 + 11], color="#1A2430", lw=0.6)

    ax.text(tx0 + 4, ty0 + 27.6, title_zh, ha="left", va="center", fontsize=9.0, fontweight="bold", color="#0F172A")
    ax.text(tx0 + 4, ty0 + 23.8, title_en, ha="left", va="center", fontsize=6.2, color="#475569")

    ax.text(tx0 + 4, ty0 + 18.2, "材質 / MATERIAL:", ha="left", va="center", fontsize=5.6, color="#64748B")
    ax.text(tx0 + 4, ty0 + 13.8, material_str, ha="left", va="center", fontsize=6.6, fontweight="bold", color="#1E293B")

    ax.text(tx0 + 118, ty0 + 18.2, "圖號 / DWG NO.:", ha="left", va="center", fontsize=5.6, color="#64748B")
    ax.text(tx0 + 118, ty0 + 13.8, dwg_no, ha="left", va="center", fontsize=7.6, fontweight="bold", color="#0F172A")

    ax.text(tx0 + 4, ty0 + 7.5, "一般公差 / TOLERANCE:", ha="left", va="center", fontsize=5.5, color="#64748B")
    ax.text(tx0 + 4, ty0 + 3.2, "ISO 2768-f/m (精密塑膠)", ha="left", va="center", fontsize=6.3, fontweight="bold")

    ax.text(tx0 + 58, ty0 + 7.5, "單位 / UNIT & PROJ.:", ha="left", va="center", fontsize=5.5, color="#64748B")
    ax.text(tx0 + 58, ty0 + 3.2, "mm | 第三角法 3RD ANGLE", ha="left", va="center", fontsize=6.2, fontweight="bold")

    ax.text(tx0 + 118, ty0 + 7.5, f"比例 SCALE: {scale_str}", ha="left", va="center", fontsize=6.1, fontweight="bold")
    ax.text(
        tx0 + 118,
        ty0 + 3.2,
        f"REV C  |  SHEET {sheet_no} OF {total_sheets}",
        ha="left",
        va="center",
        fontsize=6.8,
        fontweight="bold",
        color="#B91C1C",
    )
    return fig, ax


def _sample_wire_2d(wire: bd.Wire, axis_h: str = "X", axis_v: str = "Z", n_curve: int = 28) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for edge in wire.edges():
        gt = str(edge.geom_type)
        n = 2 if gt.endswith("LINE") else n_curve
        for k in range(n):
            p = edge.position_at(k / float(n))
            hv = (getattr(p, axis_h), getattr(p, axis_v))
            if not pts or (abs(hv[0] - pts[-1][0]) + abs(hv[1] - pts[-1][1]) > 1e-4):
                pts.append(hv)
    return pts


def draw_xz_section(
    ax,
    step_path: Path,
    cx: float,
    cy: float,
    scale: float,
    color_map: dict[str, tuple[str, str]],
    z_clip_max: float | None = None,
) -> None:
    """Slice a STEP model on exact XZ plane (Y=0) and render hatched B-Rep section faces + back outlines."""
    scene = read_scene(step_path)
    hatches = ["////", "\\\\\\\\", "////", "xxxx"]
    for idx, leaf in enumerate(scene.leaves()):
        lbl = leaf.label or ""
        fill_hex, edge_hex = "#E2E8F0", "#1E293B"
        for key, pair in color_map.items():
            if key in lbl:
                fill_hex, edge_hex = pair
                break
        shp = leaf.shape()
        if z_clip_max is not None:
            clip_box = bd.Box(60, 60, z_clip_max + 2.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(
                bd.Location((0, 0, -1.0))
            )
            shp = shp & clip_box
        sec = bd.section(shp, section_by=bd.Plane.XZ)
        for face in sec.faces():
            ow = face.outer_wire()
            pts_o = [(cx + u * scale, cy + v * scale) for u, v in _sample_wire_2d(ow, "X", "Z")]
            ax.add_patch(
                MplPolygon(
                    pts_o,
                    closed=True,
                    facecolor=fill_hex,
                    edgecolor=edge_hex,
                    linewidth=0.90,
                    hatch=hatches[idx % len(hatches)],
                    alpha=0.90,
                    zorder=4 + idx * 0.1,
                )
            )
            for iw in face.inner_wires():
                pts_i = [(cx + u * scale, cy + v * scale) for u, v in _sample_wire_2d(iw, "X", "Z")]
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


def draw_brep_ortho_edges(
    ax,
    step_path: Path,
    cx: float,
    cy: float,
    scale: float,
    axis_h: str = "X",
    axis_v: str = "Z",
    edge_color: str = "#7F1D1D",
    fill_faces_tint: str | None = None,
) -> None:
    """Project exact B-Rep 3D edges onto (axis_h, axis_v) for crisp vector orthographic views (e.g. helical core)."""
    shp = read_step(step_path)
    if fill_faces_tint:
        # Light silhouette fill from tessellated mesh triangles projected onto 2D
        verts, tris = shp.tessellate(tolerance=0.03)
        axis_d = next(a for a in ("X", "Y", "Z") if a not in (axis_h, axis_v))
        tri_depths = []
        for t in tris:
            v0, v1, v2 = verts[t[0]], verts[t[1]], verts[t[2]]
            d_avg = (getattr(v0, axis_d) + getattr(v1, axis_d) + getattr(v2, axis_d)) / 3.0
            tri_depths.append((d_avg, v0, v1, v2))
        tri_depths.sort(key=lambda item: item[0])
        for _, v0, v1, v2 in tri_depths:
            pts = [
                (cx + getattr(v0, axis_h) * scale, cy + getattr(v0, axis_v) * scale),
                (cx + getattr(v1, axis_h) * scale, cy + getattr(v1, axis_v) * scale),
                (cx + getattr(v2, axis_h) * scale, cy + getattr(v2, axis_v) * scale),
            ]
            ax.add_patch(MplPolygon(pts, closed=True, facecolor=fill_faces_tint, edgecolor="none", zorder=3.0))

    for edge in shp.edges():
        gt = str(edge.geom_type)
        n = 2 if gt.endswith("LINE") else 20
        xs, ys = [], []
        for k in range(n + 1):
            p = edge.position_at(k / float(n))
            xs.append(cx + getattr(p, axis_h) * scale)
            ys.append(cy + getattr(p, axis_v) * scale)
        ax.plot(xs, ys, color=edge_color, lw=0.62, zorder=4.2)


def dim_h(
    ax,
    x1: float,
    x2: float,
    y_ref1: float,
    y_ref2: float,
    y_dim: float,
    text: str,
    color: str = "#B91C1C",
    fontsize: float = 6.7,
) -> None:
    s1 = 1.2 if y_dim >= y_ref1 else -1.2
    s2 = 1.2 if y_dim >= y_ref2 else -1.2
    ax.plot([x1, x1], [y_ref1 + s1 * 0.4, y_dim + s1 * 1.4], color=color, lw=0.52, zorder=10)
    ax.plot([x2, x2], [y_ref2 + s2 * 0.4, y_dim + s2 * 1.4], color=color, lw=0.52, zorder=10)
    ax.annotate(
        "",
        xy=(x1, y_dim),
        xytext=(x2, y_dim),
        arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.62, mutation_scale=6.5),
        zorder=11,
    )
    va = "bottom" if y_dim >= 0.5 * (y_ref1 + y_ref2) else "top"
    dy = 1.0 if va == "bottom" else -1.0
    ax.text(
        0.5 * (x1 + x2),
        y_dim + dy,
        text,
        ha="center",
        va=va,
        fontsize=fontsize,
        color=color,
        fontweight="bold",
        bbox=dict(boxstyle="square,pad=0.08", facecolor="#FFFFFF", edgecolor="none", alpha=0.88),
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
    fontsize: float = 6.7,
) -> None:
    s1 = 1.2 if x_dim >= x_ref1 else -1.2
    s2 = 1.2 if x_dim >= x_ref2 else -1.2
    ax.plot([x_ref1 + s1 * 0.4, x_dim + s1 * 1.4], [y1, y1], color=color, lw=0.52, zorder=10)
    ax.plot([x_ref2 + s2 * 0.4, x_dim + s2 * 1.4], [y2, y2], color=color, lw=0.52, zorder=10)
    ax.annotate(
        "",
        xy=(x_dim, y1),
        xytext=(x_dim, y2),
        arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.62, mutation_scale=6.5),
        zorder=11,
    )
    offset_x = -2.2 if x_dim < 0.5 * (x_ref1 + x_ref2) else 2.2
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
        bbox=dict(boxstyle="square,pad=0.08", facecolor="#FFFFFF", edgecolor="none", alpha=0.88),
        zorder=12,
    )


def callout(ax, xy_target: tuple[float, float], xy_text: tuple[float, float], text: str, ha: str = "left", fontsize: float = 6.3) -> None:
    ax.annotate(
        text,
        xy=xy_target,
        xytext=xy_text,
        ha=ha,
        va="center",
        fontsize=fontsize,
        color="#0F172A",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#F8FAFC", edgecolor="#94A3B8", lw=0.5),
        arrowprops=dict(arrowstyle="-|>", color="#334155", lw=0.58, connectionstyle="arc3,rad=0.0"),
        zorder=15,
    )


def place_image_cropped(ax, img_path: Path, box: tuple[float, float, float, float]) -> None:
    if not img_path.exists():
        return
    im = Image.open(img_path).convert("RGBA")
    arr = np.array(im)
    bg = arr[-1, -1, :3].copy()
    arr[:90, :220, :3] = bg
    arr[:90, :220, 3] = 255
    im = Image.fromarray(arr)
    diff = np.abs(arr[:, :, :3].astype(int) - bg.astype(int)).sum(axis=2)
    ys, xs = np.where(diff > 10)
    if len(xs) > 10:
        pad = 18
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
    out_dir = ROOT / "assets/mixer_sheets"
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / f"mixer_sheet_{sheet_no}.png", dpi=180)
    plt.close(fig)


# ==============================================================================
# SHEET 1: 4-PART EXPLODED VIEW, SECTION B-B & SUB-ASSEMBLY BOM
# ==============================================================================
def build_sheet_1(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        1, 5, "CSL-CAP-201-ASSY",
        "#1 螺旋混合雙管蓋 — 四件式結構拆解總成與組裝剖視圖",
        "PART #1 HELICAL STATIC MIXER CAP — 4-PART EXPLODED VIEW, SECTION B-B & BOM",
        "4.0 : 1 (SECTION)",
        "ABS + SILICONE (SHORE A 60) + CLEAR PC + POM",
    )

    # 1. Left Box: 3D 4-Part Exploded Isometric View (x = 16..110, y = 18..276)
    ax.add_patch(Rectangle((16, 18), 94, 258, facecolor="#F4F7FA", edgecolor="#CBD5E1", lw=0.7))
    ax.text(63, 269, "四件式組裝爆炸圖\n(4-Part Rear-Loading Exploded)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#0F172A")
    place_image_cropped(ax, ROOT / "tmp/mixer_exploded_iso.png", (18, 24, 52, 236))

    # Balloon callouts cleanly aligned in right sub-column of exploded box (zero overlap with 3D parts)
    expl_labels = [
        (226, "① 1-1 外旋壓蓋\n(上方套入壓緊)", "#4D531B", "#F4F6E6"),
        (158, "③ 1-3 喇叭外管\n(穿出Ø4.08頂孔)", "#0369A1", "#E0F2FE"),
        (95,  "④ 1-4 防脫螺旋芯\n(喇叭口向上置入)", "#991B1B", "#FEE2E2"),
        (40,  "② 1-2 分流密封座\n(壓入防脫扣唇)", "#6C3B1C", "#F5EBE0"),
    ]
    for ly, ltxt, ec, fc in expl_labels:
        ax.plot([53, 66], [ly, ly], color=ec, lw=0.6, ls="--", zorder=7)
        ax.text(
            87, ly, ltxt,
            ha="center", va="center", fontsize=5.2, fontweight="bold", color=ec,
            bbox=dict(boxstyle="round,pad=0.22", facecolor=fc, edgecolor=ec, lw=0.55, alpha=0.95),
            zorder=8,
        )

    # 2. Center: Exact B-Rep Section B-B of 4-Part Assembly (x = 114..252)
    sc = 3.8
    cx, cy = 172.0, 58.0
    ax.text(cx, 271, "組裝全剖視圖 SECTION B-B (3.8:1)", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#0F172A")

    draw_xz_section(
        ax,
        ROOT / "STEP/helical_mixer_cap.step",
        cx=cx,
        cy=cy,
        scale=sc,
        color_map={
            "part1_outer_cap": ("#D9DF9D", "#4D531B"),
            "part2_seal_seat": ("#DDB892", "#6C3B1C"),
            "part3_bell_cannula": ("#BAE6FD", "#0369A1"),
            "part4_helical_core": ("#FCA5A5", "#991B1B"),
        },
    )
    ax.plot([cx, cx], [cy - 6, cy + 43.2 * sc], color="#DC2626", ls="-.", lw=0.5)
    for sign in (-1.0, 1.0):
        ax.plot([cx + sign * 1.50 * sc, cx + sign * 1.50 * sc], [cy + 10.90 * sc, cy + 41.60 * sc], color="#0369A1", lw=0.55, zorder=3.5)

    # Assembly Envelope Dimensions (strictly within x = 116 .. 228, clearing Title Block x=235!)
    dim_v(ax, cx - 11.98 * sc, cx - 2.00 * sc, cy, cy + 41.60 * sc, cx - 54, "41.60 ±0.15 (混合頭總長)")
    dim_v(ax, cx - 11.98 * sc, cx - 3.10 * sc, cy, cy + 14.87 * sc, cx - 44, "14.87 (1-1 外蓋高)")
    dim_v(ax, cx - 3.10 * sc, cx - 2.00 * sc, cy + 14.87 * sc, cy + 41.60 * sc, cx - 33, "26.73 (1-3 外露管長)")
    dim_v(ax, cx + 2.00 * sc, cx + 2.00 * sc, cy + 9.60 * sc, cy + 37.60 * sc, cx + 16, "28.00 (1-4 螺旋芯長)")
    dim_v(ax, cx + 11.98 * sc, cx + 11.98 * sc, cy, cy + 1.80 * sc, cx + 51, "1.80 (卡耳)")

    dim_h(ax, cx - 4.00 * sc, cx + 4.00 * sc, cy + 1.60 * sc, cy + 1.60 * sc, cy - 11, "8.00 ±0.03 (雙入口孔距)")
    dim_h(ax, cx - 11.00 * sc, cx + 11.00 * sc, cy + 5.00 * sc, cy + 5.00 * sc, cy - 23, "Ø22.00 ±0.10 (外蓋外徑)")
    dim_h(ax, cx - 11.98 * sc, cx + 11.98 * sc, cy, cy, cy - 35, "23.96 ±0.05 (防呆卡耳跨距)")
    dim_h(ax, cx - 2.00 * sc, cx + 2.00 * sc, cy + 41.60 * sc, cy + 41.60 * sc, cy + 41.60 * sc + 8, "Ø4.00 OD / Ø3.00 ID")

    # 4 Part Callouts placed in upper-center open zone (x = 196..254, strictly left of x = 258 notes box!)
    callout(ax, (cx + 1.1 * sc, cy + 32.0 * sc), (cx + 24, 212), "④ 1-4 防脫螺旋混合芯\n(9節×3.0 + Ø4.40止擋底座)", fontsize=5.6)
    callout(ax, (cx + 1.9 * sc, cy + 24.5 * sc), (cx + 24, 184), "③ 1-3 一體式喇叭口外管\n(喇叭口與直管一體無接縫)", fontsize=5.6)
    callout(ax, (cx + 7.2 * sc, cy + 11.8 * sc), (cx + 24, 154), "① 1-1 外旋卡口壓蓋\n(內錐面免膠壓緊喇叭口)", fontsize=5.6)
    callout(ax, (cx + 5.2 * sc, cy + 7.0 * sc),  (cx + 24, 126), "② 1-2 雙流道分流密封座\n(母套孔過盈+獨立分流隔板)", fontsize=5.6)

    # 3. Right Column: 4-Part Sub-Assembly BOM Table (x = 258..408, y = 166..258)
    bx, by = 258.0, 246.0
    ax.text(bx, by + 9, "【#1 螺旋混合頭 — 四件式子零件清單 (4-PART SUB-ASSEMBLY BOM)】", fontsize=7.4, fontweight="bold", color="#0F172A")
    col_w = [12, 26, 38, 36, 38]  # sum = 150 mm
    headers = ["編號", "圖號 DWG", "零件名稱", "材質規範", "包絡尺寸與開模方式"]
    rows = [
        ["1-1", "CSL-CAP-201-1", "外旋卡口壓蓋\nOuter Retaining Cap", "醫療級 ABS / PP\n(橄欖綠)", "Ø22(卡耳23.96)×14.87\n二板模單向向下抽芯"],
        ["1-2", "CSL-CAP-201-2", "雙流道分流密封內座\nManifold Seal Seat", "醫療級矽膠 / TPE\nShore A 60 (棕)", "Ø19.60 × 7.40\n直抽芯模 / Ø3.10過盈"],
        ["1-3", "CSL-CAP-201-3", "一體式喇叭口透明外管\n1-Pc Bell Cannula", "醫療級高透明 PC\n(透光 ≥88%)", "Ø11.40喇叭→Ø4×32.56\n單支拋光長芯針抽芯"],
        ["1-4", "CSL-CAP-201-4", "防脫底座靜態螺旋芯\nAnti-Eject Helix Core", "醫療級高流動 POM\n(暗紅塑鋼)", "Ø4.40底座 + 9節×28.0\n左右對開哈夫滑塊模"],
    ]
    cx_t = bx
    for w, h_txt in zip(col_w, headers):
        ax.add_patch(Rectangle((cx_t, by - 8), w, 8, facecolor="#1E293B", edgecolor="#0F172A", lw=0.5))
        ax.text(cx_t + w / 2.0, by - 4, h_txt, ha="center", va="center", fontsize=5.6, fontweight="bold", color="#FFFFFF")
        cx_t += w
    cur_y = by - 8
    for r_idx, r in enumerate(rows):
        rh = 16.5
        cur_y -= rh
        bg_c = "#F8FAFC" if r_idx % 2 == 0 else "#FFFFFF"
        cx_t = bx
        for c_idx, (w, val) in enumerate(zip(col_w, r)):
            ax.add_patch(Rectangle((cx_t, cur_y), w, rh, facecolor=bg_c, edgecolor="#CBD5E1", lw=0.45))
            ha_c = "center" if c_idx in (0, 1) else "left"
            tx = cx_t + w / 2.0 if ha_c == "center" else cx_t + 1.5
            ax.text(tx, cur_y + rh / 2.0, val, ha=ha_c, va="center", fontsize=5.3, color="#1E293B")
            cx_t += w

    # 4. Right Lower: Engineering Verification & Assembly Sequence Notes (x = 258..408, y = 48..166)
    ax.add_patch(FancyBboxPatch((258, 48), 150, 114, boxstyle="round,pad=1.2", facecolor="#FFFBEB", edgecolor="#D97706", lw=0.75))
    ax.text(262, 156, "【結構考證結論與免膠水防爆管組裝機制】", fontsize=7.2, fontweight="bold", color="#92400E")
    notes = [
        "1. 原廠圖面像素比對確認（確為 4 組零件）：",
        "   放大檢視原廠商 CAD 剖面 (`混合頭.png`)，底部錐形喇叭口",
        "   與 Ø4.00 直管間完全連續無分件縫線，證實為「一體式喇叭",
        "   口透明外管 (1-3)」，全混合頭共由 4 件射出零件組成。",
        "2. 免膠水機械夾持氣密 (Adhesive-Free Clamping)：",
        "   組裝順序：先將 ③(1-3) 由下往上穿出 ①(1-1) 頂孔 → 將",
        "   ④(1-4) 由喇叭口向上塞入 → 最後壓入 ②(1-2) 矽膠座扣入",
        "   Ø19.70 扣槽。藉 ① 內錐面與 ② 彈性壓縮達成高壓氣密，",
        "   零溶劑/零 UV 膠殘留，符合 ISO 10993 生物相容性要求。",
        "3. 物理防射出安全鎖定 (Positive Anti-Blowout Stop)：",
        "   1-4 螺旋芯尾部具 Ø4.40→Ø3.40 圓錐分流環 (> 直管內徑",
        "   Ø3.00)，高黏度水凝膠高壓推注時絕對無法向外噴出脫落！",
    ]
    for idx, nl in enumerate(notes):
        ax.text(262, 146 - idx * 8.2, nl, fontsize=5.45, color="#1E293B", va="center")

    _save_sheet(pdf, fig, 1)


# ==============================================================================
# SHEET 2: PART 1-1 OUTER BAYONET RETAINING CAP (CSL-CAP-201-1)
# ==============================================================================
def build_sheet_2(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        2, 5, "CSL-CAP-201-1",
        "零件 1-1：外旋卡口壓蓋 — 單件製造工程圖",
        "PART #1-1: MIXER BAYONET RETAINING OUTER CAP — DETAIL MANUFACTURING DRAWING",
        "7.5 : 1 (SECTION)",
        "MEDICAL GRADE ABS / PP (OLIVE GREEN)",
    )

    sc = 7.5
    cx, cy = 132.0, 84.0
    ax.text(cx, 270, "全剖視圖 SECTION A-A (XZ 中心剖面, SCALE 7.5:1)", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#0F172A")

    draw_xz_section(
        ax,
        ROOT / "STEP/mixer_part1_outer_cap.step",
        cx=cx,
        cy=cy,
        scale=sc,
        color_map={"mixer_part1": ("#D9DF9D", "#4D531B")},
    )
    ax.plot([cx, cx], [cy - 8, cy + 16.2 * sc], color="#DC2626", ls="-.", lw=0.5)

    # Left vertical outer height dims (part min X = 132 - 11.98*7.5 = 42.15)
    dim_v(ax, cx - 11.98 * sc, cx - 3.10 * sc, cy, cy + 14.87 * sc, 20.0, "14.87 ±0.08 (外蓋總高)")
    dim_v(ax, cx - 11.98 * sc, cx - 11.00 * sc, cy, cy + 11.87 * sc, 32.0, "11.87 ±0.06 (外直筒肩高)")

    # Right vertical internal bore step dims (part max X = 132 + 11.98*7.5 = 221.85)
    dim_v(ax, cx + 11.98 * sc, cx + 11.98 * sc, cy, cy + 1.80 * sc, 231.0, "1.80 ±0.04 (卡耳高)")
    dim_v(ax, cx + 9.85 * sc, cx + 9.85 * sc, cy, cy + 6.82 * sc, 242.0, "6.82 ±0.05 (扣唇肩深)")
    dim_v(ax, cx + 9.85 * sc, cx + 9.35 * sc, cy, cy + 8.04 * sc, 253.0, "8.04 ±0.05 (主法蘭深)")
    dim_v(ax, cx + 9.85 * sc, cx + 6.20 * sc, cy, cy + 9.55 * sc, 264.0, "9.55 ±0.05 (內錐起點深)")
    dim_v(ax, cx + 9.85 * sc, cx + 2.04 * sc, cy, cy + 11.55 * sc, 275.0, "11.55 (內夾持錐頂深)")

    # Top horizontal diameters (part top = 84 + 14.87*7.5 = 195.5)
    dim_h(ax, cx - 2.04 * sc, cx + 2.04 * sc, cy + 14.87 * sc, cy + 14.87 * sc, 207.0, "Ø4.08 +0.05/-0 (外管穿出導引孔)")
    dim_h(ax, cx - 3.10 * sc, cx + 3.10 * sc, cy + 14.87 * sc, cy + 14.87 * sc, 220.0, "Ø6.20 ±0.06 (頂端平肩外徑)")
    dim_h(ax, cx - 5.75 * sc, cx + 5.75 * sc, cy + 9.55 * sc, cy + 9.55 * sc, 233.0, "Ø11.50 → Ø4.08 (免膠夾持內錐面)")
    dim_h(ax, cx - 6.20 * sc, cx + 6.20 * sc, cy + 8.80 * sc, cy + 8.80 * sc, 246.0, "Ø12.40 +0.08/-0 (匯流凸台容置孔)")

    # Bottom horizontal diameters (part bottom = 84.0)
    dim_h(ax, cx - 9.35 * sc, cx + 9.35 * sc, cy + 7.2 * sc, cy + 7.2 * sc, 70.0, "Ø18.70 +0.08/-0 (密封座主法蘭孔)")
    dim_h(ax, cx - 9.85 * sc, cx + 9.85 * sc, cy, cy, 57.0, "Ø19.70 +0.08/-0 (防脫扣唇容置孔)")
    dim_h(ax, cx - 11.00 * sc, cx + 11.00 * sc, cy + 2.2 * sc, cy + 2.2 * sc, 44.0, "Ø22.00 ±0.10 (外蓋圓筒外徑)")
    dim_h(ax, cx - 11.98 * sc, cx + 11.98 * sc, cy, cy, 31.0, "23.96 ±0.05 (Poka-Yoke 卡耳外跨距)")

    # Right Upper: Top/Bottom Poka-Yoke Plan View (x = 286..408, y = 152..258)
    rx, ry, rsc = 347.0, 200.0, 3.0
    ax.add_patch(Rectangle((286, 150), 122, 110, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    ax.text(rx, 254, "俯視防呆卡耳圖 (TOP VIEW, 3.0:1)", ha="center", va="center", fontsize=7.4, fontweight="bold", color="#0F172A")

    # Asymmetric lugs: +X wide (26 deg), -X narrow (15 deg)
    ax.add_patch(Wedge((rx, ry), 11.98 * rsc, -13.0, 13.0, fc="#BAC370", ec="#4D531B", lw=0.85))
    ax.add_patch(Wedge((rx, ry), 11.98 * rsc, 180.0 - 7.5, 180.0 + 7.5, fc="#BAC370", ec="#4D531B", lw=0.85))
    ax.add_patch(Circle((rx, ry), 11.00 * rsc, fc="#D9DF9D", ec="#4D531B", lw=1.0))
    for i in range(16):
        ang = math.radians((i + 0.5) * 22.5)
        ax.add_patch(Circle((rx + 11.15 * rsc * math.cos(ang), ry + 11.15 * rsc * math.sin(ang)), 0.45 * rsc, fc="#FFFFFF", ec="#4D531B", lw=0.5))
    for r_dash in (9.85, 9.35, 6.20):
        ax.add_patch(Circle((rx, ry), r_dash * rsc, fill=False, ec="#64748B", ls="--", lw=0.5))
    ax.add_patch(Circle((rx, ry), 3.10 * rsc, fill=False, ec="#4D531B", lw=0.8))
    ax.add_patch(Circle((rx, ry), 2.04 * rsc, fc="#FFFFFF", ec="#4D531B", lw=0.95))
    ax.plot([rx - 14 * rsc, rx + 14 * rsc], [ry, ry], color="#DC2626", ls="-.", lw=0.4)
    ax.plot([rx, rx], [ry - 13 * rsc, ry + 13 * rsc], color="#DC2626", ls="-.", lw=0.4)

    callout(ax, (rx + 11.8 * rsc, ry + 2.0), (rx + 14, ry + 42), "+X 寬防呆卡耳\n弧角 26° ±0.5°", fontsize=5.8)
    callout(ax, (rx - 11.8 * rsc, ry - 2.0), (rx - 58, ry - 41), "-X 窄防呆卡耳\n弧角 15° ±0.5°", fontsize=5.8)
    callout(ax, (rx + 7.8 * rsc, ry - 7.8 * rsc), (rx + 10, ry - 41), "16道外周止滑直槽\nR0.45 × 長 9.00", fontsize=5.7)

    # Right Lower: Dual 3D Isometric Renders + Molding Notes (x = 286..408, y = 48..145)
    ax.add_patch(Rectangle((286, 48), 122, 97, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    place_image_cropped(ax, ROOT / "tmp/mixer_p1_iso.png", (289, 82, 56, 56))
    place_image_cropped(ax, ROOT / "tmp/mixer_p1_bot.png", (348, 82, 56, 56))
    ax.text(317, 140, "頂視立體圖 (Top Iso)", ha="center", fontsize=5.8, fontweight="bold", color="#334155")
    ax.text(376, 140, "底腔立體圖 (Cavity Iso)", ha="center", fontsize=5.8, fontweight="bold", color="#334155")
    p1_notes = [
        "● 模具結構：內腔自 Ø19.70 → Ø4.08 單調遞減無倒扣，",
        "   單支下公模仁直抽即可脫模（免內滑塊機構）。",
        "● 外表面：止滑肋區火花紋 VDI 24；內錐壓緊面 Ra ≤ 0.8 µm。",
        "● 未注圓角 R0.20 mm；頂針設置於底端環形端面。",
    ]
    for i, ln in enumerate(p1_notes):
        ax.text(289, 75 - i * 6.4, ln, fontsize=5.35, color="#1E293B", va="center")

    _save_sheet(pdf, fig, 2)


# ==============================================================================
# SHEET 3: PART 1-2 DUAL-CHANNEL MANIFOLD SEAL SEAT (CSL-CAP-201-2)
# ==============================================================================
def build_sheet_3(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        3, 5, "CSL-CAP-201-2",
        "零件 1-2：雙流道分流密封內座 — 單件製造工程圖",
        "PART #1-2: DUAL-CHANNEL MANIFOLD ELASTOMER SEAL SEAT — DETAIL DRAWING",
        "8.5 : 1 (SECTION)",
        "MEDICAL SILICONE / TPE (SHORE A 60 ±5, BROWN)",
    )

    sc = 8.5
    cx, cy = 132.0, 106.0
    ax.text(cx, 270, "全剖視圖 SECTION B-B (XZ 雙流道中心剖面, SCALE 8.5:1)", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#0F172A")

    draw_xz_section(
        ax,
        ROOT / "STEP/mixer_part2_seal_seat.step",
        cx=cx,
        cy=cy,
        scale=sc,
        color_map={"mixer_part2": ("#DDB892", "#6C3B1C")},
    )
    ax.plot([cx, cx], [cy - 6, cy + 8.6 * sc], color="#DC2626", ls="-.", lw=0.48)
    for nx in (-4.00, 4.00):
        ax.plot([cx + nx * sc, cx + nx * sc], [cy - 6, cy + 7.8 * sc], color="#2563EB", ls="-.", lw=0.45)

    # Left vertical heights (part min X = 132 - 9.80*8.5 = 48.7)
    dim_v(ax, cx - 6.80 * sc, cx - 6.10 * sc, cy, cy + 7.40 * sc, 21.0, "7.40 ±0.08 (密封座總高)")
    dim_v(ax, cx - 6.80 * sc, cx - 9.80 * sc, cy, cy + 4.40 * sc, 34.0, "4.40 ±0.05 (雙下套筒長)")

    # Right vertical heights (part max X = 132 + 9.80*8.5 = 215.3)
    dim_v(ax, cx + 5.63 * sc, cx + 5.63 * sc, cy, cy + 1.95 * sc, 226.0, "1.95 ±0.05 (母套孔深)")
    dim_v(ax, cx + 9.80 * sc, cx + 9.80 * sc, cy + 4.40 * sc, cy + 6.40 * sc, 244.0, "2.00 ±0.05 (雙階法蘭總厚: 0.78+1.22)")
    dim_v(ax, cx + 6.10 * sc, cx + 6.10 * sc, cy + 6.40 * sc, cy + 7.40 * sc, 260.0, "1.00 ±0.05 (頂凸台高)")

    # Top horizontal diameters (part top = 106 + 7.40*8.5 = 168.9)
    dim_h(ax, cx - 5.00 * sc, cx + 5.00 * sc, cy + 7.40 * sc, cy + 7.40 * sc, 181.0, "Ø10.00 ±0.05 (頂部匯流槽內徑)")
    dim_h(ax, cx - 6.10 * sc, cx + 6.10 * sc, cy + 7.40 * sc, cy + 7.40 * sc, 194.0, "Ø12.20 ±0.06 (頂部密封凸台外徑)")
    dim_h(ax, cx - 9.30 * sc, cx + 9.30 * sc, cy + 6.40 * sc, cy + 6.40 * sc, 207.0, "Ø18.60 ±0.08 (主定位法蘭外徑)")
    dim_h(ax, cx - 9.80 * sc, cx + 9.80 * sc, cy + 5.18 * sc, cy + 5.18 * sc, 220.0, "Ø19.60 ±0.08 (防脫出下扣唇外徑)")

    # Route diverter-island callout cleanly from BELOW center (zero crossing of top horizontal dims!)
    callout(
        ax,
        (cx, cy + 4.70 * sc),
        (cx, 26.0),
        "中央倒錐分流島 (Ø4.20→Ø5.40) + 0.80mm 分流隔板\n將 A/B 兩液完全隔離導引至 1-3 喇叭口入口",
        ha="center",
        fontsize=6.0,
    )

    # Bottom horizontal dims (below cy = 106.0)
    dim_h(ax, cx + 3.10 * sc, cx + 4.90 * sc, cy + 2.5 * sc, cy + 2.5 * sc, 91.0, "Ø1.80 ±0.04 (2X 獨立立孔)")
    dim_h(ax, cx - 5.63 * sc, cx - 2.37 * sc, cy, cy, 76.0, "Ø3.10 ±0.05 成型內徑 (2X 過盈密封孔)")
    dim_h(ax, cx + 1.20 * sc, cx + 6.80 * sc, cy, cy, 61.0, "Ø5.60 ±0.06 (2X 套筒外徑)")
    dim_h(ax, cx - 4.00 * sc, cx + 4.00 * sc, cy, cy, 46.0, "8.00 ±0.03 (雙入口套筒中心距)")

    # Right Upper: Top Plan View of Part 1-2 (x = 276..408, y = 152..258)
    rx, ry, rsc = 342.0, 200.0, 3.6
    ax.add_patch(Rectangle((276, 150), 132, 110, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    ax.text(rx, 254, "俯視分流結構圖 (TOP VIEW, 3.6:1)", ha="center", va="center", fontsize=7.4, fontweight="bold", color="#0F172A")

    ax.add_patch(Circle((rx, ry), 9.80 * rsc, fc="#C69C72", ec="#6C3B1C", lw=0.9))
    ax.add_patch(Circle((rx, ry), 9.30 * rsc, fc="#DDB892", ec="#6C3B1C", lw=0.9))
    ax.add_patch(Circle((rx, ry), 6.10 * rsc, fc="#E6CCB2", ec="#6C3B1C", lw=0.95))
    ax.add_patch(Circle((rx, ry), 5.00 * rsc, fc="#FFF8F0", ec="#6C3B1C", lw=0.95))
    ax.add_patch(Circle((rx, ry), 2.70 * rsc, fc="#DDB892", ec="#6C3B1C", lw=0.8))
    # Central 0.80 mm partition rib across Y
    ax.add_patch(Rectangle((rx - 0.40 * rsc, ry - 5.00 * rsc), 0.80 * rsc, 10.00 * rsc, fc="#C69C72", ec="#6C3B1C", lw=0.85, zorder=5))
    # Dual Ø1.80 ports at X = ±4.00 mm + dashed Ø5.60 lower sleeves
    for nx, ch_lbl in ((-4.00, "B流道"), (4.00, "A流道")):
        ax.add_patch(Circle((rx + nx * rsc, ry), 2.80 * rsc, fill=False, ec="#64748B", ls="--", lw=0.55))
        ax.add_patch(Circle((rx + nx * rsc, ry), 0.90 * rsc, fc="#FFFFFF", ec="#1E3A8A", lw=0.95, zorder=6))
        ax.text(
            rx + nx * rsc, ry - 2.3 * rsc, ch_lbl,
            ha="center", va="top", fontsize=5.3, fontweight="bold", color="#1E3A8A",
            bbox=dict(boxstyle="square,pad=0.06", facecolor="#FFF8F0", edgecolor="none", alpha=0.88),
            zorder=7,
        )

    dim_h(ax, rx - 0.40 * rsc, rx + 0.40 * rsc, ry + 5.0 * rsc, ry + 5.0 * rsc, ry + 24.0, "0.80 ±0.04 (中央隔離肋厚)")

    # Right Lower: 3D Top & Bottom Isometric + Elastomer Spec (x = 276..408, y = 48..145)
    ax.add_patch(Rectangle((276, 48), 132, 97, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    place_image_cropped(ax, ROOT / "tmp/mixer_p2_iso.png", (280, 82, 60, 56))
    place_image_cropped(ax, ROOT / "tmp/mixer_p2_bot.png", (344, 82, 60, 56))
    ax.text(310, 140, "頂部分流槽立體圖", ha="center", fontsize=5.8, fontweight="bold", color="#334155")
    ax.text(374, 140, "底部雙母套孔立體圖", ha="center", fontsize=5.8, fontweight="bold", color="#334155")
    p2_notes = [
        "● 材質：醫療級鉑金硫化矽膠 (LSR) 或醫用 TPE，硬度 Shore A 60±5。",
        "● 氣密配合：雙母套孔成型 Ø3.10±0.05 mm，套入針筒 Ø3.20 公嘴產生",
        "   0.10 mm 徑向彈性過盈；頂端壓承 1-3 平底緣達成免膠水雙向氣密。",
        "● 開模：全直孔無彎折流道，上下直抽芯針即可成型，毛邊 ≤ 0.04 mm。",
    ]
    for i, ln in enumerate(p2_notes):
        ax.text(280, 75 - i * 6.4, ln, fontsize=5.3, color="#1E293B", va="center")

    _save_sheet(pdf, fig, 3)


# ==============================================================================
# SHEET 4: PART 1-3 ONE-PIECE BELL-MOUTH MIXING CANNULA (CSL-CAP-201-3)
# ==============================================================================
def build_sheet_4(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        4, 5, "CSL-CAP-201-3",
        "零件 1-3：一體式喇叭口透明混合外管 — 單件製造工程圖",
        "PART #1-3: ONE-PIECE BELL-MOUTH CLEAR MIXING CANNULA — DETAIL DRAWING",
        "5.5 : 1 & 11 : 1",
        "MEDICAL CLEAR POLYCARBONATE (PC) / COC",
    )

    sc = 5.5
    cx, cy = 122.0, 56.0
    ax.text(cx, 270, "全剖視圖 SECTION C-C (5.5:1)", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#0F172A")

    draw_xz_section(
        ax,
        ROOT / "STEP/mixer_part3_bell_cannula.step",
        cx=cx,
        cy=cy,
        scale=sc,
        color_map={"mixer_part3": ("#BAE6FD", "#0369A1")},
    )
    ax.plot([cx, cx], [cy - 6, cy + 34.0 * sc], color="#DC2626", ls="-.", lw=0.48)
    for sign in (-1.0, 1.0):
        ax.plot([cx + sign * 1.50 * sc, cx + sign * 1.50 * sc], [cy + 1.86 * sc, cy + 32.56 * sc], color="#0369A1", lw=0.55, zorder=3.5)

    # Left vertical heights
    dim_v(ax, cx - 5.70 * sc, cx - 2.00 * sc, cy, cy + 32.56 * sc, 42.0, "32.56 ±0.10 (一體式外管總長；標稱 32.60)")
    dim_v(ax, cx - 5.70 * sc, cx - 2.00 * sc, cy, cy + 2.46 * sc, 58.0, "2.46 ±0.05 (喇叭口外錐高)")
    dim_v(ax, cx - 2.00 * sc, cx - 2.00 * sc, cy + 5.83 * sc, cy + 32.56 * sc, 74.0, "26.73 (伸出 1-1 外蓋之外露長)")

    # Right vertical heights
    dim_v(ax, cx + 2.00 * sc, cx + 2.00 * sc, cy + 2.46 * sc, cy + 32.56 * sc, 168.0, "30.10 (Ø4.00 直管段長)")
    dim_v(ax, cx + 5.00 * sc, cx + 1.50 * sc, cy, cy + 1.86 * sc, 184.0, "1.86 ±0.05 (內防脫收束錐深)")

    # Top & Bottom horizontal diameters
    dim_h(ax, cx - 1.50 * sc, cx + 1.50 * sc, cy + 32.56 * sc, cy + 32.56 * sc, 245.0, "Ø3.00 +0.04/-0 (混合管內徑 ID)")
    dim_h(ax, cx - 2.00 * sc, cx + 2.00 * sc, cy + 32.56 * sc, cy + 32.56 * sc, 258.0, "Ø4.00 ±0.04 (混合管外徑 OD，壁厚 0.50)")
    dim_h(ax, cx - 5.00 * sc, cx + 5.00 * sc, cy, cy, 41.0, "Ø10.00 ±0.05 (底部喇叭進料口內徑)")
    dim_h(ax, cx - 5.70 * sc, cx + 5.70 * sc, cy, cy, 28.0, "Ø11.40 ±0.06 (底部免膠夾持法蘭外徑)")

    # Center-Right Upper: Enlarged Detail D of Flared Bell Base (Scale 10.0:1)
    ax.add_patch(Rectangle((212, 150), 196, 110, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    ax.text(310, 254, "局部放大圖 DETAIL D — 喇叭口基座剖面 (10:1)", ha="center", va="center", fontsize=7.4, fontweight="bold", color="#0369A1")

    dsc = 10.0
    dcx, dcy = 278.0, 174.0
    draw_xz_section(
        ax,
        ROOT / "STEP/mixer_part3_bell_cannula.step",
        cx=dcx,
        cy=dcy,
        scale=dsc,
        color_map={"mixer_part3": ("#BAE6FD", "#0369A1")},
        z_clip_max=5.2,
    )
    ax.plot([dcx, dcx], [dcy - 4, dcy + 5.6 * dsc], color="#DC2626", ls="-.", lw=0.45)
    dim_v(ax, dcx - 5.70 * dsc, dcx - 5.70 * dsc, dcy, dcy + 0.46 * dsc, dcx - 63, "0.46 (壓緣厚)", fontsize=6.0)
    dim_h(ax, dcx - 5.70 * dsc, dcx + 5.70 * dsc, dcy, dcy, dcy - 10, "Ø11.40 法蘭外徑 / Ø10.00 內口", fontsize=6.1)
    callout(ax, (dcx + 3.4 * dsc, dcy + 1.6 * dsc), (344.0, 232.0), "外夾持斜錐 (Ø11.40→Ø4.00)\n受 1-1 內錐面軸向壓緊免膠水", fontsize=5.6)
    callout(ax, (dcx + 2.8 * dsc, dcy + 0.9 * dsc), (344.0, 202.0), "內收束防脫錐 (Ø10.00→Ø3.00)\n正止擋 1-4 之 Ø4.40 底座！", fontsize=5.6)

    # Right Lower: 3D Render + Optical & Core-Pin Tooling Spec (x = 212..408, y = 48..145)
    ax.add_patch(Rectangle((212, 48), 196, 97, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    place_image_cropped(ax, ROOT / "tmp/mixer_p3_iso.png", (216, 52, 62, 88))
    ax.text(342, 138, "【光學透明與長芯針射出成型規範】", ha="center", fontsize=7.2, fontweight="bold", color="#0F172A")
    p3_notes = [
        "1. 一體成型優勢：喇叭口匯流罩與 Ø4.00 直管為單一透明射出件，",
        "   徹底消除傳統兩件黏接處在高黏度水凝膠推注壓下爆管滲漏風險。",
        "2. 醫療光學要求：透明醫療級 PC / COC，可見光穿透率 ≥ 88%，",
        "   供臨床醫師術中即時目視確認排氣完成與雙液混合均勻狀態。",
        "3. 精密長芯針規範：內孔自底端 Ø10.00 單調縮徑至 Ø3.00 直管，",
        "   採用單支鏡面拋光長芯針 (Ra ≤ 0.2 µm) 由 -Z 方向一次抽芯；",
        "   直管內孔拔模斜度 ≤ 0.20°，偏心度 (同軸度) ≤ 0.04 mm。",
    ]
    for i, ln in enumerate(p3_notes):
        ax.text(280, 127 - i * 10.6, ln, fontsize=5.45, color="#1E293B", va="center")

    _save_sheet(pdf, fig, 4)


# ==============================================================================
# SHEET 5: PART 1-4 9-ELEMENT KENICS HELICAL CORE (CSL-CAP-201-4)
# ==============================================================================
def build_sheet_5(pdf: PdfPages) -> None:
    fig, ax = new_a3_sheet(
        5, 5, "CSL-CAP-201-4",
        "零件 1-4：防脫出底座靜態螺旋混合芯 — 單件製造工程圖",
        "PART #1-4: 9-ELEMENT KENICS HELICAL STATIC MIXER CORE WITH ANTI-EJECTION COLLAR",
        "6.2 : 1 & 12 : 1",
        "MEDICAL GRADE POM (ACETAL COPOLYMER, MAROON)",
    )

    sc = 6.2
    cx_f, cx_s, cy = 88.0, 168.0, 56.0
    ax.text(cx_f, 270, "正視圖 FRONT (0°, 6.2:1)", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#0F172A")
    ax.text(cx_s, 270, "右側視圖 RIGHT (90°, 6.2:1)", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#0F172A")

    draw_brep_ortho_edges(ax, ROOT / "STEP/mixer_part4_helical_core.step", cx_f, cy, sc, "X", "Z", "#7F1D1D", "#FECACA")
    draw_brep_ortho_edges(ax, ROOT / "STEP/mixer_part4_helical_core.step", cx_s, cy, sc, "Y", "Z", "#7F1D1D", "#FECACA")
    ax.plot([cx_f, cx_f], [cy - 6, cy + 29.2 * sc], color="#DC2626", ls="-.", lw=0.45)
    ax.plot([cx_s, cx_s], [cy - 6, cy + 29.2 * sc], color="#DC2626", ls="-.", lw=0.45)

    # Vertical dimensions on Front & Side views (28.00 * 6.2 = 173.6 -> y = 56..229.6)
    dim_v(ax, cx_f - 2.20 * sc, cx_f - 1.43 * sc, cy, cy + 28.00 * sc, 36.0, "28.00 ±0.10 (螺旋混合芯總長)")
    dim_v(ax, cx_f - 1.70 * sc, cx_f - 1.43 * sc, cy + 1.00 * sc, cy + 28.00 * sc, 52.0, "27.00 (9節正反螺旋有效混合長)")
    dim_v(ax, cx_s + 1.43 * sc, cx_s + 1.43 * sc, cy + 22.00 * sc, cy + 25.00 * sc, 200.0, "3.00 ±0.04 (單節180°節距×9)")
    dim_v(ax, cx_s + 2.20 * sc, cx_s + 1.70 * sc, cy, cy + 1.00 * sc, 214.0, "1.00 ±0.04 (防脫底座高)")

    # Top & Bottom horizontal dimensions
    dim_h(ax, cx_f - 1.43 * sc, cx_f + 1.43 * sc, cy + 28.00 * sc, cy + 28.00 * sc, 242.0, "2.86 ±0.03 (葉片跨距，配 Ø3.00 內孔)")
    dim_h(ax, cx_s - 0.21 * sc, cx_s + 0.21 * sc, cy + 28.00 * sc, cy + 28.00 * sc, 255.0, "0.42 ±0.03 (葉片與分流刃厚)")
    dim_h(ax, cx_f - 1.70 * sc, cx_f + 1.70 * sc, cy + 1.00 * sc, cy + 1.00 * sc, 42.0, "Ø3.40 (錐環頂徑 > Ø3.00 管孔)")
    dim_h(ax, cx_f - 2.20 * sc, cx_f + 2.20 * sc, cy, cy, 28.0, "Ø4.40 ±0.05 (尾部防射出圓錐底座外徑)")

    # Element orientation tags along middle between Front & Side views
    for idx in range(9):
        zy = cy + (2.50 + idx * 3.00) * sc
        hand = "R" if idx % 2 == 0 else "L"
        ax.text(128.0, zy, f"#{idx+1} ({hand} 180°)", ha="center", va="center", fontsize=5.2, color="#7F1D1D", fontweight="bold")

    # Right Upper: Bottom Plan View (12:1) + 3D Isometric Render (x = 232..408, y = 148..258)
    ax.add_patch(Rectangle((232, 148), 176, 112, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    ax.text(282, 253, "底部防脫分流環仰視圖 (12:1)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#991B1B")
    bx_p, by_p, bsc = 282.0, 198.0, 12.0
    ax.add_patch(Circle((bx_p, by_p), 2.20 * bsc, fc="#FCA5A5", ec="#7F1D1D", lw=1.0))
    ax.add_patch(Circle((bx_p, by_p), 1.70 * bsc, fc="#FEE2E2", ec="#7F1D1D", lw=0.8))
    ax.add_patch(Circle((bx_p, by_p), 1.20 * bsc, fc="#FFFFFF", ec="#7F1D1D", lw=0.85))
    # X splitter fin + Y cross-spoke + central hub
    ax.add_patch(Rectangle((bx_p - 0.26 * bsc, by_p - 1.55 * bsc), 0.52 * bsc, 3.10 * bsc, fc="#F87171", ec="#7F1D1D", lw=0.75))
    ax.add_patch(Rectangle((bx_p - 2.15 * bsc, by_p - 0.21 * bsc), 4.30 * bsc, 0.42 * bsc, fc="#EF4444", ec="#7F1D1D", lw=0.85))
    ax.add_patch(Circle((bx_p, by_p), 0.62 * bsc, fc="#DC2626", ec="#7F1D1D", lw=0.8))
    ax.text(bx_p, by_p - 34, "XZ 前緣分流刃 (厚0.42)\n同步對半切割 A/B 雙股流體", ha="center", va="center", fontsize=5.6, fontweight="bold", color="#7F1D1D")

    place_image_cropped(ax, ROOT / "tmp/mixer_p4_iso.png", (338, 152, 66, 98))
    ax.text(371, 253, "3D 立體圖", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#334155")

    # Right Lower: Kenics Mixing Mechanics & Split-Mold Specification (x = 232..408, y = 48..143)
    ax.add_patch(Rectangle((232, 48), 176, 95, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=0.6))
    ax.text(320, 136, "【靜態螺旋混合流體力學與對開滑塊模具規範】", ha="center", fontsize=7.2, fontweight="bold", color="#0F172A")
    p4_notes = [
        "1. 指數分層混合效率：共 9 節正反交錯 180° 扭轉 Kenics 螺旋葉片",
        "   (#1,#3,#5,#7,#9 右旋 180°；#2,#4,#6,#8 左旋 180°)，相鄰節前緣",
        "   呈 90° 正交切割，流體層數 N = 2⁹ = 512 層，確保雙液瞬時均質成膠。",
        "2. 結構補強圓轂：每節 90° 正交交界處設 Ø1.12 × 0.50 mm 中心連接轂，",
        "   防止高黏度 PEG 水凝膠推注壓力下發生螺旋芯軸向拉伸斷裂。",
        "3. 模具與材質：選用醫療級高流動性 POM 塑鋼 (MFR ≥ 25 g/10min)，",
        "   採左右對開哈夫滑塊精密模具成型，分模面毛邊嚴格管控 ≤ 0.03 mm。",
    ]
    for i, ln in enumerate(p4_notes):
        ax.text(236, 125 - i * 10.5, ln, fontsize=5.35, color="#1E293B", va="center")

    _save_sheet(pdf, fig, 5)


def main() -> None:
    out_pdf = ROOT / "PDF" / "螺旋混合頭_四件式零件拆解設計圖_RevC.pdf"
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(out_pdf) as pdf:
        build_sheet_1(pdf)
        build_sheet_2(pdf)
        build_sheet_3(pdf)
        build_sheet_4(pdf)
        build_sheet_5(pdf)
    print(f"Wrote 5-sheet 4-Part Mixer Detail Blueprint PDF: {out_pdf}")


if __name__ == "__main__":
    main()
