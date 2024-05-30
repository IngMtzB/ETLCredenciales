class Table:
    def __init__(self,data=None,numeroempleado=None,reciverEmail=None) :
        print("Table class created")
        if(data != None):
            self.data = data
        if(numeroempleado != None):
            self.numeroempleado = numeroempleado
        if(reciverEmail!=None):
            self.reciverEmail=reciverEmail
        

    def getTableContent(self):
        try:
            data = self.data
            tableBody = """"""

            for connectionData in data:
                tableBody += f"""
                        <tr>
                            <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center"><b>
                                {connectionData}
                            </b></td>
                            <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center">
                                {self.data[connectionData]['daysleft']}
                            </td>
                            <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center">
                                {self.data[connectionData]['valuntil']}
                            </td>
                        </tr>
                        """
            body = f"""
                <div class="centerFlex">
                    <div class="two">
                        <h1>Credenciales BD N° empleado:{self.numeroempleado} <span>Favor de no responder</span></h1>
                    </div>
                </div>
                <div class="two">
                        <h2>Correo: {self.reciverEmail}</span></h2>
                    </div>
                <div class="centerFlex">
                    <table class="styled-table">
                        <thead>
                            <th>Base de datos</th>
                            <th>Días restantes</th>
                            <th>Fecha de expiración</th>
                        </thead>
                        <tbody>"""+f"{tableBody}"+"""
                        </tbody>
                    </table>
                    <h2></h2>
                </div>
            """
            return body
        except Exception as e:
            print(f"CLASS: getTableContent / Message: {e}")

    def getTableContentOwner(self,mailSended,employeesNotNeedSendEmail):
        tableNotSended = """"""
        try:
            for user in employeesNotNeedSendEmail:
                dataTableLoop = """"""
                for dbData in employeesNotNeedSendEmail[user]:
                    dataTableLoop += f"""
                            <tr>
                                <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center"><b>
                                    {dbData}
                                </b></td>
                                <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center">
                                    {employeesNotNeedSendEmail[user][dbData]['daysleft']}
                                </td>
                                <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center">
                                    {employeesNotNeedSendEmail[user][dbData]['valuntil']}
                                </td>
                            </tr>
                            """
                tableNotSended += f"""<div>
                    <div class="two">
                        <h2>Correo: {user}</span></h2>
                    </div>
                    <table class="styled-table">
                        <thead>
                            <th>Base de datos</th>
                            <th>Días restantes</th>
                            <th>Fecha de expiración</th>
                        </thead>
                        <tbody>"""+f"{dataTableLoop}"+"""
                        </tbody>
                    </table>
                </div>"""
            preBody = f"""
                    <hr class="dashedG">
                    <div class="centerFlex">
                        <div class="two">
                            <h1>Correos enviados </span></h1>
                        </div>
                    </div>
                    <hr class="dashedG">
                    {mailSended}
                        """
            preBody += f"""
                    <hr class="dashedR">
                    <div class="centerFlex">
                        <div class="two">
                            <h1>Correos NO enviados </span></h1>
                        </div>
                    </div>
                    <hr class="dashedR">
                    {tableNotSended}
                        """
            return preBody

        except Exception as e:
            print(f'Error: {e}')

    def getTableContentOwnerWhenError(self,errors):
        tableWithErrors = """"""
        try:
            for databases in errors:
                dataTableLoop = """"""
              
                dataTableLoop += f"""
                        <tr>
                            <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center"><b>
                                {databases}
                            </b></td>
                            <td class="esd-block-text es-p15t es-p15b es-p20r es-p20l" align="center">
                                {errors[databases]}
                            </td>
                        </tr>
                            """
                tableWithErrors += f"""<div>

                    <table class="styled-table">
                        <thead>
                            <th>Base de datos</th>
                            <th>Mensaje:</th>
                        </thead>
                        <tbody>"""+f"{dataTableLoop}"+"""
                        </tbody>
                    </table>
                </div>"""

            preBody = f"""
                    <hr class="dashedR">
                    <div class="centerFlex">
                        <div class="two">
                            <h1>Errores en conexión a base de datos</span></h1>
                        </div>
                    </div>
                    <hr class="dashedR">
                    {tableWithErrors}
                        """
            return preBody

        except Exception as e:
            print(f'Error: {e}')
