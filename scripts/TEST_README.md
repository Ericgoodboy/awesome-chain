# run_cspm_file.sh 功能验证测试

## 概述
`run_cspm_file.sh` 是一个用于运行CSPM（云安全态势管理）Python脚本的bash脚本，提供环境管理、依赖安装和错误处理功能。

## 已验证的功能

### 1. 环境变量加载 ✅
- 从项目根目录加载 `.env` 文件
- 支持多行环境变量（简单实现）
- 跳过注释和空行
- 示例 `.env` 文件：
  ```bash
  OPENAI_API_KEY=sk-test1234567890abcdef
  ANTHROPIC_API_KEY=sk-ant-test1234567890
  AZURE_SUBSCRIPTION_ID=00000000-0000-0000-0000-000000000000
  ```

### 2. 虚拟环境管理 ✅
- 自动检测并激活虚拟环境（支持Windows和Linux/Mac）
- 检查Python是否在虚拟环境中可用
- 如果没有虚拟环境，提供清晰的错误信息

### 3. 依赖安装 ✅
- 从多个位置查找依赖文件（优先级）：
  1. 当前目录的 `requirement.txt`
  2. scripts目录的 `requirement.txt`
  3. 项目根目录的 `requirements.txt`
  4. 项目根目录的 `requirement.txt`
- 使用清华大学PyPI镜像加速安装：`https://pypi.tuna.tsinghua.edu.cn/simple`
- 自动升级pip

### 4. Python脚本执行 ✅
- 支持相对路径和绝对路径
- 传递所有参数给Python脚本
- 显示执行的完整命令
- 捕获并显示脚本退出代码

### 5. 错误处理 ✅
- 脚本不存在：`[ERROR] Python script not found: ...`
- 虚拟环境不存在：`[ERROR] Virtual environment not found at ...`
- Python不可用：`[ERROR] Python not found in virtual environment`
- 脚本执行失败：显示Python错误信息和退出代码

## 测试脚本

已创建测试脚本 `demo_cspm.py` 验证以下功能：

### 脚本功能
1. **系统信息显示**：Python版本、平台、工作目录
2. **虚拟环境检测**：检查是否在虚拟环境中运行
3. **环境变量验证**：显示加载的环境变量（敏感信息脱敏）
4. **命令行参数处理**：显示所有传递的参数
5. **模拟CSPM检查**：显示模拟的安全检查结果
6. **依赖检查**：检查常见云安全包是否安装
7. **报告生成**：生成JSON格式的报告
8. **文件输出**：支持 `--output <filename>` 参数保存报告

### 使用示例

```bash
# 基本用法
bash scripts/run_cspm_file.sh scripts/demo_cspm.py

# 带参数
bash scripts/run_cspm_file.sh scripts/demo_cspm.py --test "hello" --verbose

# 保存报告
bash scripts/run_cspm_file.sh scripts/demo_cspm.py --output report.json

# 错误测试（脚本不存在）
bash scripts/run_cspm_file.sh nonexistent.py

# 错误测试（无虚拟环境）
mv .venv .venv.backup
bash scripts/run_cspm_file.sh scripts/demo_cspm.py
mv .venv.backup .venv
```

## 输出示例

### 成功执行
```
[INFO] Project root: /d/workspace/awesome-chain
[INFO] Python script: scripts/demo_cspm.py
[INFO] Loading environment variables from /d/workspace/awesome-chain/.env
[INFO]   Set OPENAI_API_KEY
[INFO] Activating virtual environment: /d/workspace/awesome-chain/.venv/Scripts/activate
[INFO] Using Python 3.14.3
[INFO] Found requirement.txt in scripts directory
[INFO] Installing dependencies...
[INFO] Running Python script: scripts/demo_cspm.py
[INFO] Executing: python "./scripts/demo_cspm.py"
========================================================================
[Python脚本输出...]
========================================================================
[INFO] Script completed successfully
```

### 错误情况
```
[ERROR] Python script not found: nonexistent.py
[ERROR] Virtual environment not found at /d/workspace/awesome-chain/.venv
[ERROR] Please create it with: python -m venv .venv
```

## 注意事项

1. **Windows兼容性**：脚本检测Windows的 `Scripts/activate` 和Linux/Mac的 `bin/activate`
2. **编码问题**：Windows控制台可能不支持Unicode字符，测试脚本使用ASCII字符
3. **依赖安装**：使用清华镜像可能在某些网络环境下更快，但如果有私有仓库需调整
4. **环境变量**：简单的 `key=value` 格式解析，不支持多行值或引号

## 改进建议

1. 添加 `--help` 参数显示使用说明
2. 支持自定义虚拟环境路径
3. 添加 `--skip-deps` 跳过依赖安装
4. 支持 `.env.local` 等环境特定文件
5. 添加更详细日志级别控制

## 结论

`run_cspm_file.sh` 脚本功能完整，能够：
- 正确处理环境设置
- 管理Python依赖
- 执行脚本并传递参数
- 提供清晰的错误信息

适合用于自动化运行CSPM和安全检查脚本。