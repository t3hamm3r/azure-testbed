import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

from langchain_openai import AzureOpenAI

app = Flask(__name__)
azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
azure_deployment = os.environ['AZURE_OPENAI_DEPLOYMENT_NAME']
model_name = os.environ['OPENAI_MODEL_NAME']
api_version = os.environ['AZURE_OPENAI_API_VERSION']
api_key = os.environ['OPENAI_API_KEY']

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   req = request.form.get('req')

   llm = AzureChatOpenAI(
       api_key=api_key,
       api_version=api_version,
       azure_deployment=azure_deployment,
       model_name=model_name,
   )
   text = llm.invoke(req).content

   if req:
       print('Request for hello page received with req=%s' % req)
       return render_template('hello.html', req=text)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()
