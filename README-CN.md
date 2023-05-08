# Holoinsight AI
![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)
[![Github stars](https://img.shields.io/github/stars/traas-stack/holoinsight-ai?style=flat-square])](https://github.com/traas-stack/holoinsight-ai)
[![OpenIssue](https://img.shields.io/github/issues/traas-stack/holoinsight-ai)](https://github.com/traas-stack/holoinsight-ai/issues)

[English](./README.md)  

Holoinsight AI为[Holoinsight](https://github.com/traas-stack/holoinsight) 提供时序数据实时异常检测功能

#概述
本项目提供了一种针对时间序列的异常检测服务，适用于互联网企业海量KPI指标的实时异常检测。
采用特有的动态阈值生成技术，能够自适应地提取时间序列周期信息，并给出准确的告警阈值，在保证故障召回率的前提下能够有效抑制告警风暴的产生。

# 文档
* [HoloInsight AI 文档](https://traas-stack.github.io/holoinsight-docs/dev-guide/internals/anomaly-detection-algorithm.html)

# 构建
```bash
docker build -t holoinsight-ai:{version} .
```

# 安装
### Docker 镜像
[holoinsight/ai](https://hub.docker.com/r/holoinsight/ai)

# 开源许可
Holoinsight AI 基于 [Apache License 2.0](https://github.com/traas-stack/holoinsight/blob/main/LICENSE) 协议。
