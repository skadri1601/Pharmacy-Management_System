# Pharmacy Management System

A comprehensive web-based pharmacy management system built with Django that facilitates medicine management, user registration, chemist store operations, and online pharmacy services.

## 🚀 Features

### User Features
- **User Registration & Authentication**: Secure user registration with email-based login
- **Medicine Search & Browse**: Search medicines by symptoms, diseases, or medicine names
- **Shopping Cart**: Add medicines to cart and manage quantities
- **Medicine Guide**: Comprehensive medicine information including:
  - Symptoms and diseases treated
  - Drug composition and category
  - Dosage information (unit and package pricing)
  - Indications and contraindications
  - Side effects and cautions
- **Password Recovery**: Forgot password functionality with hint-based recovery
- **User Queries**: Contact form for user inquiries

### Chemist/Store Features
- **Chemist Registration**: Complete profile setup with store certificate upload
- **Store Management**: Manage store details and contact information
- **Inventory Management**:
  - Add and edit products
  - Track stock quantities and pricing
  - View product listings
- **Sales Management**:
  - Process sales transactions
  - Generate bills and track sales history
  - View sales reports
- **Dashboard**: Comprehensive store dashboard for operations management

### Admin Features
- **Medicine Database**: Comprehensive medicine catalog management
- **User Management**: Manage registered users and chemists
- **Store Verification**: Verify chemist store certificates
- **Query Management**: Handle user inquiries and support requests

## 🛠 Technology Stack

- **Backend**: Django 3.1+ (Python web framework)
- **Database**: SQLite3 (development), easily configurable for PostgreSQL/MySQL
- **Frontend**: HTML5, CSS3, Bootstrap
- **JavaScript**: jQuery for dynamic interactions
- **File Handling**: Django file upload for certificates and documents

## 📁 Project Structure

```
Pharmacy-Management_System/
├── Uphar/                      # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── Chemist_Master/            # Chemist/Store management app
│   ├── models.py             # Chemist, Store, Product models
│   ├── views.py              # Store operations views
│   ├── forms.py              # Store-related forms
│   └── templates/            # Store dashboard templates
├── User_Master/               # User management app
│   ├── models.py             # User, Cart models
│   ├── views.py              # User operations views
│   └── templates/            # User interface templates
├── guide/                     # Medicine guide app
│   ├── models.py             # Medicine information models
│   └── templates/            # Medicine guide templates
├── med/                       # Medicine management app
│   ├── models.py             # Medicine inventory models
│   └── templates/            # Medicine management templates
├── db.sqlite3                 # Database file
└── manage.py                  # Django management script
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Pharmacy-Management_System
   ```

2. **Create virtual environment**
   ```bash
   python -m venv pharmacy_env

   # Windows
   pharmacy_env\Scripts\activate

   # macOS/Linux
   source pharmacy_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   pip install pillow  # For image handling
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 🗃 Database Models

### User Management
- **UserRegister**: User profiles with contact details and authentication
- **cart**: Shopping cart functionality linking users to medicines
- **UserQuery**: User inquiry and support system

### Chemist Management
- **ChemistRegister**: Chemist profiles with store verification
- **StoreDetails**: Store information and contact details
- **ProductDetails**: Product management with approval workflow
- **SK_Bills**: Sales transaction records

### Medicine System
- **guides**: Comprehensive medicine database with detailed information
- **Medicine**: Medicine inventory management (legacy model)
- **StockDetails**: Stock quantity and pricing management

## 🔧 Configuration

### Settings Customization
Update `Uphar/settings.py` for:
- Database configuration
- Media file handling
- Security settings (SECRET_KEY, DEBUG)
- Allowed hosts for production

### Template Paths
The system uses multiple template directories:
- Chemist templates: `Chemist_Master/templates/`
- User templates: `User_Master/templates/`
- Medicine guide templates: `guide/templates/`

## 🌟 Key Functionalities

### Medicine Management
- Comprehensive medicine database with symptoms, diseases, and drug information
- Unit and package pricing management
- Category-based medicine organization
- Detailed medicine information including side effects and contraindications

### Store Operations
- Chemist registration with certificate verification
- Product inventory management
- Sales processing and bill generation
- Dashboard for store analytics

### User Experience
- Intuitive medicine search and browsing
- Shopping cart functionality
- Secure user authentication
- Password recovery system

## 🚀 Deployment

### Production Considerations
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL/MySQL)
3. Set up static file serving
4. Configure ALLOWED_HOSTS
5. Use environment variables for sensitive data
6. Set up proper media file handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support and inquiries:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common solutions

## 🔮 Future Enhancements

- Online payment integration
- SMS/Email notifications
- Medicine prescription upload
- Advanced analytics and reporting
- Mobile app development
- API development for third-party integrations
- Medicine expiry tracking
- Automated reorder system

---

**Note**: This is a educational/demo project. For production use, additional security measures, testing, and optimizations should be implemented.