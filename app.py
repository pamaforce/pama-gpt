from flask import Flask, request, jsonify, session
from flask_socketio import SocketIO, emit, disconnect
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps
from api import PoeApi
import datetime
import jwt
import threading


app = Flask(__name__)

# 添加配置文件
app.config.from_object(BaseConfig)
CORS(app)
# 初始化扩展，传入 app 创建 db
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
poe_api = PoeApi(app.config["POE_TOKEN"], proxy=True)

# 定义用户模型
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    account = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password
 
class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chatId = db.Column(db.Integer)
    bot = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, chatId, bot, user_id):
        self.chatId = chatId
        self.bot = bot
        self.user_id = user_id
        
    def to_dict(self):
        return {
            "bot": self.bot,
            "chatId": self.chatId,
            "user_id": self.user_id,
        }
                
        
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头中获取 Bearer Token
        bearer_token = request.headers.get("Authorization")
        if bearer_token:
            try:
                # 提取 JWT
                jwt_token = bearer_token.split(" ")[1]
                # 解码 JWT
                payload = jwt.decode(jwt_token, app.config["SECRET_KEY"], algorithms=["HS256"])

                # 获取用户 ID
                user_id = payload["user_id"]
                session['user_id'] = user_id

                # 根据用户 ID 查询用户
                user = Users.query.get(user_id)

                if user:
                    # 如果用户存在，继续执行函数
                    return f(*args, **kwargs)
                else:
                    # 用户不存在
                    return jsonify({"code": 403, "message": "用户好像不存在诶"})
            except jwt.ExpiredSignatureError:
                # JWT 已过期
                return jsonify({"code": 403, "message": "登录过期惹，请再证明一次你是你哦"})
            except (jwt.InvalidTokenError, IndexError):
                # 无效的 JWT 或未提供 JWT
                return jsonify({"code": 403, "message": "登录无效惹，请再证明一次你是你哦"})
        else:
            # 未提供 Bearer Token
            return jsonify({"code": 403, "message": "好像我还不认识你诶"})
    return decorated_function

@socketio.on('connect')
def handle_connect():
    # 从请求头中获取 Bearer Token
    bearer_token = request.headers.get("Authorization")
    if bearer_token:
        try:
            # 提取 JWT
            jwt_token = bearer_token.split(" ")[1]
            # 解码 JWT
            payload = jwt.decode(jwt_token, app.config["SECRET_KEY"], algorithms=["HS256"])

            # 获取用户 ID
            user_id = payload["user_id"]

            # 根据用户 ID 查询用户
            user = Users.query.get(user_id)

            if user:
                # 如果用户存在，将用户 ID 存储到 session 中
                session['user_id'] = user_id
            else:
                # 用户不存在
                emit('error', {"code": 403, "message": "用户好像不存在诶"})
                disconnect()
        except jwt.ExpiredSignatureError:
            # JWT 已过期
            emit('error', {"code": 403, "message": "登录过期惹，请再证明一次你是你哦"})
            disconnect()
        except (jwt.InvalidTokenError, IndexError):
            # 无效的 JWT 或未提供 JWT
            emit('error', {"code": 403, "message": "登录无效惹，请再证明一次你是你哦"})
            disconnect()
    else:
        # 未提供 Bearer Token
        emit('error', {"code": 403, "message": "好像我还不认识你诶"})
        disconnect()

@app.route("/login", methods=["POST"])
def login():
    # 获取POST请求中的账号和密码
    account = request.form.get("account")
    password = request.form.get("password")
    print(account,password)
    # 在数据库中查询用户
    user = Users.query.filter_by(account=account).first()

    if user:
        if user.password == password:
            # 密码正确，生成JWT
            payload = {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=720)  # 设置过期时间为720天
            }
            jwt_token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

            # 返回登录成功和JWT
            return jsonify({"code":0,"message": "登录成功", "token": jwt_token, "username": user.username})
        else:
            # 密码错误
            return jsonify({"code":400,"message": "密码错误，请再仔细检查一遍哦"})
    else:
        # 用户不存在
        return jsonify({"code":400,"message": "用户好像不存在诶"})

@app.route("/categories", methods=["GET"])
@jwt_required
def get_categories():
    categories = poe_api.get_available_categories()
    return jsonify({"code": 0, "message": "成功", "categories": categories})

@app.route("/bots", methods=["GET"])
@jwt_required
def get_bots():
    category = request.args.get("category")
    bots = poe_api.explore(categoryName=category, explore_all=True)
    return jsonify({"code": 0, "message": "成功", "bots": bots})

@app.route("/chat_bots", methods=["GET"])
@jwt_required
def get_chat_bots():
    bot = request.args.get("bot")
    chat_bots = poe_api.get_chat_history(bot=bot)
    return jsonify({"code": 0, "message": "成功", "chat_bots": chat_bots})

@app.route("/chat_history", methods=["GET"])
@jwt_required
def get_chat_history():
    bot = request.args.get("bot")
    chatId = get_chatId(bot)
    if(chatId is None):
        return jsonify({"code": 0, "message": "成功", "chat_history": []})
    chat_history = poe_api.get_previous_messages(bot=bot,chatId=chatId)
    return jsonify({"code": 0, "message": "成功", "chat_history": chat_history})

@app.route("/update_chat_id", methods=["POST"])
@jwt_required
def update_chat_id():
    bot = request.form.get("bot")
    chatId = request.form.get("chatId")
    update_chatId(bot, chatId)
    return jsonify({"code": 0, "message": "成功"})

def update_chatId(bot, chatId):
    s = Sessions.query.filter_by(bot=bot, user_id=session.get('user_id')).first()
    if s:
        s.chatId = chatId
    else:
        s = Sessions(bot=bot, user_id=session.get('user_id'), chatId=chatId)
        db.session.add(s)
    db.session.commit()

def get_chatId(bot):
    s = Sessions.query.filter_by(bot=bot, user_id=session.get('user_id')).first()
    if s:
        return s.chatId
    return None

def send_messages(bot, message,chatId, sid):
    newChatId = None
    for chunk in poe_api.send_message(bot, message, chatId):
        socketio.emit('response', chunk["response"], room=sid)
        newChatId = chunk["chatId"]
    if chatId is None:
        socketio.emit('chat_id',newChatId, room=sid)       
    socketio.emit('response_end', room=sid)

@socketio.on('chat')
def handle_chat(data):
    user_id = session.get('user_id')
    if user_id is None:
        emit('error', {"code": 403, "message": "好像我还不认识你诶"})
        return

    bot = data.get('bot')
    message = data.get('message')
    chatId = get_chatId(bot)
    sid = request.sid
    threading.Thread(target=send_messages, args=(bot, message,chatId, sid)).start()
        
if __name__ == '__main__':
    socketio.run(app)