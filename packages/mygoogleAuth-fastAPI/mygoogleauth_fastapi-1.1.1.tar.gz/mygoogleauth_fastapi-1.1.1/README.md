# mygoogleAuth_fastAPI

google認証をするためのライブラリです。

# 使い方

## Google認証用のIDとシークレットキーを環境変数に設定

- .env内に、以下のような環境変数を設定します。
```
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
```

- ライブラリ内のrouterをインポートし、FastAPIに登録します。
なお、google認証はhttpsである必要があるので、SessionMiddleware を使っています。
```
from mygoogleAuth_fastAPI.auth_router import router as rt
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key_here")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(rt)  # Google認証ルーターの登録
```

## 注意事項

- "data/mygoogleAuth_users.json" にユーザー情報を保存します。（dataフォルダがない場合は作成します。）
- エンドポイント `/login` `/logout` `/login/callback` が作られます。
- これらを修正したい場合は、auth_router.py を修正してください。

