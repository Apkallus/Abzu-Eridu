https://v8.dev/docs



## include —— 头定义

### v8-profiler.h

```c++
/**
 * HeapSnapshots record the state of the JS heap at some moment.
 */
class V8_EXPORT HeapSnapshot {
 public:
  enum SerializationFormat {
    kJSON = 0  // See format description near 'Serialize' method.
  };

  /** Returns the root node of the heap graph. */
  const HeapGraphNode* GetRoot() const;

  /** Returns a node by its id. */
  const HeapGraphNode* GetNodeById(SnapshotObjectId id) const;

  /** Returns total nodes count in the snapshot. */
  int GetNodesCount() const;

  /** Returns a node by index. */
  const HeapGraphNode* GetNode(int index) const;

  /** Returns a max seen JS object Id. */
  SnapshotObjectId GetMaxSnapshotJSObjectId() const;

  /**
   * Deletes the snapshot and removes it from HeapProfiler's list.
   * All pointers to nodes, edges and paths previously returned become
   * invalid.
   */
  void Delete();

  /**
   * Prepare a serialized representation of the snapshot. The result
   * is written into the stream provided in chunks of specified size.
   * The total length of the serialized snapshot is unknown in
   * advance, it can be roughly equal to JS heap size (that means,
   * it can be really big - tens of megabytes).
   *
   * For the JSON format, heap contents are represented as an object
   * with the following structure:
   *
   *  {
   *    snapshot: {
   *      title: "...",
   *      uid: nnn,
   *      meta: { meta-info },
   *      node_count: nnn,
   *      edge_count: nnn
   *    },
   *    nodes: [nodes array],
   *    edges: [edges array],
   *    strings: [strings array]
   *  }
   *
   * Nodes reference strings, other nodes, and edges by their indexes
   * in corresponding arrays.
   */
  void Serialize(OutputStream* stream,
                 SerializationFormat format = kJSON) const;
};
```

## src —— 源码

### profiler

#### heap-snapshot-generator.cc

https://github.com/v8/v8/blob/master/src/profiler/heap-snapshot-generator.cc

定义内存快照 JSON 序列格式的函数
```cpp
void HeapSnapshotJSONSerializer::SerializeImpl();
void HeapSnapshotJSONSerializer::SerializeSnapshot();
```