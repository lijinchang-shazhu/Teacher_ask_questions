from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import socketio


app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")
CORS(app, resources=r'/*')
mysql = MySQL(app)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# 配置MySQL数据库连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '722116'
app.config['MYSQL_DB'] = 'teacher_ask_questions'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save_chat', methods=['POST'])
def save_chat():
    data = request.json
    chat_text = data[0]
    if chat_text:
        
        # 将聊天内容插入到数据库中
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO chats (text) VALUES (%s)", (chat_text,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Chat saved successfully'})
    
    return jsonify({'error': 'Chat text is required'})

# @app.route('/chat', methods=['POST'])
# def chat():
#     # 处理对话框聊天逻辑
#     # 获取前端传递的数据
#     user_input = request.json['user_input']
#     print("user_input==",user_input)
#     # 进行对话框逻辑处理
#     response = chatbot_response(user_input)
#     # 返回响应数据s
#     return jsonify({'response': response})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('student_message')
def handle_student_message(message):
    # 处理学生发送的消息
    # 在这里进行聊天逻辑处理，比如将消息转发给教师
    emit('teacher_message', message, broadcast=True)

@socketio.on('teacher_message')
def handle_teacher_message(message):
    # 处理教师发送的消息
    # 在这里进行聊天逻辑处理，比如将消息转发给学生
    emit('student_message', message, broadcast=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=False)