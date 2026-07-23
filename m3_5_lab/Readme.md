# 3.5 Django Lab

## Anaconda distribution

0:09

https://www.anaconda.com/download/success

## Django forms

10:50

forms.py - тут строим форму

views.py - делаем связь с формой  15:43

Запуск формы UserForm 23:52

### Миграции

Чтобы в таблице базы данных появилось новое поле, нужно сначала добавить это поле в модель.
Это поле в модели обязательно должно содержать дефолтные значения, иначе оно не добавится.
Затем делаем migrations и migrate.

### создание нового поля в форме class ArticleForm

29:19

Руками не создаем поля у этой формы.
Поля у этой формы будут полностью зависеть от структуры в модели class Article.

```
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        db_table = 'article'
```

нужен для предоставления метаданных для модели

- model
- fields
- db_table = 'article' - для переименования ..

если хотим сделать человеку понятны имена в админке или в полях формы.

verbos_name - указываем соответствие имен полей с русскоязычными названиями.

Класс Meta в классе формы обеспечивает связь между моделью (таблицей) и формой.

Например, в классе Meta можно задать русский язык для имен полей таблицы.

### Форма form_to_db

связь формы с моделью

0:29:23

Во Views сохраняем информацию о форме 32:28

```
def form_to_db(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        form.save()
        return redirect('success')
    form = ArticleForm()
    return render(request,'advanced_form.html',{'form':form})
```

перед запуском формы form_to_db делаем нужные миграции. 0:38:20

устанавливаем драйвер для работы с субд - psycopg2

подключаемся к базе данных

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'm3_5_lab',
        "USER": 'postgres',
        "PASSWORD": 'admin',
        "HOST": 'localhost',
        "PORT": 5432
    }
}

```

0:39:58 создаем миграции и применяем их

```
python manage.py makemigrations

Migrations for 'my_app':
  my_app/migrations/0001_initial.py
    + Create model Article

python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, my_app, sessions
Running migrations:  
  Applying my_app.0001_initial... OK
  Applying sessions.0001_initial... OK

```

заполняем таблицу через форму http://127.0.0.1:8000/form

нажать отправить

итого: мы сделали связь между таблицей базы и web формой

- Сделали модель, описав структуру таблицы (class Article)
- ..

### Как откатить миграцию

То есть отменить действия в базе данных.

54:14

python manage.py migrate приложение номер/имя_миграции

python manage.py migrate my_app 0001


1:01:07 - остановился тут.