from flask import Flask, request, redirect, url_for, session, render_template, jsonify, flash
from models import db, User, Todo
from sqlalchemy.exc import IntegrityError
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form['loginId']
        action = request.form.get('action')
        print(f"로그인 시도: loginId={login_id}, action={action}")
        if action == 'Login':
            existing_user = User.query.filter_by(login_id=login_id).first()
            if existing_user:
                session['username'] = login_id
                return redirect(url_for('todo'))
            flash("ID가 잘못되었습니다. 회원가입을 먼저 진행하세요.")
            return redirect(url_for('login'))
            
        elif action == 'Join':
            existing_user = User.query.filter_by(login_id=login_id).first()
            if existing_user:
                flash("이미 존재하는 ID입니다. 다른 ID로 시도하세요.")
                return redirect(url_for('login'))
                
            # 사용자 정보 DB에 저장
            new_user = User(login_id=login_id)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("DB 오류. 다시 시도해주세요.")
                return redirect(url_for('login'))
                
            session['username'] = login_id
            return redirect(url_for('todo'))

    return render_template('login.html', login=False)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    print("add_todo 라우트 실행됨")  # ← 이 줄로 서버 콘솔에서 찍힘
    if 'username' not in session:
        return redirect(url_for('login'))
    login_id = session['username']
    user = User.query.filter_by(login_id=login_id).first()
    task = request.form.get('task')
    if not task:
        flash("할 일 내용을 입력하세요!")
        return redirect(url_for('todo'))
    new_todo = Todo(task=task, due_date=date.today(), user_id=user.id)
    db.session.add(new_todo)
    db.session.commit()
    print("할 일 저장 완료!")  # ← 이 줄로 서버 콘솔에서 찍힘
    return redirect(url_for('todo'))


@app.route('/todo')
def todo():
    if 'username' not in session:
        return redirect(url_for('login'))

    login_id = session['username']
    user = User.query.filter_by(login_id=login_id).first()
    today = date.today()
    # 오늘 할 일
    todos_today = Todo.query.filter_by(user_id=user.id, due_date=today).all()
    # 전에 못한 일 (done=False, due_date != today)
    prev_todos = Todo.query.filter(
        Todo.user_id == user.id,
        Todo.due_date != today,
        Todo.done == False
    ).all()

    return render_template(
        'todo.html',
        username=login_id,
        todos_today=todos_today,
        prev_todos=prev_todos,
        today=today.strftime("%Y년 %m월 %d일 %A")
    )

@app.route('/todo/done', methods=['POST'])
def mark_done():
    data = request.get_json()
    todo_id = data.get('todo_id')
    done = data.get('done', False)
    print(f"[CHECK] 체크박스 요청: todo_id={todo_id}, done={done}")   # <-- 이 줄 추가!
    todo = Todo.query.get(todo_id)
    if todo:
        todo.done = done
        db.session.commit()
        print(f"[UPDATE] DB 업데이트 완료: todo_id={todo_id}, done={done}")  # <-- 이 줄 추가!
        return jsonify({'result': 'success'})
    print("[FAIL] 할 일 못 찾음!")   # <-- 이 줄 추가!
    return jsonify({'result': 'fail'}), 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
