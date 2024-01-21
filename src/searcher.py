from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

class Searcher:
    def __init__(self):
        self.actions = ['start', 'help', 'short', 'full', 'nearest_show_all', 'nearest_show_id', 'nearest_show_title']
        
        # Обучающие данные для каждого действия
        self.train_data_start = ['начать', 'старт', 'привет', 'здравствуй', 'добрый день', 'поехали', 'стартуй', 'начнем', 'давай начнем', 'приветствие', 'начальное приветствие']
        self.train_data_help = ['помощь', 'что ты умеешь', 'как мне...', 'не знаю что делать', 'тебя программируют?', 'ты умеешь...', 'ты можешь...', 'как работает...', 'что такое...', 'объясни мне...']
        self.train_data_short = ['краткая информация', 'покажи театры', 'список театров', 'все театры', 'театры поблизости', 'ближайшие театры', 'театры в городе', 'лучшие театры', 'популярные театры', 'рейтинг театров']
        self.train_data_full = ['полная информация', 'все о театре', 'подробности о театре', 'расскажи о театре', 'информация о театре', 'детали о театре', 'хочу узнать о театре', 'что известно о театре', 'что ты знаешь о театре', 'подробнее о театре']
        self.train_data_nearest_show_all = ['ближайшие спектакли всех театров', 'все ближайшие спектакли', 'спектакли сегодня', 'спектакли завтра', 'что посмотреть', 'куда сходить', 'что идет в театрах', 'расписание спектаклей', 'ближайшие мероприятия', 'что идет в театре']
        self.train_data_nearest_show_id = ['ближайшие спектакли конкретного театра', 'спектакли в этом театре', 'что идет в этом театре', 'расписание этого театра', 'что посмотреть в этом театре', 'что играет в этом театре', 'что смотреть в этом театре', 'что идет в театре сегодня', 'что идет в театре завтра', 'ближайшие спектакли в этом театре']
        self.train_data_nearest_show_title = ['ближайшие спектакли с указанным названием', 'когда следующий спектакль', 'когда идет этот спектакль', 'расписание этого спектакля', 'когда будет этот спектакль', 'следующий показ спектакля', 'когда следующий показ', 'когда следующая постановка', 'когда следующий сеанс', 'когда следующее представление']
        
        # Создаем метки для обучающих данных (0 для 'start', 1 для 'help', и т.д.)
        self.train_labels_start = [0]*len(self.train_data_start)
        self.train_labels_help = [1]*len(self.train_data_help)
        self.train_labels_short = [2]*len(self.train_data_short)
        self.train_labels_full = [3]*len(self.train_data_full)
        self.train_labels_nearest_show_all = [4]*len(self.train_data_nearest_show_all)
        self.train_labels_nearest_show_id = [5]*len(self.train_data_nearest_show_id)
        self.train_labels_nearest_show_title = [6]*len(self.train_data_nearest_show_title)
        
        self.model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear'))
        self.model.fit(self.train_data_start + self.train_data_help + self.train_data_short + self.train_data_full + self.train_data_nearest_show_all + self.train_data_nearest_show_id + self.train_data_nearest_show_title, self.train_labels_start + self.train_labels_help + self.train_labels_short + self.train_labels_full + self.train_labels_nearest_show_all + self.train_labels_nearest_show_id + self.train_labels_nearest_show_title)

    def predict_action(self, message):
        prediction = self.model.predict([message])
        return self.actions[int(prediction.item())]

