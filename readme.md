
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# source-to-oss-cdn 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=source-to-oss-cdn&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=source-to-oss-cdn" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=source-to-oss-cdn&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=source-to-oss-cdn" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=source-to-oss-cdn&type=packageDownload">
  </a>
</p>

<description>

定时抓取 URL 并同步到 OSS 同时刷新 CDN 缓存

</description>

<codeUrl>



</codeUrl>
<preview>



</preview>


## 前期准备

使用该项目，您需要有开通以下服务并拥有对应权限：

| 服务/业务 |  权限/策略          |
| --------- | ------------------ |
| 函数计算 FC| AliyunFCFullAccess |
| 对象存储 OSS | AliyunOSSFullAccess |
| 内容分发网络 CDN | AliyunCDNFullAccess |

<service>
</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=source-to-oss-cdn) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=source-to-oss-cdn) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init source-to-oss-cdn -d source-to-oss-cdn`
  - 进入项目，并进行项目部署：`cd source-to-oss-cdn && s deploy -y`
   
</deploy>

## 应用详情

<appdetail id="flushContent">

通过该项目，可以定时抓取 URL 并存储到 OSS 上，还可以设置 CDN 加速节点进行刷新和预热

### 初始化参数
| 参数名称       | 参数类型 | 是否必填 | 例子                                               | 参数含义                                                                                               |
| -------------- | -------- | -------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| functionName   | String   | 必填     | source-to-oss-cdn                                 | 函数名称                                                                                               |
| roleArn        | String   | 必填     | 'acs:ram::123456:role/aliyuncdnserverlessdevsrole' | 函数执行角色                                                                                           |
| sourceUrls         | String   | 必填     | http://example.com/abc.zip              | 源 URL，多个 URL 使用逗号分隔                                                                                               |
| targetDomain   | String   | 必填     | cdn-backup-bucket.oss-cn-beijing.aliyuncs.com      | OSS Bucket 域名                                                                         |
| cdnDomain   | String   | 必填     | yourcdndomain.com      | 回源到 OSS 的 CDN 域名                                                                                          |
| cronExpression | String   | 必填     | @every 60m        

</appdetail>

## 使用文档

<usedetail id="flushContent">
</usedetail>


<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>

<testEvent>
</testEvent>
