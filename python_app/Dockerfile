# ベースイメージ:Python 3.9
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app/python_app

# 依存関係をインストール
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 必要なPythonスクリプトとテストファイルをコピー
COPY src/python_app.py ./src/
COPY src/modules/MongoDBClient.py ./src/modules/

# Pythonスクリプトを実行（本番環境用）
CMD [ "python", "src/python_app.py" ]

# デバッグ
# CMD [ "sleep", "infinity" ]
