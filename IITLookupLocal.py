import MySQLdb
import MySQLdb.cursors
import re

class IITLookupLocalDB:

        def __init__(self, dbhost='localhost', dbport=3306, dbuser=None, dbpass=None, dbname='iitlookup'):
                self.dbc=MySQLdb.connect(user=dbuser,passwd=dbpass,host=dbhost,port=dbport,db=dbname,cursorclass=MySQLdb.cursors.DictCursor)
                self.idregex = re.compile(r"^A[0-9]{8}$");
                self.cregex = re.compile(r"^[0-9]{5}$");
        
        def validateID(self, idn):
                return re.match(self.idregex, idn)
        
        def validateCard(self, cnum):
                return re.match(self.cregex, str(cnum))

        def nameByID(self,idnumber):
                c=self.dbc.cursor()
                if not (self.validateID(idnumber)):
                        raise ValueError("Invalid ID number!")
                c.execute("""SELECT * FROM iitlookup
                          WHERE idnumber = %s""", (idnumber,))
                rv=c.fetchone()
                c.close()
                return rv
        
        def nameIDByCard(self,cardnum):
                c=self.dbc.cursor()
                if not (self.validateCard(cardnum)):
                        raise ValueError("Invalid card number!")
                c.execute("""SELECT * FROM iitlookup
                          WHERE card_number = %s""", (cardnum,))
                rv = c.fetchone()
                c.close()
                return rv

        def insertRecord(self, fname, mname, lname, idnum, cardnum):
                c=self.dbc.cursor()
                if not (self.validateID(idnum)):
                        raise ValueError("Invalid ID number!")
                if not (self.validateCard(cardnum)):
                        raise ValueError("Invalid card number!")
                rv = c.execute("""INSERT INTO iitlookup (first_name, middle_name, last_name, idnumber, card_number) 
                                VALUES (%s, %s, %s, %s, %s)""", (fname,mname,lname,idnum,cardnum))
                self.dbc.commit()
                c.close()
                return rv


        def deleteRecord(self, idnum):
                c=self.dbc.cursor()
                if not (self.validateID(idnum)):
                        raise ValueError("Invalid ID number!")
                rv = c.execute("""DELETE FROM iitlookup WHERE idnumber = %s""", (idnum,))
                self.dbc.commit()
                c.close()
                return rv
