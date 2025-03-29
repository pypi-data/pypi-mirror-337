# BigModel Hub

## 概述

本项目增强 ModelScope 命令行程序的功能，优化从 Hugging Face Hub 与 ModelScope Hub 下载新模型与查询、更新、删除已下载模型的体验。

## 模型存储

默认情况下，BigModel Hub 基于 Hugging Face Hub 或 ModelScope Hub 的缓存机制来存储模型，来获取最大的兼容性与空间利用率。

如果需要更改默认的缓存目录位置，参考 Hugging Face Hub 或 ModelScope Hub 的文档，设置环境变量 `HF_HUB_CACHE` 或 `MODELSCOPE_CACHE` 来修改缓存目录位置。

如果不依赖 Hugging Face Hub 或 ModelScope Hub 的缓存机制，需要手动指定本地模型存储目录，且遵循如下目录结构：

```
|- <Local Models Directory>
   |- <Organization ID>
      |- <Model ID>
      |- ...
   |- ...
```

本地模型存储目录结构示例：

```
|- <Local Models Directory>
   |- Qwen
      |- Qwen2.5-7B-Instruct
         |- config.json
         |- ...
```

## 安装

### 本地安装

```bash
pip install bigmodel-hub
```

测试 BigModel Hub CLI 可用性。

```bash
bmhub --help
```

如果访问 Hugging Face 困难，设置环境变量 `HF_ENDPOINT` 。

```bash
HF_ENDPOINT=https://hf-mirror.com bmhub --help
```

### Docker 安装

本项目提供官方 Docker 镜像，提供本地安装的所有 CLI 功能，CLI 命令与选项均与本地安装一致。

拉取 Docker 镜像到本地。

```bash
docker pull yansh97/bigmodel-hub
```

测试 BigModel Hub CLI 可用性。

```bash
docker run --rm yansh97/bigmodel-hub --help
```

如果访问 Hugging Face 困难，设置环境变量 `HF_ENDPOINT` 。

```bash
docker run --rm -e HF_ENDPOINT=https://hf-mirror.com yansh97/bigmodel-hub --help
```

如果使用 Hugging Face Hub 的缓存机制，挂载 Hugging Face Hub 缓存目录到容器。

```bash
docker run --rm -v ~/.cache/huggingface:/root/.cache/huggingface yansh97/bigmodel-hub --help
```

如果使用 ModelScope Hub 的缓存机制，挂载 ModelScope Hub 缓存目录到容器。

```bash
docker run --rm -v ~/.cache/modelscope:/root/.cache/modelscope yansh97/bigmodel-hub --help
```

如果使用本地模型存储目录，挂载本地模型存储目录到容器。

```bash
docker run --rm -v <host-local-dir>:<container-local-dir> yansh97/bigmodel-hub --help
```

## CLI 功能

[CLI 文档](CLI.md)

### 列出模型

列出已下载的模型，可以通过模型 ID 的 Glob 模式过滤，并查看模型占用存储空间等信息。

默认在 Hugging Face Hub 或 ModelScope Hub 缓存目录中检索已下载的模型。如果指定参数 `--local-dir`，则在本地模型存储目录中检索已下载的模型。

```bash
bmhub list --help
```

[CLI 文档](CLI.md#bmhub-list)

### 下载模型

下载指定 ID 的模型，如果已下载过模型，则会更新该模型。

默认下载到 Hugging Face Hub 或 ModelScope Hub 缓存目录。如果指定参数 `--local-dir`，则下载到本地模型存储目录。

```bash
bmhub download --help
```

[CLI 文档](CLI.md#bmhub-download)

### 更新模型

更新已下载的模型，可以通过模型 ID 的 Glob 模式过滤。

默认在 Hugging Face Hub 或 ModelScope Hub 缓存目录中更新已下载的模型。如果指定参数 `--local-dir`，则在本地模型存储目录中更新已下载的模型。

```bash
bmhub update --help
```

[CLI 文档](CLI.md#bmhub-update)

### 删除模型

删除已下载的模型，可以通过模型 ID 的 Glob 模式过滤。

默认在 Hugging Face Hub 或 ModelScope Hub 缓存目录中删除已下载的模型。如果指定参数 `--local-dir`，则在本地模型存储目录中删除已下载的模型。

```bash
bmhub remove --help
```

[CLI 文档](CLI.md#bmhub-remove)
