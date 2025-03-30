import os
import json
import threading
import requests
from oauthlib.oauth2 import WebApplicationClient

class User_fastAPI:
    def __init__(self, auth_type, id_, name, email, profile_pic):
        self.auth_type = auth_type
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def to_dict(self):
        return {
            "auth_type": self.auth_type, 
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile_pic": self.profile_pic
        }

    @staticmethod
    def from_dict(data):
        return User_fastAPI(
            auth_type=data["auth_type"],
            id_=data["id"],
            name=data["name"],
            email=data["email"],
            profile_pic=data.get("profile_pic")
        )

class mygoogleAuth_fastAPI_core:

    auth_type = None

    def __init__(self, 
                 GOOGLE_CLIENT_ID    : str, 
                 GOOGLE_CLIENT_SECRET: str, 
                 GOOGLE_DISCOVERY_URL: str = 'https://accounts.google.com/.well-known/openid-configuration', 
                 endpoint_callback   : str = None, 
                 users_file          : str = None
    ):
        self.auth_type = None
        self.GOOGLE_CLIENT_ID     = GOOGLE_CLIENT_ID
        self.GOOGLE_CLIENT_SECRET = GOOGLE_CLIENT_SECRET
        self.GOOGLE_DISCOVERY_URL = GOOGLE_DISCOVERY_URL
        if not self.GOOGLE_CLIENT_ID or not self.GOOGLE_CLIENT_SECRET or not self.GOOGLE_DISCOVERY_URL:
            raise ValueError("環境変数が設定されていません。")
        
        # OAuth2クライアントのセットアップ
        self.client = WebApplicationClient(self.GOOGLE_CLIENT_ID)


        # ユーザー管理のためのJSONファイルパス
        self.users_file = users_file if users_file else 'mygoogleAuth_users.json'

        # ユーザー管理のためのロック
        self.lock = threading.Lock()

        # ユーザー情報をロード
        self.users = self.load_users()

        # Google Discoveryドキュメントをロード
        self.google_provider_cfg    = requests.get(self.GOOGLE_DISCOVERY_URL).json()
        self.authorization_endpoint = self.google_provider_cfg.get("authorization_endpoint")
        self.token_endpoint         = self.google_provider_cfg.get("token_endpoint")
        self.userinfo_endpoint      = self.google_provider_cfg.get("userinfo_endpoint")
        self.endpoint_callback      = endpoint_callback

        # LINE API設定
        self.LINE_LOGIN_URL         = "https://access.line.me/oauth2/v2.1/authorize"
        self.LINE_TOKEN_URL         = "https://api.line.me/oauth2/v2.1/token"
        self.LINE_PROFILE_URL       = "https://api.line.me/v2/profile"
        self.LINE_REDIRECT_URI      = None  # login_by_lineで設定する
        self.LINE_CLIENT_ID         = os.getenv('LINE_CLIENT_ID')
        self.LINE_CLIENT_SECRET     = os.getenv('LINE_CLIENT_SECRET')

    def load_users(self):
        """JSONファイルからユーザー情報をロード"""
        if not os.path.exists(self.users_file):
            return {}
        with self.lock:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    return {user_id: User_fastAPI.from_dict(info) for user_id, info in data.items()}
                except json.JSONDecodeError:
                    return {}

    def save_users(self):
        """ユーザー情報をJSONファイルに保存"""
        with self.lock:
            if not os.path.exists(os.path.dirname(self.users_file)):
                os.makedirs(os.path.dirname(self.users_file))
            with open(self.users_file, 'w', encoding='utf-8') as f:
                data = {user_id: user.to_dict() for user_id, user in self.users.items()}
                json.dump(data, f, ensure_ascii=False, indent=4)


    def login(self, callback_url: str):
        """Google認証開始URLを生成して返す（リダイレクトはFastAPI側で行う）"""
        self.auth_type = "google"
        print(f"Generated redirect URI: {callback_url}")
        request_uri = self.client.prepare_request_uri(
            self.authorization_endpoint,
            redirect_uri=callback_url,
            scope=["openid", "email", "profile"],
        )
        return request_uri

    def callback(self, auth_type: str, code: str, current_url: str, callback_url: str):
        """GoogleまたはLINEのコールバック処理。必要なパラメータはFastAPIのエンドポイントから渡すこと。"""
        if not code:
            return None, "認証コードが提供されていません。"

        self.auth_type = auth_type

        if self.auth_type == "google":
            # トークンリクエストの準備
            token_url, headers, body = self.client.prepare_token_request(
                self.token_endpoint,
                authorization_response=current_url,
                redirect_url=callback_url,
                code=code,
            )
            # トークンリクエストを送信
            token_response = requests.post(
                token_url,
                headers=headers,
                data=body,
                auth=(self.GOOGLE_CLIENT_ID, self.GOOGLE_CLIENT_SECRET),
            )
            # トークンを解析
            self.client.parse_request_body_response(token_response.text)
            # ユーザー情報を取得
            uri, headers, body = self.client.add_token(self.userinfo_endpoint)
            userinfo_response = requests.get(uri, headers=headers, data=body)
            userinfo = userinfo_response.json()
            # メールが確認されているかチェック
            if not userinfo.get("email_verified"):
                return None, "ユーザーのメールが利用できないか、Googleによって確認されていません。"

        elif self.auth_type == "LINE":
            # LINE用の処理
            token_data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.LINE_REDIRECT_URI,
                "client_id": self.LINE_CLIENT_ID,
                "client_secret": self.LINE_CLIENT_SECRET,
            }
            token_res = requests.post(self.LINE_TOKEN_URL, data=token_data)
            token_json = token_res.json()
            access_token = token_json.get("access_token")

            headers = {"Authorization": f"Bearer {access_token}"}
            profile_res = requests.get(self.LINE_PROFILE_URL, headers=headers)
            profile = profile_res.json()
            userinfo = {
                "sub"       : profile.get('userId'), 
                "name"      : profile.get('displayName', ''),
                "email"     : "NONE", 
                "picture"   : profile.get('pictureUrl', '')
            }
        else:
            return None, "不明な認証タイプです。"

        user = self.get_or_create_user(
            auth_type=self.auth_type,
            id_=userinfo["sub"],
            name=userinfo["name"],
            email=userinfo["email"],
            profile_pic=userinfo.get("picture") or userinfo.get("pictureUrl")
        )

        # FastAPI側でセッション管理を行うため、ここではユーザーを返すだけ
        return user, None

    def login_by_line(self, redirect_uri: str, state: str = "abcde"):
        """LINE認証開始URLを生成して返す"""
        self.auth_type = "LINE"
        self.LINE_REDIRECT_URI = redirect_uri
        line_auth_url = (
            f"{self.LINE_LOGIN_URL}?response_type=code"
            f"&client_id={self.LINE_CLIENT_ID}"
            f"&redirect_uri={self.LINE_REDIRECT_URI}"
            f"&state={state}"
            f"&scope=profile%20openid%20email"
        )
        return line_auth_url

    def get_or_create_user(self, auth_type, id_, name, email, profile_pic):
        """ユーザーを取得または新規作成"""
        user = self.users.get(id_)
        if not user:
            user = User_fastAPI(auth_type=auth_type, id_=id_, name=name, email=email, profile_pic=profile_pic)
            self.users[id_] = user
            self.save_users()
        return user

    def logout(self):
        # FastAPI側でセッション管理を行うため、このメソッドは空実装とするか必要に応じて調整
        self.auth_type = None

    def get_userid_byemail(self, email):
        for key, item in self.users.items():
            if item.email == email:
                return key
        return None

    def get_user(self, id_):
        return self.users.get(id_)
