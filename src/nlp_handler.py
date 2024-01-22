from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

class AI:
    def __init__(self):
        self.actions = ['shop_info', 'all_shops', 'shop_products', 'brand_shops']
        
        # Обучающие данные для каждого действия
        self.train_data_shop_info = ['информация о магазине', 'расскажи о магазине', 'что ты знаешь о магазине', 'хочу узнать о магазине', 'дай информацию о магазине']
        self.train_data_all_shops = ['все магазины', 'покажи все магазины', 'список всех магазинов', 'хочу увидеть все магазины', 'дай информацию обо всех магазинах']
        self.train_data_shop_products = ['товары в магазине', 'что продается в магазине', 'покажи товары в магазине', 'хочу увидеть товары в магазине', 'дай информацию о товарах в магазине']
        self.train_data_brand_shops = ['магазины бренда', 'покажи магазины бренда', 'список магазинов бренда', 'хочу увидеть магазины бренда', 'дай информацию о магазинах бренда']
        
        # Создаем метки для обучающих данных (0 для 'shop_info', 1 для 'all_shops', и т.д.)
        self.train_labels_shop_info = [0]*len(self.train_data_shop_info)
        self.train_labels_all_shops = [1]*len(self.train_data_all_shops)
        self.train_labels_shop_products = [2]*len(self.train_data_shop_products)
        self.train_labels_brand_shops = [3]*len(self.train_data_brand_shops)
        
        self.model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear'))
        self.model.fit(self.train_data_shop_info + self.train_data_all_shops + self.train_data_shop_products + self.train_data_brand_shops, self.train_labels_shop_info + self.train_labels_all_shops + self.train_labels_shop_products + self.train_labels_brand_shops)

    def predict_action(self, message):
        prediction = self.model.predict([message])
        return self.actions[int(prediction.item())]
