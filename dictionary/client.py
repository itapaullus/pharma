class Client:
    def __init__(self, inn, label = ''):
        self.inn = inn
        if label:
            self.label = label
        else:
            self.label = ext_api.Dadata.get_client_by_inn(inn)


class DBClient:
    @staticmethod
    def get():
        pass
