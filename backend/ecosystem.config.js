module.exports = {
  apps: [{
    name: "cryptomock-backend",
    script: "gunicorn",
    args: "wsgi:app --bind 0.0.0.0:8000 --workers 3 --log-file=logs/gunicorn.log --log-level=debug --timeout 120",
    interpreter: "./venv/bin/python",
    env: {
      NODE_ENV: "production"
    }
  }]
}
