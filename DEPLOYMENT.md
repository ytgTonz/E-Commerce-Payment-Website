# Quick Deployment Guide for Render

## Prerequisites
- GitHub account with your code pushed
- Render account (free tier available)

## Step-by-Step Deployment

### 1. Prepare Your Repository
Make sure your repository contains:
- ✅ `app.py` (Flask application)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `render.yaml` (Render configuration)
- ✅ `.gitignore` (excludes sensitive files)
- ✅ `Procfile` (web server configuration)

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Set environment variables (see below)
6. Click "Apply" to deploy

#### Option B: Manual Configuration
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `payment-website`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Set environment variables (see below)
6. Click "Create Web Service"

### 3. Environment Variables
In your Render dashboard, go to Environment and add:

| Variable | Value | Notes |
|----------|-------|-------|
| `FLASK_SECRET_KEY` | `your-super-secret-key-here` | Generate a strong random key |
| `FLASK_ENV` | `production` | |
| `PAYSTACK_SECRET_KEY` | `sk_live_...` | Your live Paystack secret key |
| `PAYSTACK_PUBLIC_KEY` | `pk_live_...` | Your live Paystack public key |
| `CALLBACK_URL` | `https://your-app-name.onrender.com/payment-success` | Replace with your actual domain |

### 4. Update Paystack Configuration
1. Get your live Paystack keys from your Paystack dashboard
2. Update the environment variables in Render
3. Update the callback URL to your actual Render domain

### 5. Test Your Deployment
1. Visit your Render URL (e.g., `https://payment-website.onrender.com`)
2. Add a test product
3. Test the payment flow
4. Check that images upload correctly

## Troubleshooting

### Common Issues

**Build Fails**
- Check that `requirements.txt` is in the root directory
- Verify all dependencies are listed

**App Won't Start**
- Check the start command: `python app.py`
- Verify environment variables are set
- Check logs in Render dashboard

**Payments Not Working**
- Verify Paystack keys are correct
- Check callback URL matches your domain
- Ensure you're using live keys (not test keys)

**Images Not Uploading**
- Check file permissions
- Verify upload folder exists
- Check file size limits

### Getting Help
- Check Render logs in the dashboard
- Verify environment variables are set correctly
- Test locally first with the same configuration

## Security Notes
- Never commit `.env` files to Git
- Use strong, unique secret keys
- Use live Paystack keys for production
- Consider using cloud storage for images in production 