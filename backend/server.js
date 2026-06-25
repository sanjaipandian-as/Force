const express = require('express');
const cors = require('cors');
const { google } = require('googleapis');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Service Account Credentials
const credentials = {
  type: "service_account",
  project_id: "gen-lang-client-0274305714",
  private_key_id: "b99974bfe18193cb2a9924b7c34aa73596669c07",
  private_key: "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDvddVy9Ih6Cs+4\nS/ew65QgWgXUhpvm67afil2zIbn3AB0f8+cPSmL7aRYWa7bfVGgYVVsQcu8zrm8N\n/MRQpcmKzU1SF/N6c26HU2sPf+H0KMbBlhPl/waPTAWahRz8sA537vofhRfZB8yJ\nCR1N9TLbbuS7sYubUf491HIZKDjxMAJ74gvgfGRJbXC6rLPEY28RqHIK6Q7TguPB\nP94HlT6b71rB2TBAUhUWdZdpM73ZxDynci0M7JrwGtpOI7Kff0kkmLQeToHwLmiR\nXByM3R0OMzRB0JPAcnx7uqPQsRQsOPZS8qKBbc0WFDKXmKsg9PQJ634r3psAdeRc\ncU/4SVfTAgMBAAECggEAMWXV+AZg5wg27JZjTNB0OK5JeJuiKqNig4voI21oLv+L\ngo1uk3VtcN6vS0XCLlT7ulVVWVHUbY1k5HZJyzdAGc2bTz2YoSCR4wG+2q4vXw5Q\nXhwHE9GluUbd+w/NuITbHzuhxoHOtxtIQtaqAGx+Js08C0oneg2SjI+4T98/y+UM\n3f//tuIYSOPiAtbhHsN/AvwUJafHIU/79u0lRP6vFghUmrYEhVoQPWqNKBzIS96E\nAELfNbxs0psyeO+T3QCeeJj2jyF+6TXyrhmT4MCUgPxq70UXZOQpSw/QKhsi7r7t\nQtqm7tT72pisF8yUvgk85Bu7k02OAXX2dsAH6pvUBQKBgQD59O7w/M56ByklsXeA\nxSZwqkjHRwcENJbSD/2KL5sdmf0HqN3rhgff8dQSpg5UebdTwjnFL4cZBoTXCfzS\noGnng+HLbVvTr10OH7TVO1HGN50KHfcyJcRaQe+tLAGDiMkaYce6PKVs5O80pkfn\njdMFnzT19jiDBoCs5XBh5Od5BwKBgQD1P+8kuBy0Q6VZdfArklGDxvMRnnVJ8wDp\ndyTD678pcuO92Kep0WPE2Ihce68t7ImL4OCEQblrZbyoqpBtBv+6nv4amB9SEhs2\ntihYGUS5NR1Y8gAq8mhoxo7izOFiRHCM17qwfoACgart7uEDwTjh9crw8RcHfh6c\ngFHu8bDz1QKBgDE3MPTyUhVk440wbD9GklMMtFfIfHEviaLC00EqLnidoVyou0ls\nkpBdpUwmthub+6TaUVWqDge3aOCObuFqBHA5X3QWjEYZ+VCWnZx+mZNVz+32CH4v\nQYIkCXUnfQTRIge3yQO6fTf7u726H95P5oTs3Bix6l6iISPp6T7dO1ZxAoGBAJN4\njmSWESyUQKk6seCBa2LCDwdZMU32QWYhronhCGH0I93UmX0T29pSGi0CcqQ6x7rE\nzjy5CLX7xyXk6lOlEcE2ObXkI3FGUfbkMf5Hs3tq5OrHGjK48O+P9fuLFzvvy33l\neu0GJBNdxVqtecC4P2wgUJfxYNewjteskZgM3UrBAoGAICcS3eaIMaMmdpKNIHey\nqhd8ZWIKXLG2Za/moh09Z1dV2jEkHmaGG0my8SW31i1tvpswfo80dIK13eTqbXaW\nC/cacjOJjIb53qyzxMln5B1KhTryRn9r89s8W/OJvQvEZVLcxNTNK/m4nzrDU30m\nnVOeT5TReJDlWridcjbkEIE=\n-----END PRIVATE KEY-----\n",
  client_email: "register-form@gen-lang-client-0274305714.iam.gserviceaccount.com",
  client_id: "114541550229383372670",
  auth_uri: "https://accounts.google.com/o/oauth2/auth",
  token_uri: "https://oauth2.googleapis.com/token",
  auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
  client_x509_cert_url: "https://www.googleapis.com/robot/v1/metadata/x509/register-form%40gen-lang-client-0274305714.iam.gserviceaccount.com",
  universe_domain: "googleapis.com"
};

// Google Sheet ID (from your URL)
const SPREADSHEET_ID = "1m7RqWcsz0iGzVZFajUgvcOg1Fgjr-zmZ7VwQiKT-cK8";

// Initialize Google Sheets API
const sheets = google.sheets({
  version: 'v4',
  auth: new google.auth.GoogleAuth({
    credentials: credentials,
    scopes: ['https://www.googleapis.com/auth/spreadsheets']
  })
});

// API endpoint to handle form submission
app.post('/api/register', async (req, res) => {
  try {
    const { name, phone, seminarCity, userCity } = req.body;

    // Validate required fields
    if (!name || !phone || !seminarCity || !userCity) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    // Get current timestamp
    const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });

    // Append data to Google Sheet
    const response = await sheets.spreadsheets.values.append({
      spreadsheetId: SPREADSHEET_ID,
      range: 'Sheet1!A:E', // Adjust range if needed
      valueInputOption: 'RAW',
      resource: {
        values: [[timestamp, name, phone, seminarCity, userCity]]
      }
    });

    console.log('Data appended successfully:', response.data);
    res.json({ 
      success: true, 
      message: 'Registration submitted successfully!',
      data: response.data 
    });

  } catch (error) {
    console.error('Error appending to sheet:', error);
    console.error('Full error object:', JSON.stringify(error, null, 2));
    res.status(500).json({ 
      success: false, 
      error: 'Failed to submit registration',
      details: error.message,
      errorCode: error.code
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'Server is running' });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
