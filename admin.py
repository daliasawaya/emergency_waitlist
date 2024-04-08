import datetime
from flask import Blueprint, current_app, request, jsonify, render_template, redirect

bp = Blueprint('admin', __name__, url_prefix='/admin')

#route for admin/
#assumption: The user is the admin and they have the authorization to use this page
@bp.route('/', methods=['GET'])
def get_admin_page():
    patients = current_app.config['db'].communicate(
        'SELECT p.*, (JULIANDAY(CURRENT_TIMESTAMP) - JULIANDAY(q.joined)) * 86400, q.* FROM patient p, patient_queue q '
        'WHERE p.patient_id = q.patient_id AND '
        'q.treated = 0 ' #making sure to get the not treated ones only
        'ORDER BY p.severity DESC, q.joined ASC;' #sorting first by severity and then by join time
    ).all()
    #the admins should see the following info
    patients = [
        {
            'id': p[0],
            'name': p[1],
            'code': p[2],
            'severity': p[3],
            'waiting_for_mins': int(p[4]) // 60,
            'treated': p[7]
        }
        for p in patients
    ]
    return render_template('admin.html', patients=patients)

#handling the add
#for get request, return the page that allows
#the admin to add a new user
#for post, if valid, we add the user to the database
@bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('admin_add.html')
    json_req = request.form
    name = json_req.get('patient_name')
    severity = json_req.get('severity')
    if name is None or severity is None or not severity.isdigit():
        return 'Invalid arguments', 400
    severity = int(severity)
    if severity > 4 or severity < 1:
        return 'Invalid arguments', 400
    
    patient_id = current_app.config['db'].communicate(
        'INSERT INTO patient VALUES('
            'CAST(hex(randomblob(3)) AS INTEGER), :name, hex(randomblob(3)), :severity '
        ') RETURNING patient_id;',
        {'name': name, 'severity': severity}
    ).first()[0]
    current_app.config['db'].communicate(
        'INSERT INTO patient_queue (patient_id) VALUES(:pid)',
        {'pid': patient_id}
    )
    current_app.config['db'].commit()
    return redirect('/admin')

#marks the given user as treated
@bp.route('/treat/<id>')
def treat(id):
    if not id.isdigit() or not current_app.config['db'].communicate(
        'SELECT patient_id FROM patient WHERE patient_id=:pid',
        {'pid': id}
    ).first():
        return 'Invalid id', 4
    current_app.config['db'].communicate(
        'UPDATE patient_queue SET treated=1 WHERE patient_id=:pid',
        {'pid': id}
    )
    current_app.config['db'].commit()

    return redirect('/admin')
    