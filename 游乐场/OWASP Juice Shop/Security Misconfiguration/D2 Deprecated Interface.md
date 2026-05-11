- Deprecated Interface
    - 描述：使用一个未正确关闭的已弃用的 B2B 接口。
        即文件接口
    - 在 ```main.js``` 中搜索 ```b2b```，找到
        ```javascript
        static \u0275cmp = t.VBU({
            type: n,
            selectors: [
                ["app-complaint"]
            ],
            viewQuery: function(o, a) {
                if (1 & o && t.GBs(hr, 7), 2 & o) {
                    let s;
                    t.mGM(s = t.lsd()) && (a.fileControl = s.first)
                }
            },
            decls: 46,
            vars: 34,
            consts: [
                ["complaintMessage", ""],
                ["fileControl", ""],
                [1, "center-container"],
                ["appearance", "outlined", 1, "mat-elevation-z6"],
                ["aria-live", "polite"],
                [1, "confirmation", 3, "hidden"],
                ["role", "alert", 1, "error", "fileUploadError"],
                ["id", "complaint-form", 1, "form-container"],
                ["appearance", "outline", "color", "accent"],
                ["type", "text", "matInput", "", "aria-label", "Text field for the mail address of the user", 3, "formControl"],
                [1, "fas", "fa-exclamation-circle"],
                ["id", "complaintMessage", "matAutosizeMinRows", "4", "matAutosizeMaxRows", "4", "matTextareaAutosize", "", "cols", "50", "maxlength", "160", "matInput", "", "aria-label", "Field for entering the complaint", "aria-required", "true", "aria-describedby", "messageCounter", 3, "formControl", "placeholder"],
                ["role", "alert"],
                ["align", "end", "id", "messageCounter"],
                [1, "invoice"],
                ["for", "file"],
                ["ng2FileSelect", "", "id", "file", "type", "file", "accept", ".pdf,.zip", "aria-label", "Input area for uploading a single invoice PDF or XML B2B order file or a ZIP archive containing multiple invoices or orders\x3c!----\x3e", 3, "uploader"],
                ["type", "submit", "id", "submitButton", "mat-raised-button", "", "color", "primary", "aria-label", "Button to send the complaint", 3, "click", "disabled"]
            ]
        ```
    - 分析其文本，对应客户投诉的上传文件功能
    - 在页面中打开投诉功能，``b2b```出现的位置对应 HTML 上传元素
        ```html
        <input _ngcontent-ng-c1559552500="" ng2fileselect="" id="file" type="file" accept=".pdf,.zip" aria-label="Input area for uploading a single invoice PDF or XML B2B order file or a ZIP archive containing multiple invoices or orders&lt;!----&gt;">
        ```
    - 文本内容为：
        “上传区域支持单个发票（PDF格式）或B2B订单文件（XML格式），也可上传包含多个发票/订单的ZIP压缩包”
    - 接受的文件格式为 ```accept=".pdf,.zip"```，描述中还包括B2B的 XML 格式
    - 随意上传一个 XML 格式的文件通过挑战
    - 示例解决方案
        - 在 ```main.js``` 中搜索 ```zip```。或 ```upload```
            ```javascript
            uploader = new bt.l0({
                url: x.c.hostServer + "/file-upload",
                authToken: `Bearer ${localStorage.getItem("token")}`,
                allowedMimeType: ["application/pdf", "application/xml", "text/xml", "application/zip", "application/x-zip-compressed", "multipart/x-zip", "application/yaml", "application/x-yaml", "text/yaml", "text/x-yaml"],
                maxFileSize: 1e5
            });
            ```
            得到允许的上传文件类型
    - 分析感兴趣的搜索关键词的上下文，确认并使用功能，再进一步搜索