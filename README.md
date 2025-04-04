# Facebook Group Post Sharing Automation

This script uses Selenium with undetected_chromedriver to automate sharing a specific post to multiple Facebook groups.

---

## ⚠️ Warning
Ensure that you use this script legally and in compliance with Facebook's policies. Spamming or misuse may lead to account suspension or banning.

---

## Table of Contents

- [Description](#description)
- [Code Explanation](#Code-Explanation)
- [Requirements](#requirements)
- [Features](#Features)
- [Installation](#installation)
- [Usage](#usage)
- [Additional Notes](#additional-notes)
- [Notes](#notes)
- [Supported Languages](#supported-languages)
- [License](#License)

---

## Description

This script performs the following tasks:
- Launches a Chrome browser using undetected_chromedriver to help bypass automation detection.
- Loads browser data (cookies and user agent) to facilitate logging in without requiring credentials repeatedly.
- Logs into Facebook using the provided credentials.
- Waits for the user to manually navigate to and open the desired post.
- Reads the post content from the file `post.txt`.
- Opens the share window and selects groups from the list.
- Shares the post in each group, starting from the specified group number.
- Uses multiple XPath expressions to accommodate differences in Facebook's interface.

---

## Code Explanation
The script relies on libraries like selenium and undetected_chromedriver to control a Chrome browser and avoid detection by Facebook. It includes the following steps:
* Browser Setup: Initializes Chrome with options to avoid detection, such as disabling automation-controlled features and setting a natural user agent.
* Data Saving and Loading: Saves cookies and browser data to a JSON file for faster future logins.
* Login: Prompts the user for credentials and uses them to log into Facebook.
* Post Identification: Asks the user to manually open the desired post, then reads the sharing message from post.txt.
* Post Sharing: Identifies available groups, allows the user to choose a starting point, and automatically shares the post to each group using predefined XPaths.
* Error Handling: Includes mechanisms to handle errors such as missing page elements or publishing issues.

---


## Features
- **Stealth Mode**: Utilizes `undetected_chromedriver` to avoid detection by Facebook's automation detection systems.
- **Automatic Login**: Logs into Facebook using provided credentials and saves browser data (cookies, user agent, etc.) for future use.
  * for those who makes a second Virefication for not accept the verify Every time, you can only do `Trust This Device` When you login at the first time, and ther's no need to do it any more even you have the `json Data File` in the code folder that created after run the script and login for first time.
- **Post Sharing**: Shares a predefined post (from `post.txt`) to multiple Facebook groups.
- **Group Selection**: Allows starting from a specific group number and automatically handles group selection.
- **Multi-Language Support**: Supports multiple languages for detecting the text area (see supported languages below).

---
## Requirements

The script requires the following packages:
- selenium
- undetected-chromedriver
- colorama

You can install all dependencies using the provided `requirements.txt` file.

---

## Installation

1. Ensure you have Python (preferably Python 3.7 or later) installed.
2. (Optional) Create and activate a virtual environment.
3. Install the required packages by running:

   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the post.txt file is present in the same directory as the script. This file should contain the post message you want to share.

## Usage
1. Run the script:
   ```
   python FBG-Share.py
   ```
2. When prompted, enter:
   * Your Facebook account name (email or phone number).
   * Your Facebook password.
   * The group number from which you want to start sharing (e.g., 1 for the first group).
3. The script will automatically open a Chrome browser and log into Facebook.
4. Manually navigate to your profile and open the desired post.
5. Press Enter to continue once the post is open.
6. The script will start sharing the post to the selected groups one by one.
7. A success message will be displayed after each group, and a final message will confirm the process is complete.

---

## Additional Notes
### 💬 Additional Notes
* This code uses undetected_chromedriver, which might require updates depending on the latest version of Chrome or changes in Facebook policies.
* Keep an eye on any updates to the libraries used to ensure smooth operation.
  ```bash
  pip install --upgrade pip
  pip install --upgrade -r requirements.txt
  ```
  * Verify the Updates:
    ```bash
    pip list
    ```
  * Check Specific Packages:
    ```bash
    pip show undetected_chromedriver
    pip show selenium
    pip show colorama
    ```
  ## Additional Tips:
  * Manual Updates: If you prefer updating libraries one by one, use:
    ```bash
    pip install --upgrade undetected_chromedriver
    pip install --upgrade selenium
    pip install --upgrade colorama
    ```
  * **Compatibility:** Some libraries, like undetected_chromedriver, depend on external software (e.g., Chrome). Ensure your Chrome browser is updated to match the latest undetected_chromedriver version.
---

## Notes
* Important: If the number of groups you intend to use this script for is less than 10, it is recommended to post manually. There is no need to use the script in such cases.

---

## Supported Languages
The script supports the following languages based on the aria-label attributes specified in the text_area_xpath:
  * Arabic: "إنشاء منشور عام...", "اكتب شيئًا..."
  * English: "Create a public post...", "Write something..."
  * French: "Créer une publication publique...", "Écrire quelque chose..."
  * Italian: "Crea un post pubblico...", "Scrivi qualcosa..."
  * Spanish: "Crea una publicación pública...", "Escribe algo..."
  * Portuguese: "Criar uma publicação pública...", "Escreva algo..."
  * German: "Öffentliche Beitrag erstellen...", "Schreibe etwas...", "Schrijf iets..."
  * Dutch: "Maak een openbaar bericht..."
  * Polish: "Stwórz publiczny post...", "Napisz coś..."
  * Russian: "Создать публичный пост...", "Напишите что-нибудь..."
  * Thai: "สร้างโพสต์สาธารณะ...", "เขียนอะไรบางอย่าง..."
  * Indonesian/Malay: "Buat postingan publik...", "Tulis sesuatu..."
  * Simplified Chinese: "建立公开贴文...", "写点什么..."
  * Traditional Chinese: "创建公开帖子..."
  * Filipino: "Gumawa ng pampublikong post...", "Sumulat ng isang bagay..."

If you need to add support for another language, you can modify the `text_area_xpath` in the script by adding the appropriate `aria-label` for that language. Alternatively, you can contact me (please communicate in English or Arabic).

---


## License
* This project is licensed under the MIT License.
