- Web3 Sandbox
    - 描述：找到一个意外部署的，可以即时编写智能合约的代码沙盒。
    - 提示：这与找到计分板一样容易。
    - 在 ```main.js``` 中搜索 ```sandbox```
    找到看似路由设置的内容
        ```javascript
        {
            path: "web3-sandbox",
            loadChildren: function() {
                var n = (0, S.A)(function*() {
                    return yield Jm()
                });
                return function() {
                    return n.apply(this, arguments)
                }
            }()
        }
        ```
        访问 ```http://127.0.0.1:3000/#/web3-sandbox``` 进入页面

- 编程挑战
    ```typescript
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
    - 与 D1 Score Board 查找计分板的相同的路由代码，在其中寻找 Web3 Sandbox 对应路由设置:
        ```typescript
        {
            path: 'web3-sandbox',
            loadChildren: async () => await loadWeb3SandboxModule()
	    }
        ```
    - 修复：完全删除此冗余功能
        > 这个沙盒是为应用程序的开发者准备的，它被添加是为了便于测试和原型设计。当应用程序投入生产时，这种功能绝对不应该包含在内！