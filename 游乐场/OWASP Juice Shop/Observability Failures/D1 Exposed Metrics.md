- Exposed Metrics
    - 描述：找到那个为[流行监控系统 prometheus](https://github.com/prometheus/prometheus)提供可抓取使用数据的端点。
    - [官网设置文档](https://prometheus.io/docs/introduction/first_steps/#configuring-prometheus)：
        > Prometheus 期望指标在目标上的路径为 ```/metrics``` 。因此，此默认任务通过 URL ```http://localhost:9090/metrics``` 进行扫描。
    - 访问```http://127.0.0.1:3000/metrics```
    响应为端点内容

- 编程挑战
    ```TypeScript
    /* Serve metrics */
	let metricsUpdateLoop: any
	const Metrics = metrics.observeMetrics()
	app.get('/metrics', metrics.serveMetrics())
	errorhandler.title = `${config.get<string>('application.name')} (Express ${utils.version('express')})`
	 
	export async function start (readyCallback?: () => void) {
	  const datacreatorEnd = startupGauge.startTimer({ task: 'datacreator' })
	  await sequelize.sync({ force: true })
	  await datacreator()
	  datacreatorEnd()
	  const port = process.env.PORT ?? config.get('server.port')
	  process.env.BASE_PATH = process.env.BASE_PATH ?? config.get('server.basePath')
	 
	  metricsUpdateLoop = Metrics.updateLoop()
	 
	  server.listen(port, () => {
	    logger.info(colors.cyan(`Server listening on port ${colors.bold(`${port}`)}`))
	    startupGauge.set({ task: 'ready' }, (Date.now() - startTime) / 1000)
	    if (process.env.BASE_PATH !== '') {
	      logger.info(colors.cyan(`Server using proxy base path ${colors.bold(`${process.env.BASE_PATH}`)} for redirects`))
	    }
	    registerWebsocketEvents(server)
	    if (readyCallback) {
	      readyCallback()
	    }
	  })
	 
	}
	 
	export function close (exitCode: number | undefined) {
	  if (server) {
	    clearInterval(metricsUpdateLoop)
	    server.close()
	  }
	  if (exitCode !== undefined) {
	    process.exit(exitCode)
	  }
	}
    ```
    - 其中```/metrics```的路由设置，无权限检查
        ```TypeScript
        app.get('/metrics', metrics.serveMetrics())
        ```
    - 增加中间件权限检查
        ```typescript
        app.get('/metrics', security.isAdmin(), metrics.serveMetrics())
        ```