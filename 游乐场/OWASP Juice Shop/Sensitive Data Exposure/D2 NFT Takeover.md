- NFT Takeover
    - 说明：接管包含我们官方 Soul Bound Token (NFT) 的钱包。
    - 提示：找到意外泄露的助记词。
        > 助记词 seed phrase 对应钱包的私钥。
        通常由12、18或24个英文单词组成。
    - 关键词 ```sbt```，```nft```
    - 访问“关于我们” ```http://127.0.0.1:3000/#/about```
    或以管理员账户登录管理页面 ```http://127.0.0.1:3000/#/administration```
        - 其中一条评价泄露了助记词，以及加密货币 URL ```/juicy-nft```
            ```Please send me the juicy chatbot NFT in my wallet at /juicy-nft : "purpose betray marriage blame crunch monitor spin slide donate sport lift clutch" (***ereum@juice-sh.op)```
            - 或在 ```main.js```中搜索 ```nft```，得到加密货币地址以及其他相关路由
                ```typescript
                {
                    path: "juicy-nft",
                    component: id
                }
                ```
            - 访问钱包地址
                - 拥有输入私钥的表单
                - 页面提示信息为：永远不要向任何人透露你的个人私钥和助记词。
                    ```Note: Never reveal your personal private keys and seed phrase to anyone```
                - 使用[在线助记词转换工具](https://bip39.best/)将助记词转换为```ETH - Ethereum``` 私钥:
                ```0x5bcc3e9d38baa06e7bfaab80ae5957bbe8ef059e640311d7d6d465e6bc948e3e```
            - 输入私钥访问钱包

- 代码挑战
    :x: 未解决 :x:
	加密货币代码
    ```javascript
    pragma solidity ^0.8.4;
	 
	import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
	import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
	import "@openzeppelin/contracts/access/Ownable.sol";
	import "@openzeppelin/contracts/utils/Counters.sol";
	 
	contract JuiceShopSBT is ERC721, ERC721URIStorage, Ownable {
	    using Counters for Counters.Counter;
	 
	    Counters.Counter private _tokenIdCounter;
	 
	    constructor() ERC721("JuiceShopSBT", "JS") {}
	 
	    function safeMint(address to, string memory uri) public onlyOwner {
	        uint256 tokenId = _tokenIdCounter.current();
	        _tokenIdCounter.increment();
	        _safeMint(to, tokenId);
	        _setTokenURI(tokenId, uri);
	    }
	 
	    function _beforeTokenTransfer( 
	    address from,
	    address to,
	    uint256 tokenId
	    ) internal override virtual {
	    require(from == address(0), "Err: token transfer is BLOCKED");
	    super._beforeTokenTransfer(from, to, tokenId);
	    }
	 
	    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
	        super._burn(tokenId);
	    }
	 
	    function tokenURI(uint256 tokenId)
	        public
	        view
	        override(ERC721, ERC721URIStorage)
	        returns (string memory)
	    {
	        return super.tokenURI(tokenId);
	    }
	}
    ```
    :x: 未解决 :x:
	- 读取-添加的操作存在竞态条件风险
		```
		uint256 tokenId = _tokenIdCounter.current();
		_tokenIdCounter.increment();
		```
	- 修改为原子化的操作
		```
		uint256 tokenId = _tokenIdCounter.increment();
		```
	- 代码修复显示异常