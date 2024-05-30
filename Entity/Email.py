import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Entity.Table import Table

#True -->No envia correos a usuarios
#False -->Envía correos a usuarios
isTestNotSendEmail=False

class Email:
    
    def __init__(self,reciverEmail=None,numeroempelado=None,priorityMail=None,lowestDayLeft=None,data=None):
        print("Email class created")
        if(reciverEmail != None):
            self.reciverEmail = reciverEmail
        if(numeroempelado != None):
            self.numeroempleado = numeroempelado
        if(priorityMail != None):
            self.priorityMail = priorityMail
        if(lowestDayLeft != None):
            self.lowestDayLeft = lowestDayLeft
        if(data != None):
            self.data = data



    def getPriorityMessage(self): 
        subject = ""
        if(self.priorityMail == 2):
            subject = "Fecha de vencimiento de credenciales"
        elif(self.priorityMail == 3):
            subject = f"Credencial vence en {self.lowestDayLeft} días"
        elif(self.priorityMail == 4):
            subject = "¡¡¡URGENTE!!! CREDENCIALES VENCEN HOY"  
        elif(self.priorityMail == 5):
            subject = "¡¡¡URGENTE!!! CREDENCIALES VENCIDAS"
        else:
            subject = "Fecha de vencimiento de credenciales" 
        return subject

    def sendMailTo(self):
        try:
            table = Table(self.data,self.numeroempleado,self.reciverEmail)
            body = table.getTableContent()
            print(f"--Trying to sent email to: {self.reciverEmail}")
            sender = "carlos.martinezb@coppel.com"
            senderpass ="oixy lnau vhdg klpj"

            html = """
                <html lang="en">
                <head>
                <style>
                    .body {
                        text-align: center;
                    }
                    .styled-table {
                        text-align: center;
                        border-collapse: collapse;
                        margin: 25px 0;
                        font-size: 0.9em;
                        font-family: sans-serif;
                        width: 100%;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                    }
                    .styled-table thead tr {
                        background-color: #1c9de7;
                        color: #ffffff;
                        text-align: center;
                    }
                    .styled-table th,
                    .styled-table td {
                        padding: 12px 15px;
                    }
                    .styled-table tbody tr {
                        text-align: center;
                        border-bottom: 1px solid #dddddd;
                        text-align: center;
                    }
                    .styled-table tbody tr:nth-of-type(even) {
                        background-color: #f3f3f3;
                    }
                    .styled-table tbody tr:last-of-type {
                        border: 2px solid #1c9de7;
                    }
                    .styled-table tbody tr.active-row {
                        font-weight: bold;
                        color: #009879;
                    }
                    .centerFlex {
                        align-items: center;
                        display: flex;
                        justify-content: center;
                    } 
                    h1 {
                        position: relative;
                        padding: 0;
                        margin: 0;
                        font-family: "Raleway", sans-serif;
                        font-weight: 300;
                        font-size: 40px;
                        color: #080808;
                        -webkit-transition: all 0.4s ease 0s;
                        -o-transition: all 0.4s ease 0s;
                        transition: all 0.4s ease 0s;
                    }
                    h1 span {
                        display: block;
                        font-size: 0.5em;
                        line-height: 1.3;
                    }
                    h1 em {
                        font-style: normal;
                        font-weight: 600;
                    }
                    .two h1 {
                        text-transform: capitalize;
                        text-align: center;
                    }
                    .two h1 span {
                        font-size: 13px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 4px;
                        line-height: 3em;
                        padding-left: 0.25em;
                        color: rgba(0, 0, 0, 0.4);
                        padding-bottom: 10px;
                        text-align: center;
                    }
                    

                    h2 {
                        position: relative;
                        padding: 0;
                        margin: 0;
                        font-family: "Raleway", sans-serif;
                        font-weight: 300;
                        font-size: 20px;
                        color: #080808;
                        -webkit-transition: all 0.4s ease 0s;
                        -o-transition: all 0.4s ease 0s;
                        transition: all 0.4s ease 0s;
                        letter-spacing: -0.9px;
                    }
                    h2 span {
                        display: block;
                        font-size: 0.5em;
                        line-height: 1.3;
                    }
                    h2 em {
                        font-style: normal;
                        font-weight: 600;
                    }
                    .two h2 {
                        text-align: center;
                    }
                    .two h2 span {
                        font-size: 13px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 4px;
                        line-height: 3em;
                        padding-left: 0.25em;
                        color: rgba(0, 0, 0, 0.4);
                        padding-bottom: 10px;
                        text-align: center;
                    }

                    /* Dashed border */
                    hr.dashedG {
                    border-top: 3px dashed #00ff08;
                    }

                    /* Dotted border */
                    hr.dashedR {
                    border-top: 3px dashed #ff0000;
                    }

                    /* Solid border */
                    hr.solid {
                    border-top: 3px solid #bbb;
                    }

                    /* Rounded border */
                    hr.rounded {
                    border-top: 60px solid #ffffff;
                    border-radius: 5px;
                    }
                </style>
                </head>
                <body>
                """+f"{body}"+"""
                </body>
                </html>
            """
            msg = MIMEMultipart('alternative')
            msg['From'] = sender
            msg['To'] = self.reciverEmail
            msg['Subject'] = self.getPriorityMessage()
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            if(isTestNotSendEmail == False):
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.ehlo('lowercase')
                    server.starttls()
                    server.ehlo('lowercase')
                    print("---Tryng to Login") 
                    server.login(sender, senderpass, initial_response_ok=True)      
                    print("---Loggin Success")
                    server.ehlo()
                    server.sendmail(sender, self.reciverEmail, msg.as_string())
                    print('Email sent!')
                    server.close()
            else:
                print(f"Email not sended to {self.reciverEmail} beauce is a test")
            return body  
        except Exception as e:
            print(f"CLASS: sendaMailTo / Message: {e}, success")

    def sendMailToOwner(self,mailSended,employeesNotNeedSendEmail,):
        try:
            table = Table()
            body = table.getTableContentOwner(mailSended,employeesNotNeedSendEmail)
            sender = "carlos.martinezb@coppel.com"
            senderpass ="oixy lnau vhdg klpj"

            html = """
                <html lang="en">
                <head>
                <style>
                    .body {
                        text-align: center;
                    }
                    .styled-table {
                        text-align: center;
                        border-collapse: collapse;
                        margin: 25px 0;
                        font-size: 0.9em;
                        font-family: sans-serif;
                        width: 100%;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                    }
                    .styled-table thead tr {
                        background-color: #1c9de7;
                        color: #ffffff;
                        text-align: center;
                    }
                    .styled-table th,
                    .styled-table td {
                        padding: 12px 15px;
                    }
                    .styled-table tbody tr {
                        text-align: center;
                        border-bottom: 1px solid #dddddd;
                        text-align: center;
                    }
                    .styled-table tbody tr:nth-of-type(even) {
                        background-color: #f3f3f3;
                    }
                    .styled-table tbody tr:last-of-type {
                        border: 2px solid #1c9de7;
                    }
                    .styled-table tbody tr.active-row {
                        font-weight: bold;
                        color: #009879;
                    }
                    .centerFlex {
                        align-items: center;
                        display: flex;
                        justify-content: center;
                    } 
                    h1 {
                        position: relative;
                        padding: 0;
                        margin: 0;
                        font-family: "Raleway", sans-serif;
                        font-weight: 300;
                        font-size: 40px;
                        color: #080808;
                        -webkit-transition: all 0.4s ease 0s;
                        -o-transition: all 0.4s ease 0s;
                        transition: all 0.4s ease 0s;
                    }
                    h1 span {
                        display: block;
                        font-size: 0.5em;
                        line-height: 1.3;
                    }
                    h1 em {
                        font-style: normal;
                        font-weight: 600;
                    }
                    .two h1 {
                        text-transform: capitalize;
                        text-align: center;
                    }
                    .two h1 span {
                        font-size: 13px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 4px;
                        line-height: 3em;
                        padding-left: 0.25em;
                        color: rgba(0, 0, 0, 0.4);
                        padding-bottom: 10px;
                        text-align: center;
                    }
                    

                    h2 {
                        position: relative;
                        padding: 0;
                        margin: 0;
                        font-family: "Raleway", sans-serif;
                        font-weight: 300;
                        font-size: 20px;
                        color: #080808;
                        -webkit-transition: all 0.4s ease 0s;
                        -o-transition: all 0.4s ease 0s;
                        transition: all 0.4s ease 0s;
                        letter-spacing: -0.9px;
                    }
                    h2 span {
                        display: block;
                        font-size: 0.5em;
                        line-height: 1.3;
                    }
                    h2 em {
                        font-style: normal;
                        font-weight: 600;
                    }
                    .two h2 {
                        text-align: center;
                    }
                    .two h2 span {
                        font-size: 13px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 4px;
                        line-height: 3em;
                        padding-left: 0.25em;
                        color: rgba(0, 0, 0, 0.4);
                        padding-bottom: 10px;
                        text-align: center;
                    }

                    /* Dashed border */
                    hr.dashedG {
                    border-top: 3px dashed #00ff08;
                    }

                    /* Dotted border */
                    hr.dashedR {
                    border-top: 3px dashed #ff0000;
                    }

                    /* Solid border */
                    hr.solid {
                    border-top: 3px solid #bbb;
                    }

                    /* Rounded border */
                    hr.rounded {
                    border-top: 60px solid #ffffff;
                    border-radius: 5px;
                    }
                </style>
                </head>
                <body>
                """+f"{body}"+"""
                </body>
                </html>
            """
            print("---Tryng to send Email")
            msg = MIMEMultipart('alternative')
            msg['From'] = sender
            msg['To'] = sender
            msg['Subject'] = 'Resultado de ETL de credenciales'
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo('lowercase')
                server.starttls()
                server.ehlo('lowercase')
                print("---Tryng to Login") 
                server.login(sender, senderpass, initial_response_ok=True)      
                print("---Loggin Success")
                server.ehlo()
                server.sendmail(sender, self.reciverEmail, msg.as_string())
                print('Email sent!')
                server.close()
            return 0
        except Exception as e:
            print(f"CLASS: sendMailToOwner / Message: {e}")

    def sendMailToOwnerWhenError(self,error):
        for indice in error:
            print("printing indice in error")
            print(error[indice])

        try:
            table = Table()
            sender = "carlos.martinezb@coppel.com"
            senderpass ="oixy lnau vhdg klpj"
            body = table.getTableContentOwnerWhenError(error)
            html = """
                 <html lang="en">
                <head>
                <style>
                    .body {
                        text-align: center;
                    }
                    .styled-table {
                        text-align: center;
                        border-collapse: collapse;
                        margin: 25px 0;
                        font-size: 0.9em;
                        font-family: sans-serif;
                        width: 100%;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                    }
                    .styled-table thead tr {
                        background-color: #1c9de7;
                        color: #ffffff;
                        text-align: center;
                    }
                    .styled-table th,
                    .styled-table td {
                        padding: 12px 15px;
                    }
                    .styled-table tbody tr {
                        text-align: center;
                        border-bottom: 1px solid #dddddd;
                        text-align: center;
                    }
                    .styled-table tbody tr:nth-of-type(even) {
                        background-color: #f3f3f3;
                    }
                    .styled-table tbody tr:last-of-type {
                        border: 2px solid #1c9de7;
                    }
                    .styled-table tbody tr.active-row {
                        font-weight: bold;
                        color: #009879;
                    }
                    .centerFlex {
                        align-items: center;
                        display: flex;
                        justify-content: center;
                    } 
                    h1 {
                        position: relative;
                        padding: 0;
                        margin: 0;
                        font-family: "Raleway", sans-serif;
                        font-weight: 300;
                        font-size: 40px;
                        color: #080808;
                        -webkit-transition: all 0.4s ease 0s;
                        -o-transition: all 0.4s ease 0s;
                        transition: all 0.4s ease 0s;
                    }
                    h1 span {
                        display: block;
                        font-size: 0.5em;
                        line-height: 1.3;
                    }
                    h1 em {
                        font-style: normal;
                        font-weight: 600;
                    }
                    .two h1 {
                        text-transform: capitalize;
                        text-align: center;
                    }
                    .two h1 span {
                        font-size: 13px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 4px;
                        line-height: 3em;
                        padding-left: 0.25em;
                        color: rgba(0, 0, 0, 0.4);
                        padding-bottom: 10px;
                        text-align: center;
                    }
                    

                    h2 {
                        position: relative;
                        padding: 0;
                        margin: 0;
                        font-family: "Raleway", sans-serif;
                        font-weight: 300;
                        font-size: 20px;
                        color: #080808;
                        -webkit-transition: all 0.4s ease 0s;
                        -o-transition: all 0.4s ease 0s;
                        transition: all 0.4s ease 0s;
                        letter-spacing: -0.9px;
                    }
                    h2 span {
                        display: block;
                        font-size: 0.5em;
                        line-height: 1.3;
                    }
                    h2 em {
                        font-style: normal;
                        font-weight: 600;
                    }
                    .two h2 {
                        text-align: center;
                    }
                    .two h2 span {
                        font-size: 13px;
                        font-weight: 500;
                        text-transform: uppercase;
                        letter-spacing: 4px;
                        line-height: 3em;
                        padding-left: 0.25em;
                        color: rgba(0, 0, 0, 0.4);
                        padding-bottom: 10px;
                        text-align: center;
                    }

                    /* Dashed border */
                    hr.dashedG {
                    border-top: 3px dashed #00ff08;
                    }

                    /* Dotted border */
                    hr.dashedR {
                    border-top: 3px dashed #ff0000;
                    }

                    /* Solid border */
                    hr.solid {
                    border-top: 3px solid #bbb;
                    }

                    /* Rounded border */
                    hr.rounded {
                    border-top: 60px solid #ffffff;
                    border-radius: 5px;
                    }
                </style>
                </head>
                <body>
                """+f"{body}"+"""
                </body>
                </html>
            """

            print("---Tryng to send Email to owner beacuse error")
            msg = MIMEMultipart('alternative')
            msg['From'] = sender
            msg['To'] = sender
            msg['Subject'] = 'Error en el ETL de credenciales'
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo('lowercase')
                server.starttls()
                server.ehlo('lowercase')
                print("---Tryng to Login") 
                server.login(sender, senderpass, initial_response_ok=True)      
                print("---Loggin Success")
                server.ehlo()
                server.sendmail(sender, self.reciverEmail, msg.as_string())
                print('Email sent!')
                server.close()
            return 0
        except Exception as e:
            print(f"CLASS: sendMailToOwner / Message: {e}")
