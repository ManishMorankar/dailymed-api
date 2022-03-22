from ast import Str
from flask import Blueprint, jsonify, request, send_file
import hashlib
import binascii
import os
import json
import collections
import pyodbc
import requests
import pandas as pd
from datetime import datetime
home_bp = Blueprint('home', __name__)

languages = [{'name': 'JavaScript'}, {'name': 'Python'}, {'name': 'Ruby'}]
password = ''
global filterCondition 

def dbconn():
    global conn
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=10.10.20.109;"
        "Database=DailyMedDB_Live;"
        "UID=sa;"
        "PWD=Admin!@#20;"
        "MARS_Connection=Yes;"
        # "Trusted_Connection=yes;"
    )


dbconn()
print('Database connection sucessfully')


@home_bp.route('/index/')
def index():
    global data
    data = []
    cursor = conn.cursor()
    cursor.execute("select * from dailymed_view ")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'DailyMedId': row[0], 'SetId': row[1], 
        'year': row[2], 'approvalDate': row[3], 'NDAANDABLA': row[4], 
        'applicationNumber': row[5], 'brandName': row[6], 'routeOfAdministration': row[7],
        'dosage': row[8], 'typeofDosageForm': row[9], 'typeOfRelease': row[10], 'therapeuticCategory': row[11],
        'marketingStatus': row[12], 'Marketing_Start_Date': row[13],
        'Product_Image': row[14], 'Catagory': row[15], 'Submission_Type': row[16], 'Submission_Status': row[17], 
        'Registrant_Name': row[24], 'Labeler_Name': row[25]})
    return jsonify(data)

@home_bp.route('/dropdown/')
def dropdown():
    data = []
    data1 = []
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor.execute("select DISTINCT Filing_Type  from Daily_Med_Data WHERE DATALENGTH( Filing_Type) > 0 order by Filing_Type asc")
    cursor1.execute("select DISTINCT Application_Number from Daily_Med_Data where DATALENGTH(Application_Number)> 0 order by Application_Number asc")
    rows = cursor.fetchall()
    rows1 = cursor1.fetchall()
    for row in rows:
        data.append({'applicationType': row[0]})
   
    for row in rows1:
        data1.append({'applicationNo': row[0]})
    return jsonify({'applicationTypeList': data})
    return jsonify({'applicationNoList': data1})

@home_bp.route('/applicationType/')
def ApplicationType():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Filing_Type  from Daily_Med_Data WHERE DATALENGTH( Filing_Type) > 0 order by Filing_Type asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'applicationType': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/applicationsNo/')
def applicationsNo():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Application_Number from Daily_Med_Data where DATALENGTH(Application_Number)> 0 order by Application_Number asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'applicationNo': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/activeIngredient/')
def ActiveIngredient():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Active_Ingredient from Active_Ingredient where DATALENGTH(Active_Ingredient)> 0 order by Active_Ingredient asc")
    rows = cursor.fetchall()
    for row in rows:
         data.append({'activeIngredient': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/activeStrength/')
def Strength():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Strength from Active_Ingredient where DATALENGTH(Strength)> 0 order by Strength asc")
    rows = cursor.fetchall()
    for row in rows:
         data.append({'activeStrength': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/activeUNIINumber/')
def UNIINumber():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT UNII_Number from Active_Ingredient  WHERE DATALENGTH(UNII_Number) > 0 order by UNII_Number asc")
    rows = cursor.fetchall()
    for row in rows:
        # data.append([x for x in row])  # or simply data.append(list(row))
        data.append({'activeUNIINumber': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/inActiveIngredient/')
def InActiveIngredient():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT In_Active_Ingredient from Inactive_Ingredient where DATALENGTH(In_Active_Ingredient)> 0 order by In_Active_Ingredient asc")
    rows = cursor.fetchall()
    for row in rows:
         data.append({'inActiveIngredient': " ".join(row[0].split())})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/inActiveStrength/')
def InActiveStrength():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Strength from Inactive_Ingredient where DATALENGTH(Strength)> 0 order by Strength asc")
    rows = cursor.fetchall()
    for row in rows:
         data.append({'inActiveStrength': " ".join(row[0].split())})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/inActiveUNIINumber/')
def InActiveUNIINumber():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT UNII_Number from Inactive_Ingredient  WHERE DATALENGTH(UNII_Number) > 0 order by UNII_Number asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'inActiveUNIINumber': " ".join(row[0].split())})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/routeOfAdministration/')
def RouteOfAdministration():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Route_Of_Administration from Daily_Med_Data WHERE DATALENGTH(Route_Of_Administration) > 0 order by Route_Of_Administration asc")
    rows = cursor.fetchall()
    for row in rows:
         data.append({'routeOfAdministration': " ".join(row[0].split())})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/dosageForm/')
def DosageForm():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Type_of_Dosage_Form from Daily_Med_Data WHERE DATALENGTH( Type_of_Dosage_Form) > 0 order by Type_of_Dosage_Form asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'dosageForm': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/TypeOfRelease/')
def TypeOfRelease():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Type_Of_Release  from Daily_Med_Data WHERE DATALENGTH( Type_Of_Release) > 0 order by Type_Of_Release asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'typeOfRelease': row[0]})
    return jsonify({'statusCode':'200', 'result': data})


@home_bp.route('/TherapeuticCategory/')
def TherapeuticCategory():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Therapeutic_Category  from Daily_Med_Data WHERE DATALENGTH( Therapeutic_Category) > 0 order by Therapeutic_Category asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append([x for x in row])  # or simply data.append(list(row))
    return jsonify(data)

@home_bp.route('/marketingStatus/')
def MarketingStatus():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Marketing_Status  from Daily_Med_Data WHERE DATALENGTH(Marketing_Status) > 0 order by Marketing_Status asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'marketingStatus': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/manufacureName/')
def ManufacureName():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT  Manufacturer_Name from EstablshmentManufacure_Data WHERE DATALENGTH(Manufacturer_Name) > 0 order by Manufacturer_Name asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'manufacureName': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/manufacureCountry/')
def ManufacureCountry():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT  Manufacturing_Country from EstablshmentManufacure_Data WHERE DATALENGTH(Manufacturing_Country) > 0 order by Manufacturing_Country asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'manufacureCountry': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/brandName/')
def BrandName():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Brand_Name  from Daily_Med_Data WHERE DATALENGTH(Brand_Name) > 0 order by Brand_Name asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'brandName': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/ndcCode/')
def NDCCode():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT  NDC_Code from Packaging WHERE DATALENGTH(NDC_Code) > 0 order by NDC_Code asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'ndcCode': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/packaging/')
def Packaging():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT  Packaging from Packaging WHERE DATALENGTH(Packaging) > 0 order by Packaging asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'packaging': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/category/')
def Category():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Category  from Daily_Med_Data WHERE DATALENGTH(Category) > 0 order by Category asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'category': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/submission/')
def Submission():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Submission  from Us_Fda_Data WHERE DATALENGTH(Submission) > 0 order by Submission asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'submission': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/submissionType/')
def SubmissionType():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Submission_Classification  from Us_Fda_Data WHERE DATALENGTH(Submission_Classification) > 0 order by Submission_Classification asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'submissionType': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/submissionStatus/')
def SubmissionStatus():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Submission_Status  from Us_Fda_Data WHERE DATALENGTH(Submission_Status) > 0 order by Submission_Status asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'submissionStatus': row[0]})
    return jsonify({'statusCode':'200', 'result': data})

@home_bp.route('/patentNo/')
def PatentNo():
    data = []
    cursor = conn.cursor()
    cursor.execute("select DISTINCT Patent_No  from Patent_Data WHERE DATALENGTH(Patent_No) > 0 order by Patent_No asc")
    rows = cursor.fetchall()
    for row in rows:
        data.append({'patentNo': row[0]})
    return jsonify({'statusCode':'200', 'result': data})
  

@home_bp.route('/filter',methods=['POST'])
def filter():
    PrepareFilterQuery() 
    TotalCount=''
    cursor1 = conn.cursor()
    cursor1.execute("select count(*) from dailymed_view "+filterCondition+"")
    rows = cursor1.fetchall()
    for row in rows:
        TotalCount=row[0]

    global data
    data=[]
    print(filterCondition)
    cursor = conn.cursor()
    cursor.execute("select * from dailymed_view "+filterCondition+" ORDER BY (SELECT NULL) OFFSET "+request.json["resultSkipedRows"]+" ROWS FETCH NEXT 250 ROWS ONLY")
    rows = cursor.fetchall()
    
    for row in rows:
        data.append({'DailyMedId': row[0], 'SetId': row[1], 'year': row[2], 'approvalDate': row[3], 'NDAANDABLA': row[4], 'applicationNumber': row[5],'therapeuticEquivalents': row[6], 'brandName': row[7], 'routeOfAdministration': row[8],'subRouteOfAdministration': row[9], 'dosage': row[10], 'typeofDosageForm': row[11], 'typeOfRelease': row[12],'active_Ingredient': row[13],'active_UNII_Number': row[14],'active_Strength': row[15],'inactive_Ingredient': row[16],'inctive_UNII_Number': row[17],'inactive_Strength': row[18],
        'therapeuticCategory': row[19],'subcategory':row[20], 'marketingStatus': row[21], 'marketing_Start_Date': row[22],'category': row[23],'submission': row[24], 'submission_Type': row[25], 'submission_Status': row[26],'duns_Number': row[27], 'company_Name': row[28], 'subsidiaries': row[29],'repackager': row[30], 'registrant_Name': row[31], 'labeler_Name': row[32],'manufacure_Name': row[33], 'manufacure_Address': row[34], 'manufacure_Country': row[35],
        'patent_No':row[36],'expiration_Date':row[37], 'exclusivity_Date': row[38],'ndc_Code': row[39],  'packaging': row[40], 'imageName': row[41], 'imageUrl': row[42],'country': row[43],'sector': row[44],'intStrength': row[45],'intPack': row[46],'patentExpiryDate': row[47],'countingUnits2016': row[48],'usDollarMnf2016': row[49],'countingUnits2017': row[50],'usDollarMnf2017': row[51],'countingUnits2018': row[52],'usDollarMnf2018': row[53]})
   
    return jsonify({'statusCode':'200', 'result': data,'TotalCount':TotalCount})

@home_bp.route('/export',methods=['POST'])
def export(): 
    PrepareFilterQuery()
    if(request.json["numberOfRows"] != ''):
        numberOfRows=request.json["numberOfRows"]
        skipRows=request.json["skipRows"]

        #df=pd.read_sql(sql="select top "+numberOfRows+" * from dailymed_view "+filterCondition+" and DailyMedId not in(select top "+skipRows+" DailyMedId from dailymed_view)",con=conn)
        df=pd.read_sql(sql="select * from dailymed_view "+filterCondition+" ORDER BY (SELECT NULL) OFFSET "+skipRows+" ROWS FETCH NEXT "+numberOfRows+" ROWS ONLY",con=conn)
        #print("select top "+numberOfRows+" * from dailymed_view "+filterCondition+" and DailyMedId not in(select top "+skipRows+" DailyMedId from dailymed_view)")
        df.to_excel("DailyMedData.xlsx",index=False)
        return send_file("DailyMedData.xlsx",as_attachment=True)
    else:    
        df=pd.read_sql(sql="select * from dailymed_view "+filterCondition+"",con=conn)
        # print(df)
        df.to_excel("DailyMedData.xlsx",index=False)
        return send_file("DailyMedData.xlsx",as_attachment=True)

def PrepareFilterQuery():
    global filterCondition
    filterCondition= 'where 1=1'
    if(request.json["applicationType"] != ''):
        applicationTypeList = request.json["applicationType"].split(',')
        condition = " and (Filing_Type LIKE '%" + applicationTypeList[0].strip() + "%'"
        for index,applicationType in enumerate(applicationTypeList):
            if index!=0:
                condition=condition+ " or Filing_Type LIKE '%" + applicationType.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["applicationNo"] !=''):
        applicationNoList = request.json["applicationNo"].split(',')
        condition = " and (Application_Number LIKE '%" + applicationNoList[0].strip() + "%'"
        for index,applicationNo in enumerate(applicationNoList):
            if index!=0:
                condition=condition+ " or Application_Number LIKE '%" + applicationNo.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["activeIngredient"] !=''):
        activeIngredientList = request.json["activeIngredient"].split(',')
        condition = " and (Active_Ingredient LIKE '%" + activeIngredientList[0].strip() + "%'"
        for index,activeIngredient in enumerate(activeIngredientList):
            if index!=0:
                condition=condition+ " or Active_Ingredient LIKE '%" + activeIngredient.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["activeStrength"] !=''):
        activeStrengthList = request.json["activeStrength"].split(',')
        condition = " and (Active_Strength LIKE '%" + activeStrengthList[0].strip() + "%'"
        for index,activeStrength in enumerate(activeStrengthList):
            if index!=0:
                condition=condition+ " or Active_Strength LIKE '%" + activeStrength.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["activeUNIINumber"] !=''):
        activeUNIINumberList = request.json["activeUNIINumber"].split(',')
        condition = " and (Active_UNII_Number LIKE '%" + activeUNIINumberList[0].strip() + "%'"
        for index,activeUNIINumber in enumerate(activeUNIINumberList):
            if index!=0:
                condition=condition+ " or Active_UNII_Number LIKE '%" + activeUNIINumber.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["inActiveIngredient"] !=''):
        inActiveIngredientList = request.json["inActiveIngredient"].split(',')
        condition = " and (Inactive_Ingredient LIKE '%" + inActiveIngredientList[0].strip() + "%'"
        for index,inActiveIngredient in enumerate(inActiveIngredientList):
            if index!=0:
                condition=condition+ " or Inactive_Ingredient LIKE '%" + inActiveIngredient.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["inActiveStrength"] !=''):
        inActiveStrengthList = request.json["inActiveStrength"].split(',')
        condition = " and (Inactive_Strength LIKE '%" + inActiveStrengthList[0].strip() + "%'"
        for index,inActiveStrength in enumerate(inActiveStrengthList):
            if index!=0:
                condition=condition+ " or Inactive_Strength LIKE '%" + inActiveStrength.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["inActiveUNIINumber"] !=''):
        inActiveUNIINumberList = request.json["inActiveUNIINumber"].split(',')
        condition = " and (Inactive_UNII_Number LIKE '%" + inActiveUNIINumberList[0].strip() + "%'"
        for index,inActiveUNIINumber in enumerate(inActiveUNIINumberList):
            if index!=0:
                condition=condition+ " or Inactive_UNII_Number LIKE '%" + inActiveUNIINumber.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["routeOfAdministration"] !=''):
        routeOfAdministrationList = request.json["routeOfAdministration"].split(',')
        condition = " and (Route_Of_Administration LIKE '%" + routeOfAdministrationList[0].strip() + "%'"
        for index,routeOfAdministration in enumerate(routeOfAdministrationList):
            if index!=0:
                condition=condition+ " or Route_Of_Administration LIKE '%" + routeOfAdministration.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["dosageForm"] !=''):
        dosageFormList = request.json["dosageForm"].split(',')
        condition = " and (Type_of_Dosage_Form LIKE '%" + dosageFormList[0].strip() + "%'"
        for index,dosageForm in enumerate(dosageFormList):
            if index!=0:
                condition=condition+ " or Type_of_Dosage_Form LIKE '%" + dosageForm.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["typeOfRelease"] !=''):
        typeOfReleaseList = request.json["typeOfRelease"].split(',')
        condition = " and (Type_Of_Release LIKE '%" + typeOfReleaseList[0].strip() + "%'"
        for index,typeOfRelease in enumerate(typeOfReleaseList):
            if index!=0:
                condition=condition+ " or Type_Of_Release LIKE '%" + typeOfRelease.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    # if(request.json["Therapeutic_Category"] !=''):
    #     filterCondition = filterCondition + " and Therapeutic_Category LIKE '" + request.json["Therapeutic_Category"] + "%'"
    if(request.json["marketingStatus"] !=''):
        marketingStatusList = request.json["marketingStatus"].split(',')
        condition = " and (Marketing_Status LIKE '%" + marketingStatusList[0].strip() + "%'"
        for index,marketingStatus in enumerate(marketingStatusList):
            if index!=0:
                condition=condition+ " or Marketing_Status LIKE '%" + marketingStatus.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["manufacureName"] !=''):
        manufacureNameList = request.json["manufacureName"].split(',')
        condition = " and (Manufacturer_Name LIKE '%" + manufacureNameList[0].strip() + "%'"
        for index,manufacureName in enumerate(manufacureNameList):
            if index!=0:
                condition=condition+ " or Manufacturer_Name LIKE '%" + manufacureName.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["manufacureCountry"] !=''):
        manufacureCountryList = request.json["manufacureCountry"].split(',')
        condition = " and (Manufacturing_Country LIKE '%" + manufacureCountryList[0].strip() + "%'"
        for index,manufacureCountry in enumerate(manufacureCountryList):
            if index!=0:
                condition=condition+ " or Manufacturing_Country LIKE '%" + manufacureCountry.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["brandName"] !=''):
        brandNameList = request.json["brandName"].split(',')
        condition = " and (Brand_Name LIKE '%" + brandNameList[0].strip() + "%'"
        for index,brandName in enumerate(brandNameList):
            if index!=0:
                condition=condition+ " or Brand_Name LIKE '%" + brandName.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["ndcCode"] !=''):
        ndcCodeList = request.json["ndcCode"].split(',')
        condition = " and (NDC_Code LIKE '%" + ndcCodeList[0].strip() + "%'"
        for index,ndcCode in enumerate(ndcCodeList):
            if index!=0:
                condition=condition+ " or NDC_Code LIKE '%" + ndcCode.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["packaging"] !=''):
        packagingList = request.json["packaging"].split(',')
        condition = " and (Packaging LIKE '%" + packagingList[0].strip() + "%'"
        for index,packaging in enumerate(packagingList):
            if index!=0:
                condition=condition+ " or Packaging LIKE '%" + packaging.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["category"] !=''):
        categoryList = request.json["category"].split(',')
        condition = " and (Category LIKE '%" + categoryList[0].strip() + "%'"
        for index,category in enumerate(categoryList):
            if index!=0:
                condition=condition+ " or Category LIKE '%" + category.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["fromApprovalDate"] !='' and request.json["toApprovalDate"] !=''):
        filterCondition = filterCondition + "and Approval_Date BETWEEN CONVERT(date,'"+request.json["fromApprovalDate"]+"')  and CONVERT(date,'"+request.json["toApprovalDate"]+"')"
    if(request.json["submission"] !=''):
        submissionList = request.json["submission"].split(',')
        condition = " and (Submission LIKE '%" + submissionList[0].strip() + "%'"
        for index,submission in enumerate(submissionList):
            if index!=0:
                condition=condition+ " or Submission LIKE '%" + submission.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["submissionType"] !=''):
        submissionTypeList = request.json["submissionType"].split(',')
        condition = " and (Submission_Type LIKE '%" + submissionTypeList[0].strip() + "%'"
        for index,submissionType in enumerate(submissionTypeList):
            if index!=0:
                condition=condition+ " or Submission_Type LIKE '%" + submissionType.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["submissionStatus"] !=''):
        submissionStatusList = request.json["submissionStatus"].split(',')
        condition = " and (Submission_Status LIKE '%" + submissionStatusList[0].strip() + "%'"
        for index,submissionStatus in enumerate(submissionStatusList):
            if index!=0:
                condition=condition+ " or Submission_Status LIKE '%" + submissionStatus.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["patentNo"] !=''):
        patentNoList = request.json["patentNo"].split(',')
        condition = " and (Patent_No LIKE '%" + patentNoList[0].strip() + "%'"
        for index,patentNo in enumerate(patentNoList):
            if index!=0:
                condition=condition+ " or Patent_No LIKE '%" + patentNo.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["therapeuticCategory"] !=''):
        therapeuticCategoryList = request.json["therapeuticCategory"].split(',')
        condition = " and (Therapeutic_Category LIKE '%" + therapeuticCategoryList[0].strip() + "%'"
        for index,therapeuticCategory in enumerate(therapeuticCategoryList):
            if index!=0:
                condition=condition+ " or Therapeutic_Category LIKE '%" + therapeuticCategory.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    if(request.json["companyName"] !=''):
        companyNameList = request.json["companyName"].split(',')
        condition = " and (Company_Name LIKE '%" + companyNameList[0].strip() + "%'"
        for index,companyName in enumerate(companyNameList):
            if index!=0:
                condition=condition+ " or Company_Name LIKE '%" + companyName.strip() + "%'"
        filterCondition = filterCondition + condition+")"
    
    
    if(request.json["patentExpirationDate"] !=''):
        date_obj= datetime.strptime(request.json["patentExpirationDate"], '%Y-%m-%d')
        ExpirationDate = date_obj.strftime('%d-%b-%Y')
        filterCondition = filterCondition + "and Expiration_Date LIKE '%" + ExpirationDate + "%'"

    
    if(request.json["patentExclusivityDate"] !=''):
        date = datetime.strptime(request.json["patentExclusivityDate"], '%Y-%m-%d')
        ExclusivityDate = date.strftime('%d-%b-%Y')
        filterCondition = filterCondition + "and Exclusivity_Date LIKE '%"+ExclusivityDate+"%'"

@home_bp.route('/index/', methods=['POST'])
def addOne():
    password = {'password': request.json['password']}
    # language = {'name':request.json['name']}
    # languages.append(language)
    #password=hash_password(password)
    return jsonify(password)


@home_bp.route('/postjson/', methods=['POST'])
def postJsonHandler():
    print(request.is_json)
    content = request.get_json()
    print(content)
    return 'JSON posted'

@home_bp.route('/syncOfflineData',methods=['POST'])
def updateTherapeuticCategory():
    UpdateTherapeuticCategoryForExistingData()
    UpdateSalesDataForExistingData()
    UpdateUsfdaDataForExistingData()
    UpdatePatentExclusivityForExistingData()
    return jsonify({'statusCode':'200', 'message':'Offline data synced sucessfully'})

def UpdateTherapeuticCategoryForExistingData():
    DailyMedId=''
    ActiveIngredients=''
    cursor = conn.cursor()
    cursor.execute("select d.DailyMedId,ai.Active_Ingredient From Daily_Med_Data d left join Active_Ingredient ai on d.DailyMedId =ai.DailyMedId where d.Therapeutic_Updated_Status=0")
    rows=cursor.fetchall()
    for row in rows:
        try:
            DailyMedId=row[0]
            ActiveIngredients=row[1].replace("'","''") 
            UpdateTherapeuticCategory(DailyMedId,ActiveIngredients)
        except:
            print("Exception in UpdateTherapeuticCategory for DailyMedId:"+str(DailyMedId))     

def UpdateTherapeuticCategory(DailyMedId,ActiveIngredients): 
    TherapeuticCategory=''
    SubCategory=''
    cursor = conn.cursor()
    cursor.execute("select distinct Therapeutic_Category,Sub_Category from Therapy_Index_USFDA_Data where Active_Ingredients='"+ActiveIngredients+"'")
    for row in cursor: 
        TherapeuticCategory=row[0].replace("'","''")
        if row[1] != None:
            SubCategory=row[1].replace("'","''")
        cursor = conn.cursor()
        cursor.execute("update Daily_Med_Data set Therapeutic_Category='"+TherapeuticCategory+"',Subcategory='"+SubCategory+"',Therapeutic_Updated_Status=1 where DailyMedId="+str(DailyMedId))
        conn.commit()
        break  

def UpdateSalesDataForExistingData():
    DailyMedId=''
    CompanyName=''
    ActiveIngredients=''
    ActiveStrength=''
    Packaging=''
    Repackager=''
    LabelerName=''
    ManufacturerName=''

    cursor = conn.cursor()
    cursor.execute("select d.DailyMedId,d.Company_Name,ai.Active_Ingredient,ai.Strength,p.Packaging,d.Repackager,d.Labeler_Name,esmd.Manufacturer_Name From Daily_Med_Data d left join Active_Ingredient ai on d.DailyMedId =ai.DailyMedId left join Packaging p on d.DailyMedId =p.DailyMedId left join EstablshmentManufacure_Data esmd on d.DailyMedId =esmd.DailyMedId where d.DailyMedId not in(select distinct Daily_Med_Id from Sales_Data)")
    rows=cursor.fetchall()
    for row in rows:
        DailyMedId=row[0]
        CompanyName=row[1].replace("'","''")
        ActiveIngredients=row[2].replace("'","''")
        ActiveStrength=row[3].replace("'","''")
        Packaging=row[4]
        Repackager=row[5]
        LabelerName=row[6]
        ManufacturerName=row[7]
        RLMFlag=True
        
        #Check same company name is exist or not if it's not blank
        if Repackager !=None and Repackager !="" and CompanyName.lower() not in Repackager.lower():
            RLMFlag=False 
        if LabelerName !=None and LabelerName !="" and CompanyName.lower() not in LabelerName.lower():
            RLMFlag=False                 
        if ManufacturerName !=None and ManufacturerName !="" and CompanyName.lower() not in ManufacturerName.lower():
            RLMFlag=False         
        
        #Check if Company Name is there into Repackager,LabelerName,ManufacturerName
        print(RLMFlag)
        if RLMFlag:  
            InsertSalesData(CompanyName,ActiveIngredients,ActiveStrength,DailyMedId,Packaging)     

def InsertSalesData(CompanyName,ActiveIngredients,ActiveStrength,DailyMedId,Packaging):
    try:
        ActiveStrength=ActiveStrength.replace(" ","").replace("'","")
        ActiveStrength=ActiveStrength.replace(";","+") #In Sales_Data_Input table we have + separator without space
        ActiveIngredients=ActiveIngredients.replace("; ","!") #In Sales_Data_Input table we have + separator without space
        Country=''
        Sector=''
        IntStrength=''
        IntPack=''
        IntPackSize=''
        PatentExpiryDate=''
        CountingUnits2016=''
        USDollarMNF2016=''
        CountingUnits2017=''
        USDollarMNF2017=''
        CountingUnits2018=''
        USDollarMNF2018=''
        # if Corporation = Company Name,Country = US,Molecule_List = Active_Ingredient(Alone),Int_Strength=Active_Strength
        cursor1 = conn.cursor()
        cursor1.execute(
            "select Country,Sector,Int_Strength,Int_Pack,Int_Pack_Size,Patent_Expiry_Date,Counting_Units_2016,US_Dollar_MNF_2016,Counting_Units_2017,US_Dollar_MNF_2017,Counting_Units_2018,US_Dollar_MNF_2018 from Sales_Data_Input where Corporation='"+CompanyName+"' and  Country='US' and Molecule_List='"+ActiveIngredients+"' and Int_Strength = '"+ActiveStrength+"'")
        rows=cursor1.fetchall()
        for row in rows:
            Country=row[0]
            Sector=row[1]
            IntStrength=row[2]
            IntPack=row[3]
            IntPackSize=row[4]
            PatentExpiryDate=row[5]
            CountingUnits2016=row[6]
            USDollarMNF2016=row[7]
            CountingUnits2017=row[8]
            USDollarMNF2017=row[9]
            CountingUnits2018=row[10]
            USDollarMNF2018=row[11]

            # Check IntPackSize is exist in Packaging
            if IntPackSize in Packaging:  
                cursor = conn.cursor()
                cursor.execute(
                'insert into Sales_Data(Daily_Med_Id,Country,Sector,Int_Strength,Int_Pack,Patent_Expiry_Date,Counting_Units_2016,US_Dollar_MNF_2016,Counting_Units_2017,US_Dollar_MNF_2017,Counting_Units_2018,US_Dollar_MNF_2018) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                (DailyMedId,Country,Sector,IntStrength,IntPack,PatentExpiryDate,CountingUnits2016,USDollarMNF2016,CountingUnits2017,USDollarMNF2017,CountingUnits2018,USDollarMNF2018)
                )
                conn.commit()   
    except:
        print("Exception in added Sales Data for DailyMedId:"+str(DailyMedId))         

def UpdateUsfdaData(UsfdaApplicationNumber,NdaAndaBla,Category,DailyMedId):
    global Year
    global Submission
    global SubmissionType
    global SubmissionStatus
    global MarketingStatus
    global ApprovalDate
    global CompanyName 
    Submission = ''
    SubmissionType = ''
    SubmissionStatus = ''
    MarketingStatus = ''
   #ApprovalDate = ''
    CompanyName = ''
    cursor = conn.cursor()
    cursor.execute(
        "select * from Us_Fda_Data Where Number='"+UsfdaApplicationNumber+"'")
    result=cursor.fetchall()    
    foundFlag=False
    for row in result:
        foundFlag=True
        # print(f'row = {row}')
        # date_obj = datetime.strptime(str(row[1]), '%m/%d/%Y')
        # date = date_obj.strftime('%d-%b-%Y')
        
        ApprovalDate = row[1]
        Submission = row[5]
        SubmissionType = row[8]
        if "ANIMAL".lower() in Category.lower() and (NdaAndaBla=="ANADA" or NdaAndaBla=="NADA"):
            CompanyName = ''
        else:    
            CompanyName  = row[7]
        SubmissionStatus = row[9]
        my_date = datetime.strptime(row[1], '%d-%b-%Y')
        Year = my_date.year
        if(Submission == 'ORIG-1'):
            break

    cursor1 = conn.cursor()
    cursor1.execute("SELECT MarketingStatusDescription from MarketingStatus INNER JOIN MarketingStatus_Lookup ON  MarketingStatus_Lookup.MarketingStatusID=MarketingStatus.MarketingStatusID where ApplNo='"+UsfdaApplicationNumber+"'")
    result1=cursor1.fetchall()
    for rows in result1:
        MarketingStatus = rows[0]
    
    if foundFlag==True:
        cursor = conn.cursor()
        cursor.execute("update Daily_Med_Data set Approval_Date='"+ApprovalDate+"',Submission='"+Submission+"',Submission_Type='"+SubmissionType+"',Company_Name='"+CompanyName+"',Submission_Status='"+SubmissionStatus+"',Approval_Year='"+str(Year)+"',Marketing_Status='"+MarketingStatus+"',Usfda_Data_Updated_Status=1 where DailyMedId="+str(DailyMedId))
        conn.commit()

def UpdateUsfdaDataForExistingData():
    DailyMedId=''
    ApplcationNumber=''
    NdaAndaBla=''
    Category=''
    cursor = conn.cursor()
    cursor.execute("select DailyMedId,Application_Number,Filing_Type,Category From Daily_Med_Data where Usfda_Data_Updated_Status=0")
    rows=cursor.fetchall()
    for row in rows:
        try:
            DailyMedId=row[0]
            ApplcationNumber=row[1]
            NdaAndaBla=row[2]
            Category=row[3] 
            UpdateUsfdaData(ApplcationNumber,NdaAndaBla,Category,DailyMedId)
        except:
            print("Exception in Update USFDA related data for DailyMedId:"+str(DailyMedId))

def UpdatePatentExclusivityForExistingData():
    DailyMedId=''
    ApplicationNumber=''
    ApprovalDate=''
    cursor = conn.cursor()
    cursor.execute("select DailyMedId,Application_Number,Approval_Date From Daily_Med_Data where DailyMedId not in(select DailyMedId from PatentExclusivity_Data)")
    rows=cursor.fetchall()
    for row in rows:
        try:
            DailyMedId=row[0]
            ApplicationNumber=row[1]
            ApprovalDate=row[2]
            InsertPatentExclusivity(DailyMedId,ApplicationNumber,ApprovalDate)
        except:
            print("Exception in InsertPatentExclusivity for DailyMedId:"+str(DailyMedId))     

def InsertPatentExclusivity(DailyMedId,ApplicationNumber,ApprovalDate):
    PatentName = ''
    Patent_No = []
    Expiration_Date = []
    Exclusivity_Date = []
    ExclusivityData = []
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    ApplicationNumber1 = ApplicationNumber.replace('0', '', 0)
    foundFlag=False
    cursor.execute(
        "select distinct Patent_No,Patent_Expire_Date from Patent_Data Where Appl_No='"+ApplicationNumber1+"'")
    myresult = cursor.fetchall()
    for x in myresult:
        foundFlag=True
        Patent_No.append(x[0])
        # Patent Expiration Year Correction Begins
        ExpDate= x[1].split('/')
        if ApprovalDate.split('-')[2] >= ExpDate[2]:
            ResultExpDate= ExpDate[0]+"/"+ExpDate[1]+"/" +str(int(ExpDate[2])+100)
            Expiration_Date.append(ResultExpDate)
            Patent_No.append(x[0])
            # Patent Expiration Year Correction Begins
        else:
            Expiration_Date.append(x[1])

    cursor1.execute(
        "select distinct Exclusivity_Date from Exclusivity_Data Where Appl_No='"+ApplicationNumber1+"'")
    myresult1 = cursor1.fetchall()
    for y in myresult1:
        foundFlag=True
        Exclusivity_Date.append(y[0])

    PatentNo = Patent_No
    ExpirationDate = Expiration_Date
    ExclusivityDate = Exclusivity_Date

    PatentNameList=''
    patentNoList=''
    expirationDateList=''
    exclusivityDateList=''
    if len(PatentNo) > 0:   
        for index, PaNumber in enumerate(PatentNo):
            # if len(PaNumber) <= index:
            #     patentNo = ''
            # else:
            #     patentNo = PaNumber
            if PaNumber == None:
                patentNo = ''
            else:
                patentNo = PaNumber
            if len(ExpirationDate) <= index:
                expirationDate = ''
            else:
                expirationdate_obj = datetime.strptime(
                    str(ExpirationDate[index]), '%m/%d/%Y')
                expirationDate = expirationdate_obj.strftime('%d-%b-%Y')
            if len(ExclusivityDate) <= index:
                exclusivityDate = ''
            else:
                expirationdate_obj = datetime.strptime(
                    str(ExclusivityDate[index]), '%m/%d/%Y')
                exclusivityDate = expirationdate_obj.strftime('%d-%b-%Y')

            PatentNameList=PatentNameList+PatentName+'; '
            patentNoList=patentNoList+patentNo +'; '
            expirationDateList=expirationDateList+expirationDate +'; '
            exclusivityDateList=exclusivityDateList+ exclusivityDate +'; '
        
        PatentNameList= FormatText(PatentNameList)
        patentNoList=FormatText(patentNoList)
        expirationDateList=FormatText(expirationDateList)
        exclusivityDateList=FormatText(exclusivityDateList)
        
        if foundFlag==True:
            cursor.execute(
                'INSERT INTO PatentExclusivity_Data(DailyMedId,Patent_Name,Patent_No,Expiration_Date,Exclusivity_Date) VALUES (?,?,?,?,?)',
                (DailyMedId, PatentNameList, patentNoList, expirationDateList, exclusivityDateList)
            )
            conn.commit()
    else:
        for index, exclusivityDate in enumerate(ExclusivityDate):
            # if len(PaNumber) <= index:
            #     patentNo = ''
            # else:
            #     patentNo = PaNumber
            if len(PatentNo) <= index:
                patentNo = ''
            else:
                patentNo = PatentNo[index]
            if len(ExpirationDate) <= index:
                expirationDate = ''
            else:
                expirationdate_obj = datetime.strptime(
                    str(ExpirationDate[index]), '%m/%d/%Y')
                expirationDate = expirationdate_obj.strftime('%d-%b-%Y')
            if len(ExclusivityDate) <= index:
                exclusivityDate = ''
            else:
                expirationdate_obj = datetime.strptime(
                    str(ExclusivityDate[index]), '%m/%d/%Y')
                exclusivityDate = expirationdate_obj.strftime('%d-%b-%Y')

            PatentNameList=PatentNameList+PatentName+'; '
            patentNoList=patentNoList+patentNo +'; '
            expirationDateList=expirationDateList+expirationDate +'; '
            exclusivityDateList=exclusivityDateList+ exclusivityDate +'; '    
        
        PatentNameList= FormatText(PatentNameList)
        patentNoList=FormatText(patentNoList)
        expirationDateList=FormatText(expirationDateList)
        exclusivityDateList=FormatText(exclusivityDateList)
      
        if foundFlag==True:
            cursor.execute(
                'INSERT INTO PatentExclusivity_Data(DailyMedId,Patent_Name,Patent_No,Expiration_Date,Exclusivity_Date) VALUES (?,?,?,?,?)',
                (DailyMedId, PatentNameList, patentNoList, expirationDateList, exclusivityDateList)
            )
            conn.commit()

def FormatText(input):
    output=input
    while(output.endswith("; ")):
        output= output[:-2]
    return output   

@home_bp.route('/salesDataUpload',methods=['POST'])
def salesDataUpload():
    data = pd.read_excel(request.files['InputFile'])
    for i in range(len(data)):
        Country=str(data.iloc[i]['Country']).replace('nan','')
        Sector=str(data.iloc[i]['Sector']).replace('nan','')
        Region=str(data.iloc[i]['Region']).replace('nan','')
        Sub_Region=str(data.iloc[i]['Sub_Region']).replace('nan','')
        Corporation=str(data.iloc[i]['Corporation']).replace('nan','')
        Manufacturer=str(data.iloc[i]['Manufacturer']).replace('nan','')
        Int_Product=str(data.iloc[i]['Int_Product']).replace('nan','')
        Int_Rx_Status=str(data.iloc[i]['Int_Rx_Status']).replace('nan','')
        Molecule_List=str(data.iloc[i]['Molecule_List']).replace('nan','')
        Molecule=str(data.iloc[i]['Molecule']).replace('nan','')
        NFC123=str(data.iloc[i]['NFC123']).replace('nan','')
        Int_Strength=str(data.iloc[i]['Int_Strength']).replace('nan','')
        Int_Pack=str(data.iloc[i]['Int_Pack']).replace('nan','')
        Int_Pack_Size=str(data.iloc[i]['Int_Pack_Size']).replace('nan','')
        Int_Pack_Vol=str(data.iloc[i]['Int_Pack_Vol']).replace('nan','')
        Salt=str(data.iloc[i]['Salt']).replace('nan','')
        Estimated_Date_Protection_Expiry=str(data.iloc[i]['Estimated_Date_Protection_Expiry']).replace('nan','')
        Inovation_Insights=str(data.iloc[i]['Inovation_Insights']).replace('nan','')
        Patent_Expiry_Date=str(data.iloc[i]['Patent_Expiry_Date']).replace('nan','')
        Counting_Units_2016=str(data.iloc[i]['Counting_Units_2016']).replace('nan','')
        US_Dollar_MNF_2016=str(data.iloc[i]['US_Dollar_MNF_2016']).replace('nan','')
        Counting_Units_2017=str(data.iloc[i]['Counting_Units_2017']).replace('nan','')
        US_Dollar_MNF_2017=str(data.iloc[i]['US_Dollar_MNF_2017']).replace('nan','')
        Counting_Units_2018=str(data.iloc[i]['Counting_Units_2018']).replace('nan','')
        US_Dollar_MNF_2018=str(data.iloc[i]['US_Dollar_MNF_2018']).replace('nan','')
        cursor = conn.cursor()
        cursor.execute(
            'insert into Sales_Data_Input(Country,Sector,Region,Sub_Region,Corporation,Manufacturer,Int_Product,Int_Rx_Status,Molecule_List,Molecule,NFC123,Int_Strength,Int_Pack,Int_Pack_Size,Int_Pack_Vol,Salt,Estimated_Date_Protection_Expiry,Inovation_Insights,Patent_Expiry_Date,Counting_Units_2016,US_Dollar_MNF_2016,Counting_Units_2017,US_Dollar_MNF_2017,Counting_Units_2018,US_Dollar_MNF_2018) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (Country,Sector,Region,Sub_Region,Corporation,Manufacturer,Int_Product,Int_Rx_Status,Molecule_List,Molecule,NFC123,Int_Strength,Int_Pack,Int_Pack_Size,Int_Pack_Vol,Salt,Estimated_Date_Protection_Expiry,Inovation_Insights,Patent_Expiry_Date,Counting_Units_2016,US_Dollar_MNF_2016,Counting_Units_2017,US_Dollar_MNF_2017,Counting_Units_2018,US_Dollar_MNF_2018))
        conn.commit()
    return jsonify({'statusCode':'200', 'message':'Sales data imported sucessfully'})

@home_bp.route('/replaceCompanyName',methods=['POST'])
def replaceCompanyName():
    oldCompanyName=request.json["oldCompanyName"].replace("'","''")
    newCompanyName=request.json["newCompanyName"].replace("'","''")
    cursor = conn.cursor()
    cursor.execute("update Us_Fda_Data set Company='"+newCompanyName+"' where Company='"+oldCompanyName+"'")
    cursor.execute("update Daily_Med_Data set Company_Name='"+newCompanyName+"' where Company_Name='"+oldCompanyName+"'")
    cursor.execute("update sales_data_input set Corporation='"+newCompanyName+"' where Corporation='"+oldCompanyName+"'")
    cursor.execute("update sales_data_input set Manufacturer='"+newCompanyName+"' where Manufacturer='"+oldCompanyName+"'")
    cursor.execute("update Therapy_Index_USFDA_Data set Company='"+newCompanyName+"' where Company='"+oldCompanyName+"'")
    conn.commit()
    return jsonify({'statusCode':'200', 'message':'Company name replaced successfully'})
