# Kline-Filler-Server 文档

# 一、核心逻辑

1. 其他项目按照本地 kline 的发送异常存储数据（API or RabbitMQ）
2. kline-filler-server 根据本地逻辑，存入待请求数据（MySQL）。
3. celery 启动定时心跳调用数据库查询，获取缺失 kline 数据
4. 根据 kline 数据信息，一个交易所对应一个请求类，请求类对对应的交易所 API 请求数据
5. 数据根据本地存储规则，进行清晰，并存储入库（MongoDB）。

# 二、数据库设计

```SQL
CREATE TABLE `kline_exception` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `coin_pair` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `period` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `from_time` int(11) NOT NULL,
  `end_time` int(11) NOT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

![image-20191107150100269](/Users/lin/Documents/Kline-Filler-Server%20%E6%96%87%E6%A1%A3.assets/image-20191107150100269.png)

| 字段名    | 解释                              |
| --------- | --------------------------------- |
| exchange  | 本地存储可查询的交易所名（小写）  |
| coin_pair | 币对（大写）                      |
| peirod    | kline 周期，min/hour/day/week/mon |
| from_time | 请求开始时间（10位）              |
| end_time  | 请求结束时间（10位）              |
| status    | 该条数据是否补充完成（0 or 1）    |

# 三、组件使用总结

## 3-1 celery 使用

- 项目根目录下执行;
- -n 参数用于跟别名，用于防止 worker 同名

**celery worker 启动方式(mac)**

celery worker -A celery_worker.cel_app  -l info  -n worker0

**celery worker 启动方式(win)**

celery worker -A celery_worker.cel_app  -l info -P eventlet -n worker0

**celery beat 启动方式**

celery beat -A celery_worker.cel_app  -l info -s ./lib/celery_tasks/celery_log/beat

**一起启动 worker 和 beat,不适用于win**

celery -A celery_worker.cel_app worker -B -l info  -s ./lib/celery_tasks/celery_log/beat.log -n worker0

## 3-2 新交易所接入方式

1. 在 kline-filler/service 下新建 ExchangeName.py 
2. 编码针对交易所的接入规则类，**必须为 BaseKline 的子类**
3. 规则类必须**重写四个属性**：request_type/request_address/per_count/period_rule
4. 规则类必须**重写两个方法**：get_req_rule（返回请求字典）/kline_res_handle（返回 restful 数据）
5. 在 kline-filler/instance/kline_conf 中的 **KLINE_EXCHANGE_DISPATCH 字典内写入对应规则类**（key 为本地存储的交易所名）

## 3-3 MongoDB 数据存储注意点

- _id :int32 ，10位时间戳
- 其他参数 - double：open/high/low/close/vol
- 均最多保留八位小数
- 历史遗漏问题：所有交易所下的 kline-1min 线，存在 ts 字段，用于存储数据生成的 13 位时间戳（无意义，但需补充）

