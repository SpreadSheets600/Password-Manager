
# Password Manager 🗝️

## Overview 📚

The Password Manager is a user-friendly application that helps you securely store and manage your passwords. It features a simple and intuitive interface built with CustomTkinter and utilizes SQLite for data storage. With this app, you can add, view, edit, search, and delete your saved passwords with ease.

## Features ✨

- **Add New Passwords**: Easily save passwords associated with websites, emails, and usernames.
- **View Saved Passwords**: Access a list of all stored passwords in a secure manner.
- **Edit Passwords**: Update existing passwords without creating duplicates.
- **Search Passwords**: Quickly find stored passwords based on website or email queries.
- **Delete Passwords**: Remove unwanted passwords from your database.
- **Generate Strong Passwords**: Automatically create secure passwords with the click of a button.
- **Dark and Light Mode**: Switch between different appearance modes for better user experience.

## Installation ⚙️

### Prerequisites

◉ Make sure you have Python 3.x installed on your system.

### Requirements

◉ To install the necessary dependencies, use the `requirements.txt` file included in the project. You can install them using pip:

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
    └── 📁DOCS
        └── CODE_OF_CONDUCT.md
        └── CONTRIBUTING.md
    └── 📁SRC
        └── DataBase.py
        └── Exceptions.py
        └── Main.py
        └── Utilities.py
    └── README.md
```

<details>
<summary><h2> TODO List </h2></summary>

1. **Enhance User Interface:**
   - Revise button placements and alignments for better UX.
   - Add tooltips or help icons for user guidance.
   - Implement a theme toggle (light/dark mode) for better accessibility.

2. **Improve Functionality:**
   - Implement password strength validation during password creation.
   - Add an option to categorize passwords (e.g., personal, work).
   - Introduce tags or labels for easier organization and searchability.
   - Allow exporting passwords to a CSV file for backup purposes.

3. **Implement Security Features:**
   - Add encryption for stored passwords for enhanced security.
   - Implement user authentication (master password) to access the app.
   - Enable secure password generation options (length, character types).

4. **Enhance Database Management:**
   - Implement a function to back up and restore the database.
   - Create a function to audit passwords for reusability or weak passwords.
   - Add data validation to ensure no duplicates are saved.

5. **Unit Testing:**
   - Write unit tests for critical functions (e.g., database interactions, password generation).
   - Set up automated testing with a CI/CD pipeline (e.g., GitHub Actions).

6. **Documentation:**
   - Expand the README.md with a usage guide and contribution instructions.
   - Create a wiki for detailed documentation on features and development guidelines.
   - Document the code with clear comments and docstrings for better readability.

7. **Code Refactoring:**
   - Review and refactor the code for better modularity and readability.
   - Optimize performance in database queries and UI responsiveness.

8. **User Feedback:**
   - Gather user feedback on the application’s usability and features.
   - Implement a feedback mechanism (e.g., a form or dialog within the app).

9. **Accessibility Improvements:**
   - Ensure the app meets accessibility standards (e.g., keyboard navigation, screen reader support).

10. **Mobile Compatibility:**
    - Explore options for creating a mobile version of the app using frameworks like Kivy or BeeWare.

</details>

<details>
<summary><h2>Project Screenshots</h2></summary>

![Main Interface](https://github.com/user-attachments/assets/aec80baf-91a6-4c5f-a0a5-734e763acb20)

![Password Entry](https://github.com/user-attachments/assets/59908581-28d4-4922-8fc4-187b9b27a598)

![Password List](https://github.com/user-attachments/assets/e5e4a3cb-87f0-45bd-af4b-f444c4f11cee)


</details>


## Usage Guide 📝

### Adding a Password
1. Open the application and navigate to the "Add Password" section.
2. Fill in the required fields:
   - **Website**: Enter the name of the website or service.
   - **Email/Username**: Enter the associated email or username.
   - **Password**: You can either type in your password or click the "Generate" button to create a strong password automatically.
3. Click on the "Save" button to store the password.

### Viewing Saved Passwords
1. Navigate to the "View Passwords" section.
2. You will see a list of all saved passwords.
3. You can use the search bar to quickly find a specific entry.

### Editing a Password
1. Go to the "View Passwords" section.
2. Find the password entry you wish to edit and click the "Edit" button next to it.
3. Make the necessary changes and click "Save".

### Deleting a Password
1. In the "View Passwords" section, find the password you want to delete.
2. Click the "Delete" button next to the entry.
3. Confirm the deletion when prompted.

### Searching for Passwords
1. Navigate to the "View Passwords" section.
2. Use the search bar at the top to enter a website or email.
3. The list will automatically filter to show matching entries.

### Generating Strong Passwords
1. While adding or editing a password, click the "Generate" button next to the password field.
2. The app will create a strong password for you. You can then modify it if needed before saving.

## Contributing 🤝

◉ We welcome contributions from everyone! Here’s how you can help:

### Steps to Contribute
1. **Fork the Repository**: Click on the "Fork" button at the top right corner of the repository page to create your copy.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/your-username/Password-Manager.git
   ```

3. **Create a New Branch**:
   ```bash
   git checkout -b feature-branch-name
   ```

4. **Make Your Changes**: Add features, fix bugs, or improve documentation.

5. **Commit Your Changes**:
   ```bash
   git commit -m "Description of your changes"
   ```

6. **Push to Your Fork**:
   ```bash
   git push origin feature-branch-name
   ```

7. **Submit a Pull Request**: Go to the original repository and click on "New Pull Request". Provide a clear description of your changes and why you think they should be merged.

### Guidelines for Contributions
- **Code Quality**: Ensure your code is clean, well-documented, and follows existing project conventions.
- **Issues**: If you find a bug or want to suggest a feature, please open an issue to discuss it before starting work.
- **Testing**: If your changes involve code, please write tests to ensure it works as intended.

◉ More details on how to contribute can be found in the [CONTRIBUTING.md](DOCS/CONTRIBUTING.md) file.

## Acknowledgments 🙏
Special thanks to the developers of CustomTkinter and SQLite for providing the tools used in this application.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
