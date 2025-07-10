# E-Commerce Payment Website

A modern, feature-rich e-commerce application built with Flask and Paystack payment integration. Users can add products with images, manage their inventory, and process secure payments.

## Features

### 🛍️ Product Management
- **Add Products**: Upload product images, set prices, and add descriptions
- **Edit Products**: Update product details and images
- **Delete Products**: Remove products with confirmation
- **Image Upload**: Support for PNG, JPG, JPEG, GIF, and WEBP formats
- **Drag & Drop**: Modern drag-and-drop image upload interface

### 💳 Payment Processing
- **Paystack Integration**: Secure payment processing
- **Multiple Products**: Each product has its own payment flow
- **Email Collection**: Collect customer emails for payment processing
- **Success Confirmation**: Beautiful success page with confetti animation

### 🎨 Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Gradient Backgrounds**: Beautiful gradient color schemes
- **Smooth Animations**: Hover effects and transitions
- **Font Awesome Icons**: Professional iconography
- **Bootstrap 5**: Modern CSS framework

### 📊 Dashboard Features
- **Product Statistics**: Total products, total value, products with images
- **Product Grid**: Beautiful card-based product display
- **Search & Filter**: Easy product management
- **Flash Messages**: User-friendly notifications

## Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd payment_website
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env` (if available)
   - Or create a `.env` file with your configuration:
     ```env
     PAYSTACK_SECRET_KEY=your_secret_key_here
     PAYSTACK_PUBLIC_KEY=your_public_key_here
     FLASK_SECRET_KEY=your-super-secret-key
     CALLBACK_URL=http://127.0.0.1:5000/payment-success
     ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:5000`

## Deployment to Render

### Method 1: Using Render Dashboard

1. **Create a Render account**
   - Go to [render.com](https://render.com) and sign up

2. **Connect your repository**
   - Click "New +" and select "Web Service"
   - Connect your GitHub/GitLab repository

3. **Configure the service**
   - **Name**: `payment-website` (or your preferred name)
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Set environment variables**
   In the Render dashboard, go to Environment and add:
   ```
   FLASK_SECRET_KEY=your-super-secret-key-here
   FLASK_ENV=production
   PAYSTACK_SECRET_KEY=your_paystack_secret_key
   PAYSTACK_PUBLIC_KEY=your_paystack_public_key
   CALLBACK_URL=https://your-app-name.onrender.com/payment-success
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application

### Method 2: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" and select "Blueprint"
   - Connect your repository
   - Render will automatically detect the `render.yaml` file
   - Set your environment variables in the dashboard
   - Deploy

### Environment Variables for Production

Set these in your Render dashboard:

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Secret key for Flask sessions | `your-super-secret-key-here` |
| `FLASK_ENV` | Flask environment | `production` |
| `PAYSTACK_SECRET_KEY` | Your Paystack secret key | `sk_live_...` |
| `PAYSTACK_PUBLIC_KEY` | Your Paystack public key | `pk_live_...` |
| `CALLBACK_URL` | Payment success callback | `https://your-app.onrender.com/payment-success` |

### Important Notes for Production

1. **Update Paystack Keys**: Use live keys instead of test keys
2. **Update Callback URL**: Use your actual Render domain
3. **Database**: SQLite is fine for small applications, consider PostgreSQL for larger scale
4. **File Storage**: Consider using cloud storage (AWS S3, Cloudinary) for production

## Usage

### Adding Products
1. Navigate to "Add Product" from the navigation menu
2. Fill in the product details:
   - Product name
   - Description
   - Price (in South African Rand)
3. Upload an image by clicking the upload area or dragging and dropping
4. Click "Add Product" to save

### Managing Products
1. Go to "Manage Products" to view all products
2. Use the statistics cards to see overview information
3. Click "Edit" to modify product details
4. Click "Delete" to remove products (with confirmation)

### Processing Payments
1. On the homepage, browse available products
2. Click "Buy Now" on any product
3. Enter your email address
4. Complete payment through Paystack
5. Receive confirmation on the success page

## File Structure

```
payment_website/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── Procfile              # Web server configuration
├── .env                  # Environment variables (local)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── products.db           # SQLite database (auto-created)
├── static/
│   └── uploads/          # Product image uploads
└── templates/
    ├── index.html         # Homepage with product grid
    ├── add_product.html   # Add product form
    ├── edit_product.html  # Edit product form
    ├── manage_products.html # Product management dashboard
    └── success.html       # Payment success page
```

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

### Environment Variables
- `PAYSTACK_SECRET_KEY`: Your Paystack secret key
- `PAYSTACK_PUBLIC_KEY`: Your Paystack public key
- `FLASK_SECRET_KEY`: Secret key for Flask sessions
- `FLASK_ENV`: Flask environment (development/production)
- `CALLBACK_URL`: Payment success callback URL

### File Upload Settings
- **Allowed Extensions**: PNG, JPG, JPEG, GIF, WEBP
- **Upload Folder**: `static/uploads/`
- **File Naming**: Timestamped to prevent conflicts

## Security Features

- **File Upload Validation**: Only image files are allowed
- **Secure Filenames**: Uses `secure_filename()` to prevent path traversal
- **SQL Injection Protection**: Uses parameterized queries
- **CSRF Protection**: Flask's built-in CSRF protection
- **Environment Variables**: Sensitive data stored in environment variables

## Customization

### Styling
The application uses CSS custom properties for easy theming:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --danger-color: #ef4444;
}
```

### Adding New Features
1. Add new routes in `app.py`
2. Create corresponding templates in `templates/`
3. Update navigation as needed
4. Test thoroughly before deployment

## Troubleshooting

### Common Issues

1. **Images not displaying**
   - Check that the `static/uploads/` folder exists
   - Verify file permissions
   - Ensure image files are valid

2. **Payment not working**
   - Verify Paystack keys are correct
   - Check that callback URL is accessible
   - Ensure email format is valid

3. **Database errors**
   - Delete `products.db` to reset the database
   - Restart the application

4. **Deployment issues**
   - Check environment variables are set correctly
   - Verify build and start commands
   - Check logs in Render dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please open an issue on the repository. 