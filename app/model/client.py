

class Client:    
    def __init__(self, ruc, enterprise, contact, phone, email):
        self.ruc = ruc
        self.enterprise = enterprise
        self.contact = contact
        self.phone = phone
        self.email = email

    @staticmethod
    def columns_name():
        return ['ruc', 'enterprise', 'contact', 'phone', 'email','result']


    def to_dict(self):
        return {'ruc':self.ruc, 'enterprise':self.enterprise, 'contact':self.contact, 'phone':self.phone, 'email':self.email}


    def to_csv(self):
        return "{ruc};{enterprise};{contact};{phone};{email}".format(ruc = self.ruc,enterprise = self.enterprise,contact = self.contact,phone = self.phone,email = self.email)


    def to_string(self):
        return "ruc :{}, enterprise : {}, contact : {}, phone : {}, email : {}".format(self.ruc, self.enterprise, self.contact, self.phone, self.email)