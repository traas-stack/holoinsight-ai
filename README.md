# Holoinsight AI
![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)
[![Github stars](https://img.shields.io/github/stars/traas-stack/holoinsight-ai?style=flat-square])](https://github.com/traas-stack/holoinsight-ai)
[![OpenIssue](https://img.shields.io/github/issues/traas-stack/holoinsight-ai)](https://github.com/traas-stack/holoinsight-ai/issues)

[中文](./README-CN.md)

Holoinsight AI provides real-time anomaly detection capabilities for time series data for [Holoinsight](https://github.com/traas-stack/holoinsight).

# Overview
The service utilizes a proprietary dynamic threshold generation model for anomaly detection, which is suitable for real-time anomaly detection of massive KPI data in Internet enterprises. 
The algorithm can adaptively extract time series cycle information and provide appropriate anomaly detection thresholds, effectively suppressing the occurrence of alarm storms while ensuring alarm recall.

# Documentation
* [HoloInsight AI Documentation](https://traas-stack.github.io/holoinsight-docs/dev-guide/internals/anomaly-detection-algorithm.html)

# Build
```bash
docker build -t holoinsight-ai:{version} .
```

# Install
### Docker Image
See [holoinsight/ai](https://hub.docker.com/r/holoinsight/ai)

# Licensing
Holoinsight AI is under [Apache License 2.0](https://github.com/traas-stack/holoinsight-ai/blob/main/LICENSE).