# DB Demo Studio — 需求规格说明书 v3

> 基于已实现功能、原始需求（`00_Notes/requirements/db_demo_video_requirements.md`）及产品定位升级方向整理。
> 包含**已验证可运行**需求 \+ 分阶段落地的新增核心功能，标注实现优先级与落地周期。
> 
> 

---

## 1\. 产品定位

AI 驱动的数据库教学演示与互动教学闭环工具，聚焦数据库课程教学全流程的可视化讲解与教学场景落地，通过「EXPLAIN 真值 \+ AI 智能讲解 \+ 交互式分步演示」三大核心能力，解决数据库教学中 “执行逻辑抽象难讲、知识点理解成本高、备课效率低、教学效果验证难” 的行业痛点，覆盖**教学备课、课堂互动演示、课后自主学习、教学效果验证**全链路，成为高校数据库课程、企业数据库培训的标准化教学工具。

**三场景：** 教师备课（AI Studio）・课堂分步演示（Execution Player）・学生课后自学
**双交付（同源）：** 交互网页 \+（规划中）MP4 导出
**核心演示能力分级：** 第一级（5 分钟落地 / Agent 原生）→ 第二级（1 天落地 / 轻量交互）→ 第三级（3 天落地 / 专业级教学）

---

## 2\. 核心业务流程

```Plain Text
用户输入 SQL/知识点/教学场景（ER图/JOIN/索引/事务等）
       ↓
POST /api/ai/chat  (SSE)
       ↓
  1. 基础分析层：
     sql_analyze      — 词法/语法分析、提取表名/关键字/执行阶段
     explain_mysql    — MySQL EXPLAIN FORMAT=JSON
     explain_postgres — PostgreSQL EXPLAIN (FORMAT JSON)
  2. 演示类型决策层：
     根据用户选择/场景自动匹配演示类型（Mermaid/ASCII/Streamlit-ECharts/SQLFlow/分步执行模拟器等）
  3. 内容生成层：
     ExecutionWorkflowEngine（扩展6阶段DAG） + 演示内容生成器（分三级优先级）
     ↳ 第一级：Mermaid 动态分步代码/ASCII 动画（纯文本，零前端依赖）
     ↳ 第二级：ECharts 配置/SQLFlow SVG/Pyvis 关系图（轻量交互，Streamlit集成）
     ↳ 第三级：SQL执行模拟器/索引动画/事务隔离演示（专业级，交互式分步）
  4. 讲解词生成层：
     generate_narration — 适配不同演示类型的中英双语讲解词（LLM/规则模板）
       ↓
  SSE 流式返回：
    assistant-text → step-preview×N → demo-updated → demo-complete
    （N随演示类型动态调整：基础6阶段/索引8阶段/事务5阶段等）
```

---

## 3\. 功能需求

### 核心维度定义

|优先级|落地周期|核心特征|技术依赖|
|---|---|---|---|
|🔴 第一级|本周内|Agent 原生生成、纯文本、零前端开发成本|Mermaid、ASCII|
|🟠 第二级|第 3 周|轻量交互、Streamlit 原生集成、可视化增强|Streamlit\-ECharts、SQLFlow API、Pyvis|
|🟢 第三级|第 5\-7 周|专业级动画、交互式模拟、教学核心亮点|D3\.js/React\-D3\-Tree、双数据库会话、分步执行引擎|

### 3\.1 基础能力（已实现，全优先级依赖）

|子项|状态|说明|
|---|---|---|
|F0\.1 SQL / 知识点解析|✅|自动识别 SQL，提取表名 / 关键字 / 执行阶段；支持知识点模式（curriculum\_node）|
|F0\.2 双引擎 EXPLAIN|✅|MySQL 8\.0/PostgreSQL 16 EXPLAIN JSON 提取、归一化、代价对比|
|F0\.3 AI / 规则讲解词生成|✅|基于 DeepSeek LLM（有 API Key）/ 规则模板（无 API Key）生成中英双语讲解词，适配不同演示阶段|
|F0\.4 分步播放控制|✅|进度条 / 单步进退 / 自动播放 / 键盘控制 / 当前步骤高亮|

### 3\.2 🔴 第一级：5 分钟落地（Agent 原生支持，本周内完成）

#### F1: Mermaid 动态分步演示（必做）

|子项|状态|说明|
|---|---|---|
|F1\.1 多场景 Mermaid 代码生成|📅 待实现|Agent 根据输入自动生成对应场景的 Mermaid 代码，支持直接复制使用|
|F1\.2 场景覆盖|📅 待实现|表结构与 ER 关系图、SQL 执行流程（SELECT/FROM/WHERE 等）、JOIN 操作分步匹配、事务 ACID 特性、B \+ 树索引简化版|
|F1\.3 分步高亮渲染|📅 待实现|支持 classDef/note 语法实现执行步骤动态高亮，Agent 生成可切换高亮状态的 Mermaid 代码|
|F1\.4 一键渲染预览|📅 待实现|前端支持 Mermaid 代码即时渲染，同步展示分步高亮效果|

#### F2: ASCII 动画演示

|子项|状态|说明|
|---|---|---|
|F2\.1 纯文本动画生成|📅 待实现|Agent 生成零依赖的 ASCII 文本动画，适配终端 / 无可视化环境|
|F2\.2 场景覆盖|📅 待实现|数据增删改的行级变化、锁竞争与等待、简单索引查找过程|
|F2\.3 分步文本输出|📅 待实现|按执行步骤拆分 ASCII 动画，支持与播放控制联动切换步骤|

### 3\.3 🟠 第二级：1 天落地（轻量可交互，第 3 周完成）

#### F3: Streamlit \+ ECharts 可视化

|子项|状态|说明|
|---|---|---|
|F3\.1 ECharts 配置生成|📅 待实现|Agent 自动生成 ECharts JSON 配置（适配教学场景）|
|F3\.2 可视化场景覆盖|📅 待实现|数据分布（柱状图 / 折线图 / 饼图）、SQL 执行性能对比、表 / 索引统计、慢查询分析|
|F3\.3 Streamlit 原生渲染|📅 待实现|集成 streamlit\_echarts 组件，一键渲染可视化图表，支持交互（缩放 / 筛选）|

#### F4: SQLFlow 集成

|子项|状态|说明|
|---|---|---|
|F4\.1 SQLFlow API 调用|📅 待实现|Agent 封装 SQLFlow API，传入 SQL 生成执行计划 / 数据流 SVG|
|F4\.2 场景覆盖|📅 待实现|复杂 SQL 执行计划、多表 JOIN 数据流、子查询 / CTE 嵌套、数据血缘分析|
|F4\.3 SVG 预览与交互|📅 待实现|Streamlit 中渲染 SVG，支持缩放 / 点击查看节点详情|

#### F5: Pyvis 交互式关系图

|子项|状态|说明|
|---|---|---|
|F5\.1 关系图数据生成|📅 待实现|Agent 解析数据库元数据，生成 Pyvis 所需的节点 / 边配置|
|F5\.2 场景覆盖|📅 待实现|全库 ER 图、外键依赖、多对多中间表关系|
|F5\.3 交互能力|📅 待实现|拖拽 / 缩放 / 点击节点查看表结构 / 索引信息|

### 3\.4 🟢 第三级：3 天落地（专业级教学演示，第 5\-7 周完成）

#### F6: 分步式 SQL 执行模拟器（核心亮点，第 5 周完成）

|子项|状态|说明|
|---|---|---|
|F6\.1 SQL 语法树解析|📅 待实现|拆分 SQL 执行步骤（FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY）|
|F6\.2 中间结果生成|📅 待实现|每个步骤生成对应的中间结果表，标注数据保留 / 过滤状态|
|F6\.3 交互式分步执行|📅 待实现|支持「上一步 / 下一步 / 自动播放」，实时展示当前步骤执行逻辑与中间结果|
|F6\.4 多 SQL 兼容|📅 待实现|适配 SELECT/JOIN/ 子查询 / CTE 等常见 SQL 类型|

#### F7: 索引原理动态演示器（第 7 周完成）

|子项|状态|说明|
|---|---|---|
|F7\.1 B \+ 树动画生成|📅 待实现|基于 D3\.js/React\-D3\-Tree 实现 B \+ 树的构建 / 查找 / 插入 / 删除动画|
|F7\.2 交互控制|📅 待实现|单步演示索引操作、调整动画速度、高亮当前操作节点|
|F7\.3 原理讲解联动|📅 待实现|动画与讲解词同步，解释索引底层逻辑（如叶子节点链表、非叶子节点索引值）|

#### F8: 事务隔离级别演示器（第 7 周完成）

|子项|状态|说明|
|---|---|---|
|F8\.1 双会话环境构建|📅 待实现|创建两个独立的 MySQL/PostgreSQL 连接，模拟并发事务|
|F8\.2 隔离级别切换|📅 待实现|支持 READ UNCOMMITTED/READ COMMITTED/REPEATABLE READ/SERIALIZABLE 切换|
|F8\.3 现象可视化|📅 待实现|实时展示不同隔离级别下的脏读 / 不可重复读 / 幻读现象，标注数据差异|
|F8\.4 对比讲解|📅 待实现|生成隔离级别原理讲解词，对比不同级别下的行为差异|

### 3\.5 教学闭环补充能力

|子项|状态|说明|
|---|---|---|
|F9\.1 演示内容导出|📅 规划中|支持 Mermaid 代码 / ASCII 文本 / ECharts 配置 / SVG 导出，适配备课场景|
|F9\.2 课后练习生成|📅 规划中|基于演示的 SQL / 知识点，AI 生成配套练习题（如索引优化、事务隔离级别判断）|
|F9\.3 教学效果验证|📅 规划中|学生端提交练习答案，系统自动校验并生成解析（关联演示内容）|

### 3\.6 阶段 EXPLAIN 信息展示（增强版）

|阶段|基础展示内容|新增演示联动内容|
|---|---|---|
|**lex**（词法分析）|SQL 关键字标签 \+ 数量统计|Mermaid 关键字高亮标注、ASCII 关键字清单|
|**parse**（语法分析）|表名 \+ 子句检测|Pyvis ER 图实时渲染、SQLFlow 表节点高亮|
|**optimize**（查询优化）|扫描方式 \+ 涉及表数 \+ 说明|ECharts 扫描方式性能对比图|
|**plan**（执行计划）|MySQL vs PostgreSQL 代价对比 \+ EXPLAIN JSON|SQLFlow 执行计划 SVG 渲染|
|**execute**（执行过程）|估计扫描行数 \+ EXPLAIN JSON|分步 SQL 执行模拟器中间结果、索引动画联动|
|**result**（结果集）|讲解词|事务隔离级别演示最终数据对比、练习生成触发|

### 3\.7 讲课词生成（增强版）

|模式|条件|说明|
|---|---|---|
|LLM 生成|有 `DEEPSEEK_API_KEY`|调用 DeepSeek Chat，传入 SQL \+ EXPLAIN 摘要 \+ 演示类型 \+ 阶段信息，生成适配可视化的讲解词|
|规则模板|无 API key|基于 engineEvidence \+ 演示类型生成讲解词，覆盖：<br>1\. Mermaid/ASCII 动画步骤说明<br>2\. ECharts/SQLFlow 图表解读<br>3\. 索引 / 事务原理专业解析|

规则模板 fallback 新增覆盖场景：B \+ 树索引操作、事务隔离级别现象、SQL 分步执行中间结果、多表 JOIN 匹配逻辑。

---

## 4\. 数据模型（扩展版）

### DemoPackage

|字段|类型|必填|说明|
|---|---|---|---|
|id|string|✅|`dp_<hash>`|
|title\.zh|string|✅|适配演示类型的标题（如「B \+ 树索引查找演示」）|
|title\.en|string|✅|英文标题|
|steps\[\]|DemoStep\[\]|✅|步骤列表（数量随演示类型动态调整）|
|workflowTrace|object|✅|扩展演示类型标识|
|engineCompare|object|可选|MySQL/PostgreSQL EXPLAIN 对比|
|metadata|object|✅|新增：演示优先级、落地周期、适用场景|
|playback|object|✅|扩展：动画速度、高亮配置|
|demoContent|object|✅|新增：不同演示类型的内容载体|

#### demoContent 子字段

|子字段|类型|适用优先级|说明|
|---|---|---|---|
|mermaidCode|string|🔴|Mermaid 分步演示代码（含高亮配置）|
|asciiAnimation|array|🔴|按步骤拆分的 ASCII 动画文本|
|echartsConfig|object|🟠|ECharts JSON 配置|
|sqlflowSvg|string|🟠|SQLFlow 生成的 SVG 字符串|
|pyvisConfig|object|🟠|Pyvis 节点 / 边配置|
|sqlSimulator|object|🟢|SQL 分步执行的中间结果表 \+ 步骤拆分|
|indexAnimation|object|🟢|B \+ 树动画的节点 / 操作序列配置|
|transactionDemo|object|🟢|双会话事务执行日志 \+ 数据对比|

### DemoStep（扩展版）

|字段|类型|说明|
|---|---|---|
|id|string|`wfstep_N`|
|order|int|步骤编号（动态适配演示类型，如索引演示为 1\-8）|
|workflowPhase|string|基础值：`lex|parse|optimize|plan|execute|result`<br>扩展值：`index-build|index-search|transaction-dirty-read|sql-step-where` 等|
|narration|\{zh, en, source\}|`source: "rule" | "ai"`，适配演示类型的讲解词|
|engineEvidence|object|各阶段特有数据|
|enginePlan|\{mysql, postgres\}|plan/execute 阶段特有|
|visuals|object|扩展：`type: "highlight-sql|mermaid-highlight|ascii-step|echarts|pyvis|index-animation|transaction-demo"`|
|groundingRef|string|EXPLAIN 引用 \+ 演示内容关联 ID|

---

## 5\. API 接口（扩展版）

### POST /api/ai/chat（核心扩展）

SSE 流式对话，事件序列新增演示类型相关事件：

|事件类型|说明|
|---|---|
|`assistant-text`|状态提示文字|
|`step-preview`|单步生成结果（每步一个）|
|`demo-content-generated`|特定演示类型内容生成完成（如 mermaidCode/asciiAnimation）|
|`demo-updated`|完整 DemoPackage JSON|
|`demo-complete`|完成信号，含 demo\_id \+ 演示类型标识|
|`error`|错误信息|

**请求体扩展：**

```json
{
  "message": "JOIN 查询",
  "sql": "SELECT ...",      // 可选，自动从 message 提取
  "curriculum_node": "JOIN", // 可选
  "demo_type": "mermaid"    // 可选，指定演示类型：mermaid/ascii/echarts/sqlflow/pyvis/sql-simulator/index/transaction
}
```

### GET /api/demos/:id

返回扩展版 DemoPackage JSON，包含所有演示类型的内容载体。

### GET /api/demos/:id/export

**新增**：导出指定演示类型的内容（如 Mermaid 代码、ASCII 文本、ECharts 配置），支持 `format=mermaid/ascii/echarts/svg` 参数。

---

## 6\. 技术架构（扩展版）

```Plain Text
┌─ Frontend (React 19 + TS + Vite 8 + TailwindCSS v4) ─┐
│  localhost:5173  │  proxy /api → :8000                  │
│  ┌─ ChatPanel ─┐  ┌─ FlowEditor ─┐  ┌─ Player ─────┐  │
│  │ 演示类型选择  │  │ 多类型演示卡片 │  │ 扩展播放控制  │  │
│  │ 输入/发送    │  │ 阶段标签+演示  │  │ 动画速度调节  │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
├─ Streamlit 层 (Python + Streamlit 1.30+) ────────────┤
│  localhost:8501                                       │
│  ┌─ ECharts 渲染 ┐  ┌─ SQLFlow SVG ┐  ┌─ Pyvis 渲染 ┐ │
│  │ streamlit_echarts │  markdown unsafe HTML  │  pyvis 组件 │ │
│  └────────────────┘  └───────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────┘
         │ POST /api/ai/chat (SSE)
         ▼
┌─ Backend (Flask + Flask-CORS) ──────────────────────────┐
│  localhost:8000                                          │
│  _build_demo_from_sql() → 扩展演示类型生成逻辑           │
│    → sql_analyze + explain_mysql/explain_postgres       │
│    → DemoTypeEngine (多类型演示内容生成器)               │
│      ├─ MermaidGenerator (🔴)                            │
│      ├─ ASCIIAnimationGenerator (🔴)                     │
│      ├─ EChartsConfigGenerator (🟠)                      │
│      ├─ SQLFlowAPIClient (🟠)                            │
│      ├─ PyvisGraphGenerator (🟠)                         │
│      ├─ SQLSimulatorEngine (🟢)                          │
│      ├─ IndexAnimationGenerator (🟢)                     │
│      └─ TransactionDemoEngine (🟢)                       │
│    → generate_narration (适配演示类型的讲解词)           │
│    → SSE StreamResponse                                  │
└──────────────────────────────────────────────────────────┘
         │ pymysql / psycopg2 / SQLFlow API
         ▼
┌─ Docker ────────────────────────────────────────────────┐
│  MySQL 8.0 :3308  →  db_demo 数据库                      │
│  PostgreSQL 16 :5433 →  db_demo 数据库                    │
│  含 students / courses 表 + 示例数据                      │
│  新增：双会话事务演示专用库 db_demo_transaction          │
└──────────────────────────────────────────────────────────┘
┌─ 前端动画依赖 ───────────────────────────────────────────┐
│  D3.js v7 / React-D3-Tree / Mermaid Renderer             │
└──────────────────────────────────────────────────────────┘
```

---

## 7\. 配置项（扩展版）

|变量|默认值|说明|
|---|---|---|
|`DEEPSEEK_API_KEY`|—|DeepSeek API key，启用 LLM 讲解词|
|`MYSQL_HOST`|\[127\.0\.0\.1\]\(127\.0\.0\.1\)|MySQL 主机|
|`MYSQL_PORT`|3308|MySQL 端口|
|`PG_HOST`|\[127\.0\.0\.1\]\(127\.0\.0\.1\)|PostgreSQL 主机|
|`PG_PORT`|5433|PostgreSQL 端口|
|`SQLFLOW_API_URL`|[https://sqlflow\.gudusoft\.com/api/sqlflow](https://sqlflow.gudusoft.com/api/sqlflow)|SQLFlow API 地址|
|`STREAMLIT_PORT`|8501|Streamlit 服务端口|
|`DEFAULT_ANIMATION_SPEED_MS`|2000|索引 / 事务演示默认动画速度|
|`DEMO_PRIORITY`|first|默认生成的演示优先级：first/second/third|

---

## 8\. 非功能需求（扩展版）

|指标|当前值 / 目标值|说明|
|---|---|---|
|SQL→演示生成延迟|\< 3s（🔴级），\< 5s（🟠级），\< 10s（🟢级）|无 API key 场景，含 LLM 调用时 \+ 对应耗时|
|SSE 首帧时间|\< 500ms|所有演示类型通用|
|前端构建大小|\~232KB JS \+ \~19KB CSS（gzip: \~74KB \+ \~5KB）|新增 D3\.js 后控制在～300KB JS（gzip）|
|Streamlit 渲染耗时|\< 1s（ECharts/Pyvis），\< 2s（SQLFlow SVG）|前端交互无感知|
|数据库依赖|Docker 容器（MySQL 8 \+ PG 16）|事务演示需支持双会话隔离|
|Python 依赖|flask, flask\-cors, pymysql, psycopg2\-binary, python\-dotenv, openai, streamlit, streamlit\-echarts, pyvis, requests|新增 Streamlit 相关依赖|
|浏览器兼容性|Chrome ≥ 90, Firefox ≥ 88, Edge ≥ 90|适配 Mermaid/D3\.js 渲染|

---

## 9\. 落地路线图

|时间节点|核心交付内容|验收标准|
|---|---|---|
|本周内|🔴 第一级功能（Mermaid/ASCII 演示）|Agent 生成可直接复制的 Mermaid 代码，ASCII 分步动画，前端可渲染预览|
|第 3 周|🟠 第二级功能（ECharts/SQLFlow/Pyvis）|Streamlit 中渲染可视化图表 / SVG / 关系图，支持基础交互（缩放 / 点击）|
|第 5 周|🟢 第三级核心（分步 SQL 执行模拟器）|支持 SQL 分步执行，展示中间结果表，播放控制联动|
|第 7 周|🟢 第三级亮点（索引 / 事务演示器）|B \+ 树动画演示索引操作，双会话展示事务隔离级别现象|
|第 8 周|教学闭环能力|演示内容导出、课后练习生成、答案自动校验|

> （注：文档部分内容可能由 AI 生成）
