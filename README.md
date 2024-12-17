# DocParser

文档解析器，集成各种文档解析的服务，统一使用FastAPI服务，一秒部署使用，就是快

##### Layout_Analysis: 版面分析服务

##### Table_Parser: 表格解析服务

##### Formula_Server: 公式检测识别服务

## 快速部署

1. 拉取源代码：
    ```commandline
   git clone https://github.com/yuemengrui/DocParser.git
    ```
2. docker启动服务：
    ```commandline
    sudo docker compose -f docker-compose.yml up -d
    ```
3. 查看容器状态，正常的话所有容器应该是healthy状态
    ```commandline
    sudo docker compose -f docker-compose.yml ps -a
    ```
4. 访问各服务接口文档：
    ```text
    版面分析接口文档：/ai/docparser/layout/redoc
    表格解析接口文档：/ai/docparser/table/redoc
    公式识别接口文档：/ai/docparser/formula/redoc
    ```
5. docker compose 说明
   ```yaml
   volumes:
      - ./Layout_Analysis:/workspace/Layout_Analysis  # 挂载服务源码
      - ./Layout_Analysis/configs/model_layout_yolo.json:/workspace/model_config.json  # 挂载配置文件
      - ./Models/Layout/doclayout_yolo.pt:/workspace/models/doclayout_yolo.pt  # 挂载与配置文件对应的模型
   ```
   可通过不同的配置文件启动多个模型worker服务。假设我有三个版面分析模型，每个模型适用的场景数据不一样，可分别写好配置文件，挂载不同的配置文件来启动不同的版面分析模型来应对不同的场景，其他模型同理。

## 显存占用 (Batch_Size=1)

| 版面分析 | 表格解析 | 公式（检测+识别 |
|------|------|----------|
| 1G   | 5G   | 2.5G     |

## 效果展示

##### 版面分析
![](/assets/layout_1.jpg)
![](/assets/layout_2.jpg)
##### 表格解析
![](/assets/table_parser.png)
##### 公式检测与识别
![](/assets/formula_det_1.jpg)
![](/assets/formula_rec.jpg)

