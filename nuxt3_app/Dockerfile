FROM node:18.16.1

# 作業ディレクトリを設定
WORKDIR /app/nuxt3_app

# 依存関係ファイルをコピー
COPY package.json yarn.lock ./

# 依存関係をインストール
RUN yarn install

# アプリケーションのソースコードをコピー
COPY . .

# アプリケーションをビルド
RUN yarn build

# ポート3000を公開
EXPOSE 3000

# ビルドされたアプリケーションを起動
CMD ["yarn", "preview"]

# デバッグ
# CMD [ "sleep", "infinity" ]
