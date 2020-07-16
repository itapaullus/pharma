import pandas as pd
from psycopg2 import extensions
from psycopg2.extras import DictCursor
from .BaseDict import Base
import Log

# import dictionary


class Region:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')
        self.synonyms = set(kwargs.get('synonyms', []) + [self.label])


class Regions(list):
    def __init__(self, path=None):
        super(Regions, self).__init__()
        df = pd.read_excel(path)
        for i in df.to_records():
            self.append(Region(label=i[1], synonyms=list(i)[1:]))


class DBRegion(Base):
    tablename = 'region'

    @classmethod
    def get(cls, **kwargs):
        """Ищет регион по лейблу или ID в справочнике регионов и синонимах. Возвращает объект Region"""
        logger = Log.Logger('DICTIONARY.REGION.GET')
        id, label = kwargs.get('id'), kwargs.get('label')
        if id:
            ds = cls.select(where=f'id={id}')
        elif label:
            ds = cls.select(where=f"label='{label}'")
            if not ds:  # Не нашли, надо поискать в синонимах
                logger.info(f'{label} не найден в справочнике регионов')
                ds = cls.select(where=f"synonym='{label}'", table='region_synonyms')
                resid = list(ds.values())[0]['region_id']
                logger.debug(f'Рекурсивно вызываем Region.get(id={resid})')
                return cls.get(id=resid)
        resid = list(ds.keys())[0]
        label = list(ds.values())[0]['label']
        # теперь возьмем синонимы
        syn = cls.get_synonyms(cls, resid)
        logger.debug(f'result set: {ds} {syn}')
        return Region(id=resid, label=label, synonyms=syn)

    @staticmethod
    def get_synonyms(cls, id):
        """Возвращает список синонимов по указанному ID региона"""
        logger = Log.Logger('DICTIONARY.REGION.GET_SYNONYMS')
        ds = [row['synonym'] for row in list(cls.select(where=f'region_id={id}', table='region_synonyms').values())]
        logger.debug(f'result set: {ds}')
        return ds

    @staticmethod
    def save_region(label):
        pass

    @staticmethod
    def getlist():
        pass
