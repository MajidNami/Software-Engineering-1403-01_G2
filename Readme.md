
# FarsiAid Website

Icarus project is a micro-service meant for developing articles etc. purposes, gathered around under the name group 7 and was developed as part of the **Software Engineering 1403-01 G2 Dr. Kalbasi** course and is built using Django. The application is powered by MeiliSearch for efficient word search and synonym suggestions.

## Features

- Suggest synonyms for Persian words.
- Suggest defenitions for english words in persian.
- User-friendly web interface.
- Organized structure for managing database and application logic.
- Media and static files support.
- Storing user favourite words labeled as starred words.
- Powered by MeiliSearch for fast and efficient text search.

## Project Structure

The main components of the project are organized as follows:

```
Software-Engineering-1403-01_G2
├── .venv/                # Virtual environment for dependencies
├── data.ms/             # Data files
├── dumps/               # Database dumps
├── src/
│   ├── database/           # Database-related files
│   ├── FarsiAid_website/   # Django project configuration
│   ├── group1 - group10/    # Submodules or app components
│   ├── media/              # Uploaded media files
│   ├── registration/       # User registration and authentication
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   ├── manage.py          # Django management script
├── db.sqlite3            # SQLite database
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Dockerfile for containerization
├── Readme.md             # Project documentation
```

## Screenshots

Here are some screenshots of the project:

- [Screenshot 1](https://github.com/Hessam-Hosseinian/Software-Engineering-1403-01_G2/blob/main/Screenshots/image.png)
- [Screenshot 2](https://github.com/Hessam-Hosseinian/Software-Engineering-1403-01_G2/blob/main/Screenshots/image%20(3).png)
- [Screenshot 3](https://github.com/Hessam-Hosseinian/Software-Engineering-1403-01_G2/blob/main/Screenshots/image%20(1).png)
- [Screenshot 4](https://github.com/Hessam-Hosseinian/Software-Engineering-1403-01_G2/blob/main/Screenshots/image%20(2).png)

## Prerequisites

- Python 3.8+
- Django 4.0+
- MeiliSearch
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/FarsiAid.git
   cd FarsiAid
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the MeiliSearch server:**

   - Start `meilisearch.exe` included in the project directory.

5. **Apply migrations and run the server:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Deployment

To deploy the application using Docker:

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://localhost:8000/`.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License.

---

### Acknowledgments

This project was developed as part of an academic course. Special thanks to the course instructors and team members for their support and collaboration.
