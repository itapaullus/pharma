from .BaseDict import Base, BaseExcel
import Log


class Region:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')
        self.synonyms = set(kwargs.get('synonyms', []) + [self.label])


class Regions(list):
    pass


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
                logger.warning(f'{label} не найден в справочнике регионов')
                synds = cls.select(where=f"synonym='{label}'", table='region_synonyms')
                if synds:
                    resid = list(synds.values())[0]['region_id']
                    logger.debug(f'Рекурсивно вызываем Region.get(id={resid})')
                    return cls.get(id=resid)
        else:
            logger.error('Для поиска по регионам должен быть передан ID или LABEL')
            raise TypeError('Не передан обязательный атрибут для поиска по справочнику Регион')
        if ds:
            resid = list(ds.keys())[0]
            label = list(ds.values())[0]['label']
            # теперь возьмем синонимы
            syn = cls.get_synonyms(cls, resid)
            logger.debug(f'result set: {ds} {syn}')
            return Region(id=resid, label=label, synonyms=syn)
        else:
            logger.warning(f'Не удалось найти подходящий регион!')
            return

    @staticmethod
    def get_synonyms(cls, id):
        """Возвращает список синонимов по указанному ID региона"""
        logger = Log.Logger('DICTIONARY.REGION.GET_SYNONYMS')
        ds = [row['synonym'] for row in list(cls.select(where=f'region_id={id}', table='region_synonyms').values())]
        logger.debug(f'result set: {ds}')
        return ds

    @classmethod
    def save(cls, label):
        """Сохраняет в справочник регионов указанный label"""
        logger = Log.Logger('DICTIONARY.REGION.SAVE')
        newid = cls.insert(label=label)
        logger.info(f'Сохраняем регион id:{newid} label:{label}')
        return newid


class ExcelRegion(BaseExcel):
    logger = Log.Logger('DICTIONARY.EXCELREGION.SAVETODB')

    def __init__(self, path):
        super().__init__(path)

    def savetodb(self):
        """Сохранение в БД данных из xls"""
        try:
            for row in self.xls:
                newid = DBRegion.insert(label=row[4])
                for syn in set(row):
                    DBRegion.insert(table='region_synonyms', region_id=newid, synonym=syn)
            DBRegion.commit()
            self.logger.info('Справочник Регионов успешно сохранен!')
        except Exception as e:
            self.logger.error(e)
            DBRegion.rollback()
