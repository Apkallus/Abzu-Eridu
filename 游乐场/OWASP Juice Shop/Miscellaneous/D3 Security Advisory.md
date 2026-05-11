---
title: Security Advisory
description: pass
---
:x:
- 描述：Juice Shop存在一个已知库漏洞，已有公告发布，将其标记为 known affected。修复程序尚未完成。通知商店一个合适的 checksum，作为你已尽到职责的证明。
- 提示：安全公告通常列在 security.txt 中。
- 访问 ```http://localhost:3000/.well-known/security.txt```
- 访问 ```http://localhost:3000/.well-known/csaf/2024/juice-shop-sa-disclaimer.json```
    ```json
    "vulnerabilities": [{
            "notes": [{
                "category": "details",
                "text": "The Juice Shop has intentional vulnerabilities which might be abused to attack your system",
                "title": "Intentional Vulnerable Juice Shop"
            }],
            "product_status": {
                "known_affected": [
                    "juice-shop/juice-shop"
                ]
            },
            "remediations": [{
                    "category": "no_fix_planned",
                    "date": "2024-03-03T11:00:00.000Z",
                    "details": "ONLY run the Juice Shop in an isolated training environment.",
                    "product_ids": [
                        "juice-shop/juice-shop"
                    ]
                },
                {
                    "category": "mitigation",
                    "date": "2024-03-10T08:46:00.000Z",
                    "details": "Explicitly enable safetyMode to disable unsecure challenges.\n\n```yaml\nchallenges:\n  safetyMode: enabled\n```\n",
                    "product_ids": [
                        "juice-shop/juice-shop-17-or-later"
                    ],
                    "url": "https://github.com/juice-shop/juice-shop/issues/2174"
                }
            ],
            "scores": [{
                "cvss_v3": {
                    "attackComplexity": "LOW",
                    "attackVector": "NETWORK",
                    "availabilityImpact": "NONE",
                    "baseScore": 9.1,
                    "baseSeverity": "CRITICAL",
                    "confidentialityImpact": "HIGH",
                    "environmentalScore": 9.1,
                    "environmentalSeverity": "CRITICAL",
                    "integrityImpact": "HIGH",
                    "privilegesRequired": "NONE",
                    "scope": "UNCHANGED",
                    "temporalScore": 9.1,
                    "temporalSeverity": "CRITICAL",
                    "userInteraction": "NONE",
                    "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
                    "version": "3.1"
                },
                "products": [
                    "juice-shop/juice-shop"
                ]
            }],
            "title": "Intentional Vulnerabilities"
        }
    ```
    其中，缓解措施 ```mitigation``` 
    ```json
    {
        "category": "mitigation",
        "date": "2024-03-10T08:46:00.000Z",
        "details": "Explicitly enable safetyMode to disable unsecure challenges.\n\n```yaml\nchallenges:\n  safetyMode: enabled\n```\n",
        "product_ids": [
            "juice-shop/juice-shop-17-or-later"
        ],
        "url": "https://github.com/juice-shop/juice-shop/issues/2174"
    }
    ```
    > 显式启用安全模式以禁用不安全的挑战。
    ```yaml
    challenges:
    safetyMode: enabled
    ```
- 即，修复尚未完成的情况下，