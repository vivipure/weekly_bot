# 科技爱好者周刊 bot

使用 OpenAI 的 embeddings API 生成 科技爱好者周刊的内容模型

数据来源：【科技爱好者周刊】(https://github.com/ruanyf/weekly)

教程地址： https://platform.openai.com/docs/tutorials/web-qa-embeddings

##  安装依赖
```
python3 -m venv env

source env/bin/activate

pip install -r requirements.txt
```

## 运行项目

配置 `config.py` 文件中的 token, 如果无法访问，请配置可以访问 api 的代理

```py
python app.py
```


## creadit

- 【科技爱好者周刊】(https://github.com/ruanyf/weekly)