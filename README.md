# KRM Registration Form with Google Sheets Integration

Complete registration form system that captures form data and sends it directly to Google Sheets.

## 🎯 What's Included

| File | Purpose |
|------|---------|
| **server.js** | Express backend that handles form submissions and integrates with Google Sheets API |
| **registration.js** | Frontend JavaScript for form submission handling |
| **package.json** | Node.js dependencies |
| **.env** | Configuration file with spreadsheet ID |
| **index.html** | Updated with registration function call |

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Start the Server
```bash
npm start
```

### Step 3: Test the Form
Open `index.html` in your browser and fill out the registration form. Data will be sent to Google Sheets automatically.

---

## 📝 Form Fields Captured

Your registration form collects these fields:

| Column | Field | Source |
|--------|-------|--------|
| A | Timestamp | Auto-generated (IST) |
| B | Full Name | `modal-name` input |
| C | Phone Number | `modal-phone` input |
| D | Seminar City | `modal-select-city` dropdown |
| E | User City | `modal-user-city` dropdown |

## 📊 Google Sheets Integration

**Spreadsheet:**
- ID: `1m7RqWcsz0iGzVZFajUgvcOg1Fgjr-zmZ7VwQiKT-cK8`
- Sheet: `Sheet1` (Columns A-E)
- Access: [Open in Google Drive](https://docs.google.com/spreadsheets/d/1m7RqWcsz0iGzVZFajUgvcOg1Fgjr-zmZ7VwQiKT-cK8/edit?usp=sharing)

**Service Account:**
- Email: `register-form@gen-lang-client-0274305714.iam.gserviceaccount.com`
- Role: **Editor** (required)

> ⚠️ Important: This email must have **Editor** access to your Google Sheet

## 🔧 How It Works

### Frontend Flow
```
Form Submission
    ↓
Validate Fields
    ↓
Show Loading State
    ↓
POST to http://localhost:5000/api/register
    ↓
Success → Clear Form & Close Modal
Error → Show Error Message
```

### Backend Flow
```
Receive POST Request
    ↓
Validate Required Fields
    ↓
Generate Timestamp (IST)
    ↓
Authenticate with Google
    ↓
Append to Google Sheet
    ↓
Return Response
```

## 🔌 API Endpoint

### POST `/api/register`

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "9876543210",
  "seminarCity": "Bangalore — 15 Jun",
  "userCity": "Mumbai"
}
```

**Success Response (HTTP 200):**
```json
{
  "success": true,
  "message": "Registration submitted successfully!",
  "data": { /* Google Sheets API response */ }
}
```

**Error Response (HTTP 400/500):**
```json
{
  "success": false,
  "error": "Error message here",
  "details": "Additional error details"
}
```

## 🐛 Troubleshooting

### Problem: "Network error. Please check if the server is running"

**Solution:** Make sure the server is running
```bash
npm start
```

Test the connection:
```bash
curl http://localhost:5000/api/health
```

Expected: `{"status":"Server is running"}`

---

### Problem: No data appears in Google Sheet

**Check these:**
1. ✅ Service account has **Editor** access to the sheet
2. ✅ Correct spreadsheet ID in `.env`
3. ✅ Server is running (`npm start`)

**To fix:** 
- Open Google Sheet → Share
- Add: `register-form@gen-lang-client-0274305714.iam.gserviceaccount.com`
- Select: **Editor** role
- Share

---

### Problem: Form not submitting

**Check browser console (F12 → Console tab) for errors**

Common issues:
- Port 5000 already in use
- Missing dependencies (`npm install`)
- Server not running

---

### Problem: Port 5000 is already in use

**Find and stop the process:**

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

Or change the port in `.env`:
```
PORT=3000
```

## 📁 File Structure

```
d:\Zippy\FORCE\
│
├── index.html              (Registration form - updated)
├── registration.js         (Frontend handler)
├── server.js              (Backend API)
├── package.json           (Dependencies)
├── .env                   (Configuration)
├── README.md              (This file)
│
└── assets/                (Images, logos)
    ├── Krm.svg
    ├── Hereup.png
    ├── Andijan.avif
    └── dai num.avif
```

## ⚙️ Environment Setup

**.env file:**
```env
PORT=5000
SPREADSHEET_ID=1m7RqWcsz0iGzVZFajUgvcOg1Fgjr-zmZ7VwQiKT-cK8
```

## 🛠️ Development

### Watch for Changes with Auto-Reload

```bash
npm run dev
```

Uses **nodemon** to automatically restart server on file changes.

### Install Dependencies for Development

```bash
npm install
```

All dependencies (including dev dependencies like nodemon) will be installed.

## 🚨 Security Notes

⚠️ **Important for Production:**

- Service account credentials are embedded in `server.js` (demo only)
- For production, use `.env` or environment variables
- Never commit credentials to Git
- Add rate limiting and input validation
- Use HTTPS in production
- Consider using Google Cloud Secret Manager

## 📊 Data Export

To export data from Google Sheets:
1. Open [Google Sheet](https://docs.google.com/spreadsheets/d/1m7RqWcsz0iGzVZFajUgvcOg1Fgjr-zmZ7VwQiKT-cK8/edit?usp=sharing)
2. File → Download → Choose format (CSV, Excel, PDF)

## 🚀 Deployment

Ready to deploy? Choose your platform:

- **Heroku**: `npm install && npm start`
- **Vercel**: Not suitable (requires serverless functions for backend)
- **AWS Lambda**: Use `serverless` framework
- **Google Cloud**: Cloud Run or App Engine
- **DigitalOcean**: App Platform

For deployment, remember to:
1. Set environment variables
2. Ensure Google Sheet permissions are correct
3. Update API endpoint in `registration.js` to match your deployed URL

## 📞 Support

For issues:
1. Check the **Troubleshooting** section above
2. Review server logs from `npm start` output
3. Check browser console (F12 → Console)
4. Verify Google Sheet service account permissions

## ✅ Checklist

- [ ] Run `npm install`
- [ ] Start server with `npm start`
- [ ] Test form submission
- [ ] Verify data in Google Sheet
- [ ] Update API endpoint for production
- [ ] Set up CORS for production domain
- [ ] Add environment variables to deployment

---

**Last Updated:** June 2026
**Version:** 1.0.0