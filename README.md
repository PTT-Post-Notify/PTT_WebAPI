# PTT_WebAPI
WebAPI for PTT bbs

由於 PTT 現階段並沒有提供 Web API 的功能  
因此若需取得 PTT 上面的文章資訊  
通常需要靠自行撰寫爬蟲或是 Telnet、SSH 登入等方式取回文章  
此專案的目的在於為有需要的 PTT 相關應用開發者提供一個 WEB API 介面來方便取得 PTT 內容

相關開發者可關注在應用邏輯本身，而無須關心爬蟲方式  
使用方式請見 **[Swagger UI](https://ptt-webapi-ciqjdh7yiq-de.a.run.app)**

由於此專案只是提供 API 的方式供使用者訪問 PTT.CC 的 WEB 版本  
因此功能會受限於網頁版 PTT 的能力限制

我會隨時追蹤 PTT Web BBS 是否有新增功能，並迅速補上  

如有問題回報或是有功能建議，歡迎提 Issue 或 PR

<br>

## 關於效能
目前 WebAPI 架構在 Google Cloud Run 上面  
當長久無人訪問此端點時，Container 會自動關閉以節省 CPU 時間  
再次訪問時會需要一小段冷啟動的時間，但一般來說應該不會影響到使用  

另外，取回所有看板功能會使用 BFS 從 PTT 的 根分類 (Root Class : 1)  
逐層掃描所有看板，這會花上大量的時間 (約需 1 ~ 2 mins)
雖然有做 Cache 機制，但因為 Container 會關閉的關係  
還是有可能導致你程式 Timeout，請小心服用

<br>

## Note
本專案目前還在 Alpha 版本，  
所有內容包括 Url Endpoint 都有可能隨時修改，  
若你真的很急有需要，建議你 Fork 此專案自行做二次開發  
