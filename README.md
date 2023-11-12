<div align="center">

<h1>pama-gpt <img src="./web/public/favicon.ico" height="35"></h1>
<p><em>WebSocket-Based Streaming GPT Conversation Application</em></p>
</div>

## 项目概述

这个项目是《网络协议设计与分析》课程的结课作业，旨在设计和实现一个简单的客户端-服务器系统，构建了一个基于自建GPT模型的实时对话应用，使用HTTP协议实现Restful API，通过WebSocket协议进行流式传输通信。

## 项目结构

说明项目的主要结构和模块划分，包括前端、后端、数据库等。

```
/
|-- web/
|   |-- public/
|   |   |-- favicon.ico
|   |   |-- index.html
|   |-- src/
|   |   |-- api/
|   |   |-- assets/
|   |   |-- components/
|   |   |-- router/
|   |   |-- utils/
|   |   |-- views/
|   |   |-- App.vue
|   |   |-- main.js
|   |-- package.json
|-- README.md
|-- api.py
|-- app.py
|-- config.py
|-- pama_gpt.sql
```

## 运行环境配置（此处为开发环境，生产环境建议使用WSGI服务器部署后端服务）

### Python版本及依赖项安装

使用Python版本为3.9.10

然后，安装依赖项，在项目根目录执行：

```
pip install -r requirements.txt
```

所有依赖项都将被正确安装。

### 数据库配置

确保系统中安装了 MySQL 数据库并启动了 MySQL 服务。使用数据库管理工具连接到数据库服务器。

1. 打开数据库管理工具，连接到数据库服务器。
2. 执行 `pama_gpt.sql` 文件，初始化数据库结构。
3. 在 `users` 表中插入登录 GPT 会话系统所需的用户名和密码（注意数据库中储存的是加密后的用户密码，加密逻辑在前端）。
4. 在`config.py`中配置数据库相关信息。

### 端口配置

在项目中，确保本地已搭建了梯子服务，并将其运行在本地的 `127.0.0.1:10810` 端口。在浏览器中设置代理服务器的 IP 地址为 `127.0.0.1`，端口为 `10810`。

### 启动后端服务

在项目根目录下运行后端服务：

```
python app.py
```

确保后端服务正常运行并监听指定端口。

### 前端依赖项的配置
所用`Node.js`的版本为`14.20.1`。
在项目的 `web` 目录下执行以下命令，根据 `package.json` 文件安装所有前端依赖项：

```
npm install
```

### 启动Vue服务

执行以下命令，启动 Vue 服务：

```
npm run serve
```

Vue 服务将在默认端口（通常是 `http://127.0.0.1:8080`）上启动，用户可以在浏览器中访问该地址查看前端页面。

通过以上步骤，完成了后端和前端环境的配置，确保系统在正确的数据库配置下正常运行。

## 主要技术栈

前端:

- Vue - 前端框架
- Vue Router - 处理前端路由与页面跳转
- Axios - 提供HTTP请求客户端,调用后端接口
- webpack - 项目构建工具,打包优化前端资源
- SCSS - CSS预处理器,简化样式的开发
- Swiper - 实现触屏滑块组件
- React Naive - 将网页打包成App

后端:

- Python 3.x
- SocketIO — WebSocket协议,全双工通信的协议
- 流式传输 - 以流的形式传输数据
- Flask - Python web框架
- SQLAlchemy - 对数据库进行对象映射
- MySQL - 关系型数据库
- Flask-JWT - 生成和验证JWT token,实现用户会话
- Poe API - 聊天机器人平台API


## 小组成员

- pama
- buta
