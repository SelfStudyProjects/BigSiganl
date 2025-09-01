# BIGSIGNAL Project

## Overview
BIGSIGNAL is a comprehensive application designed to manage and analyze trading portfolios. The project consists of a backend built with Django and a frontend developed using React. It provides functionalities for trade management, portfolio analysis, and data visualization.

## Project Structure
The project is organized into two main directories: `backend` and `frontend`.

### Backend
The backend is responsible for handling data processing, business logic, and serving API endpoints. It is structured as follows:

- **config/**: Contains configuration files for the Django application.
  - `settings.py`: Configuration settings including database settings and installed apps.
  - `urls.py`: URL routing for the backend application.
  - `wsgi.py`: Entry point for WSGI-compatible web servers.
  - `asgi.py`: Entry point for ASGI-compatible web servers.

- **trades/**: Manages trade-related functionalities.
  - `models.py`: Defines data models for trades.
  - `serializers.py`: Serializes trade model instances to and from JSON.
  - `views.py`: Handles HTTP requests related to trades.
  - `urls.py`: URL routing for the trades module.
  - `admin.py`: Registers trade models with the Django admin site.
  - `apps.py`: Configuration for the trades application.

- **portfolios/**: Manages portfolio-related functionalities.
  - `models.py`: Defines data models for portfolios.
  - `serializers.py`: Serializes portfolio model instances to and from JSON.
  - `views.py`: Handles HTTP requests related to portfolios.
  - `urls.py`: URL routing for the portfolios module.
  - `admin.py`: Registers portfolio models with the Django admin site.
  - `apps.py`: Configuration for the portfolios application.

- **analysis/**: Contains logic for analyzing portfolios and investment strategies.
  - `portfolio_engine.py`: Logic for analyzing portfolios.
  - `buy_hold_calculator.py`: Functions for calculating buy-and-hold strategies.
  - `views.py`: Handles HTTP requests related to analysis.
  - `urls.py`: URL routing for the analysis module.
  - `utils.py`: Utility functions for the analysis module.

- **scripts/**: Contains scripts for data collection and seeding.
  - `telegram_collector.py`: Scripts for collecting data from Telegram.
  - `message_parser.py`: Functions for parsing messages.
  - `data_seeder.py`: Scripts for seeding initial data into the database.

- `manage.py`: Command-line utility for interacting with the Django project.
- `requirements.txt`: Lists dependencies required for the backend application.
- `.env.example`: Provides an example of environment variables needed for the application.

### Frontend
The frontend is responsible for the user interface and user experience. It is structured as follows:

- **public/**: Contains static files for the frontend application.
  - `index.html`: Main HTML file for the frontend application.
  - `favicon.ico`: Favicon for the frontend application.

- **src/**: Contains the source code for the React application.
  - **components/**: Contains React components for the application.
    - `Dashboard.jsx`: Dashboard component.
    - `PortfolioChart.jsx`: Portfolio chart component.
    - `PortfolioSelector.jsx`: Portfolio selector component.
    - `ComparisonTable.jsx`: Comparison table component.
    - `TradesList.jsx`: Trades list component.
    - `Header.jsx`: Header component.
  - **services/**: Contains utility functions for API calls and charting.
    - `api.js`: Functions for making API calls.
    - `chartUtils.js`: Utility functions for charting.
  - **styles/**: Contains CSS files for styling the application.
    - `Dashboard.css`: Styles for the Dashboard component.
    - `Chart.css`: Styles for chart components.
    - `global.css`: Global styles for the application.
  - `App.js`: Main application component.
  - `index.js`: Entry point for the React application.
  - `constants.js`: Constant values used throughout the application.

- `package.json`: Configuration file for npm, listing dependencies and scripts for the frontend application.
- `firebase.json`: Firebase configuration settings.
- `.firebaserc`: Firebase project settings.

## Getting Started
To get started with the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the backend directory and install the required dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the environment variables by copying `.env.example` to `.env` and updating the values as needed.

4. Run database migrations:
   ```
   python manage.py migrate
   ```

5. Start the backend server:
   ```
   python manage.py runserver
   ```

6. Navigate to the frontend directory and install the required dependencies:
   ```
   cd frontend
   npm install
   ```

7. Start the frontend development server:
   ```
   npm start
   ```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.