- Score Board
    - 描述：寻找隐藏的计分板
    - 指导教程：猜测计分板 URL 或查看 JavaScript 代码
    1. 访问首页后在 burp 的代理历史记录中过滤关键词“board”
    2. 查看剩余消息，其中
        请求行
        ```GET /rest/admin/application-configuration HTTP/1.1```
        部分响应
        ```json
        {
            "securityTxt": {
                "contact": "mailto:donotreply@owasp-juice.shop",
                "encryption": "https://keybase.io/bkimminich/pgp_keys.asc?fingerprint=19c01cb7157e4645e9e2c863062a85a8cbfbdcda",
                "acknowledgements": "/#/score-board",
                "hiring": "/#/jobs",
                "csaf": "/.well-known/csaf/provider-metadata.json"
            }
        }
        ```
        使用此信息访问```http://127.0.0.1:3000/#/score-board```进入计分板
    - 之前的猜测没有获得足够多的信息：```ScoreBoard```与```scoreboard```。
    命名模式为单词之间使用连字符```-```
    - 对应 URL 在 ```.well-known``` 目录下
    ```http://localhost:3000/.well-known/security.txt```


- 编程挑战
    TypeScript 变量声明后的```: 类型```是对变量类型的约束
    ```TypeScript
        const routes: Routes = [
        {
            path: 'administration',
            component: AdministrationComponent,
            canActivate: [AdminGuard]
        },
        {
            path: 'accounting',
            component: AccountingComponent,
            canActivate: [AccountingGuard]
        },
        {
            path: 'about',
            component: AboutComponent
        },
        {
            path: 'address/select',
            component: AddressSelectComponent,
            canActivate: [LoginGuard]
        },
        {
            path: 'address/saved',
            component: SavedAddressComponent,
            canActivate: [LoginGuard]
        },
        {
            path: 'address/create',
            component: AddressCreateComponent,
            canActivate: [LoginGuard]
        },
        {
            path: 'address/edit/:addressId',
            component: AddressCreateComponent,
            canActivate: [LoginGuard]
        },
        {
            path: 'delivery-method',
            component: DeliveryMethodComponent
        },
        {
            path: 'deluxe-membership',
            component: DeluxeUserComponent,
            canActivate: [LoginGuard]
        },
        {
            path: 'saved-payment-methods',
            component: SavedPaymentMethodsComponent
        },
        {
            path: 'basket',
            component: BasketComponent
        },
        {
            path: 'order-completion/:id',
            component: OrderCompletionComponent
        },
        {
            path: 'contact',
            component: ContactComponent
        },
        {
            path: 'photo-wall',
            component: PhotoWallComponent
        },
        {
            path: 'complain',
            component: ComplaintComponent
        },
        {
            path: 'chatbot',
            component: ChatbotComponent
        },
        {
            path: 'order-summary',
            component: OrderSummaryComponent
        },
        {
            path: 'order-history',
            component: OrderHistoryComponent
        },
        {
            path: 'payment/:entity',
            component: PaymentComponent
        },
        {
            path: 'wallet',
            component: WalletComponent
        },
        {
            path: 'login',
            component: LoginComponent
        },
        {
            path: 'forgot-password',
            component: ForgotPasswordComponent
        },
        {
            path: 'recycle',
            component: RecycleComponent
        },
        {
            path: 'register',
            component: RegisterComponent
        },
        {
            path: 'search',
            component: SearchResultComponent
        },
        {
            path: 'hacking-instructor',
            component: SearchResultComponent
        },
        {
            path: 'score-board',
            component: ScoreBoardComponent
        },
        {
            path: 'track-result',
            component: TrackResultComponent
        },
        {
            path: 'track-result/new',
            component: TrackResultComponent,
            data: {
            type: 'new'
            }
        },
        {
            path: '2fa/enter',
            component: TwoFactorAuthEnterComponent
        },
        {
            path: 'privacy-security',
            component: PrivacySecurityComponent,
            children: [
            {
                path: 'privacy-policy',
                component: PrivacyPolicyComponent
            },
            {
                path: 'change-password',
                component: ChangePasswordComponent
            },
            {
                path: 'two-factor-authentication',
                component: TwoFactorAuthComponent
            },
            {
                path: 'data-export',
                component: DataExportComponent
            },
            {
                path: 'last-login-ip',
                component: LastLoginIpComponent
            }
            ]
        },
        {
            path: 'juicy-nft',
            component: NFTUnlockComponent
        },
        {
            path: 'wallet-web3',
            loadChildren: async () => await loadWeb3WalletModule()
        },
        {
            path: 'web3-sandbox',
            loadChildren: async () => await loadWeb3SandboxModule()
        },
        {
            path: 'bee-haven',
            loadChildren: async () => await loadFaucetModule()
        },
        {
            matcher: oauthMatcher,
            data: { params: (window.location.href).substr(window.location.href.indexOf('#')) },
            component: OAuthComponent
        },
        {
            matcher: tokenMatcher,
            component: TokenSaleComponent
        },
        {
            path: '403',
            component: ErrorPageComponent
        },
        {
            path: '**',
            component: SearchResultComponent
        }
        ]
    ```

    在其中找到：
    ```typescript
    {
        path: 'score-board',
        component: ScoreBoardComponent
    }
    ```
    修复为：
    ```typescript
    {
        path: 'score-board', // Must remain as is! Needed for challenge tracking!
        component: ScoreBoardComponent
    }
    ```
    无需修复