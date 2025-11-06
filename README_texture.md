# 数字人换装工具使用说明

## 功能说明

这个工具可以根据用户输入的服装描述，使用Gemini/Nano Banana API生成新的纹理图片，替换数字人的texture_00.png文件，实现换装效果。

## 安装依赖

```bash
pip install -r requirements.txt
```

或者单独安装：

```bash
pip install requests Pillow google-generativeai
```

## 配置API密钥

### 方式1：环境变量（推荐）

```bash
# 使用Gemini API
export GEMINI_API_KEY='your_gemini_api_key_here'

# 或使用Nano Banana API
export NANOBANANA_API_KEY='your_nanobanana_api_key_here'
```

### 方式2：在代码中设置

编辑 `generate_texture.py` 文件，在相应位置添加API密钥。

## 获取API密钥

### Gemini API
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建新的API密钥

### Nano Banana API
1. 访问 [Nano Banana官网](https://www.nanobananapic.org/zh)
2. 注册并获取API密钥

## 使用方法

### 基本使用

```bash
python generate_texture.py
```

### 交互式使用

运行脚本后：
1. 输入服装描述，例如：
   - "红色T恤"
   - "蓝色牛仔裤和白色运动鞋"
   - "粉色连衣裙"
2. 脚本会自动生成新纹理并替换原文件
3. 刷新浏览器查看效果
4. 如果效果不满意，输入 `restore` 恢复原始纹理
5. 输入 `quit` 退出

### 示例

```bash
$ python generate_texture.py
==================================================
数字人换装工具
==================================================

请输入服装描述（例如：红色T恤、蓝色牛仔裤、白色运动鞋）
或者输入 'restore' 恢复原始纹理
输入 'quit' 退出

> 红色T恤和蓝色牛仔裤
🔄 正在生成纹理图片...
提示词: 红色T恤和蓝色牛仔裤
✓ 新纹理已保存到: runtime/mark_free_t04.2048/texture_00.png

✓ 换装完成！请刷新浏览器查看效果
如果效果不满意，输入 'restore' 可以恢复原始纹理
```

## 注意事项

1. **备份功能**：脚本会自动备份原始纹理到 `texture_00_backup.png`
2. **恢复功能**：输入 `restore` 可以恢复原始纹理
3. **图片尺寸**：生成的图片会自动调整为2048x2048像素
4. **浏览器刷新**：替换纹理后需要刷新浏览器才能看到效果
5. **API限制**：请注意API的使用限制和费用

## 故障排除

### 问题：API请求失败

- 检查API密钥是否正确设置
- 检查网络连接
- 查看API服务状态

### 问题：生成的图片不符合预期

- 尝试更详细的描述
- 使用 `restore` 恢复原始纹理
- 调整提示词（可以在代码中修改 `enhanced_prompt`）

### 问题：导入错误

- 确保已安装所有依赖：`pip install -r requirements.txt`
- 检查Python版本（建议3.8+）

