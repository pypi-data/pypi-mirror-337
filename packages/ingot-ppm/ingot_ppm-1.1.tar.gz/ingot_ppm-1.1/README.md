# PPM - A faster and more comprehensive Python package manager

一个更快速、更全面的Python包管理器，默认使用清华PyPI镜像源。

**版本**: 1.1
**作者**: IngotStudio

## 特点

- 使用异步IO实现快速下载
- 默认使用清华PyPI镜像源
- 美观的进度条显示
- 简单直观的命令行接口
- 自动更新功能

## 安装

```bash
pip install ppm
```

### 配置镜像源

PPM默认使用清华PyPI镜像源，无需额外配置。如需手动配置，可使用以下命令：

```bash
ppm config set mirror https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用方法

### 安装包

```bash
# 安装最新版本
ppm add package_name

# 安装指定版本
ppm add package_name -v=1.0.0

# 安装开发依赖
ppm add package_name --dev

# 从requirements.txt安装
ppm add -r requirements.txt
```

### 包管理

```bash
# 列出已安装的包
ppm list

# 查看包信息（版本、作者、描述等）
ppm info package_name

# 卸载包
ppm remove package_name
```

### 更新

```bash
# 更新PPM和所有过期的包
ppm update
```

## 特色功能

- 自动检测并更新过期的包
- 智能版本管理
- 详细的包信息展示
- 安全的包卸载机制

## 开发

1. 克隆仓库
2. 安装依赖: `pip install -e .`
3. 运行测试: `pytest`

## 许可证

MIT