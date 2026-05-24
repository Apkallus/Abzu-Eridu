Kubernetes 架构
- 控制平面组件
	- api server 通信核心
	- etcd 键值数据库
	- kube-schedule 调度
	- kube-controller-manager 控制器
	- cloud-controller-manager 云抽象
- 节点组件
	- kubelet 与通信核心通信的代理
	- kube-proxy 端口转发工具

api server 
- 查找 api server 
	- 证书透明度
	- dns条目
	- 披露信息
- 连接后探测常见端点以收集信息
- 在特权容器中
	- 设置新 pod 的配置文件并下载管理工具以应用
	- 此容器具有各种设置的特权
		
内部攻击 Kubernetes
- 使用工具 Kubestriker 搜集信息
- 探查容器系统与用户信息
- 下载网络探测工具
- 查询本地主机ip
- 扫描本机端口
