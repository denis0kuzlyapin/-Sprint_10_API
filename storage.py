class TestStorage:
    # Хранилище для данных между тестами и фикстурами
    _offers = []

    @classmethod
    def add_offer(cls, token, offer_id):
        # Добавить объявление для удаления после теста
        cls._offers.append((token, offer_id))

    @classmethod
    def get_offers(cls):
        # Получить все объявления
        return cls._offers.copy()

    @classmethod
    def clear_offers(cls):
        # Очистить список объявлений
        cls._offers.clear()
