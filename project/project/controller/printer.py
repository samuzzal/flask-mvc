from project import app
from project.models import Printer
from flask import render_template, request, jsonify
from .utils import call_service, API_ACCESS_KEY

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/print',methods=['GET','POST'])
def printer():
    if request.method=='POST':
         printer = Printer()
         printer.show_string(request.form['text'])
         return render_template('index.html')
    return render_template('print.html')

@app.route('/account_plan',methods=['POST'])
def create_account_plan():
    params = request.get_json()
    plan_name = params['plan_name']
    system_plan = params['system_plan']

    print ("{}-{}".format(plan_name, system_plan))
    data = "access_token={}&name={}&system_name={}".format(API_ACCESS_KEY, plan_name, system_plan)
    response = call_service('account_plans.xml', data)
    return jsonify(status = response.status_code)

@app.route('/application_plan',methods=['POST'])
def create_application_plan():
    params = request.get_json()
    plan_name = params['plan_name']
    system_plan = params['system_plan']
    print ("{}-{}".format(plan_name, system_plan))

    data = "access_token={}&name={}&system_name={}".format(API_ACCESS_KEY, plan_name, system_plan)
    response = call_service('account_plans.xml', data)
    return jsonify(status = response.status_code)

@app.route('/account',methods=['POST'])
def create_account():
    params = request.get_json()
    arr = []
    arr.append("access_token={}".format(API_ACCESS_KEY))
    arr.append("username={}".format(params['username']))
    arr.append("email={}".format(params['email']))
    arr.append("password={}".format(params['password']))

    response = call_service('users.xml', '&'.join(arr))
    return jsonify(status = response.status_code)

@app.route('/app_info',methods=['GET'])
def get_app_info():
    response = call_service('accounts', None, method='get')
    
    account_id = None
    if 'email' in request.args:
        search_field = 'email'
    else:
        search_field = 'username'
    
    for account in response.get('accounts', {}).get('account', []):
        for key,value in account.get('users', {}).items():
            print (value.get(search_field))
            print (request.args.get(search_field))

            if value.get(search_field) == request.args.get(search_field):
                account_id = value.get('account_id')
                break;
        if account_id is not None:
            break
    print ('Account ID = {}'.format(account_id))
    
    # Get the application key and id based on the account id
    data = "account_id={}".format(account_id)
    response = call_service('applications', data, method='get')

    return jsonify(response)
