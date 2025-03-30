# mcp server入门开发


初始化项目
```
uv init mcp_getting_started
```

初始化虚拟环境
```
uv venv
```
安装依赖
```
uv add "mcp[cli]" httpx openai
```

项目打包发布：
```
python -m build
```