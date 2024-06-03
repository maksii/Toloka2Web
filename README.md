# Toloka2Web [![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

## English Section
WebUI for Toloka2MediaServer

## Розгортання за допомогою Docker

Дотримуйтесь цих кроків для розгортання `Toloka2Web` за допомогою Docker:

### Передумови

Переконайтеся, що Docker встановлено на вашій системі. Ви можете завантажити його з [офіційного сайту Docker](https://www.docker.com/get-started).

### Клонування репозиторію

Спочатку клонуйте репозиторій на ваш локальний комп'ютер:

```bash
cd ~
git clone https://github.com/maksii/Toloka2Web
cd Toloka2Web
```

### Файли конфігурації

Перед побудовою образу Docker створіть і налаштуйте необхідні файли конфігурації:

```bash
mkdir -p /home/appconfig

# Створіть і відредагуйте файл app.ini
nano /home/appconfig/app.ini

# Створіть і відредагуйте файл titles.ini
nano /home/appconfig/titles.ini
```

Переконайтеся, що ви заповнили файли `app.ini` та `titles.ini` відповідно до вимог вашого додатку.

### Побудова образу Docker

Побудуйте образ Docker за допомогою наступної команди:

```bash
docker build -t Toloka2Web .
```

### Запуск контейнера Docker

Запустіть ваш контейнер Docker за допомогою наступної команди:

```bash
docker run -d -p 5000:5000 -v /home/appconfig:/app/Toloka2Web/data --name toloka Toloka2Web
```

Ця команда запустить контейнер у відокремленому режимі, відображатиме порт 5000 контейнера на порт 5000 на хості і приєднає створену вами директорію конфігурації `/home/appconfig` до `/app/Toloka2Web/data` всередині контейнера.

### Перевірка розгортання

Після запуску контейнера ви можете перевірити, що додаток працює, відвідавши:

```
http://localhost:5000
```

Замініть `localhost` на IP-адресу вашого сервера, якщо ви звертаєтесь з іншої машини.

## Розгортання за допомогою готового образу Docker

Цей розділ пояснює, як розгорнути `Toloka2Web` використовуючи готовий образ з Docker Hub.

### Використання Docker

1. **Завантаження образу Docker**
   Завантажте готовий образ з Docker Hub за допомогою наступної команди:

   ```bash
   docker pull maksii/Toloka2Web:latest
   ```


2. **Запуск контейнера**
   Використовуйте наступну команду для запуску контейнера:

   ```bash
   docker run -d -p 5000:5000 -v /path/to/your/config:/app/Toloka2Web/data --name toloka maksii/Toloka2Web:latest
   ```

   Замініть `/path/to/your/config` на шлях до вашої папки конфігурації.

### Використання Portainer

Якщо ви використовуєте Portainer для управління контейнерами Docker, ви можете легко розгорнути `Toloka2Web` як стек:

1. **Логін в Portainer**
   Увійдіть у вашу панель керування Portainer .

2. **Створення стека**
   Перейдіть до розділу "Stacks" і натисніть "Add Stack".

3. **Конфігурація стека**
   Дайте ім'я вашому стеку і вставте наступний YAML конфіг у поле "Web editor":

   ```yaml
   version: '3.8'
   services:
     Toloka2Web:
       image: maksii/Toloka2Web:latest
       ports:
         - "5000:5000"
       volumes:
         - /path/to/your/config:/app/Toloka2Web/data
       restart: unless-stopped
   ```

   Замініть `/path/to/your/config` на шлях до вашої папки конфігурації.

4. **Розгортання стека**
   Натисніть "Deploy the stack" для запуску вашого додатку.


## License

- [GPL-v3](https://choosealicense.com/licenses/gpl-3.0/)

