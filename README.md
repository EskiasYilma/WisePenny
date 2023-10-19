
# WisePenny: (Health Information System)
![Latest commit](https://img.shields.io/github/last-commit/EskiasYilma/WisePenny?style=round-square)

![logo](https://github.com/EskiasYilma/WisePenny/blob/main/product/static/wisepenny/discount_2.png)

A light-weight but Robust Django web application designed to facilitate price comparison for a wide range of electronics products available in Ethiopia.

As a Specialization Portfolio Project for ALX Software Engineering Program/Holberton School, this web app showcases my expertise in web development and demonstrates my ability to tackle complex projects independently. Throughout the development process, which spanned about couple of weeks, I meticulously crafted the app, ensuring its functionality, usability, and security. (Note: Ongoing work is required for continuous improvement.)

This Project endeavors to Empower Ethiopian consumers with the tools to make informed purchasing decisions. In an effort to Streamline the online shopping experience, saving both time and money, this project strives to incorporate Electronics product categories (expanding to all categories in the future), ensuring accurate and relevant comparisons.

## Video Demo



My dynamic Django web application, Wisepenny, is on a mission to revolutionize the way consumers in Ethiopia purchase electronics products.

## Challenges:

- In the dynamic Ethiopian electronics market, online pricing variations are common, and language complexities pose unique challenges.
- Wisepenny bridges these gaps, offering consumers the ability to make informed choices and save money.
- It streamlines the online shopping experience, addressing market complexities head-on.

## Journey:

As a solo developer on this project, I poured my passion and dedication into creating a solution that would make a meaningful impact in the electronics consumers sector. Throughout the development process, I embraced a human-centered approach, always keeping in mind the end-users – the buyers who rely on this system to make informed purchasing decisions.
The journey to build WisePenny was filled with both triumphs and struggles. I meticulously planned the project timeline, leveraging tools like Trello to track progress and set deadlines. However, I faced technical complexities and design challenges that required thoughtful problem-solving and perseverance. Despite the hurdles, I remained committed to delivering a high-quality solution.

## Limitations:

### Focus on Electronics: Rationale for Limited Product Category

The present system confines its analytical purview to the fundamental domain of price comparison, particularly within the realm of electronics. This selective approach emanates from a judicious consideration of several pertinent factors:

**Product Availability:** Electronics emerge as an ideal focal point due to their ubiquity and availability within the Ethiopian market. This ensures a robust and comprehensive dataset, facilitating a more meaningful and actionable price comparison.

**Linguistic Complexity:** A significant barrier in expanding the scope to include a broader array of product categories is the predominant use of the Amharic language within various classified platforms. The complexity of Amharic text encoding presents a formidable challenge in the context of efficient data extraction and comparative analysis.

**Price Dynamism:** The system's choice to specialize in electronics is further substantiated by the dynamic nature of pricing patterns within this category. Frequent updates and revisions of product prices by sellers necessitate a responsive and adaptable analytical framework.

**Terminological Precision:** The electronics category lends itself favorably to precise analysis, as sellers demonstrate a proclivity for utilizing technology-specific terminology and nomenclature in their product descriptions and titles. This precision augments the system's ability to provide accurate and contextually relevant price comparisons.

As I reflect on this project, I recognize that there is always room for improvement and growth. In the next iteration, I envision expanding the system's capabilities to include more categories, advanced analytics and reporting tools, integrating Price History Changes functionalities, Product Reviews, Recommendation Algorithms and enhancing the user interface for a seamless user experience.

If you are passionate about this project or discuss potential opportunities, I would love to connect with you. Feel free to reach out to me via [Linkedin](https://www.linkedin.com/in/eskiasyilma) or [Email](eskias@m-ini.me).

## Deployed Demo Site
You can test the deployed webapp on https://wisepenny.m-ini.me.


## Screenshots
![User Dashboard](https://github.com/EskiasYilma/Mini-HIS/assets/113903630/069ebb66-e287-43cb-b2f3-058647ccd18b)
![HomePage](https://github.com/EskiasYilma/Mini-HIS/assets/113903630/bb8cf2a9-f1d6-4318-8be1-03cdb5fe3bd1)
![Quick Results](https://github.com/EskiasYilma/Mini-HIS/assets/113903630/f9a8eda8-2413-4b40-ab2c-fd2749dbe634)
![Detailed Results](https://github.com/EskiasYilma/Mini-HIS/blob/master/screenshots/patient_dash.png)


## Tech Stack

**FrontEnd:** HTML, CSS, Vanilla JavaScript, Bootstrap

**BackEnd:** Django, Python3 [deployed with v3.8.6, tested with v3.11]

**Database:** MySQL, SQLite3(current)


## Color Reference

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Yellow | ![#FFC801](https://via.placeholder.com/10/ffc801?text=+) #FFC801 |
| Grey | ![#212529](https://via.placeholder.com/10/212529?text=+) #212529 |
| Light Grey | ![#39404a](https://via.placeholder.com/10/39404a?text=+) #39404a |

## Run Locally

Clone the project

```bash
  git clone https://github.com/EskiasYilma/WisePenny.git
```

Create a Python3 Virtual environment and activate it (optional)

```bash
  python3 -m venv your_venv_name
  source your_venv_name/bin/activate
```

Go to the project directory

```bash
  cd wisepenny
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Configure Environment Variables (/HIS_V1/.env)

```bash
  # Generate a Secret key
  python manage.py shell
  >>> from django.core.management.utils import get_random_secret_key
  >>> get_random_secret_key()
  # SECRET_KEY > key_generated_above
  # DEBUG > 0 = On   1 = Off
  # ALLOWED_HOST > your_domain_name (eg. 127.0.0.1)
  # EMAIL_HOST > your_smtp_host
  # EMAIL_PORT > your smtp port
  # EMAIL_HOST_USER > your smtp username
  # EMAIL_HOST_PASSWORD > your smtp password
  # NAME > your database name
  # HOST > your database host
  # PORT > your database port
  # USER > your database username
  # PASSWORD > your database password
```

Migration

```bash
  python3 manage.py makemigrations
  python3 manage.py makemigrations product
  python3 manage.py migrate
```

Start the server

```bash
  python3 manage.py runserver
```

## Features

- Electronics Price Comparision, Sorting and Search
- Personal Dashboard to track user searches
- Notification [Not Complete]
- Custom analytics for products and price sources

## Contributing

Thank you for your interest in contributing to the WisePenny app! I welcome contributions from the community to help improve and enhance the project. To contribute, please follow the guidelines below:

    Reporting Issues:
        If you encounter any bugs, issues, or have feature requests, please create a new issue on our issue tracker.
        Provide a clear and detailed description of the problem or request, including steps to reproduce if applicable.
        Check the existing issues to avoid creating duplicates.

    Pull Requests:
        Fork the repository and create a new branch for your contribution.
        Ensure your code follows the project's coding style and conventions.
        Write clear and concise commit messages.
        Submit a pull request to the main branch and provide a detailed description of the changes made.
        Your pull request will be reviewed by the project maintainers.

    Development Setup:
        Clone the repository to your local machine.
        Set up the development environment following the instructions in the Development Setup Guide.
        Make your changes and run tests to ensure everything is working as expected.
        Update the documentation, if necessary.
        Push your changes to your branch and submit a pull request.

By contributing to this project, you agree to abide by the [Code of Conduct](https://github.com/EskiasYilma/WisePenny/blob/master/CODE_OF_CONDUCT.md) and create a positive and inclusive environment for all contributors.
I appreciate your contributions and look forward to your involvement in making the WisePenny app even better!

## Authors

- [@EskiasYilma](https://www.github.com/EskiasYilma)
- [Twitter](https://twitter.com/eskiasyilma)
