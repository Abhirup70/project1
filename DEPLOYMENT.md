# Deployment Guide

## Quick Start (Local Development)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python main.py

# 3. Visit http://localhost:8000
```

## Docker Deployment

### Build Image
```bash
docker build -t currency-converter:latest .
```

### Run Container
```bash
docker run -p 8000:8000 currency-converter:latest
```

### Using Docker Compose
Create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## Cloud Deployment

### Heroku
```bash
# Install Heroku CLI first
heroku create your-app-name
git push heroku main
```

### AWS (Elastic Beanstalk)
```bash
eb init
eb create
eb deploy
```

### DigitalOcean App Platform
1. Connect your GitHub repository
2. Select `Dockerfile` as the build source
3. Deploy

### Railway
1. Push to GitHub
2. Connect repository to Railway
3. Auto-deploys on push

### Render
1. Connect GitHub account
2. Create new Web Service
3. Select repository and branch
4. Auto-deploys

## Production Considerations

### 1. Use Gunicorn for Production
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### 2. Add Environment Variables
Create `.env`:
```
EXCHANGE_API_KEY=your_api_key_here
PORT=8000
```

### 3. Add SSL/HTTPS
Use a reverse proxy like Nginx:
```nginx
server {
    listen 443 ssl;
    server_name api.yoursite.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### 4. Rate Limiting (Optional)
Install `slowapi`:
```bash
pip install slowapi
```

### 5. Monitoring
- Use APM tools like DataDog, New Relic, or Elastic
- Set up error tracking with Sentry
- Monitor API logs and performance

### 6. Database for Caching (Optional)
For production, replace in-memory cache with Redis:
```bash
pip install redis
```

Then update `main.py` to use Redis instead of the `exchange_cache` dict.

## API Key Setup (Recommended)

Get a free API key from https://exchangerate-api.com/

Update `main.py`:
```python
API_KEY = os.getenv("EXCHANGE_API_KEY", "")
url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}?apikey={API_KEY}"
```

## SSL Certificate

For HTTPS, use Let's Encrypt:
```bash
certbot certonly --standalone -d api.yoursite.com
```

## Load Testing

Test with Apache Bench:
```bash
ab -n 1000 -c 100 http://localhost:8000/health
```

Or using `wrk`:
```bash
wrk -t4 -c100 -d30s http://localhost:8000/health
```

## Monitoring Uptime

Use free services like:
- Uptime Robot
- Pingdom
- Healthchecks.io

## Scale to Multiple Instances

Behind a load balancer (Nginx, HAProxy, etc.):
```
Load Balancer
    ├─ Instance 1 (port 8001)
    ├─ Instance 2 (port 8002)
    └─ Instance 3 (port 8003)
```

## Cost Estimates (per month)

- **Free Tier**: ~$0 (Heroku free tier, Railway free tier)
- **Hobby**: ~$5-20 (DigitalOcean, Render)
- **Production**: $20-100+ depending on traffic
- **Enterprise**: $100+

## Next Steps

1. Add authentication (API keys)
2. Add rate limiting
3. Add database for logging conversions
4. Create admin dashboard
5. Add webhook support
6. Add batch conversion endpoint
7. Create mobile app
8. Add currency data caching strategy
