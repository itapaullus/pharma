from .BaseDict import Base, BaseExcel
import Log

class Network:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')


class DBNetwork(Base):
    tablename = 'network'

    @classmethod
    def get(cls, **kwargs):
        """Ищет сеть по лейблу или ID в справочнике network. Возвращает объект Network"""
        logger = Log.Logger('DICTIONARY.NETWORK.GET')
        id, label = kwargs.get('id'), kwargs.get('label')
        if id:
            ds = cls.select(where=f'id={id}')
        elif label:
            ds = cls.select(where=f"label='{label}'")
        else:
            logger.error('Для поиска по сетям должен быть передан ID или LABEL')
            raise TypeError('Не передан обязательный атрибут для поиска по справочнику Сети')
        if ds:
            resid = list(ds.keys())[0]
            label = list(ds.values())[0]['label']
            logger.debug(f'result set: {ds}')
            return Network(id=resid, label=label)
        else:
            logger.warning(f'Не удалось найти сеть!')
            return

    @classmethod
    def save(cls, label):
        """Сохраняет в справочник регионов указанный label"""
        logger = Log.Logger('DICTIONARY.NETWORK.SAVE')
        newid = cls.insert(label=label)
        logger.info(f'Сохраняем сеть id:{newid} label:{label}')
        return newid


class ExcelNetwork(BaseExcel):
    logger = Log.Logger('DICTIONARY.NETWORK.SAVETODB')

    def __init__(self, path):
        super().__init__(path)

    def savetodb(self):
        """Сохранение в БД данных из xls"""
        try:
            N = 0
            for row in self.xls:
                N += 1
                print(row[1])
                if N == 5:
                    break
            if input('Подтвердите корректность загружаемых данных: (y/n)').upper() == 'N':
                self.logger.info('Загрузка отменена!')
                return
            for row in self.xls:
                newid = DBNetwork.insert(label=row[1])
            DBNetwork.commit()
            self.logger.info('Справочник сетей успешно сохранен!')
        except Exception as e:
            self.logger.error(e)
            DBNetwork.rollback()
