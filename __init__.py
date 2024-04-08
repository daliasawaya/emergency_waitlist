from flask import Flask, redirect, request, jsonify, render_template
import db
import admin
import line

#application instance
app = Flask(
    __name__,
    template_folder='client/html',
    static_folder='client/static'
)

#setting up the app and registering the line and admin blueprints
with app.app_context():
    app.config['db'] = db.Database(app)
    app.register_blueprint(admin.bp)
    app.register_blueprint(line.bp)

#should just redirect to index
@app.route('/', methods=['GET'])
def main_rt():
    return redirect('/index')

#should provide users with the environment to insert their code
@app.route('/index', methods=['GET'])
def index():
    #checking query
    query = request.args.get('code')
    if query:
        user_info = app.config['db'].communicate(
            'SELECT p.*  FROM patient p WHERE code=:code',
            {'code': query}
        ).first()
        if user_info is not None:
            return redirect(f'/line?code={query}')
        
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run()


