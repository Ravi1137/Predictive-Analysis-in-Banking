from flask import Flask, render_template, request
import numpy as np
import pickle
from sklearn import preprocessing

pathloan="./static/model/loanmodel"
pathfraud="./static/model/fraudmodel"
pathchurn="./static/model/churnmodel"
model = pickle.load(open(pathloan, 'rb'))
churnmodel = pickle.load(open(pathchurn, 'rb'))
fraudmodel = pickle.load(open(pathfraud, 'rb'))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/loan')
def loan():
    return render_template('loan.html')


@app.route('/fraud')
def fraud():
    return render_template('fraud.html')


@app.route('/churn')
def churn():
    return render_template('churn.html')


def gender_con(x):
    if x == "Male":
        return 1
    else:
        return 0


def married_con(x):
    if x == "Yes":
        return 1
    else:
        return 0


def education_con(x):
    if x == "Graduate":
        return 1
    else:
        return 0


def employed_con(x):
    if x == "Yes":
        return 1
    else:
        return 0


def dependents_con(x):
    if x == "1":
        return 1
    elif x == "2":
        return 2
    elif x == "0":
        return 0
    else:
        return 3


def property_con(x):
    if x == "Rural":
        return 0
    elif x == "Semiurban":
        return 1
    else:
        return 2


# for Loan Prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        aincome = request.form['aincome']
        coincome = request.form['coincome']
        amount = request.form['amount']
        term = request.form['term']
        creadit = request.form['creadit']
        property = request.form['property']

    gender1 = gender_con(gender)
    married1 = married_con(married)
    dependents1 = dependents_con(dependents)
    education1 = education_con(education)
    employed1 = employed_con(employed)
    property1 = property_con(property)

# 'Gender',  'Married',   'Dependents',   'Education',  'Self_Employed','ApplicantIncome',
# 'CoapplicantIncome' , 'LoanAmount',  'Loan_Amount_Term',  'Credit_History', 'Property_Area',

    value = [gender1, married1, dependents1, education1, employed1,
             aincome, coincome, amount, term, creadit, property1]
    ans = model.predict([value])
    if ans == 1:
        prediction = "User is Eligble for loan"
    else:
        prediction = "User is not Eligble for loan"

    if creadit == "1":
        creadit = "High"
    else:
        creadit = "Low"

    # return "<h2>values are {} {} {} {} </h2>".format(value1,value2,value3,value4)
    return render_template('loanpredict.html', name=name, age=age, gender=gender, married=married, dependents=dependents, education=education, employed=employed,
                           aincome=aincome, coincome=coincome, amount=amount, term=term, creadit=creadit, property=property, prediction=prediction)


def occupation_con(x):
    if x == "Self Employed":
        return 1
    elif x == "Salaried":
        return 2
    elif x == "Student":
        return 3
    elif x == "Retired":
        return 4
    else:
        return 5


def networth_con(x):
    if x == "Low":
        return 1
    elif x == "Medium":
        return 2
    else:
        return 3


# for Churn Prediction
@app.route('/churnpredict', methods=['POST'])
def churnpredict():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        dependents = request.form['dependents']
        occupation = request.form['occupation']
        networth = request.form['networth']
        vintage = request.form['vintage']
        lastdayoftransaction = request.form['lastdayoftransaction']
        currentbalance = request.form['currentbalance']
        previous_month_end_balance = request.form['previous_month_end_balance']
        average_monthly_balance_quaterly = request.form['average_monthly_balance_quaterly']
        average_monthly_balance_quarterly_prev = request.form['average_monthly_balance_quarterly_prev']
        current_month_credit = request.form['current_month_credit']
        previous_month_credit = request.form['previous_month_credit']
        current_month_debit = request.form['current_month_debit']
        previous_month_debit = request.form['previous_month_debit']
        current_month_balance = request.form['current_month_balance']
        previous_month_balance = request.form['previous_month_balance']

    gender1 = gender_con(gender)
    occupation1 = occupation_con(occupation)
    networth1 = networth_con(networth)

# feature = ['vintage', 'dependents', 'days_since_last_transaction',
#        'current_balance', 'previous_month_end_balance',
#        'average_monthly_balance_prevQ', 'average_monthly_balance_prevQ2',
#        'current_month_credit', 'previous_month_credit', 'current_month_debit',
#        'previous_month_debit', 'current_month_balance',
#        'previous_month_balance', 'gender', 'occupation',
#        'customer_nw_category', 'age']

    value = [vintage, dependents, lastdayoftransaction,
             currentbalance, previous_month_end_balance,
             average_monthly_balance_quaterly, average_monthly_balance_quarterly_prev,
             current_month_credit, previous_month_credit, current_month_debit,
             previous_month_debit, current_month_balance,
             previous_month_balance, gender1, occupation1,
             networth1, age]

    ans = churnmodel.predict([value])
    if ans == 1:
        prediction = "Customer is Likly to Leave Bank"
    else:
        prediction = "Customer is Retain to Bank" 

    return render_template('churnpredict.html', name=name, age=age, gender=gender, dependents=dependents,
                           occupation=occupation, networth=networth, vintage=vintage, lastdayoftransaction=lastdayoftransaction,
                           currentbalance=currentbalance, previous_month_end_balance=previous_month_end_balance,
                           average_monthly_balance_quaterly=average_monthly_balance_quaterly,
                           average_monthly_balance_quarterly_prev=average_monthly_balance_quarterly_prev,
                           current_month_credit=current_month_credit, previous_month_credit=previous_month_credit,
                           current_month_debit=current_month_debit, current_month_balance=current_month_balance,
                           previous_month_balance=previous_month_balance,prediction=prediction)






# for fraud
@app.route('/fraudpredict', methods=['POST'])
def fraudpredict():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        amount=request.form['amount']
        v1=request.form['v1']
        v2=request.form['v2']
        v3=request.form['v3']
        v4=request.form['v4']
        v5=request.form['v5']
        v6=request.form['v6']
        v7=request.form['v7']
        v8=request.form['v8']
        v9=request.form['v9']
        v10=request.form['v10']
        v11=request.form['v11']
        v12=request.form['v12']
        v13=request.form['v13']
        v14=request.form['v14']
        v15=request.form['v15']
        v16=request.form['v16']
        v17=request.form['v17']
        v18=request.form['v18']
        v19=request.form['v19']
        v20=request.form['v20']
        v21=request.form['v21']
        v22=request.form['v22']
        v23=request.form['v23']
        v24=request.form['v24']
        v25=request.form['v25']
        v26=request.form['v26']
        v27=request.form['v27']
        v28=request.form['v28']



    value = [v1,v2,v3,v4,v5,v6,v7,v8,v9,v1,
            v11,v12,v13,v14,v15,v16,v17,v18,v19,v2,
            v21,v22,v23,v24,v25,v26,v27,v28,amount]

    ans = fraudmodel.predict([value])
    if ans == 1:
        prediction = "Fraud Transaction"
    else:
        prediction = "Normal Transaction" 

    return render_template('fraudpredict.html',prediction=prediction)



if __name__ == '__main__':
    app.run(debug=True)
