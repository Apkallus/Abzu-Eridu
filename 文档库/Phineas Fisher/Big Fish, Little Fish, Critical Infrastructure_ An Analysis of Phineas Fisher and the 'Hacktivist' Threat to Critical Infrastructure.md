https://arxiv.org/abs/2004.14360

**Big Fish, Little Fish, Critical Infrastructure: An Analysis of Phineas Fisher and the 'Hacktivist' Threat to Critical Infrastructure**

Peter Maynard and Kieran McLaughlin Centre for Secure Information Technology Queen's University Belfast, UK {p.maynard,kieran.mclaughlin}@qub.ac.uk

**摘要**——活动黑客（hacktivist）威胁行为者被列在许多风险决策文件中。然而，他们的战术和技术往往仍然是个谜。我们为一个以 Phineas Fisher 为化名的知名活动黑客创建了 MITRE ATT&CK（ATT&CK）模型，并将该威胁映射到关键基础设施。该分析源自黑客宣言、新闻报道和官方政府文件。这项分析填补了当前威胁模型中的一个空白，以更好地界定一个坚定的黑客可能采用哪些技能和方法。本文还确定了七项基本缓解措施，关键基础设施运营方和资产所有者可以部署这些措施，以防止活动黑客的此类入侵。我们正在将此威胁行为者贡献到 MITRE ATT&CK 知识库中。

**索引词**——ATT&CK、关键基础设施、活动黑客

## I. 引言

国家行为者被广泛认为是关键基础设施的默认威胁行为者，因为他们是媒体中最常讨论的威胁。例如，2017 年发现恶意软件 CrashOverride [^1] 被用于 2016 年乌克兰停电事件，该事件中工业控制设备被操纵，导致局部地区停电数小时。2019 年发布的一份报告[^2]表明，他们的目标是让整个国家的电网瘫痪更长时间。虽然对运营方来说，入侵者是谁可能没有实际区别，但充分理解对手可能部署的战术和技术是一种良好实践。在这个例子中，创建者有时间和资金投入到开发一个专门设计用于攻陷目标的复杂恶意软件上。他们部署的技能和技术已被充分理解，而且此类攻击正变得越来越普遍。然而，资源较少的行动者所使用的技术和战术往往未得到讨论。

现有文献[^3] [^4]并未详细说明活动黑客可能采用的技术威胁，因为在未识别和调查入侵者的情况下很难获得此类信息。因此，我们对一个以 Phineas Fisher 为化名的知名活动黑客进行了分析（见第 IV 节）。本分析的大部分内容基于其自行发布的宣言，这些宣言分解了攻陷目标所采取的步骤。该分析还得到了新闻报道和学术文献的进一步支持。随后，我们推导出其技术的 MITRE ATT&CK（ATT&CK）模型，并确定了像 Fisher 这样能力相当的活动黑客可能如何攻陷关键基础设施。基于这项研究，我们确定了七项可部署在工业网络中的缓解措施。这项工作的动机来自 Fisher 在 2019 年 11 月的一篇近期出版物，其中写道：“根据材料的公共利益和影响，每次此类信息泄露我将支付最高 10 万美元……”[^5]，她在其中倡导入侵石油、天然气、采矿、伐木和畜牧公司，以及 NSO 集团等监视公司等。虽然我们不打算对此类“活动黑客”的政治目标做出评判，但基于这一号召，以及对活动黑客方法缺乏洞察，显然需要进一步的技术分析。

本文其余部分提供了对相关工作的讨论（第 II 节），随后介绍了 ATT&CK 模型（第 III 节）和被称为 Phineas Fisher（或 Phisher）的活动黑客（第 IV 节）。然后我们分析了 Fisher 的攻击（第 V-A 节）以及该威胁可能如何映射到关键基础设施（第 V-B 节），随后是拟议的缓解措施（第 V-C 节）和结束语（第 VI 节）。

## II. 相关工作

迄今为止，已有若干研究调查了对关键基础设施和工业控制系统的威胁。其中一篇由 Rudner [^6] 撰写的论文识别了几个威胁行为者：国际恐怖主义、国家支持的恐怖主义、间谍活动和破坏、恶意活动黑客以及内部威胁。Rudner 考察了那些已知威胁关键国家基础设施的实体的宣称意图、战略、目标和已展示的能力。这些威胁与 NIST SP800-82 工业控制系统安全指南[^7]中的定义一致，即四种主要对手行为者：个人；团体；组织；和国家。然而，这些出版物都没有定义这些行为者可能对其目标采取什么行动。

就我们的调查而言，最有趣的威胁是“恶意活动黑客”，Rudner 引用美国国土安全部的警告称，Anonymous 可能“作为其绿色能源议程的一部分”以关键基础设施为目标[^8]，这具体支持了针对阿尔伯塔油砂和拟建的 Keystone XL 石油管道的环保运动。还列出了另外两个团体（Deep Green Resistance 和 Fertile Ground），它们在 2011/12 年宣布有意以关键基础设施为目标。Fertile Ground 提出的观点是，关键基础设施高度脆弱且设计拙劣，因此打击关键节点的网络攻击可能产生重大影响。截至 2020 年初，作者未能找到任何可归因于它们的 incident。

虽然各种事件被归因于 Anonymous，但没有一个似乎（或已被公开报道为）直接影响关键基础设施。与此同时，Anonymous 声称[^9]他们可以访问 Stuxnet 源代码，但没有证据表明他们使用了它。此外，Stuxnet 是为在特定站点运行而设计的，单独使用并不特别有用。

Ghafir [^3] 讨论了对关键基础设施的人为威胁，其中他们提出了一种提高业务环境员工安全意识系统。特别有趣的是 Ghafir 对社会工程和攻击策略的讨论，建议使用 Kevin Mitnick 的攻击周期，即研究；建立信任；利用信任，以及；利用信息。在许多分散部门和业务伙伴都需要互操作的紧急情况下，社会工程成为对关键基础设施非常真实的威胁。事实上，正如[^10]所报道的，鱼叉式钓鱼是一种常见的入口点。尽管如此，Ghafir 提出的安全意识交付方法似乎不太适合应用于 SCADA/ICS 系统，因为它会在员工工作流程中添加“弹出窗口”以及额外的网络连接。

总的来说，当前的研究体系在非常抽象的层面上描述入侵，主要关注不同类型威胁行为者的动机和描述。缺乏对活动黑客在攻陷关键基础设施时可能采用的技能的详细技术分析。人们可能会认为活动黑客和国家行为者之间没有区别，并且由于没有公开归因于个人或活动黑客团体对关键基础设施的攻击，人们可以假设他们可能遵循 ICS-CERT 报告的现有入侵趋势。本文旨在探讨这些假设。

## III. MITRE ATT&CK

MITRE ATT&CK（ATT&CK）[^11] 于 2015 年发布，是一个经过策划的对手行为知识库。ATT&CK 有三个主要语料库，包括前 ATT&CK、移动和企业。本文考虑企业版本，因为它是为基于 Microsoft Windows 和 Linux 的操作系统设计的。该知识库由对手战术（为什么）和技术（如何）组成，防御者可以使用它们来确定其系统的安全性。战术作为单个技术的有用上下文类别，涵盖对手在操作期间所做事情的标准表示法，例如持久化、发现信息、横向移动、执行文件和泄露数据。技术表示对手通过执行某个动作实现战术目标的方式。如[^12]所述，ATT&CK 有多种应用：对手模拟；红队演练；行为分析开发；防御差距评估；SOC 成熟度评估；网络威胁情报丰富化。本文将使用该模型分析 Fisher 对关键基础设施的威胁，在某种意义上，将基于活动黑客威胁进行差距评估。

> 图略，见原始 PDF
Fig. 1. 模型和威胁知识数据库的抽象层次[^12]

与其他模型如 Microsoft 的 STRIDE [^13] 和 Lockheed Martin 的网络杀伤链[^14]不同，ATT&CK 并非高度抽象于低级概念，但同时 ATT&CK 不包含低级细节，如入侵指标（IOC）、漏洞利用或漏洞。图 1 显示了高级、中级和低级模型之间的抽象层次。该知识库基于已观察和合理的对手行为，这些行为很可能被遇到，而不是由于使用困难或低效用而不太可能看到的理论技术。ATT&CK 模型描述的行为可以编码为 IDS 系统中的签名，并且还附有潜在的反制措施。

## IV. Phineas Fisher

Phineas Fisher 是一个化名[^15]，自我认同为女性[^5]，她声称并验证了对许多高调入侵和数据泄露的责任。2014 年，Fisher 以 Gamma Group [^16] 为目标。Gamma Group 向世界各地的政府和警察部队销售监视软件，其中许多受到人权组织的批评[^17]。在发布 Gamma Group 的客户名单、源代码和私人细节后，Fisher 发布了一份分步指南[^18]，说明她是如何攻陷他们的系统的。

一年后的 2015 年，Fisher 攻陷了另一家名为 Hacking Team 的监视公司[^19] [^20]，随后公布了细节和源代码，并附有另一份关于她方法的说明[^21]。

2016 年 5 月，她入侵了加泰罗尼亚警察工会网站[^22]，篡改了它，然后泄露了大约 5,000 名警察的个人信息。Fisher 制作了一段记录黑客攻击步骤的视频，显示他们系统中的简单漏洞。作为对这次黑客攻击的回应，警察部队对社会中心和黑客实验室进行了突袭，他们声称在那里逮捕了 Fisher。此后不久，Fisher 与媒体沟通，并同意接受 Vice News 的采访[^15]。

2016 年 7 月 19 日，Fisher 攻陷了土耳其正义与发展党（AKP）网络[^23]，并正在收集数据以移交给 Wikileaks。虽然 Fisher 特别[^24]告诉他们不要发布数据，但这被忽视了。这次黑客攻击没有附带操作指南，随后 Fisher 一度不活跃[^25]。

2019 年 11 月，Fisher 泄露了位于马恩岛的 Cayman Bank and Trust Company 的内部电子邮件[^26]。除了这次泄露，她还从该银行窃取了一大笔钱。这次盗窃已被确认，发生在 2016 年[^27]。与其他攻击一样，她发布了一份事后分析[^5]，并悬赏 10 万美元入侵银行和石油公司，这可能有助于披露符合公共利益的文件。时至今日，似乎没有人能够识别出 Phineas Fisher 是谁，意大利对 Hacking Team 黑客攻击的调查在没有答案的情况下结案[^28]。虽然有一些猜测认为 Phineas Fisher 可能是政府行动，但人们普遍认为她是一名活动黑客[^29]。Fisher 的主要信息是发起一场黑客革命，他们将为社会公益而黑客，并以被认为邪恶和腐败的公司为目标。通过发布她的事后分析文档，她展示了闯入这些系统所需的简单技术。因此，对于关键基础设施如工业控制系统（ICS），识别这些系统可能受到像 Phineas Fisher 这样的活动黑客多大程度的威胁是有价值的。

## V. 分析

本节对 Phineas Fisher 的入侵进行分析，随后讨论由此对关键基础设施的潜在威胁以及可能的检测方法。

### A. Fisher 入侵分析

MITRE ATT&CK 框架目前在企业矩阵中有 266 项技术，从这些技术中我们选择了一个子集来代表 Phineas Fisher 的战术和技术。这是基于她自行发布的每次攻击的分解[^22] [^18] [^21] [^5]，呈现在表 I 中。该表遵循标准的 MITRE ATT&CK 呈现格式，其中列标题描述对手战术，其余单元格描述 Fisher 执行的技术。现在依次讨论每种战术。每种技术都映射回来源：A、Gamma Group；B、Hacking Team；C、警察工会；D、Cayman Bank。未明确说明的技术用“I”标注，表示根据上下文“推断”。红色背景的单元格被第 V-C 节讨论的反制措施缓解。

**表 I. 基于 Fisher 各宣言的合并 ATT&CK 模型**
> 略，查看原始 PDF

1) **初始访问**：在所有这些入侵中，初始访问是通过利用互联网面向的应用程序获得的，通常是通过执行 SQL 注入攻击。在 Hacking Team 事件中，Fisher 能够进行逆向工程并识别其 VPN 设备中的零日漏洞。后来发现该设备也容易受到简单执行的 shellshock 漏洞的影响。虽然 Fisher 没有使用鱼叉式钓鱼来获得访问权限，但她确实在她的指南中提到了它们。

2) **执行**：在这些漏洞利用期间，大约 2015 年，PowerShell 通常被用来在获得初始访问后执行大量操作。今天，微软已经部署了几项针对其滥用的缓解措施，虽然这阻止了相同的方法起作用，但有大量其他方法可以实现相同的结果。这引出了其他技术，如命令行界面、脚本、图形用户界面和 Windows 管理规范/Windows 远程管理，如果在此目标上启用，将允许对手执行命令。所有这些方法都是 Fisher 使用或讨论过的。有趣的是，这些都是企业网络中通常能找到的工具，并遵循了在宣言中强烈倡导的“就地取材”理念。

3) **持久化**：持久化通常通过上传到受攻陷服务的 Web Shell 来执行。Hacking Team 是一个特别的例外，她为其 VPN 服务开发了一个后门固件。这个固件包括下一阶段所需的许多额外工具。Fisher 还维护了一个冗余访问服务，以防她被锁定在主持久化方法之外。指南中写道：“我总是使用 Duqu 2 风格的‘持久化’，在几台高在线时长的服务器上于 RAM 中执行”[^21]，Duqu2 是 Stuxnet 的亲戚，执行隐蔽的内存间谍操作[^30]。

4) **权限提升与凭据访问**：权限提升通过监视操作员的活动来执行，使用技术捕获用户输入并劫持已认证的多因素会话，以及通过修改流行服务来记录明文以拦截凭据，这是针对加泰罗尼亚警察工会的技术。这些方法与国家行为者的方法相似。

5) **防御规避**：在大多数情况下，很少有主动防御需要规避，因为 Fisher 试图保持仅在 RAM 中的存在，例如利用服务而不在磁盘上放置可能触发警报的恶意软件。当接触磁盘时，执行了时间戳操作，掩盖了更改文件的修改日期。当冒充用户登录时，Fisher 会更改记录的 IP 和 UserAgent 以匹配历史访问日志。

6) **发现与横向移动**：Fisher 的所有指南都从发现尽可能多的关于目标的信息开始。她使用 Nmap 等工具进行网络服务扫描，使用 `net view` 和 PowerView 进行账户和网络共享发现。横向移动主要通过远程文件复制和远程服务（如 `psexec` 和 WMI）进行。她还使用远程桌面协议（RDP）和 SSH 进行访问。

7) **收集与影响**：收集和影响是 Fisher 的主要 ATT&CK 战术（目标），通过多种技术实现。网络文件共享被远程访问并下载到本地，最常见的目标是收集目标的电子邮件存档、内部文档、客户/员工详细信息和源代码。对于任何公司来说，这可能对其日常运营以及公众如何看待它们产生重大影响。作为最后一步，Fisher 此前曾接管公司社交媒体账户并向世界宣布他们已被攻陷。虽然 ATT&CK 模型没有将披露私人信息作为影响战术的技术，但它确实包括篡改和账户访问移除。

8) **命令与控制与泄露**：命令与控制以及泄露通过常用端口号和连接代理执行。虽然 Fisher 会使用多跳和现成的远程访问工具，并且通常通过 HTTP 和 SSH 进行简单的文件传输。这些方法通常足以绕过未受监控的简单 IDS，因为生成的流量与日常操作相匹配（尽管可能使用更多带宽，但这通常不被监控）。

值得注意的是，Fisher 的入侵方法在每次攻击之间使用的技术并没有显著变化。虽然技术取决于环境，但执行成功入侵所需的技能是容易获得的。

### B. 对关键基础设施的威胁

基于 Fisher 采用的技术，我们可以推断，一个坚定的活动黑客是关键基础设施的真实威胁。此外，近年来对气候变化的担忧日益增长，这可能促使人们特别针对石油、天然气和其他能源相关基础设施。这种针对关键基础设施的“活动黑客”威胁可以可行地采用类似于上述讨论的技术，然而，关键基础设施内部的环境与传统企业网络不同，因为底层操作和要求不同。常见的是较旧的操作系统和应用程序，它们已经过验证和认证用于特定操作。可能无法更新系统以包含最新的攻击缓解措施，因为这可能需要额外的验证。例如，许多技术利用 PowerShell，它于 2006 年首次发布。从那时起，在威胁缓解和事件日志记录方面有了大量改进。这些改进可能在关键基础设施系统中找不到。此外，可能存在许多旧的 Unix 系统和架构，它们包含可利用的漏洞，允许对手采用替代攻击途径。正如我们在分析中发现的那样，Fisher 会在其受攻陷的网络中维护几条远程访问路径，以确保如果其中一台受攻陷的机器被检测到，她还有另一个入口点。在关键网络中，通常有多条冗余网络路径提供弹性网络，虽然这是必要的，但它也为对手提供了替代攻击路径。

正如 ICS-CERT [^10] 所报道的，鱼叉式钓鱼在关键基础设施运营方中已变得常见。虽然 Fisher 没有使用这种技术，但它在她的宣言中经常被提及。根据我们的分析，开发后门固件在活动黑客的能力范围内。这对关键基础设施网络来说是一个担忧，因为它们通常包含许多嵌入式设备和网络设备，这些设备可能没有最近修补，正如在 Duqu 和 Stuxnet 入侵中所见。

由于安全控制和缓解措施的进步和普及，对手不得不诉诸更隐蔽的操作模式。正如 2016 年乌克兰停电事件和 Fisher 所展示的那样，对手模仿合法用户的操作以逃避检测。活动黑客的动机可能是查找和泄露关于公司的信息或破坏运营。泄露信息可能是制造公司的一个担忧，这些公司通常将商业机密编码到网络中。与此同时，发电和输电运营方可能因服务中断而被处以罚款。

### C. 缓解措施

基于对 Fisher 使用的战术和技术的分析，这些技术可能被任何活动黑客威胁行为者部署，我们现在强调由 ATT&CK 框架定义的七种缓解方法，这些方法可以部署在关键基础设施系统中。缓解措施按部署复杂性排序，并根据它们缓解的技术数量选择：

1) **执行预防**：应用程序白名单可能能够防止运行伪装成其他文件的可执行文件。

2) **应用程序隔离和沙盒**：通过操作系统调用执行应用程序隔离，或虚拟化和应用程序微分割以减轻攻陷的影响。

3) **网络入侵防御**：使用网络签名识别特定对手恶意软件流量的网络入侵检测和防御系统可用于在网络层面缓解活动。签名通常针对协议内的独特指标，并且在不同恶意软件家族和版本之间会有所不同。对手可能会更改工具签名。

4) **多因素认证**：将多因素认证（MFA）作为组织政策的一部分整合，可以大大降低对手获得有效凭据控制权的风险，这些凭据可能用于初始访问、横向移动和收集信息等其他战术。MFA 还可用于限制对云资源和 API 的访问。

5) **特权账户管理**：审计账户和组权限，以确保用于管理服务器的账户不与内部网络中用户的账户和权限重叠，这些账户可能通过凭据访问获得，并用于登录 Web 服务器并植入 Web Shell 或从 Web 服务器转向内部网络。

6) **过滤网络流量**：使用基于主机的安全软件阻止非必要流量，例如 LLMNR/NetBIOS。

7) **限制文件和目录权限**：将脚本的写访问权限限制为特定管理员。在可能的情况下执行访问和执行日志记录。

表 I 包括哪些缓解措施可以防止每种技术，通过将单元格着色为红色并包括每种缓解措施的编号。

## VI. 结论

据作者所知，这是对 Phineas Fisher 的首次学术分析，也是第一篇提供对关键基础设施“活动黑客”威胁的技术分析的论文。我们选取了一个以前未知的威胁行为者，并识别了一组可用于缓解未来攻击的战术和技术。我们正在将此威胁行为者提交到 MITRE ATT&CK（ATT&CK）知识库，该知识库将提供给其他研究人员和安全从业者。更广泛地说，还需要研究在工业控制环境中检测和预防此类威胁行为者。

## 关于可复现性的说明

用于创建这些模型的所有信息都在正文中引用。由于一些宣言难以确定，我们维护了一个本地副本，其中包括各个 ATT&CK 模型以及本手稿中讨论的合并模型。

## 致谢

作者感谢审稿人的有益反馈。我们还要感谢 Risky Biz 播客的主持人（Patrick Gray 和 Adam Boileau），他们提供了对 Fisher 漏洞利用的有启发性的报道，并让作者注意到了 Fisher。

## 参考文献

[^1]: ESET, “Industroyer: Biggest threat to industrial control systems since Stuxnet,” p. 17. [Online]. Available: https://www.welivesecurity.com/2017/06/12/industroyer-biggest-threat-industrial-control-systems-since-stuxnet/
[^2]: J. Slowik, “CRASHOVERRIDE: Reassessing the 2016 Ukraine Electric Power Event as a Protection-Focused Attack.” [Online]. Available: https://dragos.com/resource/crashoverride-reassessing-the-2016-ukraine-electric-power-event-as-a-protection-focused-attack/
[^3]: I. Ghafir, J. Saleem, M. Hammoudeh, H. Faour, V. Prenosil, S. Jaf, S. Jabbar, and T. Baker, “Security threats to critical infrastructure: The human factor,” vol. 74, no. 10, pp. 4986–5002.
[^4]: R. White, “Risk Analysis for Critical Infrastructure Protection,” in Critical Infrastructure Security and Resilience: Theories, Methods, Tools and Technologies, ser. Advanced Sciences and Technologies for Security Applications, D. Gritzalis, M. Theocharidou, and G. Stergiopoulos, Eds. Springer International Publishing, pp. 35–54.
[^5]: P. Fisher. HackBack - A DIY Guide To Rob Banks. [Online]. Available: https://packetstormsecurity.com/files/155392/HackBack-A-DIY-Guide-To-Rob-Banks.html
[^6]: M. Rudner, “Cyber-Threats to Critical National Infrastructure: An Intelligence Challenge,” vol. 26, no. 3, pp. 453–481.
[^7]: K. Stouffer, V. Pillitteri, S. Lightman, M. Abrams, and A. Hahn, “Guide to Industrial Control Systems (ICS) Security.”
[^8]: Department of Homeland Security. DHS warns Anonymous may target critical infrastructure. [Online]. Available: https://web.archive.org/web/20180916124235/http://www.homelandsecuritynewswire.com/dhs-warns-anonymous-may-target-critical-infrastructure
[^9]: O. Yaron, “Hackers Threaten Cyber Attack Against Israel; Mossad, IDF Websites Down.” [Online]. Available: https://www.haaretz.com/1.5207001
[^10]: ICS-CERT, “Incident Response Summary Report (2009-2011),” p. 17. [Online]. Available: https://ics-cert.us-cert.gov/Other-Reports
[^11]: B. E. Strom, J. A. Battaglia, M. S. Kemmerer, W. Kupersanin, D. P. Miller, C. Wampler, S. M. Whitley, and R. D. Wolf, “Finding Cyber Threats with ATT&CK-Based Analytics.” [Online]. Available: https://www.mitre.org/publications/technical-papers/finding-cyber-threats-with-attck-based-analytics
[^12]: B. E. Strom, A. Applebaum, D. P. Miller, K. C. Nickels, A. G. Pennington, and C. B. Thomas, “MITRE ATT&CK: Design and Philosophy.” [Online]. Available: https://www.mitre.org/publications/technical-papers/mitre-attack-design-and-philosophy
[^13]: A. Shostack, Threat Modeling: Designing for Security. Wiley.
[^14]: E. M. Hutchins, M. J. Cloppert, and R. M. Amin, “Intelligence-driven computer network defense informed by analysis of adversary campaigns and intrusion kill chains,” vol. 1, no. 1, p. 80.
[^15]: L. Franceschi-Bicchierai. Hacker Phineas Fisher Speaks on Camera for the First Time Through a Puppet. [Online]. Available: https://www.vice.com/en_us/article/78kwke/hacker-phineas-fisher-hacking-team-puppet
[^16]: Jeff Larson and Mike Tigas. Leaked Docs Show Spyware Used to Snoop on U.S. Computers. [Online]. Available: https://www.propublica.org/article/leaked-docs-show-spyware-used-to-snoop-on-u.s.-computers
[^17]: M. Marquis-Boire and B. Marczak. From Bahrain With Love: FinFisher’s Spy Kit Exposed. [Online]. Available: https://citizenlab.ca/2012/07/from-bahrain-with-love-finfishers-spy-kit-exposed/
[^18]: P. Fisher, “Hack Back: A DIY Guide for those without the patience to wait for whistleblowers.”
[^19]: J.M. Porup. How Hacking Team got hacked. [Online]. Available: https://arstechnica.com/information-technology/2016/04/how-hacking-team-got-hacked-phineas-phisher/
[^20]: L. Franceschi-Bicchierai. The Vigilante Who Hacked Hacking Team Explains How He Did It. [Online]. Available: https://www.vice.com/en_us/article/3dad3n/the-vigilante-who-hacked-hacking-team-explains-how-he-did-it
[^21]: P. Fisher. HackBack - DIY Guide (HackingTeam). [Online]. Available: https://www.exploit-db.com/exploits/41915
[^22]: Collective. HackBack! Talking with Phineas Fisher: Hacking as Direct Action against the Surveillance State. [Online]. Available: https://crimethinc.com/2018/06/05/hackback-talking-with-phineas-fisher-hacking-as-direct-action-against-the-surveillance-state
[^23]: A. Greenberg, “WikiLeaks Dumps ‘Erdogan Emails’ After Turkey’s Failed Coup.” [Online]. Available: https://www.wired.com/2016/07/wikileaks-dumps-erdogan-emails-turkeys-failed-coup/
[^24]: Emma Best. Renowned hacker and former WikiLeaks source Phineas Fisher says organization misled people about their files Emma Best. [Online]. Available: https://emma.best/2019/07/18/hacker-wikileaks-source-phineas-fisher-says-organization-misled-people-about-their-files/
[^25]: L. Franceschi-Bicchierai. Hacking Team Hacker Phineas Fisher Is Taking a Break Because of Stress. [Online]. Available: https://www.vice.com/en_us/article/xy5enw/hacking-teams-phineas-fisher-will-return-but-only-after-a-break-at-the-beach
[^26]: ——. Phineas Fisher Offers $100,000 Bounty to Hack Banks and Oil Companies. [Online]. Available: https://www.vice.com/en_us/article/vb5agy/phineas-fisher-offers-dollar100000-bounty-for-hacks-against-banks-and-oil-companies
[^27]: J. Cox. Offshore Bank Targeted by Phineas Fisher Confirms It Was Hacked. [Online]. Available: https://www.vice.com/en_ca/article/ne8p9b/offshore-bank-targeted-phineas-fisher-confirms-hack-cayman-national-bank
[^28]: L. Franceschi-Bicchierai. Hacking Team Hacker Phineas Fisher Has Gotten Away With It. [Online]. Available: https://www.vice.com/en_us/article/3k9zzk/hacking-team-hacker-phineas-fisher-has-gotten-away-with-it
[^29]: ——. Vigilante Hacker Phineas Fisher Denies Working for the Russian Government. [Online]. Available: https://www.vice.com/en_ca/article/qv7y8m/vigilante-hacker-phineas-fisher-denies-working-for-the-russian-government
[^30]: P. Maynard, K. McLaughlin, and S. Sezer, “Modelling Duqu 2.0 Malware using Attack Trees with Sequential Conjunction,” in 2nd International Conference on Information Systems Security and Privacy.