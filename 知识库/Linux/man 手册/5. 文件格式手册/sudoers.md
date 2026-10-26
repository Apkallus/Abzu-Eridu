https://www.man7.org/linux/man-pages/man5/sudoers.5.html

https://www.sudo.ws/docs/man/sudoers.man/

https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file

```sh
visudo [-chqsV] [-f sudoers]
```

`visudo` 以安全的方式编辑 `sudoers` 文件，类似于 `vipw(8)`。`visudo` 锁定 `sudoers` 文件以防止多个同时编辑，提供基本的合理性检查，并检查解析错误。如果 `sudoers` 文件当前正在被编辑，你会收到一条消息提示稍后再试。