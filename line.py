from flask import Blueprint, current_app, redirect, request, render_template

bp = Blueprint('line', __name__, url_prefix='/line')

#route for line that provides the information given the code
@bp.route('/', methods=['GET'])
def line():
    code = request.args.get('code')
    if not code:
        return redirect('/')
    patient = current_app.config['db'].communicate(
        'SELECT * FROM patient WHERE code=:code',
        {'code': code}
    ).first()
    if patient is None:
        print('None')
        return redirect('/')
    queue = current_app.config['db'].communicate(
        'SELECT q.*, (JULIANDAY(CURRENT_TIMESTAMP) - JULIANDAY(q.joined)) * 86400'
        ' FROM patient_queue q, patient p WHERE'
        ' q.treated=0 AND p.patient_id=q.patient_id'
        ' ORDER BY p.severity DESC, q.joined ASC'
    ).all()
    pos = -1
    for i in range(len(queue)):
        if queue[i][0] == patient[0]:
            pos = i + 1
            break
    if pos == -1:
        print('Invalid index')
        return redirect('/')
    waiting_time = queue[pos - 1][-1] // 60
    est_wait = (pos - 1) * 15 #15 minutes for each patient
    ret_dict = {
        'name': patient[1],
        'position': pos,
        'wait_time': int(waiting_time),
        'est_wait': est_wait
    }
    return render_template('line.html', **ret_dict)
