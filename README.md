LandMark - Real Estate Listings Platform
A full-stack Django-based web application that allows users to browse, post, and manage real estate listings for sale or rent. Designed with a user-friendly interface and a focus on efficient property discovery and management.

🚀 Features
🏡 Browse Listings: Users can view available properties with images, prices, and details.

🔍 Search & Filters: Filter listings by location, price, type, and more.

📢 Post Listings: Registered users can post their own property ads for sale or rent.

✅ Ad Approval System: Admin reviews and approves submitted ads before they're published.

📊 Market Insights Page: View trends on property prices, house loans, and real estate news.

🔐 User Authentication: Sign up, log in, log out, and manage account securely.

📦 Session-Based Ad Posting: Step-by-step guided ad creation with session tracking.

🖼️ Image Upload: Add multiple images to property listings.


🛠️ Technologies Used
Backend: Django, Python

Frontend: HTML, CSS, Bootstrap, JavaScript

Database: SQLite (default), customizable to PostgreSQL/MySQL

Other: Django sessions, Django Admin, Media files handling


📦 Setup Instructions
Clone the repo:

bash
Copy
Edit
git clone https://github.com/your-username/real-estate-platform.git
cd real-estate-platform
Create virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run migrations:

bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
Create superuser:

bash
Copy
Edit
python manage.py createsuperuser
Run the server:

bash
Copy
Edit
python manage.py runserver
Access the app:
Go to http://127.0.0.1:8000/

📌 Notes
Media files are stored in the /media folder and served via Django during development.

Admin dashboard is accessible at /admin/.


📷 Screenshots
![Screenshot 2025-05-06 220729](https://github.com/user-attachments/assets/8b05dca5-02a7-4899-be36-229d5ece875f)

![Screenshot 2025-05-06 220743](https://github.com/user-attachments/assets/a5dc0cd5-9ee8-495c-96b1-38878d19e02a)

![Screenshot 2025-05-06 220811](https://github.com/user-attachments/assets/e95373ce-2bda-46b0-ac80-6fea614e5bbe)

![Screenshot 2025-05-06 220831](https://github.com/user-attachments/assets/3d419de8-af09-4914-8471-9507de6be1b2)

![Screenshot 2025-05-06 220849](https://github.com/user-attachments/assets/9f53654b-b88c-48db-97ed-9570f7642cc3)

![Screenshot 2025-05-06 220900](https://github.com/user-attachments/assets/0808a127-01fe-4c19-99df-671538a16c27)

![Screenshot 2025-05-06 220939](https://github.com/user-attachments/assets/9ba309b6-f898-4b7b-a32c-1b7eb17aa624)



