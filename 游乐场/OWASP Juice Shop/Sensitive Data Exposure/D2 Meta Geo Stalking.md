- Meta Geo Stalking
    - 说明：通过查看 Photo Wall 中上传的 John 的照片来确定他的安全问题，并使用忘记密码机制重置他的密码。
    - 照片墙中照片对应 HTML 代码为
        ```html
        <img _ngcontent-ng-c1771354057="" class="image" src="assets/public/images/uploads/favorite-hiking-place.png" alt="I love going hiking here... (© j0hNny)">
        <div _ngcontent-ng-c1771354057="">I love going hiking here... (© j0hNny)</div>
        ```
    - 登录管理员账户在管理页面中确定邮件为
    ```john@juice-sh.op```
    - 使用忘记密码功能时，秘密问题为
    ```What's your favorite place to go hiking?```
    - 下载图片，使用图像编辑器 GIMP 或数据查看器检查图像文件的元数据
        ```
        Exif.GPSInfo.GPSLongitude
        84deg 20' 53.580"
        Exif.GPSInfo.GPSLongitudeRef
        西
        Exif.GPSInfo.GPSLatitude
        36deg 57' 31.380"
        Exif.GPSInfo.GPSLatitudeRef
        北
        Exif.GPSInfo.GPSMapDatum
        WGS-84。 
        Exif.GPSInfo.GPSVersionID
        2.2.0.0
        ```
    - 检查得到的 GPS 定位信息
        西经 84°20'53.580"
        北纬 36°57'31.380"
        地理坐标系 WGS-84
        GPS 版本 2.2.0.0
    - 十进制为：
        -84.3482167, 36.9587167
        > 西经负值，北纬正值 
        十进制度 = 度 + 分/60 + 秒/3600 
    - 在[网页地图的按坐标搜索功能](https://lbs.baidu.com/maptool/getpoint)中使用十进制 GPS 信息后得到位置：
        Laurel, Kentucky, United States
        Daniel Boone National Forest
    - 使用 ```Daniel Boone National Forest``` 作为安全问题的答案后成功重置密码