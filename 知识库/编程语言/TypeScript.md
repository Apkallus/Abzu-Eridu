- [类型注解](https://geek-docs.com/typescript/typescript-questions/123_typescript_typescript_annotations.html)
    变量声明后的```: 类型```对变量类型的约束
    ```typescript
    const routes: Routes = [
	  {
	    path: 'administration',
	    component: AdministrationComponent,
	    canActivate: [AdminGuard]
	  }
    ]
    ```
    