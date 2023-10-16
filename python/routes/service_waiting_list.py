from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.index import ServiceWaitingList, SalesTarget
from schemas.index import ServiceWaitingListTargetRelateUserSchema, ServiceWaitingListSchema, TokenDataSchema
from config.index import get_db

from midlewares.index import get_current_bearer_token

service_waiting_list = APIRouter(
    prefix="/api/service-waiting",
    tags=["ServiceWaitingList"]
)

@service_waiting_list.get("/", response_model= List[ServiceWaitingListTargetRelateUserSchema])
async def read_all_users(
    db: Session = Depends(get_db),
    # get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """データベースから全てのユーザーを読み込む

    Args:
        db (Session):  使用するデータベースセッション

    Returns:
        List[ShowUserSchema]: 全ユーザのリスト

    Raises:
        HTTPException: データベースからユーザーを取得する際にエラーが発生した場合

    """
    services = db.query(ServiceWaitingList).all()
    return services

# 新しいservice_waiting_listへのPOSTリクエストを定義
@service_waiting_list.post("/", response_model= ServiceWaitingListTargetRelateUserSchema)
async def create_service_waiting(
        request: ServiceWaitingListSchema,
        db: Session = Depends(get_db),
        get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args:
        request (ServiceWaitingListSchema): サービス待機リストの新規作成のためのデータを含むリクエストオブジェクト。
        db (Session): SQLAlchemyのセッションオブジェクト。
        get_bearer_token (TokenDataSchema): ミドルウェアから取得したベアラトークンデータ。
    """
    # ユーザーIDを取得
    user_id = get_bearer_token.user_id

    # 企業IDに基づいてSalesTargetを検索
    sales_target = db.query(SalesTarget).filter(SalesTarget.id == request.company_id).first()

    # 該当のSalesTargetの所有者IDと認証ユーザーのIDが一致しない場合、HTTPExceptionを発生させる
    if sales_target.owners.id != int(user_id):
        print("heare")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'SalesTarget with the id {sales_target.owners.id} is not match'
        )

    # サービス待機リストモデルのインスタンスを作成
    waiting_list_model = ServiceWaitingList(
        summarize=request.summarize,
        is_selected=request.is_selected,
        company_id=request.company_id
    )

    # セッションにモデルを追加し、コミット
    db.add(waiting_list_model)
    db.commit()

    # セッションをリフレッシュ
    db.refresh(waiting_list_model)

    # 新しいサービス待機リストモデルを返す
    return waiting_list_model
