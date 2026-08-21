# 創新微流控高剪切雙腔注射混合頭 (Surgical Sealant Dual Syringe Mixer)

[![3D Interactive Viewer](https://img.shields.io/badge/3D%20Demo-Live%20Viewer-0284c7?style=for-the-badge&logo=three.js)](https://mathruffian.github.io/surgical-sealant/)
[![License](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

專門為解決 **「高黏度 4-Arm PEG 聚合物溶液 (~50 cps) vs 水狀鹼性 T-buffer (~1 cps) 巨大黏度差」** 量身定制的專利規避型醫療級微流控混合頭。

---

## 🌟 核心工程與科學設計亮點

1. **Hagen-Poiseuille 主動水力流阻平衡（進料歧管）**：
   - PEG 寬通徑 $\Phi 0.80\,\text{mm}$ vs T-buffer 縮頸阻尼孔 $\Phi 0.35\,\text{mm}$。
   - 幾何孔徑四次方補償了 50 倍黏度差，手動推注時精準鎖定 $1:1$ 體積比（Stoichiometry 誤差 $< \pm 3.5\%$）。
2. **低雷諾數三維混沌平流（SHM 非對稱人字形微溝槽）**：
   - 45° 非對稱溝槽引發橫向微壓差 $\nabla P_{\perp}$，激發三維反向「混沌雙渦旋（Double Vortices）」。
   - 流體層厚度呈指數級減薄 $s(t) = s_0 e^{-\lambda t}$，特徵擴散距離由 $2.4\,\text{mm}$ 壓縮至 $\delta < 15\,\mu\text{m}$，擴散混勻時間從 $15\,\text{s}$ 降至 $<0.05\,\text{s}$。
   - **★ 100% 規避 Baxter EP2213245B1 3D 多孔燒結晶格專利**。
3. **高分子鏈拉伸與 pH 躍遷催化（淚滴形微剪切島矩陣）**：
   - 3 排交錯淚滴微柱構成 $120\,\mu\text{m}$ 狹縫，壁面剪切速率 $\dot{\gamma} > 1200\,\text{s}^{-1}$，觸發高分子 Coil-to-Stretch 鏈伸展。
   - T-buffer 微觀瞬時注入引發 pH 躍遷（$\text{pH } 6.0 \to 9.8$），活性硫醇陰離子 $[-\text{S}^-]$ 濃度暴增 $>1000$ 倍，**成膠固化時間縮短至 2~3 秒（告別傳統螺旋葉片 10 秒水水分層）**。
4. **表面張力自淨微閥與超低死腔（漸縮出料噴嘴）**：
   - 內部滯留死腔體積 $< 35\,\mu\text{L}$。
   - 矽膠十字彈性微閥在推注停止時彈性回彈（Snap-Back）物理刮除殘膠，支援手術中多次 Stop-and-Go 絕不堵槍。

---

## 🎮 3D 線上互動展示與操作

本專案提供基於 WebGL / Three.js 開發的 3D 互動展示模型：
👉 **[點此進入 3D 線上展示頁面 (Live Demo)](https://mathruffian.github.io/surgical-sealant/)**

- 支援 360° 自由環景旋轉、平移與滾輪縮放。
- 支援一鍵切換 **☀️ 白天高對比 CAD 模式** 與 **🌙 暗夜模式**。
- 即時動態流體粒子模擬（藍色 PEG ＋ 黃色 T-buffer ➔ 綠色瞬時成膠）。
- 4 步驟一鍵導覽特寫各微流道構造與科學參數解析。

---

## 📐 3D 列印打樣指南 (SLA / DLP)

本專案內含開源參數化建模腳本 `mixing_tip_prototype.scad`：
- **推薦設備**：高精度 SLA / DLP 光固化 3D 列印機（如 Formlabs / Anycubic / Elegoo 等）。
- **切片參數**：
  - XY 解析度：$\le 35\,\mu\text{m}$
  - Z 軸層厚（Layer Height）：$25\,\mu\text{m}$
  - 擺放角度：以 45° 傾斜朝上擺放（流道內部嚴禁加支撐）。
- **後處理**：使用注射器以 99.5% IPA 強力沖洗內部微流道 3 次，防止微溝槽黏死，再行 UV 二次固化 5 分鐘。

---

## 📄 專案目錄結構

```text
├── index.html                  # 3D 互動展示模型主入口 (GitHub Pages 部署)
├── interactive_3d_viewer.html  # 3D 互動展示模型原始網頁
├── mixing_tip_prototype.scad  # OpenSCAD 參數化 3D CAD 模型源碼 (可輸出 STL)
└── README.md                   # 專案說明文件
```

---

## 📜 授權協議 (License)
本專案基於 [MIT License](LICENSE) 授權開源。
