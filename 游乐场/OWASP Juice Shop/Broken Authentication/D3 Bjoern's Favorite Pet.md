- Bjoern's Favorite Pet
    - 描述：通过忘记密码机制，使用他安全问题的原始答案重置Bjoern的OWASP账户密码。
    - 使用管理员账户访问管理页面得到目标用户的邮件地址 
    ```bjoern.kimminich@gmail.com```
    ```bjoern@juice-sh.op```
    ```bjoern@owasp.org```
    - 搜索 ```Bjoern``` 对应 Juice Shop 开发者 Björn Kimminich
    - 搜索 ```Björn Kimminich pet```
        得到社交媒体的宠物相关帖子 https://x.com/bkimminich/status/1900763651977495004
        > Zaya, the Three-Legged - ⚪⚫ - 1/3 Creature Cat - Toyfall: Gains protection from green and battle cry until end of turn.
    - 使用 ```Zaya``` 重置密码

- 代码挑战：
    ```
    -
	  question: 'Your eldest siblings middle name?'
	-
	  question: "Mother's maiden name?"
	-
	  question: "Mother's birth date? (MM/DD/YY)"
	-
	  question: "Father's birth date? (MM/DD/YY)"
	-
	  question: "Maternal grandmother's first name?"
	-
	  question: "Paternal grandmother's first name?"
	-
	  question: 'Name of your favorite pet?'
	-
	  question: "Last name of dentist when you were a teenager? (Do not include 'Dr.')"
	-
	  question: 'Your ZIP/postal code when you were a teenager?'
	-
	  question: 'Company you first work for as an adult?'
	-
	  question: 'Your favorite book?'
	-
	  question: 'Your favorite movie?'
	-
	  question: 'Number of one of your customer or ID cards?'
	-
	  question: "What's your favorite place to go hiking?"
    ```
    - 选择宠物问题部分
    - 修复：全部删除
        > 当如实回答时，所有安全问题都容易受到在线调查（如在Facebook、LinkedIn等）的影响，并且通常甚至会被暴力破解。如果真的要使用，它们不应该是安全相关功能的唯一因素。