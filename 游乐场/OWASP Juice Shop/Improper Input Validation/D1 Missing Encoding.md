- Missing Encoding
    - 描述：获取 Bjoern's cat 在 "melee combat-mode" 的图片
    - 访问照片墙功能
        ```http://127.0.0.1:3000/#/photo-wall```
        - 未显示图片的代码块为
            ```html
            <img _ngcontent-ng-c1771354057="" class="image" src="assets/public/images/uploads/ᓚᘏᗢ-#zatschi-#whoneedsfourlegs-1572600969477.jpg" alt="😼 #zatschi #whoneedsfourlegs">
            <div _ngcontent-ng-c1771354057="">😼 #zatschi #whoneedsfourlegs</div>
            ```
            - URL 的 hash ```#``` 字符未编码，导致地址被截断，实际请求地址为
            ```assets/public/images/uploads/ᓚᘏᗢ-```
            - 在浏览器中对字符编码后得到图片
            ```assets/public/images/uploads/ᓚᘏᗢ-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg```
            - 实际请求为
            ```GET /assets/public/images/uploads/%E1%93%9A%E1%98%8F%E1%97%A2-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg HTTP/1.1```