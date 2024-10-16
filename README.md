# Password Manager

## Overview

The Password Manager is a user-friendly application that helps you securely store and manage your passwords. It features a simple and intuitive interface built with CustomTkinter and utilizes SQLite for data storage. With this app, you can add, view, edit, search, and delete your saved passwords with ease.

## Features

- **Add New Passwords**: Easily save passwords associated with websites, emails, and usernames.
- **View Saved Passwords**: Access a list of all stored passwords in a secure manner.
- **Edit Passwords**: Update existing passwords without creating duplicates.
- **Search Passwords**: Quickly find stored passwords based on website or email queries.
- **Delete Passwords**: Remove unwanted passwords from your database.
- **Generate Strong Passwords**: Automatically create secure passwords with the click of a button.
- **Dark and Light Mode**: Switch between different appearance modes for better user experience.

## Installation

### Prerequisites

Make sure you have Python 3.x installed on your system.

### Requirements

To install the necessary dependencies, use the `requirements.txt` file included in the project. You can install them using pip:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Clone this repository to your local machine.
2. Navigate to the `SRC` directory.
3. Run the application:

```bash
python Main.py
```

## File Structure

```markdown
└── 📁Password-Manager
  └── 📁SRC
  └── DataBase.py # Database management functionalities.
  └── Exceptions.py # Custom exceptions for error handling.
  └── Main.py # Main application file that runs the Password Manager.
  └── Utilities.py # Utility functions, including password generation.
```

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

More details on how to contribute can be found in the [CONTRIBUTING.md](DOCS/CONTRIBUTING.md) file.

## Acknowledgments

- Special thanks to the developers of CustomTkinter and SQLite for providing the tools used in this application.
