import boto3, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.index import LoginSchema, SendResetPasswordUrlData, ResetPasswordData, UserOut, UserAuth
from config.index import get_db
from models.index import User, SalesTarget
from services.hashing import Hash
from services.jwt_token import create_access_token, verify_password_reset_token, verify_password, create_refresh_token, get_hashed_password
from schemas.index import TokenSchema
from uuid import uuid4

auth = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

@auth.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db.query(User).filter(User.email == data.email).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = get_hashed_password(data.password)
    db.add(user)
    db.commit()
    return True

@auth.post("/login", status_code=status.HTTP_201_CREATED, response_model=TokenSchema)
async def login(request: LoginSchema, db: Session = Depends(get_db)):
    """
    引数:
        request (LoginSchema): ログインリクエストを表すデータ。
        db (Session): データベースセッション。

    戻り値:
        dict: 生成されたアクセストークンとトークンタイプ。

    例外:
        HTTPException: ユーザーが見つからないか、パスワードが間違っている場合。
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password'
        )
 
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

@auth.post("/send_reset_password_email", status_code=status.HTTP_201_CREATED)
def resend_password(request:SendResetPasswordUrlData):
    """
    引数:
        email (str): メールアドレス
        company_id (str): 会社ID

    戻り値:
        bool: True

    例外:
        HTTPException: ユーザーが見つからない場合。
    """
    # TODO: パスワード再発行のためのメール送信を実装する
    # verify if the user exists
    # user = get_user_by_email(email)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f'「{email}」のユーザーは見つかりません。'
    #     )
    
    password_reset_token = create_password_reset_token(request.email)
    
    # Construct the password reset URL
    password_reset_url = f"https://example.com/reset-password?token={password_reset_token}"
    
    # Compose the email message
    subject = "パスワード再発行"
    body = f"次のURLをクリックしてパスワードを再発行してください: {password_reset_url}"
    
    # Send the email
    # send_email(subject, email, body, company_id)
    return password_reset_url
    # return True

def create_password_reset_token(email):
    # TODO: パスワード再発行のためのメール送信を実装する
    
    password_reset_token = create_access_token(data={"sub": email}, expires_delta=datetime.timedelta(minutes=10))
    return password_reset_token

def send_email(subject, email, message, company_id):
    # TODO: パスワード再発行のためのメール送信を実装する
    # companyテーブルのメールアドレスを取得して、メールを送る
    company_email = get_company_email(company_id)
    
    # send email using aws service (SES)
    ses_client = boto3.client('ses')
    response = ses_client.send_email(
        Source=company_email,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': message}}
        }
    )
    return response

def get_company_email(
    company_id: str,
    db: Session = Depends(get_db)
    ):
    # companyテーブルのメールアドレスを取得して
    company = db.query(SalesTarget).filter(SalesTarget.id == company_id).first()
    return company.email


def get_user_by_email(
        email: str, 
        db: Session = Depends(get_db)
    ):
    user = db.query(User).filter(User.email == email).first()
    return user

@auth.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(
    request: ResetPasswordData, 
    db: Session = Depends(get_db)
):
    
    email = verify_password_reset_token(request.reset_token, HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid token or expired token'
        ))
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Password reset token is invalid or expired.'
        )

    # Get the user from the database
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Could not find user'
        )
    user.password = get_hashed_password(request.new_password)
    db.commit()
    return user
