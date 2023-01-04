# import datetime
import logging
# from datetime import datetime
import json
import pyodbc as po
import requests
import azure.functions as func
# import json
import os
import datetime as dt
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ClientAuthenticationError



def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = dt.datetime.utcnow().replace(
        tzinfo=dt.timezone.utc).isoformat()
    

    # vault_url = "https://mecpgovframework-kv01.vault.azure.net/"
    # credential = DefaultAzureCredential()
    # logging.info('Created managed identity.')

    # secret_client = SecretClient(vault_url=vault_url, credential=credential)
    # logging.info('Created secret client.')

    # retrieved_secret = secret_client.get_secret("mecpBearertokenArtifactoryDataTransferStorage011")
    # logging.info('Got secret from Key Vault.')

    # print (f"mecpBearertokenArtifactoryDataTransferStorage011 is set to  {retrieved_secret.value} in key vault.")
    # sent = retrieved_secret.value
    # logging.info(sent)

# def gettoken():    

vault_url = "https://mecpgovframework-kv01.vault.azure.net/"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=vault_url, credential=credential)
retrieved_secret = secret_client.get_secret("mecpBearertokenArtifactoryDataTransferStorage011")
print (f"mecpBearertokenArtifactoryDataTransferStorage011 is set to  {retrieved_secret.value} in key vault.")
sent = retrieved_secret.value
print(sent)
# logging.info(sent)

def getrepo():
    payload = []
    logging.info('We are in get repo function')

    headers = { "Authorization": 'sent' }
    
            #"Accept": "application/vnd.github+json"}
    url = "https://mcd.jfrog.io/artifactory" 
    # token = os.getenv['secret']
    resp = requests.get(url,headers=headers,data=payload)
    payloadList = resp.json()
    print(type(payloadList))
    result = resp.content
    list1 = json.loads(result)
    insert_data_into_table(payloadList)
    return payloadList 

def insert_data_into_table(payloadList):
    for i in range(0,len(payloadList["repositoriesSummaryList"])-1):
       
        repo_info= {}
        # print(team_name)
        repo_info["repoKey"]= payloadList["repositoriesSummaryList"][i]["repoKey"]
        repo_info["repoType"]= payloadList["repositoriesSummaryList"][i]["repoType"]
        repo_info["projectKey"] = payloadList["repositoriesSummaryList"][i]["projectKey"]
        repo_info["foldersCount"] = payloadList["repositoriesSummaryList"][i] ["foldersCount"]
        repo_info["filesCount"] = payloadList["repositoriesSummaryList"][i]["filesCount"]
        repo_info["usedSpace"] = payloadList["repositoriesSummaryList"][i]["usedSpace"]
        repo_info["usedSpaceInBytes"] = payloadList["repositoriesSummaryList"][i]["usedSpaceInBytes"]
        repo_info["itemsCount"] = payloadList["repositoriesSummaryList"][i]["itemsCount"]
        repo_info["packageType"] = payloadList["repositoriesSummaryList"][i]["packageType"]
        repo_info["percentage"] = payloadList["repositoriesSummaryList"][i]["percentage"]

        now = dt.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        data = [dt_string,repo_info["repoKey"],repo_info["repoType"],repo_info["foldersCount"],repo_info["filesCount"],repo_info["usedSpace"],repo_info["usedSpaceInBytes"],repo_info["packageType"],repo_info["projectKey"],repo_info["percentage"]]
        print(data)
        print(dt_string +" , "+ repo_info["repoKey"] + " , " + repo_info["repoType"]+ " , " + repo_info["projectKey"]+ " , " + (repo_info["foldersCount"]) + " , " + (repo_info["filesCount"]) + " , " + (repo_info["usedSpace"]) + " , " + (repo_info["usedSpaceInBytes"]) + " , " + (repo_info["itemsCount"]) + " , " + repo_info["packageType"] + " , " + repo_info["percentage"] )        
        server = 'tcp:mecpgovframework01.database.windows.net'
        database ='mecpgovframeworkdb01'
        username = 'gfatadmin01'
        password = 'Password@1234'
        
        cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +server+';DATABASE='+database+';UID='+username+';PWD=' + password)
        cursor = cnxn.cursor()
        # cursor.execute("CREATE TABLE jfrogstoragedata (dateTime VARCHAR(255), repoKey VARCHAR(255), repoType VARCHAR(255), projectKey VARCHAR(255), foldersCount INT(255), filesCount INT(255), usedSpace VARCHAR(255), usedSpaceInBytes INT(255), itemsCount INT(255), packageType VARCHAR(255), percentage INT(255))")
        # query = "INSERT INTO jfrogstoragedata(dateTime, repoKey , repoType, projectKey, foldersCount, filesCount, usedSpace, usedSpaceInBytes, itemsCount, packageType, percentage) VALUES (" + repo_info['repoKey'] + "," + str(repo_info["foldersCount"]) + ","+ repo_info['repoType'] + "," + repo_info['projectKey'] + "," + str(repo_info['filesCount']) + "," + str(repo_info['usedSpace']) + "," + repo_info['usedSpaceInBytes'] + "," + str(repo_info["itemsCount"]) + "," + repo_info['packageType'] + "," + repo_info['percentage'] + ")"
        query = "INSERT INTO Artifactory_Data_Transfer_Storage (dateTime, repoKey , repoType, projectKey, foldersCount, filesCount, usedSpace, usedSpaceInBytes, itemsCount, packageType, percentage) VALUES ('" + dt_string +"','" + repo_info["repoKey"] + "','" + repo_info["repoType"] + "','" + repo_info["projectKey"] + "'," + (repo_info["foldersCount"]) + "," + (repo_info["filesCount"]) + ",'" + (repo_info["usedSpace"]) + "'," + (repo_info["usedSpaceInBytes"]) + "," + (repo_info["itemsCount"]) + ",'" + repo_info["packageType"] + "','" + repo_info["percentage"] + "')"

        # print (query)
        cursor.execute(query)
        cursor.commit()
getrepo()



# def gettoken():    

#     vault_url = "https://mecpgovframework-kv01.vault.azure.net/"
#     credential = DefaultAzureCredential()
#     # credential = ManagedIdentityCredential()
#     secret_client = SecretClient(vault_url=vault_url, credential=credential)
#     retrieved_secret = secret_client.get_secret("mecpBearertokenArtifactoryDataTransferStorage011")
#     print (f"mecpBearertokenArtifactoryDataTransferStorage011 is set to  {retrieved_secret.value} in key vault.")
#     return retrieved_secret.value
# gettoken()



# def new_func(retrieved_secret):
#     return retrieved_secret.value


# def main(mytimer: func.TimerRequest) -> None:
#     utc_timestamp = datetime.datetime.utcnow().replace(
#         tzinfo=datetime.timezone.utc).isoformat()

#     if mytimer.past_due:
#         logging.info('The timer is past due!')

#     logging.info('Python timer trigger function ran at %s', utc_timestamp)


# def getrepo():
#     payload = []
#     logging.info('We are in get repo function')

#     headers = { "Authorization":"token"}
    
#             #"Accept": "application/vnd.github+json"}
#     url = "https://mcd.jfrog.io/artifactory" 
#     # token = os.getenv['secret']
#     resp = requests.get(url, headers=headers,data=payload)
#     payloadList = resp.json()
#     result = resp.content
#     list1 = json.loads(result)
#     # print (payloadList)
#     insert_data_into_table(payloadList)
#     return payloadList 
# # for data in list1:
# #     print (data)

# # with open('payloadrequest.json','wb') as json_file1:
# #     data1 = json_file1.write(response.content)


# def insert_data_into_table(payloadList):
#     for i in range(0,len(payloadList["repositoriesSummaryList"])-1):
       
#         repo_info= {}
#         # print(team_name)s
#         repo_info["dateTime"]= payloadList["repositoriesSummaryList"][i]["dateTime"]
#         repo_info["repoKey"]= payloadList["repositoriesSummaryList"][i]["repoKey"]
#         repo_info["repoType"]= payloadList["repositoriesSummaryList"][i]["repoType"]
#         repo_info["projectKey"] = payloadList["repositoriesSummaryList"][i]["projectKey"]
#         repo_info["foldersCount"] = payloadList["repositoriesSummaryList"][i] ["foldersCount"]
#         repo_info["filesCount"] = payloadList["repositoriesSummaryList"][i]["filesCount"]
#         repo_info["usedSpace"] = payloadList["repositoriesSummaryList"][i]["usedSpace"]
#         repo_info["usedSpaceInBytes"] = payloadList["repositoriesSummaryList"][i]["usedSpaceInBytes"]
#         repo_info["itemsCount"] = payloadList["repositoriesSummaryList"][i]["itemsCount"]
#         repo_info["packageType"] = payloadList["repositoriesSummaryList"][i]["packageType"]
#         repo_info["percentage"] = payloadList["repositoriesSummaryList"][i]["percentage"]

#         now = dt.now()
#         # dd/mm/YY H:M:S
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         data = [dt_string,repo_info["repoKey"],repo_info["repoType"],repo_info["foldersCount"],repo_info["filesCount"],repo_info["usedSpace"],repo_info["usedSpaceInBytes"],repo_info["packageType"],repo_info["projectKey"],repo_info["percentage"]]
#         print(data)
#         print(dt_string +" , "+ repo_info['repoKey'] + " , " + repo_info['repoType']+ " , " + repo_info['projectKey']+ " , " +str(repo_info["foldersCount"]) + " , " +str(repo_info['filesCount']) + " , " + str(repo_info['usedSpace']) + " , " + str(repo_info['usedSpaceInBytes']) + " , " + str(repo_info["itemsCount"]) + " , " + repo_info['packageType'] + " , " + repo_info['percentage'] )        
#         server = 'tcp:mecpgovframework01.database.windows.net'
#         database ='mecpgovframeworkdb01'
#         username = 'gfatadmin01'
#         password = 'Password@1234'
        
#         cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +server+';DATABASE='+database+';UID='+username+';PWD=' + password)
#         cursor = cnxn.cursor()
#         # cursor.execute("CREATE TABLE jfrogstoragedata (dateTime VARCHAR(255), repoKey VARCHAR(255), repoType VARCHAR(255), projectKey VARCHAR(255), foldersCount INT(255), filesCount INT(255), usedSpace VARCHAR(255), usedSpaceInBytes INT(255), itemsCount INT(255), packageType VARCHAR(255), percentage INT(255))")
#         #query = "INSERT INTO jfrogstoragedata(repoKey , repoType, projectKey, foldersCount, filesCount, usedSpace, usedSpaceInBytes, itemsCount, packageType, percentage) VALUES (" + repo_info['repoKey'] + "," + str(repo_info["foldersCount"]) + ","+ repo_info['repoType'] + "," + repo_info['projectKey'] + "," + str(repo_info['filesCount']) + "," + str(repo_info['usedSpace']) + "," + repo_info['usedSpaceInBytes'] + "," + str(repo_info["itemsCount"]) + "," + repo_info['packageType'] + "," + repo_info['percentage'] + ")"
#         query = "INSERT INTO Artifactory_Data_Transfer_Storage(dateTime, repoKey , repoType, projectKey, foldersCount, filesCount, usedSpace, usedSpaceInBytes, itemsCount, packageType, percentage) VALUES ('" + dt_string +"','" + repo_info['repoKey'] + "','" + repo_info['repoType'] + "','" + repo_info['projectKey'] + "'," + str(repo_info["foldersCount"]) + "," + str(repo_info['filesCount']) + ",'" + str(repo_info['usedSpace']) + "'," + str(repo_info['usedSpaceInBytes']) + "," + str(repo_info["itemsCount"]) + ",'" + repo_info['packageType'] + "','" + repo_info['percentage'] + "')"        
#         # # print (query)
#         cursor.execute(query)
#         cursor.commit()
# getrepo()
        
# query = "insert into github_repo_storage_details (dateTime, repoKey , repoType, projectKey, foldersCount, filesCount, usedSpace, usedSpaceInBytes, itemsCount, packageType, percentage) values (?,?,?,?,?,?,?,?,?,?.?)"
# res = mycursor.execute(query, payloadList)
# cursor.commit()
# print(cursor.rowcount)
# print("data inserted", res)
  
# # import datetime
# import logging
# # from datetime import datetime
# import json
# import pyodbc as po
# import requests
# import azure.functions as func
# # import json
# import os
# import datetime as dt
# from azure.identity import DefaultAzureCredential
# # from azure.identity import ManagedIdentityCredential
# from azure.keyvault.secrets import SecretClient
# from azure.core.exceptions import ClientAuthenticationError



# def main(mytimer: func.TimerRequest) -> None:
#     utc_timestamp = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc).isoformat()
#     getrepo()


# def gettoken():    

#     str = 'Bearer eyJ2ZXIiOiIyIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJicThLOGFNUGl5b0o4SGdZNEJXeW8xWVNHQkdkaVdUMUJaemFXdExiVFI4In0.eyJleHQiOiJ7XCJyZXZvY2FibGVcIjpcInRydWVcIn0iLCJzdWIiOiJqZmFjQDAxZmU0bXNoMGdiZnZtMGptcHpiOHkwdzcxXC91c2Vyc1wvbWFub2ouY2hhdWhhbkB1cy5tY2QuY29tIiwic2NwIjoiYXBwbGllZC1wZXJtaXNzaW9uc1wvYWRtaW4iLCJhdWQiOiIqQCoiLCJpc3MiOiJqZmZlQDAwMCIsImV4cCI6MTgxNDEzMDc5MCwiaWF0IjoxNjU2NDUwNzkwLCJqdGkiOiIxYTIwYmVmYi0zMWExLTRiNTQtYWY5NS1lOGM2Yzc5YjZiN2UifQ.c9IeQM6XmdiwypcIKEc3miGFGYIF94pop74-8NKmejAjdOVtTmfQ-YVth5LiKvE85Ph9nAokcgIMvifoAWf5Lvn_qKbqmlSlWHzpsciTIU2BfPorByGP_r0CO9VOV77j3LOnp2vJQ8508B6RKSnU9l-OwhQDNuEGk0B5VnZtErWiLPKUE1qlM0rk-H8vUguByrX-husI7nJCGcz2Oamf-lyHbVkeS0CFo6rxq-U1620NLp4iaWFZZlIXeln5seZGYoVlWafF0ZVLLfk6-ua7xBpzCzq-0YVx0YMSoUgGWUUzXrM29OIRz9EGYEuPAPRcgXZ9B3Oq0xJ8ywHAJhxXwQ'
#     return (str)
   

# def getrepo() -> None:
#     payload = []
#     logging.info('We are in get repo function')
#     token = gettoken()
#     print(token)
#     headers = { "Authorization": token}
    
#             #"Accept": "application/vnd.github+json"}
#     url = "https://mcd.jfrog.io/artifactory" 
#     # token = os.getenv['secret']
#     resp = requests.get(url,headers=headers,data=payload)
#     print(resp)
#     payloadList = resp.json()
#     print(type(payloadList))
#     result = resp.content
#     list1 = json.loads(result)
#     # insert_data_into_table(payloadList)
#     return payloadList 

# def insert_data_into_table(payloadList) -> None:
#     for i in range(0,len(payloadList["repositoriesSummaryList"])-1):
#         repo_info= {}
#         repo_info["repoKey"]= payloadList["repositoriesSummaryList"][i]["repoKey"]
#         repo_info["repoType"]= payloadList["repositoriesSummaryList"][i]["repoType"]
#         repo_info["projectKey"] = payloadList["repositoriesSummaryList"][i]["projectKey"]
#         repo_info["foldersCount"] = payloadList["repositoriesSummaryList"][i] ["foldersCount"]
#         repo_info["filesCount"] = payloadList["repositoriesSummaryList"][i]["filesCount"]
#         repo_info["usedSpace"] = payloadList["repositoriesSummaryList"][i]["usedSpace"]
#         repo_info["usedSpaceInBytes"] = payloadList["repositoriesSummaryList"][i]["usedSpaceInBytes"]
#         repo_info["itemsCount"] = payloadList["repositoriesSummaryList"][i]["itemsCount"]
#         repo_info["packageType"] = payloadList["repositoriesSummaryList"][i]["packageType"]
#         repo_info["percentage"] = payloadList["repositoriesSummaryList"][i]["percentage"]
#         now = dt.now()
#         # dd/mm/YY H:M:S
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         data = [dt_string,repo_info["repoKey"],repo_info["repoType"],repo_info["foldersCount"],repo_info["filesCount"],repo_info["usedSpace"],repo_info["usedSpaceInBytes"],repo_info["packageType"],repo_info["projectKey"],repo_info["percentage"]]
#         print(data)
#         print(dt_string +" , "+ repo_info["repoKey"] + " , " + repo_info["repoType"]+ " , " + repo_info["projectKey"]+ " , " + (repo_info["foldersCount"]) + " , " + (repo_info["filesCount"]) + " , " + (repo_info["usedSpace"]) + " , " + (repo_info["usedSpaceInBytes"]) + " , " + (repo_info["itemsCount"]) + " , " + repo_info["packageType"] + " , " + repo_info["percentage"] )        
#         server = 'tcp:mecpgovframework01.database.windows.net'
#         database ='mecpgovframeworkdb01'
#         username = 'gfatadmin01'
#         password = 'Password@1234'
#         cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +server+';DATABASE='+database+';UID='+username+';PWD=' + password)
#         cursor = cnxn.cursor()
#         # cursor.execute("CREATE TABLE jfrogstoragedata (dateTime VARCHAR(255), repoKey VARCHAR(255), repoType VARCHAR(255), projectKey VARCHAR(255), foldersCount INT(255), filesCount INT(255), usedSpace VARCHAR(255), usedSpaceInBytes INT(255), itemsCount INT(255), packageType VARCHAR(255), percentage INT(255))")
#         # query = "INSERT INTO jfrogstoragedata(dateTime, repoKey , repoType, projectKey, foldersCount, filesCount, usedSpace, usedSpaceInBytes, itemsCount, packageType, percentage) VALUES (" + repo_info['repoKey'] + "," + str(repo_info["foldersCount"]) + ","+ repo_info['repoType'] + "," + repo_info['projectKey'] + "," + str(repo_info['filesCount']) + "," + str(repo_info['usedSpace']) + "," + repo_info['usedSpaceInBytes'] + "," + str(repo_info["itemsCount"]) + "," + repo_info['packageType'] + "," + repo_info['percentage'] + ")"
#         query = "INSERT INTO Artifactory_Data_Transfer_Storage (dateTime, repoKey , repoType, projectKey, foldersCount, filesCount, usedSpace, usedSpaceInBytes, itemsCount, packageType, percentage) VALUES ('" + dt_string +"','" + repo_info["repoKey"] + "','" + repo_info["repoType"] + "','" + repo_info["projectKey"] + "'," + (repo_info["foldersCount"]) + "," + (repo_info["filesCount"]) + ",'" + (repo_info["usedSpace"]) + "'," + (repo_info["usedSpaceInBytes"]) + "," + (repo_info["itemsCount"]) + ",'" + repo_info["packageType"] + "','" + repo_info["percentage"] + "')"
#         # print (query)
#         cursor.execute(query)
#         cursor.commit()
