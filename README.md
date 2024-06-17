# Geocoding Web Service

[![GitHub](https://badgen.net/badge/icon/GitHub?icon=github&color=black&label)](https://github.com/MaxineXiong)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://www.python.org)
[![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Flask](https://img.shields.io/badge/Flask-323232?logo=Flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Folium](https://img.shields.io/badge/Folium-77B829?logo=Folium&logoColor=white)](https://python-visualization.github.io/folium/latest/)

<br>


## Project Description

[**SuperGeocoder**](https://supergeocoder-838a4a6bdd3b.herokuapp.com/) is an online geocoding service built in Python with [Flask](https://flask.palletsprojects.com/) that effortlessly **transforms all address data within user-uploaded files into precise latitude and longitude coordinates**. Upon uploading a file, users can instantly preview the output table on the website or opt to download the file in its converted format. Additionally, the integrated mapping service enhances the user experience by enabling them to visualise the exact location of each address on a map, offering deeper insights into each site.

You can check out the **web service demo video** by clicking on the badge below:

[![View Demo - SuperGeocoder](https://img.shields.io/badge/View_Demo-SuperGeocoder-DD0700)](https://1drv.ms/v/s!AhxVr7ogXVBRlTHtLlsWej5oeUib)

<br>

## Features

- **Geocoding**: Converts address data in uploaded files to precise latitude and longitude coordinates.
- **Data Preview**: Allows users to preview the geocoded data table on the website.
- **File Download**: Users can download the geocoded file in its converted format.
- **Mapping Service**:  Enables users to visualise the exact location of each address on a map.

<br>

## Repository Structure

The repository is structured as follows:

```
SuperGeocoder/
├── app.py
├── templates/
│   ├── index.html
│   ├── file_processed.html
│   ├── invalid_file_uploaded.html
│   └── example.html
├── static/
│   ├── main.css
│   └── assets/
│       ├── favicon.ico
│       └── background.jpg
├── sample inputs/
│   ├── bad_sample.csv
│   ├── sample_1.csv
│   ├── sample_2.csv
│   ├── sample_3.xlsx
│   └── sample_4.xlsx
├── sample outputs/
│   ├── geocoded_sample_1.csv
│   ├── geocoded_sample_2.csv
│   ├── geocoded_sample_3.xlsx
│   └── geocoded_sample_4.xlsx
├── requirements.txt
├── .gitignore
├── Procfile
├── README.md
└── LICENSE

```

- **app.py**: The main application file for the Flask web application, [**SuperGeocoder**](https://supergeocoder-838a4a6bdd3b.herokuapp.com/). It handles all the backend logic, including routing, file processing, and interactions with geocoding services.
- **templates/**: Contains HTML templates for rendering web pages.
    - **index.html**: The home page of the application.
    - **file_processed.html**: Displays the processed data table and allows download.
    - **invalid_file_uploaded.html**: Error page shown when an invalid file is uploaded.
    - **example.html**: Provides an example of a valid input file format.
- **static/**: Holds static assets and CSS files.
    - **main.css**: Contains styles for the web pages.
    - **assets/**: Includes images and icons.
        - **favicon.ico**: The favicon for the web application.
        - **background.jpg**: The background image used on the web pages.
- **sample inputs/**: Contains sample CSV and Excel input files for testing the application.
- **sample outputs/**: Contains the geocoded output files corresponding to the sample input files.
- **requirements.txt**: Lists all necessary Python libraries and dependencies required to run the application. These can be installed via the command `pip install -r requirements.txt`.
- **.gitignore**: Specifies which files and directories Git should ignore, helping to keep the repository clean from unnecessary or sensitive files.
- **Procfile**: Used for deploying the application on [*Heroku*](https://www.heroku.com/).
- **README.md**: Provides a detailed overview of the repository, including descriptions of its features, usage instructions, and information on how to contribute.
- **LICENSE**: The license file for the project.

<br>

## **Usage**

You can either access the **[SuperGeocoder](https://supergeocoder-838a4a6bdd3b.herokuapp.com/)** web service in production by clicking on the badge below:

[![SuperGeocoder](https://img.shields.io/badge/SuperGeocoder-DD0700?style=for-the-badge&logo=Google+Maps&logoColor=white)](https://supergeocoder-838a4a6bdd3b.herokuapp.com/)

Or run the web application locally on your computer by following these steps:

1) Clone this repository to your local machine using the following command:
    
    ```
    git clone https://github.com/MaxineXiong/Geocoding-Web-Service.git
    ```
    
2) Download and install the latest version of [Python](https://www.python.org/downloads/) for your system. Make sure to select the "Add Python to PATH" option during the installation process.
3) Navigate to the project folder using File Explorer, type `cmd` in the address bar at the top of the window, and press Enter. This will open Command Prompt in the project folder.
4) Install the required packages by executing the following command in the Command Prompt:
    
    ```
    pip install -r requirements.txt
    ```
    
5) Now run the geocoding web application by entering the following command in the Command Prompt:
    
    ```
    python app.py
    ```
    
6) Open your web browser and go to `http://127.0.0.1:5000/` to access the web app locally.

<br>

## Contribution

Contributions to this geocoding web service are welcome! If you have suggestions to improve the application or add new features, please fork the repository and submit a pull request, or open an issue detailing the changes or additional features you have in mind.

<br>

## **License**

This project is licensed under the MIT License. See the [LICENSE](https://choosealicense.com/licenses/mit/) file for more details.

<br>

## Acknowledgements

Special thanks to the following tools and libraries that have made this project possible:

- [**Flask**](https://flask.palletsprojects.com/): A lightweight and flexible web framework for Python. It allows developers to build web applications quickly and efficiently. Flask provides essential features for routing, handling requests, and managing sessions.
- [**Folium**](https://python-visualization.github.io/folium/latest/): Python library for visualizing geospatial data. It is built on top of Leaflet.js, a JavaScript library for interactive maps.
- [**Pandas**](https://pandas.pydata.org/): Python data analysis library. It provides data structures (such as DataFrames and Series) and functions for data cleaning, transformation, and analysis.
- [**Geopy**](https://geopy.readthedocs.io): Python library that provides geocoding and reverse geocoding capabilities. It converts addresses into geographic coordinates (latitude and longitude) and vice versa.
- [**Werkzeug**](https://werkzeug.palletsprojects.com/): Comprehensive WSGI web application library. It provides low-level utilities for handling HTTP requests, routing, and other web-related tasks.
- [**Python**](https://www.python.org/): The programming language used to develop this application.
