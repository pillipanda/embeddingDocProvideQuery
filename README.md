> 将全部文档转换为embedding并提供根据query查询相关文本块的接口

### 使用教程：
1. 将需要支持查询的文档（目前支持pdf、txt、markdown、csv格式）都放到static目录下(默认有几个文件在里面，如果只是试试可以直接使用，如果要用自己的文档，请删除之)
2. 安装依赖库：`pip install -r requirements.txt` (供参考：我使用的python版本为3.10.4)
3. 打开 `.env` 文件，输入你的 openai-api-key（此key仅用于首次embedding新文件时使用[openai的text-embedding-ada-002模型](https://openai.com/blog/new-and-improved-embedding-model)，后续查询/重启服务等其他操作均不需要使用/耗费。embedding模型的费用相当低 - $0.0004 / 1K tokens，目前是为了保证效果+考虑这个模型的费用很低故选择使用）
4. 启动网络服务器：`uvicorn api_server:app` （由于要访问openai服务，故注意可能需要科学上网）
5. 当看到输出 "👏 all paper get indexed, enjoy it now! 🔥"后代表所有文档已经完成索引，可以开始使用服务了

> 备注：如果想新增文档，先将新文档放到static目录下，然后按照步骤3重启下服务即可（会增量索引新文档）

### 检查服务是否正常
通过下面类似的访问（请替换对应的"query"字段为你想要的问题；amount字段为期望返回的
```shell
curl --location 'http://127.0.0.1:8000/get_query_about_papers' \
--header 'token: RfWrw0Yt4j' \
--header 'Content-Type: application/json' \
--data '{
    "content": "Core Data是用来做什么的?",
    "require_chunk_amount": 2
}'
```

返回：
```json
[
    {
        "file": "core_data.pdf-page 0",
        "paper": "Core Data 是⼀种在  Swift 和  iOS 应⽤程序之间⼴泛使⽤的持久化框架。它允许开发者将应⽤程序的数据模型 （对象）保存到本地持久存储中，如  SQLite 数据库，然后在需要时从本地加载该数据。 Core Data 可以处理许多应⽤程序所需的数 据管理任务，包括创建、读取、更新和删除数据记录。 在 Swift 编程中，通过操作托管对象上下⽂和⽤预先定义的数据模型创建托管对象实 例， Core Data 能帮助你 轻松管理应⽤程序的数据，并确保数据与本地存储保持同步。这意味着当⽤户退出应⽤程序时，他们之前的数 据和配置将得到保留，下次使⽤应⽤程序时会加载这些数据。 关联数据库的概念来看，  Core Data 的  Entity 與  Attribute ⼤約可以⽐對到  Table 和  Field Core Data 是⼀个完整的持久化框架，由多 个组件组成，这些组件⼀起协作来管理应⽤程序的数据模型。以下 是 Core Data 的主要组件： 1. Managed Object Model （托管对象模型） ：定义了数据模型中的实体、属性和关系，它是 Core Data 的核 ⼼部分。 2. Managed Object （托管对象）：是实体在 应⽤程序中的表示，开发⼈员可以通过 Managed Object 对实体 的属性和关系进⾏操作。 3. Managed Object Context （托管对象上下 ⽂）：管理托管对象的⽣命周期、状态变化以及持久化操作。 它是应⽤程序与数据存储器之间的桥梁。 4. Persistent Store Coordinator （持久化存储协调器）：管理应⽤程序的持久化存储，负责将托管对象的 数据存储在持久化存储器（通常是 SQLite 数据库）中。 5. Persistent Store （持久化存储器）：实际存储应⽤程序的数据的地⽅，它是⼀个底层 的数据存储器，通 常是⼀个 SQLite 数据库。 6. Fetch Request （获取请求）：⽤于检索托管对象的数据的查询对象，可以使⽤它来 执⾏复杂的数据查询 操作。 7. Fetched Results Controller （获取结果控制器）：将 Fetch Request 的结果转换为可供⽤户界⾯显示的数 据。C o r e  D a t a +---------------------+   |   Managed Object    |   +---------------------+             |             |             v   +---------------------+   |  Managed Object     |   |       Context       |   +---------------------+             |             |             v   +---------------------+  2 3 4 5 6 7 8 9 10 11 12 13 14 15"
    },
    {
        "file": "core_data.pdf-page 1",
        "paper": "在这个示意图中，箭头表示组件之间的关系 : 1. Managed Object 是托管对象模型中定义的实体在应⽤程序中的表示，它们由  Managed Object Context 进⾏管理和操作 2. Managed Object Context 是应⽤程序与数据存储器之间的桥梁，负责管理托管对象 的⽣命周期、状态变 化以及持久化操作 3. Persistent Store Coordinator 管理应⽤程 序的持久化存储，并负责将托管对象的数据存储在持久化存储 器中，通常是⼀个  SQLite 数据库 4. Persistent Store 是实际存储应⽤程序数据 的地⽅，它是⼀个底层的数据存储器 5. FetchRequest 是⽤于检索托管对象的数据的查询对象， Fetched Results Controller 将  Fetch Request 的结果转换为可供⽤户界⾯显示的数据 Q： NSPersistentContainer 是什么？ NSPersistentContainer 是  Core Data 中新增的⼀个类，它是⼀个⾼级别的对象，⽤于管理托管对象模型、托 管对象上下⽂和持久化存储器之间的关系。 NSPersistentContainer 简化了 Core Data 的配置和使⽤，它将多个组件封装在⼀个对象中，简化了  Core Data 的初始化过程。 使⽤ NSPersistentContainer ，开发⼈员⽆需⼿动配置托管对象模型、持久化存储器 和持久化存储协调器等组 件，它们都被⾃动创建和配置。 NSPersistentContainer 还提供了⽅便的 API ，使开发⼈员可以轻松地进⾏常 ⻅的数据操作，例如创建托管对象、查询数据、保存数据等。 NSPersistentContainer 还提供了多线程⽀持，使得多个线程可以同时访问 Core Data 的组件。它为每个线程 提供了⼀个独⽴的托管对象上下⽂，每个上下⽂都使⽤相同的持久化存储器和持久化存储协调器。这使得开发 ⼈员可以轻松地实现多线程数据操作，提⾼了应⽤程序的性能和响应速度。 总的来说， NSPersistentContainer 简化了  Core Data 的配置和使⽤，并提供了多线程⽀持，使得开发⼈员可 以更加⽅便地管理和操作应⽤程序的数据模型。 NS 前缀|Persistent Store     |   |     Coordinator     |   +---------------------+             |             |             v   +---------------------+   |  Persistent Store   |   +---------------------+  16 17 18 19 20 21 22 23"
    }
]
```
如果正常返回了，就表示服务没有问题了
