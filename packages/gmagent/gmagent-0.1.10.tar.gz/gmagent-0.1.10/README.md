# 掘金Agent Service API

一个同时提供 Function Calling API 和 MCP（模型上下文协议）接口的服务，用于与掘金交易 API 进行交互。该项目帮助投资者创建和管理他们的交易策略，同时通过现代 FastAPI 服务提供实用工具。

## 功能特性

- **市场数据**
  - 当前价格：获取任何交易标的的实时价格数据
  - 历史数据：访问日线和分钟级历史价格数据
  - 行业信息：获取行业分类、成分股和标的行业信息
- **交易工具**
  - 策略执行：运行自定义 Python 交易策略
  - 标的信息：获取交易标的的详细信息
  - 市场分类：访问市场行业分类
- **双重接口**
  - Function Calling API：为 Web 和应用程序客户端提供标准 HTTP 端点
  - MCP 服务器：为 AI 代理集成提供模型上下文协议服务器

## 架构

应用程序采用模块化架构：

1. **核心 API 层**：所有 API 功能的共享实现
2. **FastAPI 服务器**：为 Web 和应用程序客户端提供 REST API 服务器
3. **MCP 服务器**：为 Claude 等 AI 代理提供模型上下文协议服务器

您可以独立运行 FastAPI 服务器或 MCP 服务器，它们都使用相同的底层核心 API 实现。

## 安装

### 前提条件

- Python 3.10 或更高版本
- [uv](https://github.com/astral-sh/uv) 用于依赖管理

### 设置

1. 克隆仓库：
```bash
git clone <仓库地址>
cd gmagent
```

2. 创建并激活虚拟环境：
```bash
uv venv
source .venv/bin/activate  # Windows 上使用: .venv\Scripts\activate
```

3. 安装带依赖项的包：
```bash
uv pip install -e .
```

## 配置

在项目根目录创建一个 `.env` 文件，包含您的掘金 API 凭据：

```env
GM_TOKEN=your_gm_token
GM_SERV_ADDR=your_gm_server_address
```

可选环境变量：
```env
PROJECT_NAME=GM Trading Agent
API_V1_STR=/api/v1
```

## 使用方法

### 运行服务器

`gmagent` 命令行工具支持 FastAPI 和 MCP 服务器：

```bash
# 运行 FastAPI 服务器（默认）
gmagent

# 使用自定义主机/端口运行 FastAPI 服务器
gmagent --host 127.0.0.1 --port 9000

# 使用自动重载运行 FastAPI 服务器（用于开发）
gmagent --reload

# 运行 MCP 服务器
gmagent --server mcp
```

### REST API 端点

FastAPI 服务器提供以下端点：

#### 市场数据

```http
# 当前价格
GET /api/v1/current_price?symbol={symbol}

# 日线历史
GET /api/v1/daily_history?symbol={symbol}&start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}

# 分钟历史
GET /api/v1/minute_history?symbol={symbol}&start_time={YYYY-MM-DD HH:MM:SS}&end_time={YYYY-MM-DD HH:MM:SS}
```

#### 市场结构

```http
# 行业分类
GET /api/v1/sector/category?sector_type={sector_type}

# 行业成分股
GET /api/v1/sector/constituents?category_id={category_id}

# 标的行业
GET /api/v1/symbol/sector?symbol={symbol}&sector_type={sector_type}
```

#### 标的信息

```http
# 列出标的
GET /api/v1/symbols?sec_type1={type1}&sec_type2={type2}&exchanges={exchanges}&symbols={symbols}

# 标的详情
GET /api/v1/symbol_infos?symbols={symbol1,symbol2,...}
```

#### 策略执行

```http
# 运行策略
POST /api/v1/strategy/run
Content-Type: application/json

{
    "code": "your_python_code_here"
}
```

### MCP 工具

以 MCP 服务器运行时，AI 代理可以使用以下工具：

- `get_current_time()`：获取带时区信息的服务器时间
- `get_current_price(symbol)`：获取实时价格数据
- `get_daily_history(symbol, start_date, end_date)`：获取日线历史数据
- `get_minute_history(symbol, start_time, end_time)`：获取分钟级数据
- `get_sector_category(sector_type)`：获取行业分类
- `get_sector_constituents(category_id)`：获取行业成员
- `get_symbol_sector(symbol)`：获取标的的行业信息
- `get_symbols(sec_type1, ...)`：列出可用标的
- `get_symbol_infos(symbols)`：获取标的详细信息
- `run_strategy(code)`：执行交易策略

## 开发

### 项目结构

```
gmagent/
├── src/
│   └── gmagent/
│       ├── app/
│       │   ├── api/
│       │   │   └── core.py      # 核心 API 实现
│       │   ├── models/          # 数据模型
│       │   ├── services/        # 业务逻辑
│       │   ├── config.py        # 配置
│       │   ├── fastapi_server.py # FastAPI 实现
│       │   └── mcp_server.py    # MCP 服务器实现
│       └── __init__.py          # 入口点
├── tests/                       # 测试套件
├── docs/                        # 文档
│   ├── gmapi.md                # 掘金 API 文档
│   ├── 策略示例.md              # 策略示例文档
├── pyproject.toml              # 项目元数据和依赖
├── README.md                   # 本文件
└── .env                        # 环境配置
```

### 测试

运行测试套件：

```bash
uv run pytest
```

## API 文档

运行 FastAPI 服务器时，访问 `/docs` 或 `/redoc` 以访问交互式 API 文档。

## 开发

该项目遵循现代 Python 最佳实践：
- 所有函数和类的类型提示
- 全面的文档字符串
- FastAPI 最佳实践
- 错误处理和日志记录
- 为开发启用 CORS

## 与 Dify Cloud 测试

以 API 服务器方式运行以配合 Dify 使用。
- 使用 ngrok 进行 API 反向代理
- 导出 openapi schema 到 Dify 以集成自定义工具
- 添加缺失的 "server" 部分

## LLM 知识库

docs/gmapi.md    完整的掘金api定义
docs/策略示例.md  策略示例

## Cherry Studio

MCP 服务器支持

## 掘金策略Agent提示词

```
你是一名量化策略师，能熟练使用python与掘金sdk(gm.api)完成以下目标: 

1. 根据知识库回答用户查询类问题
2. 实现投研或交易逻辑片段
3. 编写完整的股票与期货策略
4. 根据需要调用掘金Agent MCP

为了避免幻觉，限定只能使用知识库中定义的掘金API（包括但不限于types, enum, event, data api, trade api etc.），示例策略，以及额外的pandas, numpy, ta-lib完成上述目标。

如果实现完整的策略，策略框架要严格遵循知识库中的策略模板示例(no class inheritance, directly call api or handle event）。

正确地填写回测参数，包括回测起止时间等。

标的格式采用: exchange.sec_id格式。例如SHSE.600000, CFFEX.IF2501

生成策略的两个参数固定名称作为占位符：your_strategy_id, your_token。

生成的策略代码，不用中文注释，避免编码问题。

对生成的最终代码，双重确认是否存在与知识库中API与策略示例定义不符的引用。

输出python策略代码时，要正确地格式化与语法高亮。

检查是否有能匹配的掘金MCP tools: 掘金Agent MCP，有则正确调用

```

## 掘金策略Agent文本测试集

```
测试集
=========

查询类（基于知识库）
--------

掘金有哪些下单函数

掘金有哪些两融相关函数

OrderType有哪些类型？要罗列完整

请详细解释order_target_volume的调用参数


查询类（基于MCP外部工具增强）
--------

当前系统什么时间？

当前系统什么时间？不查询工具

查询贵州茅台的最新股价

查询贵州茅台最近10日的股价，并用表格展示。

先查询当前系统时间，再根据系统时间查询贵州茅台最近10日的股价，并用表格展示。

查询今天最后20分钟的分钟数据。（需要推测收市截止时间）。

调用工具查询有哪些概念板块？

调用工具查询有哪些地域板块？

调用工具查询贵州茅台的标的信息(symbol info)


选股逻辑
--------

选股逻辑：最近60日，连续3日涨幅大于5%的股票，需要过滤停牌与ST的股票。


交易逻辑
--------

交易逻辑：5日线上传10日线，买入；5日线下穿10日线，卖出；

交易逻辑：实现一个典型的股票网格交易策略

更多用例，直接让LLM给出文本测试用例，再用掘金API实现为可以运行的策略。
```

## 贡献

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 运行测试
5. 提交拉取请求

## 许可证

[在此处添加您的许可证]

## 致谢

- [掘金 API](https://www.myquant.cn/) - 交易 API 提供商
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Web 框架
- [MCP](https://github.com/lhenault/mcp) - 模型上下文协议实现
