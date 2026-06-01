# 使用记录 — execution-workflow 引擎

> 日期：2026-06-02  
> 任务：Step 2 下半 — execution-workflow 工作流引擎  
> 项目：`02_DB_Demo_Studio/packages/execution-workflow/`  
> AI 工具：Claude Code  
> 耗时：约 30 min

---

## 任务

实现 SQL 执行工作流引擎：接收 SQL → 解析 → 生成标准 6 步 DAG（lex/parse/optimize/plan/execute/result）→ 输出与 DemoStep schema 兼容的格式。

## AI 帮了什么

1. **数据模型**：`ExecutionWorkflowIR` + `WorkflowPhase` + `StepMapping` 完全对齐 ai-workflow.md 中的 TypeScript 接口
2. **SQL 解析器**：用 `LexPattern` 提取关键字，`extract_tables()` 提取表名，`estimate_scan_type()` 从 EXPLAIN JSON 推断扫描方式
3. **工作流引擎**：`ExecutionWorkflowEngine.build()` 生成 6 步完整 DAG，包含 engine 证据链
4. **转换器**：`to_demo_package_steps()` 将 IR 转换为 Player 可消费的 `DemoStep[]`
5. **双引擎支持**：`--explain` 模式连接 db-engine 获取真实 EXPLAIN

## 产出

| 文件 | 说明 |
|---|---|
| `packages/execution-workflow/workflow.py` | 工作流引擎（~240 行） |
| `packages/execution-workflow/tests/` | 测试目录 |

## 验证

```bash
# 纯解析模式
python workflow.py "SELECT s.name, c.course_name FROM students s INNER JOIN courses c ON s.id = c.student_id"

# 带 EXPLAIN 模式（需要 db-engine 容器运行中）
python workflow.py "SELECT s.name, c.course_name FROM students s INNER JOIN courses c ON s.id = c.student_id" --explain
```

## 可复用经验

- 用 `--explain` 参数可选接 db-engine，开发时无需启动容器也能调试
- `to_demo_package_steps()` 的输出直接兼容 Player，减少了一个转换层
