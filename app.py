from flask import Flask, request, jsonify
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps
from api import PoeApi
from example import PoeExample
import datetime
import jwt

app = Flask(__name__)

# 添加配置文件
app.config.from_object(BaseConfig)
CORS(app)
# 初始化扩展，传入 app 创建 db
db = SQLAlchemy(app)

# 全局变量，用来在不同函数之间传递用户 ID
global_user_id = None
poe_api = PoeApi(app.config["POE_TOKEN"], proxy=True)
#poe_api = PoeExample(app.config["POE_TOKEN"]).chat_with_bot()

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

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id
        
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
        }
        
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global global_user_id
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
                global_user_id = user_id

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

@app.route("/sessions", methods=["GET"])
@jwt_required
def get_sessions():
    global global_user_id
    # 根据用户 ID 获取会话
    sessions = Sessions.query.filter_by(user_id=global_user_id).all()
    # 将会话转换为字典列表
    sessions_dict_list = [session.to_dict() for session in sessions]
    return jsonify({"code": 0, "message": "成功", "sessions": sessions_dict_list})

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
    chat_history = poe_api.get_chat_history(bot=bot)
    return jsonify({"code": 0, "message": "成功", "chat_history": chat_history})

if __name__ == '__main__':
    app.run()