from Entity.Email import Email
import pandas as pd
import psycopg2

#--Start Declare
print("START")
mailSended = ""
# TV Credentials
usertv=""
passtv=""
hosttv=""
porttv=""
dbtv=""
# T0800 Credentials
usert800=""
passt800=""
hostt800=""
portt800=""
dbt800=""
# CECv2 Credentials
usercev2=""
passcev2=""
hostcev2=""
portcev2=""
dbcev2=""
#Vas used to send a list of mails sended and not
employeesNeedSendEmail = {}
employeesNotNeedSendEmail = {}
#All data from users
employeenumers = [{}]
print('Reading data from sheet')
dataFromCSV = pd.read_csv('C:/Users/carlos.martinezb/Documents/ETL/Python/Tools/Database/ETL_credenciales/UsersETLCredencialesDB.csv')
#print(dataFromCSV.to_string()) 
print('Data readed')
#Query
query = """SELECT usename,valuntil, 
(valuntil::DATE - NOW()::DATE) AS daysleft
FROM pg_user 
WHERE usename ~ (%s);"""
proccess = {"isError":False,"message":{}}

#define dictionary
userCredentialsExpireData = {}
usersNumberEmployee = ""
dataFromCSV['daysleft_TV'] = -1
dataFromCSV['dayexpire_TV'] = None
dataFromCSV['daysleft_T800'] = -1
dataFromCSV['dayexpire_T800'] = None
dataFromCSV['daysleft_CCV2'] = -1
dataFromCSV['dayexpire_CCV2'] = None

# Add all employee number found in csv file to a single string
for ind in dataFromCSV.index:
    if(ind !=(len(dataFromCSV.index)-1)):
        usersNumberEmployee += (f"{dataFromCSV['NumeroEmpleado'][ind]}|")
        
    else:
        usersNumberEmployee += (f"{dataFromCSV['NumeroEmpleado'][ind]}")

if(usersNumberEmployee==""):
    print("No se encontró numero de empleados en el csv")

##############              TIENDA VIRTUAL              ##############
try:
    #establishing the connection
    connTV = psycopg2.connect(database=dbtv, user=usertv, password=passtv, host=hosttv, port=porttv)
    cursorTV = connTV.cursor()
    cursorTV.execute(query,[usersNumberEmployee])
    #Fetching 1st row from the table
    dataFetchedFromTV = cursorTV.fetchall()
    cursorTV.close()
    print('Data fetched from database TV')
    print(dataFetchedFromTV)
except Exception as e:
    print(f"Error en la transacción SQL: {e}")
    proccess.update({"isError":True})
    proccess["message"]["Tiendavirtual"] = f"{e}"
    pass
    
##############              TIENDA 800              ##############
try:
    #establishing the connection
    connT800 = psycopg2.connect(database=dbt800, user=usert800, password=passt800, host=hostt800, port=portt800)
    cursorT800 = connT800.cursor()
    cursorT800.execute(query,[usersNumberEmployee])
    #Fetching 1st row from the table
    dataFetchedFromT800 = cursorT800.fetchall()
    cursorT800.close()
    print('Data fetched from database Tienda 800')
    print(dataFetchedFromT800)
except Exception as e:
    print(f"Error en la transacción SQL Tienda 800: {e}")
    proccess.update({"isError":True})
    proccess["message"]["Tienda800"]= f"{e}"
    pass 
##############              CORREOSECOMMERCEV2              ##############
try:
    #establishing the connection
    connCCV2 = psycopg2.connect(database=dbcev2, user=usercev2, password=passcev2, host=hostcev2, port=dbcev2)
    cursorCCV2 = connCCV2.cursor()
    cursorCCV2.execute(query,[usersNumberEmployee])
    #Fetching 1st row from the table
    dataFetchedFromCCV2 = cursorCCV2.fetchall()
    cursorCCV2.close()
    print('Data fetched from database Correosecommercev2')
    print(dataFetchedFromCCV2)
except Exception as e:
    print(f"Error en la transacción SQL Correosecommercev2: {e}")
    proccess.update({"isError":True})
    proccess["message"]["correosecommercev2"]= f"{e}"
    pass

if(proccess["isError"] == False):
    dataFrameTV = dataFromCSV.copy()

    #Get each element founded in TV database
    try:
        for ind in range(len(dataFetchedFromTV)):
            # Try to find if any of the employee numbers in the csv are in data fetched from the database
            for ind2 in dataFromCSV.index:
                # If found, then associate it with email to 
                if str(dataFromCSV['NumeroEmpleado'][ind2]) in dataFetchedFromTV[ind]:
                    #Assign the new values to the column named daysleft in the data frame
                    dataFromCSV.loc[ind2,'daysleft_TV'] = dataFetchedFromTV[ind][2]
                    #Assign the new values to the column named dayexpire in the data frame
                    dataFromCSV.loc[ind2,'dayexpire_TV'] = dataFetchedFromTV[ind][1]
                    #if str(dataFromCSV['NumeroEmpleado'][ind2]) == dataFetchedFromTV[ind]:

        #Get each element founded in T800 database
        for ind in range(len(dataFetchedFromT800)):
            # Try to find if any of the employee numbers in the csv are in data fetched from the database
            for ind2 in dataFromCSV.index:
                # If found, then associate it with email to 
                if str(dataFromCSV['NumeroEmpleado'][ind2]) in dataFetchedFromT800[ind]:
                    #print(f"Found: {dataFromCSV['NumeroEmpleado'][ind2]}")
                    #Assign the new values to the column named daysleft in the data frame
                    dataFromCSV.loc[ind2,'daysleft_T800'] = dataFetchedFromT800[ind][2]
                    #Assign the new values to the column named dayexpire in the data frame
                    dataFromCSV.loc[ind2,'dayexpire_T800'] = dataFetchedFromT800[ind][1]

        #Get each element founded in T800 database
        for ind in range(len(dataFetchedFromCCV2)):
            # Try to find if any of the employee numbers in the csv are in data fetched from the database
            for ind2 in dataFromCSV.index:
                # If found, then associate it with email to 
                if str(dataFromCSV['NumeroEmpleado'][ind2]) in dataFetchedFromCCV2[ind]:
                    #print(f"Found: {dataFromCSV['NumeroEmpleado'][ind2]}")
                    #Assign the new values to the column named daysleft in the data frame
                    dataFromCSV.loc[ind2,'daysleft_CCV2'] = dataFetchedFromCCV2[ind][2]
                    #Assign the new values to the column named dayexpire in the data frame
                    dataFromCSV.loc[ind2,'dayexpire_CCV2'] = dataFetchedFromCCV2[ind][1]
    except Exception  as e:
        proccess.update({"isError":True})
        proccess["message"]["dataferchedLoop"]= f"{e}"
        pass
    #Convert to list to reduce resources when loop all data
    dataFromCSVList = dataFromCSV.values.tolist()
    print("Finish to assing values")
    #Get length  loop data
    length = len(dataFromCSV)
    #loop data to send email to user

    
    if(length>0):
        for position in range(length):
            employee = {}
            try:
                needToSendMail = False
                priorityMail = 0
                #Use a dictionary and assing values for each loop
                employee.update ({
                            "tiendavirtual":{"valuntil":dataFromCSVList[position][3],"daysleft":dataFromCSVList[position][2]},
                            "tienda800":{"valuntil":dataFromCSVList[position][5],"daysleft":dataFromCSVList[position][4]},
                            "correosecommercev2":{"valuntil":dataFromCSVList[position][7],"daysleft":dataFromCSVList[position][6]}
                            })
                daysleft = [dataFromCSVList[position][2],dataFromCSVList[position][4],dataFromCSVList[position][6]]
                lowestDayLeft = min(daysleft)


                #check if any of the days needs to trigger the email sender

                #-1 means that permissions have expired, mail must be sent with high priority
                if(lowestDayLeft <= -1 ):
                    priorityMail = 5
                    needToSendMail = True
                #0 means that permissions expire today and priority is number 4
                elif (lowestDayLeft == 0):
                    priorityMail = 4
                    needToSendMail = True
                #1-2 priority 2, means that permits expire in the next 3 days and mail must be sent
                elif (lowestDayLeft >= 1) and (lowestDayLeft <= 2):
                    priorityMail = 3
                    needToSendMail = True
                #3-5 days, priority 2, means that permits are close to expire
                elif (lowestDayLeft >= 3) and (lowestDayLeft <= 4):
                    priorityMail = 2
                    needToSendMail = True
                #more than 5 days email shouldn't be triggered
                elif (lowestDayLeft >4):
                    priorityMail = 0 
                    needToSendMail = False
                #non of the above cases, so, mail must not be sended, only to notify to the owner
                else:
                    priorityMail = -1
                    needToSendMail = False

                #--------------------------------------------------------------------------------SEND MAIL-------------------------------------------------------------------------------------#
                if(needToSendMail == True):
                    email = Email(dataFromCSVList[position][1],dataFromCSVList[position][0],priorityMail,lowestDayLeft,employee)
                    tempMailSended=email.sendMailTo()
                    mailSended+=tempMailSended
                    print(f"END: sended with priority {priorityMail}, success")
                    #Add to a dictionary every employee that will recive a email
                    employeesNeedSendEmail[dataFromCSVList[position][1]]=employee
                else:
                    print(f"priority: {priorityMail}")
                    print(f"END: email not sended because priorityMail is {priorityMail}, transaction success")
                    #Add to a dictionary every employee that will not recive a email
                    employeesNotNeedSendEmail[dataFromCSVList[position][1]]=employee
                #FALTA VALIDAR DÍAS QUE NO SE REPITAN CORREOS DE URGENCIA
                
            except Exception as e:
                print(f'CLASS: Main / General error {e}')  
                proccess.update({"isError":True})
                proccess["message"]["emailconstruction"]= f"{e}"
    else:
        print('no data in dataFromCSV')

    try:
        print("Sending email to owner:")
        email = Email('carlos.martinezb@coppel.com')
        email.sendMailToOwner(mailSended,employeesNotNeedSendEmail)
    except Exception as e:
        print(f'Exception error when trying to send mail to owner {e}')
        proccess.update({"isError":True})
        proccess["message"]["emailtoowner"]= f"{e}"
else:
    email = Email('carlos.martinezb@coppel.com')
    email.sendMailToOwnerWhenError(proccess["message"])
#Agregar colores en caso de que falten x días, ejemplo; rojo o amarillo dependiendo de prioridad