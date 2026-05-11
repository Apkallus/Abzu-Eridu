- Weird Crypto
    - 描述：通知商店 http://127.0.0.1:3000/#/contact ，它绝对不应该以这种方式使用某个算法或库。
    - 回想起之前尝试获得管理员账户的明文密码的挑战 Broken Authentication- Password Strength
        使用 MD5 对密码进行散列而未加盐
    - 在联系的文本中输入 ```MD5``` 后通过挑战
    - [示例解决方案](https://pwning.owasp-juice.shop/companion-guide/latest/appendix/solutions.html#_inform_the_shop_about_an_algorithm_or_library_it_should_definitely_not_use_the_way_it_does)中拥有对其他挑战的不当加密的剧透，暂且忽略