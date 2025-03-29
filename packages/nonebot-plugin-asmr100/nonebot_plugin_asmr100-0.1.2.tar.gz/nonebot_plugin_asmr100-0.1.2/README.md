# nonebot-plugin-asmr100

<div align="center">

一个基于 [NoneBot2](https://github.com/nonebot/nonebot2) 的插件，用于在QQ群中分享ASMR音声。

</div>

## 功能特点

- 🔍 通过关键词或标签搜索音声
- 📂 查看音声的详细信息和轨道列表
- 🎵 下载并分享单个音频文件
- 📦 将多个音频文件打包成加密ZIP文件分享
- 🔒 支持文件加密保护隐私
- 🔄 支持格式转换，优化文件大小
- 🛡️ 文件反和谐处理，避免内容审查 

## 安装

### 使用 pip

```bash
pip install nonebot-plugin-asmr100
```

### 使用 nb-cli

```bash
nb plugin install nonebot-plugin-asmr100
```

## 配置

在 NoneBot2 的 `.env` 文件中添加以下配置：

```dotenv
# ASMR插件配置
# 数据保存目录，默认为 data/asmr100
ASMR_DATA_DIR=data/asmr100
# ZIP文件密码，默认为 afu3355
ASMR_ZIP_PASSWORD=afu3355
# 最大错误尝试次数，默认为 3
ASMR_MAX_ERROR_COUNT=3
```

## 前置要求

1. 需要安装 [nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender) 以支持图片渲染
2. 可选：安装 `ffmpeg` 以支持音频格式转换
3. 可选：安装 `7z` 或 `zip` 命令行工具以支持高强度加密

## 使用方法

### 命令列表

- `搜音声 [关键词] [页数]` - 搜索音声，可用空格或"/"分割不同tag
- `搜索下一页` - 显示搜索结果的下一页
- `听音声 [RJ号] [选项]` - 下载并分享音声文件

### 选项说明

- 数字序号：下载并发送对应序号的单个音频文件
- 数字+zip：下载对应序号的音频文件并创建加密ZIP
- "全部"/"all"：下载所有音频文件并创建加密ZIP
- 字母序号：下载对应字母序号的文件夹并创建加密ZIP

### 示例

```
搜音声 伪娘 催眠 1
搜索下一页
听音声 RJ123456
听音声 RJ123456 2
听音声 RJ123456 2 zip
听音声 RJ123456 all
听音声 RJ123456 A
```

## 注意事项

- 文件大小受QQ群文件上传限制，过大的文件可能无法上传
- 为提高成功率，建议使用压缩方式发送文件
- 密码保护的ZIP文件需要使用密码解压
- 本插件仅供学习交流使用，请勿用于非法用途
- 请遵守相关法律法规，尊重版权

## 更新日志

### 0.1.0 (初始版本)

- 实现基本的搜索和下载功能
- 支持文件夹结构和文件列表显示
- 支持文件转换和压缩

## 开源协议

本项目采用 [MIT](./LICENSE) 许可证。

## 致谢

- [NoneBot2](https://github.com/nonebot/nonebot2)：优秀的聊天机器人框架
- [nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)：提供HTML渲染支持

## 作者

- 阿福 (主要开发者)

---

*本项目仅供技术研究使用，请勿用于任何违法违规用途*