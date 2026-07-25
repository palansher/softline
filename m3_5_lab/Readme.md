# 3.5 Django Lab

- [3.5 Django Lab](#35-django-lab)
  - [Anaconda distribution](#anaconda-distribution)
  - [Django forms](#django-forms)
    - [Миграции](#миграции)
    - [создание нового поля в форме class ArticleForm](#создание-нового-поля-в-форме-class-articleform)
    - [Форма form\_to\_db](#форма-form_to_db)
    - [Как откатить миграцию](#как-откатить-миграцию)
    - [Coockies](#coockies)
  - [Anaconda](#anaconda)
    - [устанавливаем Mini Conda на Ubuntu](#устанавливаем-mini-conda-на-ubuntu)
    - [Создайте изолированное окружение для вашего проекта](#создайте-изолированное-окружение-для-вашего-проекта)
      - [To accept these channels' Terms of Service](#to-accept-these-channels-terms-of-service)
      - [создаем окружение](#создаем-окружение)
      - [Активируйте созданное окружение](#активируйте-созданное-окружение)
  - [Подготовка среды для Jupiter и pandas](#подготовка-среды-для-jupiter-и-pandas)
    - [Установите Pandas и ядро для графического отображения (ipykernel)](#установите-pandas-и-ядро-для-графического-отображения-ipykernel)
    - [Настройка Visual Studio Code на Windows](#настройка-visual-studio-code-на-windows)
      - [Установите расширения](#установите-расширения)
      - [Запуск графического интерфейса (Jupyter)](#запуск-графического-интерфейса-jupyter)
        - [Создать и запустить файл блокнота](#создать-и-запустить-файл-блокнота)
  - [Conda - продолжение вебинара](#conda---продолжение-вебинара)
    - [Conda на Windows](#conda-на-windows)
    - [создание виртуального окружения](#создание-виртуального-окружения)
    - [активация виртуального окружения](#активация-виртуального-окружения)
    - [установка пакетов в окружение](#установка-пакетов-в-окружение)
  - [Jupyter - IDE для аналитиков](#jupyter---ide-для-аналитиков)
    - [установка](#установка)
    - [Jupyter Notebook, более старый](#jupyter-notebook-более-старый)
    - [Jupyter Lab](#jupyter-lab)
    - [SQL запросы к базам в расширении Jupyter в VS Code](#sql-запросы-к-базам-в-расширении-jupyter-в-vs-code)
  - [Pandas использование](#pandas-использование)
    - [использование датафрейм](#использование-датафрейм)
    - [Фильтрация данных](#фильтрация-данных)

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

### Coockies

1:01:07

## Anaconda

1:15:10

переменные пути для установки конды на Windows

![alt text](demo_pandas/doc/conda-windows-env.png)

Делал самостоятельно на Ubuntu, так как на вебинаре использовался пакет для Windows.

https://www.anaconda.com/download/success

https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install

**устанавливаем Conda на Ubuntu, а работаем на Windows удаленно через Jupiter Notebook Visual Studio Code.**

### устанавливаем Mini Conda на Ubuntu

```bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

~/Miniconda3-latest-Linux-x86_64.sh
```

```text
Do you wish to update your shell profile to automatically initialize conda?
This will activate conda on startup and change the command prompt when activated.
If you'd prefer that conda's base environment not be activated on startup,
   run the following command when conda is activated:

conda config --set auto_activate_base false

Note: You can undo this later by running `conda init --reverse $SHELL`

Proceed with initialization? [yes|no]

Proceed with initialization? [yes|no]
[no] >>> yes
no change     /home/vp/miniconda3/condabin/conda
no change     /home/vp/miniconda3/bin/conda
no change     /home/vp/miniconda3/bin/activate
no change     /home/vp/miniconda3/bin/deactivate
no change     /home/vp/miniconda3/etc/profile.d/conda.sh
no change     /home/vp/miniconda3/etc/fish/conf.d/conda.fish
no change     /home/vp/miniconda3/shell/condabin/Conda.psm1
no change     /home/vp/miniconda3/shell/condabin/conda-hook.ps1
no change     /home/vp/miniconda3/lib/python3.14/site-packages/xontrib/conda.xsh
no change     /home/vp/miniconda3/etc/profile.d/conda.csh
modified      /home/vp/.bashrc

==> For changes to take effect, close and re-open your current shell. <==

Thank you for installing Miniconda3!
```

```bash
source ~/.bashrc

conda list
# packages in environment at /home/vp/miniconda3:
#
# Name                      Version          Build               Channel
_libgcc_mutex               0.1              main
_openmp_mutex               5.1              52_gnu
anaconda-anon-usage         0.8.1            pyhb46e38b_100

...
```

```bash

conda -V
conda 26.5.3

```

После перезапуска перед вашим именем пользователя появится надпись (base)

### Создайте изолированное окружение для вашего проекта

(назовем его data_env)

#### To accept these channels' Terms of Service

run the following commands:

```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

```

#### создаем окружение

```bash
# conda create -n data_env python=3.11 -y
conda create -n data_env python=3.14 -y
```

```text
2 channel Terms of Service accepted
Retrieving notices: done
Channels:
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/vp/miniconda3/envs/data_env

  added / updated specs:
    - python=3.14


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    ca-certificates-2026.7.16  |       h06a4308_0         106 KB
    pthread-stubs-0.3          |       h47b2149_2           7 KB
    python-3.14.6              |h4bdf6f9_101_cp314        35.3 MB
    tzdata-2026c               |       he532380_0         117 KB
    ------------------------------------------------------------
                                           Total:        35.5 MB

The following NEW packages will be INSTALLED:

  _libgcc_mutex      pkgs/main/linux-64::_libgcc_mutex-0.1-main
  ..
  zstd               pkgs/main/linux-64::zstd-1.5.7-h11fc155_0



Downloading and Extracting Packages:

Preparing transaction: done
Verifying transaction: done
Executing transaction: done
#
# To activate this environment, use
#
#     $ conda activate data_env
#
# To deactivate an active environment, use
#
#     $ conda deactivate


Channel "defaults" has the following notices:
  [info] -- Tue Jun  9 00:00:00 2026
  PyTorch 2.12 with CUDA support is now available to install with your current channel (Anaconda Main). Learn more: https://anaconda.org/main/pytorch?utm_source=channel_notices

WARNING conda.conda_pypi.main:notify_externally_managed_future(156):
  Did you know? You can install many PyPI packages with conda
  using the conda-pypi beta. Get started:
    https://docs.conda.io/projects/conda/en/stable/new-features.html


```

#### Активируйте созданное окружение

```bash
# conda activate data_env

(base) vp@vm-perepechenko01\:~$ conda activate data_env
(data_env) vp@vm-perepechenko01\:~$

```

## Подготовка среды для Jupiter и pandas

### Установите Pandas и ядро для графического отображения (ipykernel)

Термин ядро (kernel) в контексте Jupyter означает не графический движок операционной системы, а интерпретатор кода,
который работает в фоновом режиме на Ubuntu.Пакет ipykernel — это невидимый мост, который связывает
консольную Ubuntu с графическим интерфейсом VS Code на Windows.

```bash
# conda install pandas ipykernel -y

(data_env) vp@vm-perepechenko01\:~$ conda install pandas ipykernel -y
```

```text
2 channel Terms of Service accepted
Channels:
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/vp/miniconda3/envs/data_env

  added / updated specs:
    - ipykernel
    - pandas


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    asttokens-3.0.1            |  py314h06a4308_0          69 KB
    ...
    zeromq-4.3.5               |       hf801bfb_2         338 KB
    ------------------------------------------------------------
                                           Total:       198.6 MB

The following NEW packages will be INSTALLED:

  asttokens          pkgs/main/linux-64::asttokens-3.0.1-py314h06a4308_0
  ...
  zeromq             pkgs/main/linux-64::zeromq-4.3.5-hf801bfb_2



Downloading and Extracting Packages:

Preparing transaction: done
Verifying transaction: done
Executing transaction: done
WARNING conda.conda_pypi.main:notify_externally_managed_future(156):
  Did you know? You can install many PyPI packages with conda
  using the conda-pypi beta. Get started:
    https://docs.conda.io/projects/conda/en/stable/new-features.html

(data_env) vp@vm-perepechenko01\:~$

```

### Настройка Visual Studio Code на Windows

#### Установите расширения

- Python (от Microsoft)
- Jupyter (от Microsoft)

>Убедитесь, что они установились именно в разделе «SSH: IP_АДРЕС — INSTALLED», а не просто локально на Windows

#### Запуск графического интерфейса (Jupyter)

Это тот самый шаг, который заменит вам любые сторонние программы и даст графику.

##### Создать и запустить файл блокнота

- В VS Code откройте любую папку на сервере (File -> Open Folder).
- Создайте новый файл с расширением .ipynb (например, test_pandas.ipynb).

Это формат интерактивных блокнотов Jupyter.

Переключиться на Python Environment: В правом верхнем углу открывшегося файла нажмите Select Kernel (Выбрать ядро) -> Python Environments и выберите ваше окружение data_env (там будет написан путь к conda).

Переключиться можно с помощью расширения Visual Studio Code -  Environment Managers.

- Нажмите кнопку Open in Notebook Editor

- Вставьте в первую ячейку код для проверки:

```python
import pandas as pd
df = pd.DataFrame({'Имя': ['Анна', 'Иван', 'Петр'], 'Возраст': [24, 30, 18]})
df
```

Нажмите кнопку Run (Ctrl+Enter) слева от ячейки.

VSCode на Windows покажет вам красивую интерактивную графическую таблицу со строками и столбцами, хотя сам код выполнился на удаленной Ubuntu!

## Conda - продолжение вебинара

продолжаем вебинар
1:26:07

канал в Conda это то место откуда берут пакеты

Самый популярный канал это Conda Forge.

Если работаем с бигдата, то одного пандас недостаточно. Нужен еще nampy (для работы с векторами или AI).

Аналитики данных не работают в обычном программистском IDE, они работают в специализированных средах, например, в Jupyter.

Jupyter - это интерактивная web IDE.

### Conda на Windows

при установке Conda на Windows появляется много команд и средств, например, Conda Prompt или Conda PowerShell. PyCharm может глючить, поэтому команды лучше запускать в Conda Prompt.

### создание виртуального окружения

```bash
# conda create --name lesson5 python=3.14

# conda deactivate

conda create --name lab35 python=3.14

```

### активация виртуального окружения

```bash
# conda activate lesson5
conda activate lab35
```

### установка пакетов в окружение

```bash
conda install numpy pandas

conda list
```

На всякий случай:

После этого вы сможете импортировать обе библиотеки в вашем файле .ipynb в VS Code:

```python
import numpy as np
import pandas as pd
```

## Jupyter - IDE для аналитиков

### установка

`conda install jupyter`

Есть два вида Jupyter: старый и новый.

### Jupyter Notebook, более старый

запускать `jupyter notebook`

```text
To access the server, open this file in a browser:
        file:/home/vp/.local/share/jupyter/runtime/jpserver-2389418-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/tree?token=f54e2812673a4c845d66528a91784624646ef31cbcb92c01
        http://127.0.0.1:8888/tree?token=f54e2812673a4c845d66528a91784624646ef31cbcb92c01
```

открываем веб-интерфейс http://localhost:8888/tree?token=f54e2812673a4c845d66528a91784624646ef31cbcb92c01

### Jupyter Lab

запускать `jupyter lab`

```
To access the server, open this file in a browser:
        file:/home/vp/.local/share/jupyter/runtime/jpserver-2391523-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/lab?token=24cb50026d9fa053ad0840da362f6307de56e96b06573758
        http://127.0.0.1:8888/lab?token=24cb50026d9fa053ad0840da362f6307de56e96b06573758
```

в веб-интерфейсе создайте новый ноутбук. Файл, Нью, ноутбук

В интерфейсе ноутбука есть три режима данных: Code, Markdown и Raw.

Запуск введенного кода - Ctrl Enter

В ячейки можно вводить как цифры, арифметические выражения, так и код.

В ноутбуке удобно и писать код, и описывать его сразу (тип ячейки Markdown).

Например, сделаем матрицу Markdown:

`$S=\pi*r^2$`

$S=\pi*r^2$

`$\frac{1}{3}$`

$\frac{1}{3}$

### SQL запросы к базам в расширении Jupyter в VS Code

pip install ipython-sql SQLAlchemy

Чистый Python + Pandas (Стандартный путь)

Вы можете подключаться к БД стандартным кодом с помощью встроенной в Pandas функции read_sql.

Пример кода для ячейки Jupyter:

```python
import pandas as pd
from sqlalchemy import create_engine

# Создаем подключение (например, к SQLite или удаленному серверу)
engine = create_engine('postgresql://postgres:admin@localhost/m3_4_lab') 

# Загружаем данные из БД сразу в DataFrame
df = pd.read_sql("SELECT * FROM person", engine)
df.head()
```

## Pandas использование

1:58:04

Pandas — это такой модуль, который позволяет работать с данными как с таблицами

Можем работать с любыми типами документов.

используя два объекта Series и DataFrame описывает структуру данных

см презентацию

см m3_5_lab/demo_pandas/index.py

### использование датафрейм

### Фильтрация данных

2:04:25

