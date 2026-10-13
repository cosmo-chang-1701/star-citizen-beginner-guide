---
description: 遊戲連線錯誤代碼速查手冊：Error 30000、30009、19004、50001、60015、0 錯誤排查與快速自救步驟。
icon: triangle-exclamation
---

# 附錄 D：錯誤代碼對照表

## 錯誤代碼分類對照矩陣

本節將遊戲所有常見錯誤劃分為三大矩陣：啟動與反作弊、帳號與大廳、伺服器連線與持久化。

### 類別 A：啟動器、圖形驅動與反作弊 (Launcher, GPU & EAC)

此類別問題主要發生於進入 3D 世界之前，集中於本地作業系統環境、顯卡底層驅動、安全防護軟體攔截或反作弊模組衝突。

| 錯誤代碼 | 錯誤訊息與技術成因 | 官方 / 社群實證解決方案 | 參考資料連結 |
| :--- | :--- | :--- | :--- |
| **0 (Code 0)** | **Easy Anti-Cheat (EAC) Initialization Failed / Anti-Cheat Error**<br>`Error - Anticheat (CODE: 0)`。Easy Anti-Cheat 反作弊模組初始化失敗、反作弊核心檔案損壞，或遭到背景防毒/安全防護軟體攔截隔離。 | <ul><li>開啟工作管理員，強制結束所有殘留的 `RSI Launcher` 與 `StarCitizen.exe` 進程。</li><li>進入遊戲安裝目錄 `\StarCitizen\LIVE`，手動刪除整個 `EasyAntiCheat` 資料夾。</li><li>開啟啟動器，進入「Settings」點擊 `VERIFY`（分析遊戲檔案完整性），自動重新下載純淨 EAC 元件。</li><li>關閉可能與反作弊衝突之第三方軟體（如特定 RGB 控制軟體或畫面注入層）。</li></ul> | [官方 RSI 知識庫 - EAC 疑難排解](https://support.robertsspaceindustries.com/hc/en-us/articles/4412276152343-Easy-Anti-Cheat-Troubleshooting) |
| **206 / 207** | **Easy Anti-Cheat (EAC) Validation Failed / Service Error**<br>Easy Anti-Cheat 模組驗證失敗、EAC 執行核心檔案損壞、數位簽章校驗不合，或 EAC 背景守護服務遭安全軟體強制隔離。 | <ul><li>進入遊戲安裝目錄 `\StarCitizen\LIVE`，手動刪除整個 `EasyAntiCheat` 資料夾。</li><li>至使用者路徑 `%appdata%\EasyAntiCheat` 清空暫存檔案。</li><li>開啟啟動器，進入「Settings」頁面點擊 `VERIFY`（驗證），自動重新下載部署純淨 EAC 元件。</li><li>確認防毒軟體未將 `EasyAntiCheat_EOS.sys` 封鎖。</li></ul> | [官方 EAC 疑難排解指南](https://support.robertsspaceindustries.com/hc/en-us/articles/4412276152343-Easy-Anti-Cheat-Troubleshooting) |
| **210** | **Unrecognized Game Client**<br>EAC 引擎無法辨識遊戲客戶端主程式 (`Unrecognized game client. Cannot continue.`)。通常發生在更新修補中斷、二進位檔案校驗和 (Hash) 不符，或第三方注入工具 (如舊版 Reshade / 覆蓋層) 干擾。 | <ul><li>暫時關閉所有第三方遊戲外掛、字型包或畫面注入器 (ReShade / Special K)。</li><li>於啟動器 Settings 中執行完整 `VERIFY` 檔案驗證。</li><li>若驗證無效，執行針對 **206 / 207** 的 EAC 目錄清理重裝 SOP。</li><li>確保遊戲主程式安裝路徑未包含異常特殊字元或非預設捷徑。</li></ul> | [官方 EAC 支援 - 錯誤 210 排查說明](https://eoshelp.epicgames.com/s/article/What-causes-the-anti-cheat-error-Unrecognized-game-client-Cannot-continue) |
| **1275 / 30005** | **EAC Driver Load Error / StartService Failed**<br>EAC 核心驅動程式載入失敗 (`StartService failed with 1275`)。核心成因為 Windows 11 核心隔離 (Core Isolation) 之「記憶體完整性 (HVCI)」或核心模式硬體強制堆疊保護安全策略阻斷未簽章或舊版 EAC 核心驅動載入。 | <ul><li>開啟 Windows「設定」→「隱私權與安全性」→「Windows 安全性」→「裝置安全性」。</li><li>點選「核心隔離詳細資料」，暫時將「記憶體完整性」設為關閉並重新啟動電腦。</li><li>若近期安裝了特定 Windows 預覽更新（如 KB5044376），可檢查是否有後續微軟修補。</li><li>進入 `\StarCitizen\LIVE\EasyAntiCheat`，以管理員身分執行 `EasyAntiCheat_Setup.exe` 點選修復。</li></ul> | [Epic 支援 - EAC Error 1275 處理](https://www.epicgames.com/help/c-202300000001639/c-202300000001736/eac-driver-error-1275-driver-load-error-in-windows-11-a202300000010435) |
| **2000 / 50XX** | **Generic Launcher / Installer / Download Pipeline Failure**<br>啟動器安裝或下載傳輸管道失敗。多因儲存裝置非 NTFS 格式、磁碟寫入權限受阻、剩餘空間不足或 CDN 檔案區塊校驗逾時（包含 5007、5008、5010、5012、5015、5018、5021 等）。 | <ul><li>確認遊戲安裝目錄所在磁碟為 **NTFS** 格式（不支援 exFAT / FAT32），且剩餘可用空間不少於 100 GB。</li><li>以系統管理員身分啟動 RSI Launcher。</li><li>在啟動器 Settings 中將 `Concurrent Downloads` 調降為 5，並設定 `Max Download Speed` 限制頻寬，減輕網路堆疊負載。</li><li>檢視 `%appdata%\rsilauncher\logs` 日誌確認卡住的具體檔案。</li></ul> | [官方 RSI 知識庫 - 錯誤 2000 與 50XX](https://support.robertsspaceindustries.com/hc/en-us/articles/22514899089431-Error-2000-or-50XX) |
| **GPU Crash / GPU Hang** | **Shader Compilation Crash / GPU Timeout Detection and Recovery (TDR)**<br>顯卡設備超時掛起 (`DXGI_ERROR_DEVICE_HUNG` / `GPU Device Instance Paused`)、著色器編譯失敗或顯存 (VRAM) 溢出。多因過期著色器快取、顯卡過度超頻或驅動版本衝突引發。 | <ul><li>**清除著色器快取**：完全刪除 `%localappdata%\Star Citizen` 資料夾內的所有檔案。</li><li>使用 DDU (Display Driver Uninstaller) 工具乾淨移除舊驅動，安裝最新版 NVIDIA / AMD 官方驅動。</li><li>關閉 MSI Afterburner 等工具之顯卡超頻、顯存超頻或降電壓設定，回復原廠預設時脈。</li><li>確保系統分頁檔 (Pagefile) 設在高速 NVMe SSD 上且由系統自動管理（建議不少於 32 GB）。</li><li>若在 Vulkan 模式下頻繁崩潰，可於顯示設定切換至 DirectX 11 進行對照測試。</li></ul> | [官方 RSI 圖形疑難排解指南](https://support.robertsspaceindustries.com/hc/en-us/articles/360000081887-Guide-to-Graphic-Issues) |

### 類別 B：帳號認證與大廳佇列 (Authentication, Entitlement & Lobby)

此類別問題集中於玩家從啟動器登入、帳號資產核對，到大廳匹配並嘗試接入伺服器分片 (Shard) 的過程。

| 錯誤代碼 | 錯誤訊息與技術成因 | 官方 / 社群實證解決方案 | 參考資料連結 |
| :--- | :--- | :--- | :--- |
| **15008 / 16008** | **Account Authentication / Service Outage / CDN Unreachable**<br>雲端身分認證服務中斷 (`CIG services CODE 16008` / `Account data update failed CODE 15008`)、登入驗證端點無回應，或玩家本機 DNS 無法正確解析 RSI 全球 CDN 認證節點。 | <ul><li>造訪 [RSI Status 頁面](https://status.robertsspaceindustries.com/) 檢查官方伺服器群與驗證服務是否處於 Degraded 或 Maintenance 狀態。</li><li>開啟命令提示字元 (cmd) 執行 `ipconfig /flushdns` 刷新快取。</li><li>將系統 DNS 變更為 Google DNS (`8.8.8.8`) 或 Cloudflare DNS (`1.1.1.1`)。</li><li>重啟路由器與電腦，排除本地網路 Session 鎖死。</li></ul> | [官方 RSI 知識庫 - 錯誤 15008 與 16008](https://support.robertsspaceindustries.com/hc/en-us/articles/360012425434-Error-Code-15008-16008) |
| **16007** | **Account Data Fetch Timeout**<br>帳號資料拉取逾時 (`Account data update failed CODE 16007`)。客戶端向中央資料庫請求該玩家的角色基礎屬性、資產快照與外觀資料時逾時，常見於大型版本釋出初期或伺服器承載尖峰。 | <ul><li>在啟動器主介面按下 `Ctrl + Alt + Shift + R` 重置快取並重新登入。</li><li>使用瀏覽器登入 RSI 官方網站，進入帳號設定刷新連線狀態。</li><li>若持續受阻，代表資料庫中該玩家的實體索引指針鎖死，請前往官網執行「Character Repair」（角色修復）。</li><li>避開晚間尖峰時段，等待 15~30 分鐘讓資料庫佇列消化後重試。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 16007](https://support.robertsspaceindustries.com/hc/en-us/articles/360051485014-Error-Code-16007) |
| **19000 / 19003 / 19004** | **Login & Authentication Token Desync / System Clock Mismatch**<br>帳號登入憑證失效、本地驗證 Token 損毀，或電腦自睡眠/休眠喚醒後本地時鐘與伺服器 UTC 時間戳脫節導致握手拒絕。 | <ul><li>**19003 專用**：休眠喚醒後時鐘脫節。開啟 Windows 設定「時間與語言」→「日期和時間」，點擊「立即同步」確保時鐘分秒不差，或直接完全重新開機。</li><li>**19004 專用**：在啟動器介面按下快捷鍵 `Ctrl + Alt + Shift + R`，清除本機過期憑證快取後重新登入。</li><li>**19000 專用**：使用瀏覽器「無痕式視窗」登入官網並勾選「Trust this device」，隨後重新登入啟動器。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 19000 與 19005](https://support.robertsspaceindustries.com/hc/en-us/articles/4409503463831-Error-Code-19000-19005)<br>[社群討論 - Reddit 19004 解決指南](https://www.reddit.com/r/starcitizen/comments/11osctx/19004_error_fix/) |
| **19005** | **Entitlement Processing Timeout**<br>權益處理解析逾時（通常與 19000 歸屬於同一驗證佇列問題）。多見於大型促銷節慶（如 IAE、Invictus、探索月等活動）或大版本更新後，後端權益服務需同時為巨量帳號結算船隻與道具，導致帳號清單同步逾時。 | <ul><li>此為後端佇列壅塞引發，**切勿頻繁重複瘋狂點擊進入**，以免加劇逾時。</li><li>登入 RSI 官網「My Hangar」檢查最新入庫的物品訂單是否已完成「Attributed」。</li><li>耐心等待 30 至 60 分鐘，待後端完成批次權益結算後再次登入。</li><li>若超過 24 小時仍被此代碼阻擋，向 RSI 官方支援中心提交客服工單 (Support Ticket)。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 19000 與 19005](https://support.robertsspaceindustries.com/hc/en-us/articles/4409503463831-Error-Code-19000-19005) |
| **40014 / 40015** | **Connection to Session Host Failed / Shard Capacity Exceeded**<br>大廳連線失敗、跨區組隊分片衝突，或目標伺服器分片已達到最大承載上限 (Full Shard)，客戶端接入請求遭到拒絕。 | <ul><li>若為組隊狀態，退回主選單解散隊伍，由房員各自單獨進入伺服器測試，或更換另一名玩家擔任隊長重新組隊。</li><li>於主選單伺服器區域 (Region) 選擇清單中，將 `Best` 手動更換為指定區域（如 `EU`、`USA` 或 `AUS`）以切換至其他未滿載分片。</li><li>檢查本地網路路由，嘗試開啟或關閉 VPN 繞開特定出口節點的 UDP 壅塞。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 60015 與 40015](https://support.robertsspaceindustries.com/hc/en-us/articles/360041558213-Error-Code-60015)<br>[社群討論 - Reddit 40014 錯誤排查](https://www.reddit.com/r/starcitizen/comments/126za2u/error_code_40014_details/) |

### 類別 C：伺服器網格、連線與持久化 (Server Meshing, Replication Layer & PES)

此類別為當前核心宇宙中最關鍵的連線與數據持久化錯誤，涉及複寫層、實體圖 (EntityGraph) 以及多節點伺服器網格協同運作。

| 錯誤代碼 | 錯誤訊息與技術成因 | 官方 / 社群實證解決方案 | 參考資料連結 |
| :--- | :--- | :--- | :--- |
| **30000 (Code 30k)** | **General Connection Timeout / Disconnection from Replication Layer**<br>通用伺服器通訊逾時中斷。在當前複寫層架構下，此代碼專指客戶端與獨立複寫層之間的通訊徹底斷絕（當 RLCR 伺服器崩潰恢復倒數超時或全域分片崩解時觸發）。 | <ul><li>**關鍵判斷**：若畫面上方出現「Server Error: Attempting Recovery」，請**原地等待 30~60 秒**等待 RLCR 救援，切勿強退！僅在畫面彈出「Connection Lost: 30000」對話方塊時才代表救援失敗（真 30k）。</li><li>**飛船與貨物救援 SOP**：返回主選單後切換區域重新進服，直接前往太空港 ASOP 終端查詢。PES 崩潰保護機制會將船隻狀態鎖定在太空港，通常可直接「Retrieve」（取回）且裝載貨物完全保留（狀態為 Stored）。**切勿手快點擊「Claim」（保險理賠）**，否則原有貨物將被永久銷毀！</li><li>若剛進載入畫面就遭遇 30k，刪除本機 `USER` 與 `Shaders` 資料夾。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 30000](https://support.robertsspaceindustries.com/hc/en-us/articles/360053608633-Error-Code-30000) |
| **30009** | **Entity Graph Desync / Bed Logout Stall**<br>角色或載具實體狀態逾時。通常因在飛船床鋪登出 (Bed Logout)、躍遷途中離線或伺服器卡頓時強退遊戲，導致客戶端載入時與後端 EntityGraph 資料庫的實體指針無法匹配同調（實體處於幽靈占用狀態）。 | <ul><li>**Arena Commander 實體刷新 SOP（社群首選實證解法）**：<br>1. 進入主選單，點選進入 **Arena Commander** 模式。<br>2. 選擇 **Single Player (單人模式)** → **Free Flight (自由飛行)**。<br>3. 載具選擇當初床鋪登出的那艘船艦（若不可選，選擇任意單座戰機）。<br>4. 成功載入地圖後駕駛飛船飛行並切換視角操作 30 秒，隨後透過選單正常退出至主選單。此操作可強迫後端伺服器改寫實體指針。<br>5. 重新進入常規宇宙 (Persistent Universe)。</li><li>進入角色自訂器 (Character Customizer)，隨意更換性別或眼球顏色後儲存，刷新資料庫標籤。</li><li>切換不同伺服器區域（例如從 USA 切至 EU）嘗試登入。</li><li>若以上均無效，至官網帳號設定執行「Character Repair」（角色修復）。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 30009 與 30018](https://support.robertsspaceindustries.com/hc/en-us/articles/360038342233-Error-Code-30009-30018) |
| **30011 / 30012** | **Socket Connection Interrupted / UDP Packet Loss**<br>底層網路通訊端斷開 (`Socket Error: Unable to send data`)、遊戲 UDP 封包嚴重遺失、路由路徑中斷，或路由器 MTU 封包大小不相容。 | <ul><li>將家用光纖數據機與路由器完全拔除電源，靜置 30 秒後重新通電重啟。</li><li>檢查防毒軟體或第三方防火牆，確保 UDP 埠口 64090 - 64110 未被封閉。</li><li>更新網路卡驅動程式，停用任何主機板附帶的封包最佳化軟體（如 Killer Control Center / ROG GameFirst）。</li><li>執行 `ipconfig /flushdns` 並檢查網路連線 MTU 值是否標準（推薦預設 1500）。</li></ul> | [官方支援 - 網路連線已知問題排查](https://support.robertsspaceindustries.com/hc/en-us/articles/360056254754-Star-Citizen-Known-Issues) |
| **30018** | **Persistent Universe Session Loading Stall**<br>與 30009 同屬官方成對收錄之連線/載入停滯問題。客戶端嘗試進入常規宇宙時，因先前非正常離線或在艦船床鋪登出導致 Session 狀態未能及時釋放，進入讀取等待逾時。 | <ul><li>與 **30009** 採取完全相同的排除 SOP：優先進入 **Arena Commander** 單人自由飛行模式駕駛載具滯空 30 秒後退出刷新實體。</li><li>給予後端清理窗口，暫停登入等待 15 分鐘讓伺服器自動剔除幽靈 Session。</li><li>於主選單切換至其他伺服器區域（如 EU 或 AUS）。</li><li>若持續卡死無法載入，前往 RSI 官網帳號設定提交「Character Repair」（角色修復）。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 30009 與 30018](https://support.robertsspaceindustries.com/hc/en-us/articles/360038342233-Error-Code-30009-30018) |
| **50001** | **CIG Services Connection Timeout**<br>`ERROR - CIG services (CODE 50001)`。客戶端與 CIG 後端微服務通訊逾時中斷，常見於官方伺服器臨時維護、後端服務負載降級或玩家本地網路路由阻塞。 | <ul><li>造訪 [RSI Status 頁面](https://status.robertsspaceindustries.com/) 檢查官方伺服器群是否正在進行熱修復或例行維護。</li><li>完全重啟 RSI 啟動器與遊戲進程，使用 `Ctrl + Alt + Shift + R` 清除啟動器本機快取。</li><li>檢查本地網路防護軟體，確認未攔截遊戲通訊連接埠。</li><li>若伺服器狀態正常且持續報錯，嘗試切換 DNS 為 `8.8.8.8` 或重開路由器。</li></ul> | [官方 RSI 即時服務狀態 (RSI Status)](https://status.robertsspaceindustries.com/) |
| **60012** | **Mesh Node Unavailable / Shard Frozen**<br>伺服器網格節點不可用、指定分片實體管理器陷入凍結死鎖狀態，分片調度器拒絕新客戶端接入。 | <ul><li>於主選單伺服器選擇中，手動將區域從 `Best` 切換至特定區域（如 `EU` 或 `USA`），強制分配至不同分片。</li><li>若多次嘗試任何區域均跳出 60012，代表該帳號角色實體被困在已死鎖的分片節點中，請登入官網執行「Character Repair」（角色修復）。</li><li>刪除遊戲目錄 `\StarCitizen\LIVE\USER` 資料夾排除本機狀態殘留。</li></ul> | [Reddit 社群 - 60012 實證排除方案](https://www.reddit.com/r/starcitizen/comments/1kky6a0/cant_log_in_error_code_60012/) |
| **60015 / 60016** | **Game Instance Error / Shard Load Issue**<br>嘗試登入宇宙時，系統嘗試分配的目標遊戲實例/分片異常或已滿員 (60015)；或後端伺服器與網路負載過高 (60016)。 | <ul><li>**60015 官方實證解法**：在主選單將伺服器區域 (Region) 從 `Best` 手動變更為特定區域（如 `EU`、`USA` 或 `AUS`）再點選進入宇宙，強制繞開故障實例。</li><li>**60016 官方建議**：通常為短暫網路與伺服器峰值負載引起，等待數分鐘後重試。</li><li>完全重啟 RSI 啟動器並重設快取 (`Ctrl + Alt + Shift + R`)。</li><li>若帳號角色狀態卡在異常實例中，至官網執行「Character Repair」。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 60015](https://support.robertsspaceindustries.com/hc/en-us/articles/360041558213-Error-Code-60015)<br>[官方支援 - 網路連線已知問題排查](https://support.robertsspaceindustries.com/hc/en-us/articles/360056254754-Star-Citizen-Known-Issues) |
| **65000 / 65002** | **Universe Loading Error**<br>常規宇宙載入錯誤。客戶端在嘗試載入常規宇宙 (Persistent Universe) 階段發生未知錯誤或數據讀取中斷。 | <ul><li>執行針對 **30009** 的「Arena Commander 自由飛行刷新大法」，重置本地實體狀態。</li><li>前往官網執行「Character Repair」（角色修復）。</li><li>清除本機著色器快取 `%localappdata%\Star Citizen` 與遊戲安裝目錄下的 `USER` 資料夾。</li><li>在啟動器 Settings 中點擊 `VERIFY` 驗證主遊戲檔案完整性。</li></ul> | [官方 RSI 知識庫 - 錯誤代碼 65000](https://support.robertsspaceindustries.com/hc/en-us/articles/34409251540887-Error-Code-65000) |

---

## 萬用自救三板斧 (Universal Troubleshooting SOP)

當您遭遇未明錯誤碼、遊戲啟動失敗或載入介面持續卡死時，無需慌張重新下載整個遊戲。請依序執行以下經過社群與官方實證的「萬用自救三板斧」，高達 90% 的常見客戶端與連線故障均可藉此迅速排解。

### 第一斧：啟動器重設快取組合鍵 (Ctrl + Alt + Shift + R)

* **適用場景**：錯誤代碼 `19004`、`0`、`2000`、啟動器白屏/黑屏無反應、更新進度條卡死、無法點擊 Launch Game 按鈕。
* **技術原理**：RSI 啟動器基於 Electron 框架構建，長期運行會積累大量本機身分憑證、CDN 快取與通訊 Session。該組合鍵可強制抹除本機認證暫存，使啟動器回復純淨初始狀態。
* **標準操作流程**：
  1. 開啟 RSI Launcher 啟動器（無需成功登入）。
  2. 在鍵盤上同時按下快捷鍵組合：`Ctrl + Alt + Shift + R`。
  3. 螢幕將跳出確認對話方塊，詢問是否要重設啟動器並清除快取。
  4. 點選「OK / Confirm」，啟動器將自動清空 `%appdata%\rsilauncher` 並重新啟動。
  5. 重新輸入 RSI 帳號、密碼以及二階段驗證碼 (2FA) 登入。

### 第二斧：清除本機著色器快取與 USER 檔案夾

* **適用場景**：GPU Hang / DXGI 設備掛起閃退、著色器編譯異常、進入主選單卡黑屏、角色或艦船貼圖破圖、大版本更新後幀率驟降或異常卡頓。
* **技術原理**：
  * **著色器快取 (Shaders)**：在現代渲染架構下，Vulkan 與 DirectX 的著色器快取集中存放於使用者本機 AppData 路徑中。當顯卡驅動更新或遊戲釋出修補檔後，舊的編譯二進位二級快取可能與新驅動指令集衝突，導致 GPU 超時崩潰。
  * **USER 檔案夾**：存放本機圖形自訂檔、暫存 UI 狀態及本地實體快取。定期清理可避免過期設定檔干擾遊戲運行。
* **標準操作流程**：
  1. **清除著色器快取**：
     * 按下鍵盤 `Win + R` 開啟「執行」視窗。
     * 輸入 `%localappdata%\Star Citizen` 並按下 Enter。
     * 將該資料夾內的所有檔案與子目錄全數刪除（下次進入遊戲時引擎將自動重新編譯乾淨的著色器，首次進入主城幀率稍有波動屬正常現象）。
  2. **清除 USER 檔案夾（請注意自訂鍵位備份）**：
     * 進入遊戲安裝路徑（預設為 `C:\Program Files\Roberts Space Industries\StarCitizen\LIVE`）。
     * **重要備份**：若您有精心配置的自訂按鍵對應，請先進入 `LIVE\USER\Client\0\Controls\Mappings`，將您的自訂 `.xml` 導出設定檔複製備份至其他安全路徑（有關鍵位配置請參閱 [附錄 A：快捷鍵小抄](keybindings.md)）。
     * 備份完畢後，將整個 `USER` 資料夾刪除。

### 第三斧：官方角色修復 (Character Repair)

* **適用場景**：錯誤代碼 `30009`、`30018`、`60012`、`65000`、角色無頭/無眼球/無法召喚 mobiGlas、太空港 ASOP 終端全部黑屏無反應、所有船隻均卡在「Unknown」狀態無法召喚。
* **技術原理**：直接向 RSI 後端資料庫伺服器發送重置請求，強制解除該帳號在後端 EntityGraph 中的所有實體鎖死狀態，並重新生成基礎角色節點。
* **標準操作流程**：
  1. 完全關閉《星際公民》遊戲客戶端與 RSI 啟動器。
  2. 開啟瀏覽器造訪 [Roberts Space Industries 官方網站](https://robertsspaceindustries.com/) 並登入您的帳號。
  3. 點選右上角個人頭像，選擇「Account」進入帳號管理介面。
  4. 於左側導航選單中點選「Settings」→「Character Repair」。
  5. 仔細閱讀頁面說明後，點選紅色的「Submit Request」按鈕確認執行。
* **重要資產保留與冷卻須知**：
  * **資產完全保留**：角色修復**不是**帳號重置 (Wipe)！您的 **aUEC 遊戲幣、已購買或租賃之船艦、船艦改裝配件、個人武器與裝甲均不會遺失**。
  * **重置項目說明**：系統僅會將您的角色重生點（醫療床）重設回當前設定的主要居留地主城，所有已穿戴裝備將自動脫卸並放回該主城的本機倉庫存儲，且未完成的進行中任務合約將被放棄。
  * **60 分鐘冷卻警示**：提交角色修復後，後端資料庫批次處理需耗時約 15 分鐘。此功能設有 **60 分鐘冷卻時間 (Cooldown)**，在此期間內無法再次提交。**請於提交後至少耐心等待 15 分鐘，再重新開啟啟動器登入遊戲**，切勿在送出後立即秒開遊戲，以免干擾資料庫寫入程序。

---

{% hint style="info" %}
**延伸閱讀與進階資源**
* 欲深入理解伺服器網格化之底層架構原理，請參閱 [附錄 C：巨擘的統一：深入解析《星際公民》伺服器網格化技術及其發展軌跡](server-meshing-deep-dive.md)。
* 如需查詢官方即時伺服器節點健康度與維護公告，請隨時追蹤 [RSI 官方即時服務狀態頁面](https://status.robertsspaceindustries.com/)。
{% endhint %}
