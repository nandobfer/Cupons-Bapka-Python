import mysql.connector, config

class Mysql():
    def __init__(self) -> None:
        pass
    
    def connect(self, auth):
        ''' Try to connect to a database with auth params defined in config file '''
        try:
            self.connection = mysql.connector.connect(host=auth['host'],
                                                database=auth['database'],
                                                user=auth['user'],
                                                password=auth['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                # cursor.close()
                self.auth = auth
                
                return self.connection

        except Exception as e:
            print(e)
            
    def disconnect(self):
        ''' Disconnect from database '''
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
            
    def fetchTable(self, rows, table, condition = None, value = None):
        ''' Fetch a number of rows from a table that exists in database.
        Number of rows and table defined in config file.
        if number of rows equals to 0, will try to fetch all rows.'''
        
        if condition:
            sql = f"SELECT * FROM `{table}` WHERE {condition} = {value}"
        else:
            sql = f"SELECT * FROM `{table}` WHERE 1"
        
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        if rows > 0:
            records = cursor.fetchmany(rows)
        else:
            records = cursor.fetchall()
            
        print(f'Total number of rows in table: {cursor.rowcount}')
        print(f'Rows fetched: {len(records)}')
        
        data = []
        for row in records:
            row = list(row)
            data.append(row)
            
        cursor.close()
        return data
    
    def insertClient(self, data):
        ''' Função utilizada para inserir novo cliente no banco de dados.
        DATA requer (ID, NOME, CPF, CUPONS, TELEFONE, SENHA, EMAIL) '''
        sql = f"INSERT INTO Clientes (ID, NOME, CPF, CUPONS, TELEFONE, SENHA, EMAIL) VALUES {data}"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        
    def insertHistory(self, data):
        sql = f"INSERT INTO Historico (ID_PARCEIRO, ID_CLIENTE, DATA, HORARIO, QUANTIDADE, PEDIDO) VALUES {data}"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
    
# database = Mysql()
# database.connect(config.mysql_bapkasor_cupons)
# id = len(database.fetchTable(0, 'Historico'))
# data = (0, 0, '09/05/222', '10:51', 2, id)
# # data = (id, 'Teste', '12345678901', 0, '41988776655', '123', '@')
# database.insertHistory(str(data))