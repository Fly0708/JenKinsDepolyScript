# JenkinsDeployScript

**快速部署jenkins, 部署成功后弹框通知, 不分心于对jenkins的部署和关注**


## 环境

python : 3.10
依赖安装: pip install -r requirements.txt

## 使用

### 第一步: 配置

python main.py config -g : 生成空的配置文件
config.yml 配置示例

```yaml
server:
  token: '11c70e729edc570002ae3ce7c87d4'
  url: 'http://127.0.0.1:8858/job'
  username: 'developer'
deploy:
  my_folder:
    my_job_1:
      feature_branch_1:
        b1
    my_job_2:
      feature_branch_2:
        b2
```

### 第二步: 部署

python main.py -d b1 含义 部署my_folder下的my_job_1的feature_branch_1分支