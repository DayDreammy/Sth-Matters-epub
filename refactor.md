我们将策略调整为 **“AI 负责生产数据（JSON），Python 负责消费数据（生成文档）”**。

以下是分步落地的具体方案：

### 第一步：精简并重构 SOP (`ai_prompt.md`)

我们将原有的 Prompt 剥离掉所有“文档生成命令”和“项目介绍废话”，只保留 **搜索** 和 **整合** 的核心逻辑。

**新的 `config/ai_prompt.md` 建议如下：**

````markdown
# Deep Search Agent SOP

## Role
You are an expert researcher. Your goal is to analyze the local knowledge base and produce a structured **Knowledge Index JSON**.

## Workflow

### Phase 1: Exploration (Iterative Search)
1.  **Analyze Request**: Identify key concepts from the user's topic.
2.  **Broad Search**: Use your tools `Search` to find relevant files in `knowledge_base/`
    * Look for filenames matching the topic.
    * Search for tags or keywords inside files.
3.  **Deep Dive**: Read the content of the most relevant files.
    * Identify related concepts and expand your search if necessary (Multi-hop reasoning).
    * **Constraint**: Do not read more than 10 files to avoid context overflow. Select the highest quality ones.

### Phase 2: Synthesis (Data Construction)
Construct a JSON object containing the synthesized knowledge. The structure must be:
```json
{
  "metadata": { "topic": "...", "timestamp": "..." },
  "sources": [
    { "title": "...", "path": "...", "summary": "...", "relevance_score": 0-10 }
  ],
  "content_synthesis": {
    "key_concepts": ["..."],
    "summary_text": "...",
    "relationships": ["..."]
  }
}
````

### Phase 3: Handoff (Crucial)

1.  **Save File**: Save the JSON content to `output/[topic]_index.json`.

2.  **Get Absolute Path**: Determine the absolute path of this saved file.

3.  **Signal Completion**:

      * **DO NOT** run any Python generation scripts (like `md_generator.py`).
      * **DO NOT** output conversational filler after the final signal.
      * **FINAL ACTION**: Print the absolute path of the JSON file on the very last line, wrapped in triple brackets.

    Example:
    `[[[ /Users/username/project/output/search_topic_index.json ]]]`

<!-- end list -->

````

---

### 第二步：定义清晰的输入输出协议

为了让 Python 代码能准确接住 AI 的球，我们需要定义严格的“协议”：

1.  **输入 (Python -> Claude Code)**:
    * 不再只传 topic。
    * 命令：`claude "Please research [TOPIC] following instructions in config/ai_prompt.md"`
    * 这里利用 Claude Code 自身读取本地文件的能力，让它自己去读 SOP，而不是把 SOP 拼接到命令行参数里（防止参数过长）。

2.  **输出 (Claude Code -> Python)**:
    * **文件产物**：硬盘上的 `output/xxx.json`。
    * **控制信号**：标准输出（stdout）的最后一行 `[[[ /abs/path/to/json ]]]`。

---

### 第三步：Python 侧的“接力”逻辑

Python 代码（`rpa.py` 或 `main.py`）现在只需要做三件事：**启动 AI -> 捕获路径 -> 执行生成**。

以下是伪代码逻辑，展示了如何配合上面的 SOP：

```python
import subprocess
import re
import os

def run_deep_search_workflow(topic: str):
    print(f"--- 启动深度搜索 Agent: {topic} ---")
    
    # 1. 构造给 Claude Code 的指令
    # 让 Claude 自己去读取 SOP 文件，减少命令行参数复杂度
    prompt_command = (
        f"Read config/ai_prompt.md and perform the Deep Search for topic: '{topic}'. "
        "Focus on Phase 1 and 2. Stop after Phase 3. "
        "Remember to output the absolute path in brackets."
    )
    
    # 2. 调用 Claude Code (这是一个阻塞操作，等待 AI 思考和搜索)
    # 假设 'claude' 命令已在环境变量中
    process = subprocess.Popen(
        ["claude", prompt_command], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate()
    
    # 3. 解析 AI 的输出，寻找“接力棒”（JSON路径）
    # 正则匹配 [[[ /path/to/file ]]]
    match = re.search(r"\[\[\[\s*(.*?)\s*\]\]\]", stdout)
    
    if not match:
        print("错误：AI 未能返回有效的索引文件路径。")
        print("AI Output:", stdout) # 调试用
        return
        
    json_path = match.group(1)
    
    if not os.path.exists(json_path):
        print(f"错误：路径 {json_path} 不存在。")
        return
        
    print(f"--- AI 搜索完成，索引文件位于: {json_path} ---")
    print("--- 开始生成文档 (Python Execution) ---")
    
    # 4. 确定性执行：Python 拿到数据，自己调用生成器
    # 这里不再依赖 AI 去敲命令，而是我们自己敲
    try:
        # 调用 MD 生成器
        subprocess.run([
            "python", "src/document_generator/md_generator.py",
            "-i", json_path,
            "-o", "output",
            "-k", "knowledge_base"
        ], check=True)
        
        # 调用 EPUB 生成器
        subprocess.run([
            "python", "src/document_generator/epub_cli.py",
            "-i", json_path,
            "-o", "output"
        ], check=True)
        
        print("--- 所有文档生成完毕 ---")
        
    except subprocess.CalledProcessError as e:
        print(f"文档生成脚本执行失败: {e}")

````

### 这种改进的好处

1.  **发挥 Claude Code 强项**：文件系统浏览、内容读取、多轮思考（"我搜到了A，觉得还要搜B"）这些逻辑完全保留在 Claude Code 内部，我们不需要写复杂的 `While` 循环。
2.  **规避 Claude Code 弱项**：不再让 AI 去运行 Python 脚本。避免了 AI 搞错参数、环境配置不对、或者 CLI 交互卡死的问题。
3.  **调试方便**：
      * 如果搜索结果不好，只改 Prompt。
      * 如果文档排版不好，只改 Python 生成器代码。
      * 两边解耦，中间通过一个干净的 JSON 文件连接。

