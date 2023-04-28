from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {
            'dataCreation': ['gt'],  # позже какой-либо даты, что указал пользователь
            'title': ['icontains'], # мы хотим чтобы нам выводил заголовок хотя бы отдалённо похожее на то, что запросил пользователь
            'author': ['exact'] ,  # должен точно совпадать тому, что указал пользователь
            'category': ['exact'] ,  # должен точно совпадать тому, что указал пользователь
        }