from django.shortcuts import render, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
import pandas as pd
from .rf import prediction, preprocess
from sklearn.preprocessing import LabelEncoder
import numpy as np


# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/signup")
    # return HttpResponse("this is homepage")
    return render(request, "index.html")


def signupUser(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(
            request, "Your Account has been successfully created!!")

    return render(request, "signup.html")


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if user has enterd correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "index.html", {'fname': fname})

        else:
            messages.error(request, "Bad Credentials!!!")
            return redirect("/")

    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    messages.success(request, "Log out successfully!!")

    return redirect("/login")


def loanModel(request):

    return render(request, "loanModel.html")


def formInfo(request):
    if request.user.is_anonymous:
        return redirect("/signup")

    if request.method == 'POST':

        Gender = request.POST.get('Gender')
        Married = request.POST.get('Married')
        Dependents = request.POST.get('Dependents')
        Education = request.POST.get('Education')
        Self_Employed = request.POST.get('Self_Employed')
        ApplicantIncome = request.POST.get('ApplicantIncome')
        CoapplicantIncome = request.POST.get('CoapplicantIncome')
        LoanAmount = request.POST.get('LoanAmount')
        Loan_Amount_Term = request.POST.get('Loan_Amount_Term')
        Credit_History = request.POST.get('Credit_History')
        Property_Area = request.POST.get('Property_Area')

        LoanAmount = int(LoanAmount)
        Loan_Amount_Term = int(Loan_Amount_Term)
        ApplicantIncome = int(ApplicantIncome)
        CoapplicantIncome = int(CoapplicantIncome)

        Total_Income = ApplicantIncome + CoapplicantIncome
        Total_Income = int(Total_Income)

        Total_Income_log = Total_Income
        Total_Income_log = int(Total_Income_log)

        EMI = LoanAmount / Loan_Amount_Term
        EMI = int(EMI)

        BalanceIncome = Total_Income - (EMI*1000)
        BalanceIncome = int(BalanceIncome)

        del ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term

        data_frame = pd.DataFrame({
            'Gender': Gender,
            'Married': Married,
            'Dependents': Dependents,
            'Education': Education,
            'Self_Employed': Self_Employed,
            'Credit_History': Credit_History,
            'Property_Area': Property_Area,
            'Total_Income': Total_Income,
            'Total_Income_log': Total_Income_log,
            'EMI': EMI,
            'BalanceIncome': BalanceIncome,
        }, index=[0])

        Total_Income_log = data_frame['Total_Income_log']
        Total_Income_log = np.log(Total_Income_log)

        processed_data = np.array([[Gender, Married, Dependents, Education, Self_Employed,
                                   Credit_History, Property_Area, Total_Income, Total_Income_log, EMI, BalanceIncome]])

        processed_data = preprocess(data_frame)

        result = prediction(processed_data)

        print(result)

        if result == 0:
            result = 'you are not eligible for loan'
        else:
            result = 'your loan is approved'

        print(result)

    return render(request, 'result.html', {'result': result})

    # encoding = LabelEncoder()
    # Gender = encoding.fit_transform(data_frame['gender'])
    # Married = encoding.fit_transform(data_frame['married'])
    # Education = encoding.fit_transform(data_frame['education'])
    # Self_Employed = encoding.fit_transform( data_frame['self_employed'])
    # Property_Area = encoding.fit_transform( data_frame['property_area'])

    # data_frame.drop("gender", axis=1, inplace=True)
    # data_frame.drop("married", axis=1, inplace=True)
    # data_frame.drop("education", axis=1, inplace=True)
    # data_frame.drop("self_employed", axis=1, inplace=True)
    # data_frame.drop("property_area", axis=1, inplace=True)

    # data_frame['gender'] = Gender
    # data_frame['married']= Married
    # data_frame['education'] = Education
    # data_frame['self_employed'] =Self_Employed
    # data_frame['property_area'] = Property_Area
