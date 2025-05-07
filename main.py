from fastapi import FastAPI, UploadFile, Form, Response, Depends #65강추가
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
# 64강 추가 - Fast API Login 불러오기
from fastapi_login import LoginManager # Fast API Login 불러오기 end
# 64강 추가 - 유효하지 않은 계정정보에 대한 에러처리하기
from fastapi_login.exceptions import InvalidCredentialsException # 유효하지 않은 계정정보에 대한 에러처리하기 end
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread = False)
cur = con.cursor()


app = FastAPI()

# 64강 추가 - 토큰 발급하기
SERCRET = 'super-coding'
manager = LoginManager(SERCRET, './login')

# 64강 추가 - 유저 조회하기
@manager.user_loader()
def query_user(data): #65강 수정 - data
    # 65강 추가 start
    WHERE_STATEMENTS = f'id = "{data}"'
    if type (data) == dict:
        WHERE_STATEMENTS = f'''id = "{data['id']}"'''
    # 65강 추가 end
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                    SELECT * from users WHERE {WHERE_STATEMENTS}
                    """).fetchone() # 유저 조회하기 end
    return user

@app.post('/login')
def login(id: Annotated[str, Form()], 
        password: Annotated[str, Form()]
        ): 
    user = query_user(id)
    # 64강 추가 - 유저 존재 여부 판단하기 Start
    if not user :
        raise InvalidCredentialsException
    # InvalidCredentialsException 이 401을 자동으로 생성해서 내려준다
    elif password != user['password']:
        raise InvalidCredentialsException # 유저 존재 여부 판단하기 End
    
    access_token = manager.create_access_token(data={
        # 65강 추가
        'sub': user['id']
        
        # 'sub' : {
        #     'id' : user['id'],
        #     'name' : user['name'],
        #     'email' : user['email']
        # }
    });
    
    return {'access_token' : access_token}  #자동으로 200 상태코드로 내려줌
    #64강 추가 - 액세스 토큰 만들기 Start
    
# 토큰 발급하기 end


# 63강 추가
@app.post('/signup')
def signup(id: Annotated[str, Form()], 
        password: Annotated[str, Form()],
        # 64강 추가 - dbeaver 연결하기
        name : Annotated[str, Form()],
        email : Annotated[str, Form()]):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit() # 64강 추가 - dbeaver 연결하기 end
    return '200'


@app.post('/items')
async def create_item(image : UploadFile, 
                title : Annotated[str, Form()], 
                price : Annotated[int, Form()], 
                description : Annotated[str, Form()], 
                place : Annotated[str, Form()],
                insertAt : Annotated[int, Form()],
                user=Depends(manager)
                ):
    
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items (title, image, price, description, place, insertAt)
                VALUES ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}', {insertAt})
                """)
    con.commit()
    return '200'


@app.get('/items')
async def get_items(user=Depends(manager)): #65강 추가 - 유저가 인증된 상태에서만 응답 보낼수 있도록 하기 user=Depends(manager)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                        SELECT * from items;
                        """).fetchall()
    
    return JSONResponse (jsonable_encoder(dict(row) for row in rows))


@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                            SELECT image from items WHERE id = {item_id}
                            """).fetchone()[0]
    return Response(content = bytes.fromhex(image_bytes), media_type = 'image/*')

app.mount('/', StaticFiles(directory='frontend', html = True), name = 'frontend')