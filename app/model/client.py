

class Client:
    
    def __init__(self, id, ruc, enterprise, contact, phone, email, state):
        self.id = id
        self.ruc = ruc
        self.enterprise = enterprise
        self.contact = contact
        self.phone = phone
        self.email = email
        self.state = state

    @staticmethod
    def columns_name():
        return ['id', 'ruc', 'enterprise', 'contact', 'phone', 'email','result', 'state']


    def to_dict(self):
        return {'id':self.id, 'ruc':self.ruc, 'enterprise':self.enterprise, 'contact':self.contact, 'phone':self.phone, 'email':self.email, 'state':self.state}


    def to_csv(self):
        return "{id};{ruc};{enterprise};{contact};{phone};{email};{state}".format(id = self.id, ruc = self.ruc, enterprise = self.enterprise, contact = self.contact, phone = self.phone, email = self.email, state = self.state)


    def to_string(self):
        return "id : {}, ruc :{}, enterprise : {}, contact : {}, phone : {}, email : {}, state : {}".format(self.id, self.ruc, self.enterprise, self.contact, self.phone, self.email, self.state)