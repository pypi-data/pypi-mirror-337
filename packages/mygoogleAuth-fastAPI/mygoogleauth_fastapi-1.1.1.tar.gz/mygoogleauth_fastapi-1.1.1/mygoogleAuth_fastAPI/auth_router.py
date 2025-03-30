# auth_routes.py
import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import logging
from .mygoogleAuth_fastAPI_core import mygoogleAuth_fastAPI_core

router = APIRouter()

# 変数の設定（必要に応じて設定を調整）
fn_userlist = "data/mygoogleAuth_users.json"

google_auth = mygoogleAuth_fastAPI_core(
    os.getenv('GOOGLE_CLIENT_ID'),
    os.getenv('GOOGLE_CLIENT_SECRET'),
    os.getenv('GOOGLE_DISCOVERY_URL'),
    'callback', 
    users_file=fn_userlist
)

logger = logging.getLogger(__name__)

@router.get("/login")
async def login(request: Request):
    callback_url = str(request.url_for("callback"))
    logger.info(f"/login エンドポイントにアクセス: callback_url={callback_url}")

    site_name = request.query_params.get("site_name", "")
    request.session["site_name"] = site_name
    print(f"[login] site_name: `{site_name}`")

    auth_url = google_auth.login(callback_url=callback_url)
    logger.info(f"Google認証URL生成: {auth_url}")

    return RedirectResponse(url=auth_url)

@router.get("/logout")
async def logout(request: Request):
    # セッションからユーザー情報を削除し、Google認証のログアウト処理を実行
    user_info = request.session.get('user')
    if user_info:
        google_auth.logout()
    request.session.clear()

    site_name = request.query_params.get("site_name", "/")
    print(f"[logout] site_name: `{site_name}`")
    return RedirectResponse(url=f"{site_name}")

@router.get("/login/callback")
async def callback(request: Request):
    logger.debug("/login/callback エンドポイントにアクセス")
    
    # クエリパラメータから認証コードを取得
    code = request.query_params.get("code")
    logger.debug(f"受信した認証コード: {code}")

    if not code:
        logger.error("認証コードが提供されていません。")
        raise HTTPException(status_code=400, detail="認証コードが提供されていません。")

    # 現在のURLおよびコールバックURLを取得
    current_url = str(request.url)
    callback_url = str(request.url_for("callback"))
    logger.debug(f"現在のURL: {current_url}")
    logger.debug(f"コールバックURL: {callback_url}")
    
    # Google OAuth2のコールバック処理を実行
    user, error = google_auth.callback(
        auth_type="google",
        code=code,
        current_url=current_url,
        callback_url=callback_url
    )
    
    if error:
        logger.error(f"Google認証エラー: {error}")
        raise HTTPException(status_code=400, detail=error)
    
    logger.info(f"ユーザーが正常に認証されました: ID={user.id}, Name={user.name}, Email={user.email}")

    # セッション管理のための処理
    request.session["user"] = {"id": user.id, "name": user.name, "email": user.email}
    logger.debug(f"セッションにユーザー情報を保存しました: {request.session['user']}")

    site_name = request.session["site_name"]
    print(f"[callback] site_name: {site_name}")
    return RedirectResponse(url=f"/{site_name}")
