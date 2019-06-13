# Auto-Generating Tags for Content using Amazon SageMaker BlazingText with fastText

Multi label text classification using the fastText with SageMaker BlazingText.
Model is trained on the public dataset of [10% of Stack Overflow Q&A dataset](https://medium.com/r/?url=https%3A%2F%2Fwww.kaggle.com%2Fstackoverflow%2Fstacksample).

## SageMaker Jupyter notebook

- fastTextClassification.ipynb

## Install node dependencies

```
npm Install
```

## Deploy Serverless Api gateway

```
sls deploys
```

## Invoke SageMaker endpoint

```
curl -d '{"img_url":"https://image-url.jpg"}' -H "Content-Type: application/json" -X POST https://api_gatewat_endpoint
```
