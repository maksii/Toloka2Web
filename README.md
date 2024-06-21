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
- [x] **Studios and Anime Local DB Preview** - DB based on streaming sites auto-downloaded on first application start
- [x] **Jobs Schedule** - Cron job inside docker config.
- [ ] **Integration with Stream2MediaServer to Replicate Logic for Online Cinemas** - Future plans to integrate with Stream2MediaServer to handle content from online cinemas similarly.
- [ ] **Improved Parsing and Result Linking** - Aiming to enhance the parsing algorithms and result linking for better accuracy and user experience.
- [ ] **Migration to Single DB** - Plans to consolidate multiple databases into a single, more efficient database system.
- [x] **MAL, TheMovieDB Integration to Fetch Info** - MAL and TheMovieDB results in multi-search
- [ ] **UI Improvements** - improvements on the user interface to enhance usability and aesthetics.


## Розгортання за допомогою Docker

Дотримуйтесь цих кроків для розгортання `Toloka2Web` за допомогою Docker:

Docker image - https://hub.docker.com/r/maksii/toloka2web

tags:
- latest - main branch latest stable release
- develop - unstable development version

copy configs and db into /path/to/config/

### Використання Docker(Portainer)

**Конфігурація стека**

   ```yaml
version: '3.8'
services:
  toloka2web:
    image: maksii/toloka2web:latest
    container_name: toloka2web
    volumes:
      - /path/to/your/config:/app/data
       - /path/to/your/downloads:/path/to/your/downloads
    environment:
      - PORT=80 
      - PUID=1024
      - PGID=100
      - CRON_SCHEDULE=0 */2 * * *
      - TZ=Europe/Kiev
    restart: unless-stopped
    user: "${PUID}:${PGID}"
   ```

   Замініть `/path/to/your/config` на шлях до вашої папки конфігурації.

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

### Author's Vision

#### Purpose of the Project
The primary objective of this project is to streamline the process of downloading, naming, and organizing anime series on my Plex media server. While the project is designed to be somewhat flexible and not exclusively tied to anime content, it predominantly caters to this genre. This is because other types of content, such as movies and TV series, can be efficiently managed using existing tools that interact well with trackers like Utopia, which adhere to naming conventions and integrate seamlessly with the arr suite of applications.

#### Challenges Addressed
One of the challenges specific to the Ukrainian anime community is that local studios often do not upload their content to trackers. When they do, the naming conventions are inconsistent and varied. This project aims to mitigate these issues by providing a more standardized approach to content management.

#### Contribution and Development
If you have specific requests regarding functionality, support for different torrent clients, trackers, or sites, please feel free to create an issue or submit a pull request (PR). While I will prioritize issues that align with my ongoing work, I welcome all contributions. Please note that I am not a professional Python or frontend developer; therefore, the project may contain suboptimal code that will likely require refactoring as I continue to learn and improve the software.

#### Політика внесків та мови
PR, що містять коментарі в коді українською мовою або будь-якою іншою мовою, крім англійської, будуть відхилені без додаткового розгляду. Локалізація UI/UX та загальна локалізація будуть виконані мною українською мовою як мій останній внесок у цей проєкт. Наразі я не планую витрачати зусилля на постійно змінюваний інтерфейс користувача, особливо враховуючи, що більшість коду знаходиться на ранній стадії прототипу. PR, які вводять українську мову на даному етапі, будуть відхилені, окрім випадків, коли ви готові забезпечувати їхню підтримку на тижневій основі.

## License

- [GPL-v3](https://choosealicense.com/licenses/gpl-3.0/)

