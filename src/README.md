# 雙單管混合裝置 3D CAD 模型與工程圖原始碼目錄 (`src/`)

本目錄包含參考 **Baxter CoSeal** 雙腔手術封合劑系統並補齊原委託廠商（禾晉有限公司 `20261028雙單管混合裝置`）設計缺漏之 **Rev. B 完整參數化 B-Rep 3D CAD 原始碼**（基於 `cadgen 0.7.21` / `build123d` OCCT 核心）。

---

## 1. 參數庫與共用幾何模組 (`src/lib/`)

| 檔案 | 說明 |
| :--- | :--- |
| `lib/specs.py` | 全系統主參數表（Master Parametric Spec Table）：包含廠商原圖 1:1 尺寸、雙筒容量計算（單管工作 4.0 mL / 最大 5.0 mL）、非對稱防呆卡口角度、ISO 80369-7 6% 魯爾錐度與配合公差 |
| `lib/cap_features.py` | 三款功能蓋（`#1`、`#2`、`#3`）共用之非對稱防呆卡口翼片（26° 寬耳 / 15° 窄耳，外跨 23.96 mm）與雙流道醫用矽膠彈性塞座模組 |

---

## 2. 零件與次組件 3D 模型腳本 (`@cad_model`)

執行任一腳本即可重新建構對應之 `../STEP/*.step`（及 STL / 3MF / GLB 網格檔）：

| 原始碼檔案 | 對應圖號 / 名稱 | 匯出檔案 | 關鍵機構特徵 |
| :--- | :--- | :--- | :--- |
| `dual_barrel_body.py` | `CSL-PRT-101` 雙連針筒本體 | `STEP/dual_barrel_body.step`, `STL/dual_barrel_body.stl` | 雙腔中心距 14.40 mm、內徑 Ø12.20 mm、人體工學蝶翼指托 46.10 × 33.41 mm、Ø3.20 雙公頭出液嘴（間距 8.00 mm）及 +Y 60° / -Y 20° 防呆卡口環 |
| `plunger_rod.py` | `CSL-PRT-102` 十字肋推桿 | `STEP/plunger_rod.step`, `STL/plunger_rod.stl` | 十字導引肋 Ø12.00 mm、中段 Ø6.40 樞軸頸部、Ø12.80 尾端推盤、前端球頭卡榫 |
| `elastomer_stopper.py` | `CSL-PRT-103` 雙環醫用橡膠活塞 | `STEP/elastomer_stopper.step`, `STL/elastomer_stopper.stl` | 三道環形密封唇（成型 Ø12.50 mm，裝配壓縮至 Ø12.16 mm）、高 7.00 mm、底部球窩卡槽 |
| `plunger_clip.py` | `CSL-PRT-104` `#4 單雙管推拉切換片` | `STEP/plunger_clip.step`, `STL/plunger_clip.stl` | 30.00 × 16.40 × 4.00 mm；左側常駐樞軸孔扣於 B 推桿頸部可旋 90°，右側 C 型彈扣顎（開口 11.90 mm）鎖定/解鎖 A 推桿 |
| `helical_mixer_cap.py` | `CSL-SUB-201` `#1 螺旋混合雙管蓋` | `STEP/helical_mixer_cap.step`, `STL/helical_mixer_cap.stl` | 5 件式次組件（卡口下座、矽膠雙孔塞座、Y 型分流漏斗、Ø4.00/Ø3.00 混合外管、8 節正反旋 180° Kenics 靜態螺旋葉片），總長 41.60 mm |
| `luer_transfer_cap.py` | `CSL-SUB-202` `#2 魯爾混合單管蓋` | `STEP/luer_transfer_cap.step`, `STL/luer_transfer_cap.stl` | 4 件式次組件（Ø30 紫色 65° 旋鎖外環、青色止轉內座 +4.00 mm 偏心 ISO 80369-7 6% 母魯爾接口、B 腔盲塞矽膠墊、止轉定位銷），總高 15.00 mm |
| `initial_plug_cap.py` | `CSL-SUB-203` `#3 初始塞閥蓋` | `STEP/initial_plug_cap.step`, `STL/initial_plug_cap.stl` | 2 件式次組件（藍色卡口外蓋 + 雙盲塞醫用矽膠彈性塞），總高 17.00 mm，供出廠無菌雙液封存 |
| `powder_syringe.py` | `CSL-REF-301` 單管粉劑魯爾注射筒 | `STEP/powder_syringe.step` | Stage 2 單管預混狀態展示用公魯爾鎖定（Male Luer-Lock）參考針筒組件 |

---

## 3. 總成模型與動態機構展示 (`KINEMATICS` & `ANIMATION`)

| 原始碼檔案 | 匯出檔案 | 說明 |
| :--- | :--- | :--- |
| `coseal_device_dispense.py` | `STEP/coseal_device_dispense.step` (+ `.step.json`), `STL/`, `3MF/`, `GLB/` | 雙管點膠總成（總長 166.60 mm），內建 **5 個可動自由度**（`clip_mode_deg` 切換片 0°/90°、`plunger_a_stroke`、`plunger_b_stroke`、`cap_lock_deg`、`cap_lift_mm`）與 `clinical_workflow` 臨床動作動畫 |
| `coseal_system_overview.py` | `STEP/coseal_system_overview.step`, `GLB/coseal_system_overview.glb` | 臨床三階段（Stage 1 封存 → Stage 2 單管魯爾預混 → Stage 3 雙管靜態螺旋點膠）並列展示與全配件總覽 |

---

## 4. 工程製圖腳本 (`PDF/`)

| 原始碼檔案 | 輸出工程圖 PDF | 說明 |
| :--- | :--- | :--- |
| `generate_bilingual_blueprint.py` | `PDF/雙單管混合裝置_完整專業設計圖_RevB.pdf` | **5 張 A3 繁中/英文專業工程藍圖**：含 B-Rep 精確剖面線視圖（Section A-A, B-B, C-C, D-D, E-E）、完整配合公差、防呆卡口角度、10 項 BOM 物料表與三階段機構圖 |
| `coseal_engineering_drawings.py` | `PDF/coseal_iso_engineering_drawings.pdf` | **8 張 A3 ISO 標準第三角法工程投影圖**（使用 `cadgen.drawing.Sheet` 自動投影實線/虛線隱藏線與基準尺寸） |

---

## 5. 建構與確定性幾何驗證指令

於專案根目錄 `/Users/chenyu/Documents/antigravity/surgical sealant` 執行：

```bash
# 重新建構主總成與全系統展示模型
uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/coseal_device_dispense.py
uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/coseal_system_overview.py

# 執行確定性尺寸包絡、拓樸有效性與零干涉驗證（55 組零件對 overlap_volume == 0.00 mm³）
uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python checks/verify_coseal_cad.py

# 重新產出兩套 A3 專業工程設計圖 PDF
MPLCONFIGDIR=/tmp/mpl uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/coseal_engineering_drawings.py
MPLCONFIGDIR=/tmp/mpl uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.21 python src/generate_bilingual_blueprint.py
```
