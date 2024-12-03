<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://i.ibb.co/9VMMZ0Z/462576758-984678703495193-5655876495060392474-n.png" alt="Logo" height="100">
</a>

<h3 align="center">IntelliForums</h3>

<p align="center">
  Final Requirement for Information Management 2
  <br>
  <a href="https://github.com/Anato-Eini/IntelliForums/issues/new?assignees=&labels=&projects=&template=bug_report.md"><strong>Report Bug</strong></a>
  ·
  <a href="https://github.com/Anato-Eini/IntelliForums/issues/new?assignees=&labels=&projects=&template=feature_request.md"><strong>Request Feature</strong></a>
</p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    <li>
        <a href="#functional-requirements">Functional Requirements</a>
        <ul>
            <li><a href="#user-management">User Management</a></li>
            <li><a href="#post-management">Post Management</a></li>
            <li><a href="#comment-management">Comment Management</a></li>
            <li><a href="#admin-management">Admin Management</a></li>
        </ul>
    </li>
    <li>
        <a href="#entity-relationship-diagram-erd">Entity-Relationship Diagram (ERD)</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About The Project
IntelliForums is a web-based forum application designed to facilitate discussions and information sharing among users. The platform allows users to create and manage posts, comment on discussions, and interact with other users through upvotes and downvotes. Admins have the ability to moderate content and manage user activities to ensure a safe and productive environment.

Key features of IntelliForums include:

- User registration and login
- Profile management
- Post creation, editing, and deletion
- Commenting on posts
- Upvoting and downvoting posts and comments
- Reporting inappropriate content
- Admin panel for user and content management

The project aims to provide a robust and user-friendly forum experience, leveraging modern web technologies to ensure scalability and maintainability.

### Built With
The project is built using the following libraries/frameworks:

<div align="center">
    <a href="https://getbootstrap.com/">
        <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
    </a>
    <a href="https://jquery.com/">
        <img src="https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white" alt="jQuery">
    </a>
    <a href="https://www.djangoproject.com/">
        <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" alt="Django">
    </a>
    <a href="https://www.sqlite.org/">
        <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
    </a>
    <a href="https://developer.mozilla.org/en-US/docs/Web/HTML">
        <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
    </a>
</div>

<div align="right">
    <a href="#readme-top">
        <img src="https://img.shields.io/badge/back%20to%20top-%E2%86%A9-blue?style=for-the-badge" alt="Back to top">
    </a>
</div>

## Figma

<a href="https://www.figma.com/design/RyUp3QbuiyquVUd6hOr0Bn/IM2?node-id=0-1&node-type=canvas" target="_blank">
    <img src="https://img.shields.io/badge/View%20Figma%20Design-%E2%86%A9-blue?style=for-the-badge" alt="View Figma Design">
</a>

## Gantt Chart

<a href="https://docs.google.com/spreadsheets/d/1emJhUlhcaSpzuB8jP_2BvoRQ1bP72NqA/edit?gid=610723999#gid=610723999" target="_blank">
    <img src="https://scontent.fcgy2-4.fna.fbcdn.net/v/t1.15752-9/462645479_8565679093542147_5851800317613133830_n.png?stp=dst-png_s2048x2048&_nc_cat=110&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeGnwvpdAo3TQJsmpDTaHaPiNaQn-H2gH_A1pCf4faAf8IR_7ErkD4puasXLwZcWoR0vhTvAyilIgJRhcpJaAgS5&_nc_ohc=Jq_h0vBJMRQQ7kNvgFNScme&_nc_zt=23&_nc_ht=scontent.fcgy2-4.fna&oh=03_Q7cD1QHKNqsHqPcOqdm3xLT6HIQOJh3osf-SJZj2hV8P-832gg&oe=6776C2E2" alt="View Gantt Chart">
    <br>
</a>



## Functional Requirements

### User Management
- **User Registration**: Allow users to create an account.
- **User Login**: Enable users to log into their account.
- **View Own Profile**: Users can view and edit their own profile information.
- **View Others’ Profile**: Users can view the profiles of other users.
- **Appeal for Unban (for Banned Users)**: Banned users can submit an appeal to be unbanned.

### Post Management
- **Post Creation**: Users can create new posts.
- **Update Post**: Users can edit their existing posts.
- **Soft-delete Post**: Users can temporarily delete their posts.
- **Restore Soft-deleted Post**: Users can restore their temporarily deleted posts.
- **Permanently Delete Post**: Users can permanently delete their posts.
- **Upvote/Downvote Posts**: Users can upvote or downvote posts.
- **Report Post**: Users can report posts that violate guidelines.

### Comment Management
- **Comment Creation**: Users can add comments to posts.
- **Update Comment**: Users can edit their comments.
- **Delete Comment**: Users can delete their comments.
- **Upvote/Downvote Comments**: Users can upvote or downvote comments.
- **Report Comment**: Users can report comments that violate guidelines.

### Admin Management
- **Ban User**: Admins can ban users who violate guidelines.
- **Unban User**: Admins can unban users.
- **View Admin Panel**: Admins can access the admin panel to manage the platform.
- **Resolve Post Reports**: Admins can review and resolve reported posts.
- **Resolve Comment Reports**: Admins can review and resolve reported comments.

## Entity-Relationship Diagram (ERD)
<a href="https://scontent.fcgy2-2.fna.fbcdn.net/v/t1.15752-9/467019518_1111649553167318_238892060902087252_n.png?_nc_cat=104&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeFD9UULvhw5Vs0PKEFvFXqD-EmNKzPaWjT4SY0rM9paNKoyoW7rBekDziv1uCRPR5IjuIKoMhtOwds9BFybZHr1&_nc_ohc=7s61v_gGAWQQ7kNvgEE-qz9&_nc_zt=23&_nc_ht=scontent.fcgy2-2.fna&oh=03_Q7cD1QGgoupOhEqQdIxXYmXUUp9-mf_47S3lA-Fvd1ZAkcjRng&oe=6776A09F">
<img src="https://scontent.fcgy2-2.fna.fbcdn.net/v/t1.15752-9/467019518_1111649553167318_238892060902087252_n.png?_nc_cat=104&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeFD9UULvhw5Vs0PKEFvFXqD-EmNKzPaWjT4SY0rM9paNKoyoW7rBekDziv1uCRPR5IjuIKoMhtOwds9BFybZHr1&_nc_ohc=7s61v_gGAWQQ7kNvgEE-qz9&_nc_zt=23&_nc_ht=scontent.fcgy2-2.fna&oh=03_Q7cD1QGgoupOhEqQdIxXYmXUUp9-mf_47S3lA-Fvd1ZAkcjRng&oe=6776A09F"></img>
</a>


### Prerequisites

* Python 3.x
    ```sh
        # For Ubuntu
        sudo apt-get install python3

        # For Windows
        choco install python

        # For macOS
        brew install python
    ```
* pip
    ```sh
        # For Ubuntu
        sudo apt-get install python3-pip

        # For Windows
        python -m ensurepip --upgrade

        # For macOS
        python3 -m ensurepip --upgrade
    ```
* Django
    ```sh
        pip install django
    ```
* SQLite (optional, if not already installed)
    ```sh
        # For Ubuntu
        sudo apt-get install sqlite3

        # For Windows
        choco install sqlite

        # For macOS
        brew install sqlite
    ```

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/Anato-Eini/IntelliForums.git
    ```
2. Navigate to the project directory
    ```sh
    cd IntelliForums
    ```
3. Create a virtual environment
    ```sh
    python3 -m venv venv
    ```
4. Activate the virtual environment
    ```sh
    # For Ubuntu/macOS
    source venv/bin/activate

    # For Windows
    .\venv\Scripts\activate
    ```
5. Install the required packages
    ```sh
    pip install -r requirements.txt
    ```
6. Apply migrations
    ```sh
    python manage.py migrate
    ```
7. Run the development server
    ```sh
    python manage.py runserver
    ```

<div align="right">
    <a href="#readme-top">
        <img src="https://img.shields.io/badge/back%20to%20top-%E2%86%A9-blue?style=for-the-badge" alt="Back to top">
    </a>
</div>





<!-- ROADMAP -->
## Roadmap


See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<div align="right">
    <a href="#readme-top">
        <img src="https://img.shields.io/badge/back%20to%20top-%E2%86%A9-blue?style=for-the-badge" alt="Back to top">
    </a>
</div>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this project better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<div align="right">
    <a href="#readme-top">
        <img src="https://img.shields.io/badge/back%20to%20top-%E2%86%A9-blue?style=for-the-badge" alt="Back to top">
    </a>
</div>

### Top contributors:

<a href="https://github.com/othneildrew/Best-README-Template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Anato-Eini/IntelliForums" alt="contrib.rocks image" />
</a>

<div align="right">
    <a href="#readme-top">
        <img src="https://img.shields.io/badge/back%20to%20top-%E2%86%A9-blue?style=for-the-badge" alt="Back to top">
    </a>
</div>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<div align="right">
    <a href="#readme-top">
        <img src="https://img.shields.io/badge/back%20to%20top-%E2%86%A9-blue?style=for-the-badge" alt="Back to top">
    </a>
</div>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Anato-Eini/IntelliForums.svg?style=for-the-badge
[contributors-url]: https://github.com/Anato-Eini/IntelliForums/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Anato-Eini/IntelliForums.svg?style=for-the-badge
[forks-url]: https://github.com/Anato-Eini/IntelliForums/network/members
[stars-shield]: https://img.shields.io/github/stars/Anato-Eini/IntelliForums.svg?style=for-the-badge
[stars-url]: https://github.com/Anato-Eini/IntelliForums/stargazers
[issues-shield]: https://img.shields.io/github/issues/Anato-Eini/IntelliForums.svg?style=for-the-badge
[issues-url]: https://github.com/Anato-Eini/IntelliForums/issues
[license-shield]: https://img.shields.io/github/license/Anato-Eini/IntelliForums.svg?style=for-the-badge
[license-url]: https://github.com/Anato-Eini/IntelliForums/blob/master/LICENSE
[product-screenshot]: images/screenshot.png
