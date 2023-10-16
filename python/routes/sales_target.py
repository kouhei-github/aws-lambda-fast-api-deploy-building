from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.index import get_db
from schemas.index import SalesTargetSchema, SalesTargetRelateUserSchema, ShowUserSchema, TokenDataSchema
from models.index import SalesTarget
from midlewares.index import get_current_bearer_token

sales_target = APIRouter(
    prefix="/api/sales",
    tags=["Sales"]
)

@sales_target.get("/", response_model=List[SalesTargetRelateUserSchema], )
async def read_all_sales(
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args:
        db (Session): データベースへの問い合わせに使われる SQLAlchemy セッション
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        List[SalesTargetRelateUserSchema]: すべてのSalesTargetを表すSalesTargetRelateUserSchema オブジェクトのリスト。

    Raises:
        HTTPException: データベース接続に問題がある場合

    """
    users = db.query(SalesTarget).all()
    return users


@sales_target.get("/my-list", response_model=List[SalesTargetRelateUserSchema], status_code=status.HTTP_200_OK)
async def get_my_sales_list(db:Session = Depends(get_db), get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)):
    """
    1. API が sales_target ルーターの /my-list エンドポイントで GET HTTP リクエストを受信すると、この関数が呼び出されます。

    2. レスポンスは SalesTargetRelateUserSchema オブジェクトのリストで、デフォルトの HTTP ステータスコードは 200 (OK) です。

    3. 非同期関数 get_my_sales_list() は、/my-list エンドポイントで GET リクエストを受信したときの動作を定義します。この関数は、SQLAlchemy の Session (DB セッションを取得する Depends(get_db) によって提供されます) と、ベアラートークン (リクエストからベアラートークンを抽出する Depends(get_current_bearer_token) によって提供されます) に依存しています。

    4. 関数内部では、現在認証されているユーザーを示す user_id が get_bearer_token から取得され、その user_id に関連付けられた SalesTarget レコードを取得するためにデータベースへのクエリが実行されます。

    5. 一致するセールスターゲットが見つからなかった場合、HTTPステータスコード404(not found)のHTTPExceptionが発生し、指定されたユーザーIDを持つセールスターゲットが見つからないという詳細メッセージが表示されます。

    6. セールス・ターゲットが見つかった場合、APIコールのレスポンスとしてそのリストが返されます。このリストの項目は SalesTargetRelateUserSchema のシェイプに従わなければなりません。これは、ルート・デコレータの response_model プロパティが、これが期待されるレスポンス・フォーマットであることを示しているためです。ルートデコレーターでは、sales_target は APIRouter() のインスタンスでなければならないことを覚えておいてください。

    7. また、この関数は非同期(async defで定義)であることに留意してください。これは、Pythonのasyncioの機能を最大限に活用し、イベントループをブロックすることなく、IOバウンドタスク(データベースへのクエリのような)を処理するように設計されていることを意味します。
    Args:
        db (Session): データベースセッションオブジェクト。
        get_bearer_token (TokenDataSchema): トークンデータスキーマオブジェクト。

    Returns:
        List[SalesTargetRelateUserSchema]: ユーザーに関連するsales_targetのリスト。

    Raises:
        HTTPException: ユーザーのsales_targetが見つからない場合。
    """
    user_id = get_bearer_token.user_id
    sales_target = db.query(SalesTarget).filter(SalesTarget.user_id == user_id).all()
    if not sales_target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'SalesTarget with the id {SalesTarget.user_id} is not available'
        )
    return sales_target


@sales_target.get("/{id}", response_model=SalesTargetRelateUserSchema)
async def show_sales(
    id: int,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    指定されたIDに関連する情報を返します。

    Args:
        id (int): The ID of the sales target.
        db (Session): The database session to use.
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        SalesTargetRelateUserSchema:  指定されたIDに関連するSalesTarget情報

    Raises:
        HTTPException: 指定した IDが存在しない場合((status code 404).

    Example:
        >>> show_sales(1, db)
        SalesTargetRelateUserSchema(...)
    """
    sales_target = db.query(SalesTarget).filter(SalesTarget.id == id).first()
    if not sales_target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'SalesTarget with the id {id} is not available'
        )
    return sales_target


@sales_target.post("/", response_model=SalesTargetRelateUserSchema, status_code=status.HTTP_201_CREATED)
async def write_sales(
    request: SalesTargetSchema,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args:
        request (SalesTargetSchema): sTarget詳細を含むリクエストオブジェクト.
        db (Session): SQLAlchemy セッションオブジェクト
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        SalesTargetRelateUserSchema: 作成されたalesTarget

    Raises:
        HTTPException: リクエストまたはデータベース操作にエラーがある場合

    """
    new_sales_target = SalesTarget(
        company_name=request.company_name,
        email=request.email,
        phone=request.phone,
        url=request.url,
        user_id=request.user_id,
    )
    db.add(new_sales_target)
    db.commit()
    db.refresh(new_sales_target)
    return new_sales_target
