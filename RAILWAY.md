# Deploying Nag Queen to Railway

This guide walks through deploying the full Nag Queen stack to Railway.

## Architecture

You'll create 3 Railway services:
1. **PostgreSQL** - Database
2. **Backend** - FastAPI Python service
3. **Frontend** - Vue static site

## Step 1: Create a New Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Empty Project"

## Step 2: Add PostgreSQL Database

1. In your project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will provision a PostgreSQL instance
4. Note: The `DATABASE_URL` will be automatically available to linked services

## Step 3: Deploy the Backend

1. Click "+ New" → "GitHub Repo"
2. Select the `nagqueen` repository
3. Railway will detect it - configure as follows:

**Settings:**
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: (auto-detected from Procfile)

**Environment Variables (in Railway dashboard):**
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
JWT_SECRET=<generate-a-secure-random-string>
TWILIO_ACCOUNT_SID=<your-twilio-sid>
TWILIO_AUTH_TOKEN=<your-twilio-token>
TWILIO_PHONE_NUMBER=<your-twilio-number>
CORS_ORIGINS=https://<your-frontend-url>.railway.app
```

4. Click "Deploy"
5. Once deployed, go to Settings → Networking → Generate Domain
6. Note your backend URL (e.g., `https://nagqueen-backend-production.up.railway.app`)

## Step 4: Deploy the Frontend

1. Click "+ New" → "GitHub Repo"
2. Select the same `nagqueen` repository again
3. Configure:

**Settings:**
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Start Command: `npm run start`

**Environment Variables:**
```
VITE_API_URL=https://<your-backend-url>.railway.app
```

4. Click "Deploy"
5. Generate a domain for the frontend

## Step 5: Update Backend CORS

After you have the frontend URL, update the backend's `CORS_ORIGINS`:

```
CORS_ORIGINS=https://your-frontend.railway.app
```

Redeploy the backend for changes to take effect.

## Step 6: Create Initial Admin User

1. Open your frontend URL
2. Sign up with your phone number
3. You'll receive an OTP via SMS
4. Connect to the database to manually approve and make yourself admin:

```sql
UPDATE users SET is_approved = true, is_admin = true WHERE phone_number = '+1234567890';
```

You can run this via Railway's database connection or use a tool like pgAdmin.

## Environment Variables Reference

### Backend

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes (auto from Railway) |
| `JWT_SECRET` | Secret key for JWT tokens | Yes |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | Yes |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | Yes |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone number | Yes |
| `CORS_ORIGINS` | Comma-separated allowed origins | Yes |
| `PORT` | Server port | Auto-set by Railway |

### Frontend

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | Yes |
| `PORT` | Server port | Auto-set by Railway |

## Troubleshooting

### Database connection issues
- Ensure `DATABASE_URL` is using the Railway variable reference: `${{Postgres.DATABASE_URL}}`

### CORS errors
- Make sure `CORS_ORIGINS` in the backend includes your frontend URL exactly (with https://)
- Redeploy backend after changing CORS settings

### SMS not sending
- Verify Twilio credentials are correct
- Check Twilio dashboard for error logs
- Ensure your Twilio number is SMS-capable

### Frontend not loading API
- Verify `VITE_API_URL` points to the correct backend URL
- Rebuild frontend after changing environment variables (Railway does this automatically on redeploy)
