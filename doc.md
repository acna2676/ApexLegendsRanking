## 機能要件

- ストック数でフィルタリング
- LGMT 数でフィルタリング
- 各月のランキングが閲覧できる（その月に作成された記事で）

## Todo

- リッチデザイン採用（bootstrap など）
- s3 and lambda で公開
- portfolio 連携
- 更新は週１でリクエストのたびに API を使用しないようにする（閲覧できるのは半年前まで）レートリミットは 500 リクエスト/月(RakutenRapidAPI 情報)
- 各記事の作成日、更新日表示
- ページ遷移が遅い
- POST の後 api なしのパスで css を読んで 403 エラーになるバグ修正

## ローカルテスト

- [DynamoDB Local 環境構築](https://hackers-high.com/aws/dynamodb-local-development/)
  dynamodb-admin で GUI 操作可能
  docker-compose コマンド一覧
  ```bash
  docker-compose up -d # コンテナ立ち上げ時
  docker-compose start
  docker-compose stop
  docker-compose down # コンテナ、ネットワーク情報削除される
  ```
  - [local table](http://localhost:8000)
  - [dynamodb-admin](http://localhost:8001)

## Tips

- [Flask アプリの Chalice 化](https://qiita.com/t-kigi/items/418908e290b54732968f)
  - [原著?](https://linuxtut.com/en/418908e290b54732968f/)
- [Flask アプリで作成したテンプレートをを Chalice で使えるようにする](https://medium.com/@tim_33529/creating-a-serverless-blog-with-chalice-bdc39b835f75)
- Winodws で Chalice がうまく動かないため Chalice を使用するプロジェクトは Mac で開発する
- [APIGateway にカスタムドメインを設定して Route53 をネームサーバーにする方法](https://www.beex-inc.com/blog/apigateway-using-custom-domain)
