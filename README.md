# Toloka2Web [![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

This project is a WebUI for media management tools designed to streamline the process of searching, downloading, and organizing media content from various sources.

Power By:
- [Toloka2Python](https://github.com/CakesTwix/toloka2python)
- [Toloka2MediaServer](https://github.com/CakesTwix/Toloka2MediaServer)
- [Stream2MediaServer](https://github.com/maksii/Stream2MediaServer)

Tech Stack:
- Python+Flask
- Bootstrap 5.3
- [Datatables.js](https://datatables.net/) MIT license


Badges:
- latest [![CI](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml/badge.svg?branch=main)](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml)
- develope [![CI](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml/badge.svg?branch=develop)](https://github.com/maksii/Toloka2Web/actions/workflows/docker_hub.yml)

## Roadmap

Here is the roadmap for the project, outlining both completed and planned developments. Checked boxes indicate completed items, while unchecked boxes represent upcoming features:

- [x] **Integration with Toloka2MediaServer** - Achieved seamless integration with Toloka2MediaServer for enhanced media handling.
- [x] **Docker** - Simplify deployment and updates.
- [x] **Search, Add, Download Results from Toloka** - Implemented functionality to search, add, and download content directly from Toloka.
- [x] **Add Assistant to Adjust Naming** - Developed an assistant to help with file naming conventions, ensuring consistency across downloads.
- [x] **Studios and Anime Local DB Preview** - Created a local database for studios and anime to allow quick previews and access.
- [ ] **Jobs Schedule** - Plan to implement a scheduling system for automated tasks and jobs within the application.
- [ ] **Integration with Stream2MediaServer to Replicate Logic for Online Cinemas** - Future plans to integrate with Stream2MediaServer to handle content from online cinemas similarly.
- [ ] **Improved Parsing and Result Linking** - Aiming to enhance the parsing algorithms and result linking for better accuracy and user experience.
- [ ] **Migration to Single DB** - Plans to consolidate multiple databases into a single, more efficient database system.
- [ ] **MAL, TVDB, TheMovieDB Integration to Fetch Info** - Intend to integrate with external APIs like MAL (MyAnimeTable), TVDB (The TV Database), and TheMovieDB to fetch and display additional information.
- [ ] **UI Improvements** - Scheduled improvements on the user interface to enhance usability and aesthetics.


## Розгортання за допомогою Docker

Дотримуйтесь цих кроків для розгортання `Toloka2Web` за допомогою Docker:

Docker image - https://hub.docker.com/r/maksii/toloka2web

tags:
- latest - main branch latest stable release
- develop - unstable development version

copy configs and db into /path/to/config/

### Використання Docker

1. **Завантаження образу Docker**
   Завантажте готовий образ з Docker Hub за допомогою наступної команди:

   ```bash
   docker pull maksii/toloka2web:latest
   ```


2. **Запуск контейнера**
   Використовуйте наступну команду для запуску контейнера:

   ```bash
   docker run -d -p 5000:5000 -v /path/to/your/config:/app/data --name toloka maksii/toloka2web:latest
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
       image: maksii/toloka2web:latest
       ports:
         - "5000:5000"
       volumes:
         - /path/to/your/config:/app/data
       restart: unless-stopped
   ```

   Замініть `/path/to/your/config` на шлях до вашої папки конфігурації.

4. **Розгортання стека**
   Натисніть "Deploy the stack" для запуску вашого додатку.


## Disclaimer

This project is designed with a simplified technology stack to maximize accessibility and encourage contributions from a wide range of developers, regardless of their experience level. The current technology choices, including the use of Flask and Python, SQLite for database, and vanila JavaScript for frontend interactions, have been deliberately chosen to keep the project straightforward and manageable.

We have no plans to switch to modern JavaScript frameworks, replace Flask with another backend framework, or upgrade from SQLite to a more advanced database system until all planned features are fully implemented and thoroughly tested. As such, any pull requests that introduce increased complexity without significant benefit will not be accepted. This approach ensures that the project remains accessible and maintainable for contributors at all levels.

## Contributing

We welcome contributions from the community. Here are a few ways you can help:

### Issues and Discussions
- **Suggestions and Discussions:** Please create issues in this repository for any suggestions or discussions about new features or improvements.
- **UI/Visual Bugs:** Report any UI or visual bugs directly in this repository.

### Pull Requests
- Feel free to fork the repository and submit pull requests. Make sure your changes are clear and do not introduce unnecessary complexity as mentioned in the disclaimer.

### Specific Issues
- **Toloka Functionality:** Issues related to Toloka information, search results, and release information should be submitted to [Toloka2Python](https://github.com/CakesTwix/toloka2python).
- **Toloka Torrents:** Issues about torrents added to torrent clients, file renaming, etc., should go to [Toloka2MediaServer](https://github.com/CakesTwix/Toloka2MediaServer).
- **Streaming and Database Updates:** For issues related to downloading from streaming sites or outdated databases of studios or anime lists, please use [Stream2MediaServer](https://github.com/maksii/Stream2MediaServer).

We appreciate your contributions and look forward to collaborating with you!

---

## License

- [GPL-v3](https://choosealicense.com/licenses/gpl-3.0/)

