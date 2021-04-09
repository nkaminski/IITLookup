from requests import Session, auth
import zeep


class IITLookup:

        def __init__(self, wsurl, user=None, pwd=None, idlength=6):
                self.idlength=idlength
                if(user or pwd):
                    session = Session()
                    session.auth = auth.HTTPBasicAuth(user, pwd)
                    self.sclient=zeep.Client(wsdl=wsurl, transport=zeep.Transport(session=session))
                else:
                    self.sclient=zeep.Client(wsdl=wsurl)

        def nameByID(self, idnumber):
                try:
                    return self.sclient.service.PCSGetName(idNumber=idnumber)
                except zeep.exceptions.Error as zeep_error:
                    print(zeep_error)
                    return None

        def nameIDByCard(self,cardnum):
                lookupstr = str(cardnum).zfill(self.idlength)
                try:
                    ret = self.sclient.service.PCSGetbyCardNum(cardNumber=lookupstr)
                except zeep.exceptions.Error as zeep_error:
                    print(zeep_error)
                    return None
                if(ret == 'Not Found'):
                    return None
                ret = ret.split(',')
                output = {}
                output['last_name'] = ret[0]
                output['first_name'] = ret[1]
                output['middle_name'] = ret[2]
                output['idnumber'] = ret[3]
                return output

        def inquiryByID(self,idnumber):
                try:
                    ret = self.sclient.PCSGetInquiry(idNumber=idnumber)['PCSGetInquiryResult']
                except SoapFault:
                    return None
                output = {}
                for x in ret:
                    x = x['InquiryRecord']
                    n_obj = {}
                    n_obj['blocked'] = x['blocked']
                    n_obj['limit'] = x['limit']
                    n_obj['balance'] = x['balance']
                    output[x['tender']] = n_obj
                return output

        def inquiryByCard(self,cardnum):
                idn = self.nameIDByCard(cardnum)
                if not idn:
                        return None
                return self.inquiryByID(idn['idnumber'])
        
