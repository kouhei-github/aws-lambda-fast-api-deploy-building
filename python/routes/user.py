from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.index import User
from schemas.index import UserSchema, ShowUserSchema, TokenDataSchema
from config.index import get_db
from services.hashing import Hash
from midlewares.index import get_current_bearer_token

user = APIRouter(
    prefix="/api/user",
    tags=["Users"]
)

@user.get("/", response_model= List[ShowUserSchema])
async def read_all_users(
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """データベースから全てのユーザーを読み込む

    Args:
        db (Session):  使用するデータベースセッション

    Returns:
        List[ShowUserSchema]: 全ユーザのリスト

    Raises:
        HTTPException: データベースからユーザーを取得する際にエラーが発生した場合

    """
    users = db.query(User).all()
    return users

@user.get("/{id}", response_model=ShowUserSchema)
async def show_user(
    id: int,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    ユーザーを表示

    データベースから特定のユーザーを取得する

    Args:
        id (int):  取得するユーザーのID
        db (Session): データベースセッション
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        ShowUserSchema: 取得したユーザー

    Raises:
        HTTPException:  指定した ID のユーザがデータベースに存在しない場合
    """
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    return user

@user.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUserSchema)
async def write_user(
    request: UserSchema,
    db: Session = Depends(get_db),
):
    """
    このFastAPIメソッドは新しいユーザーをシステムに作成、または「書き込む」ためのものです。
    コードを詳しく見てみましょう：
    ・インポート：このスクリプトではFastAPI, SQLAlchemy, 独自のスキーマとモデル, パスワードハッシングサービスなどから重要なクラスと関数をインポートしています。
    ・@user.post(...)デコレータ：このデコレータは関数 write_user がパス "/api/user" 上でのPOSTリクエストエンドポイントであることを示しています。 また、デコレータは成功時のHTTPステータスコード (201 はリソースが作成されたことを示す) とレスポンスのモデル (ShowUserSchema) を指定しています。 "tags" 属性はFastAPIの自動ドキュメンテーションでルートをグループ化するために使用されます。
    ・write_user関数：この非同期関数は新しいユーザーを作成します。request（タイプはUserSchema）とdb（タイプはSession）の2つの引数を取ります。dbは依存性注入を使用しています。つまり、Depends(get_db)を使用してSQLAlchemy の現在のセッションを取得しています。
    ・パスワードハッシング：新しいHashオブジェクトが作成され、ストレージ前にユーザーのパスワードをハッシュ化します。これは良いセキュリティ習慣で、データベースが侵害された場合でも、攻撃者がプレーンテキストのパスワードを持つことはありません。
    ・ユーザー作成：リクエストからメール、名前、（ハッシュ化された）パスワードを取り出し、新しいUserオブジェクトを作成し、新しいユーザーをデータベースの現在のセッションに追加します。
    ・DBコミットとリフレッシュ：変更をコミット（保存）し、データベースからの任意の更新（新しいユーザーのIDなど、データベースによる自動インクリメントがある場合）を取得するためにセッションをリフレッシュします。
    ・戻り値：new_userオブジェクトを返します。これは自動的にJSONに変換され、デコレータで指定されたモデル（ShowUserSchema）を使って行われます。
    ・このメソッドは、リクエストボディがJSONフォーマットで送信され、それがUserSchemaによって定義されたスキーマに一致すると想定しています。
    Args:
        request (UserSchema): The incoming request containing user information.
        db (Session): The database session.
        get_bearer_token (TokenDataSchema): The current bearer token.

    """
    hashing = Hash()
    new_user = User(
        email=request.email,
        name=request.name,
        password=hashing.bcript(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(
    id: int,
    request: UserSchema,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args:
        id (int): The ID of the user to be updated.
        request (UserSchema): The updated user data.
        db (Session): The SQLAlchemy session.
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        dict: A dictionary with the message "update completed"

    Raises:
        HTTPException: If the user with the specified ID is not found in the database.

    """
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    hashing = Hash()
    request.password = hashing.bcript(request.password)
    user.update(request.dict())
    db.commit()
    return {"msg": "update completed"}

@user.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args:
        id (int): The ID of the user to be deleted.
        db (Session): The database session.
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        dict: A dictionary with the message "delete completed".

    Raises:
        HTTPException: If a user with the specified ID is not found.

    """
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"msg": "delete completed"}

