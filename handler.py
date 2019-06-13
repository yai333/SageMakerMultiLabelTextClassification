try:
  import unzip_requirements
except ImportError:
  pass

import json
import os
import boto3
import string
import re

runtime= boto3.client('runtime.sagemaker')
SAGEMAKER_ENDPOINT_NAME = os.environ['SAGEMAKER_ENDPOINT_NAME']

def generateTag(event, context):
    sentence=[]
    data = json.loads(event['body'])
    raw_sentence = data["sentence"]
    sentence.append(clean_text(raw_sentence))

    try:
        payload = {"instances" : sentence,"configuration": {"k":3}}

        response = runtime.invoke_endpoint(EndpointName=SAGEMAKER_ENDPOINT_NAME,
                                            ContentType='application/json',
                                            Body=json.dumps(payload))

        result = json.loads(response['Body'].read().decode())
        preb = []
        labels = []
        for label in result[0]['label']:
            labels.append(label[9:])
        return {'statusCode': 200, 'body': json.dumps(labels)}
    except Exception as e:
        print(e)
        return {'statusCode': 400,
                'body': json.dumps({'error_message': 'Unable to generate tag.'})}


def clean_text(text):
    if not isinstance(text, str):
        return text
    def cleanhtml(raw_html):
        cleanr = re.compile('<[^>]+>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    def replace_link(match):
        return '' if re.match('[a-z]+://', match.group(1)) else match.group(1)
    def removeContractions(raw_text):
        CONTRACTIONS = {"mayn't":"may not", "may've":"may have","isn't":"is not","wasn't":"was not","'ll":" will","'have": "have"}
        raw_text = raw_text.replace("’","'")
        words = raw_text.split()
        reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
        raw_text = " ".join(reformed)
        return raw_text
    text = cleanhtml(text)
    text = re.sub('<pre><code>.*?</code></pre>', '', text)
    text = re.sub('<a[^>]+>(.*)</a>', replace_link, text)
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", text).split())
    text = ' '.join(re.sub("[\.\,\(\)\{\}\[\]\`\'\!\?\:\;\-\=]", " ", text).split())
    return text
