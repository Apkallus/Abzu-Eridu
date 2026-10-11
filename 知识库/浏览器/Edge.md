
## devtools

### memory-problems

#### heap-snapshot-schema —— 内存快照结构

https://learn.microsoft.com/en-us/microsoft-edge/devtools/memory-problems/heap-snapshot-schema

##### Schema of the `.heapsnapshot` data

| 属性 | 描述 | 格式 |
| --- | --- | --- |
| `snapshot` | 包含有关内存图数据格式及其大小的所有信息。 | `Object` |
| `nodes` | 重新创建图节点所需的全部信息。要解析此数据，请使用 `snapshot.meta.node_types` 和 `snapshot.meta.node_fields`。 | `Array` |
| `edges` | 重新创建图的边所需的全部信息。要解析此数据，请使用 `snapshot.meta.edge_types` 和 `snapshot.meta.edge_fields`。 | `Array` |
| `trace_function_infos` | *尚未记录* | `Array` |
| `trace_tree` | *尚未记录* | `Array` |
| `samples` | *尚未记录* | `Array` |
| `locations` | 包含节点的脚本位置信息。要解析此数据，请将 `snapshot.meta.location_fields` 与 `nodes` 数组一起使用。 | `Array` |
| `strings` | 内存中保存的所有字符串组成的数组。这些可以是任何字符串，例如用户定义的字符串或代码。 | `Array` |