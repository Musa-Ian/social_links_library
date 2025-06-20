# Getting Started with Social Links Library

This guide will help you set up and run the Social Links Library API on your local machine.

## 1. Prerequisites
- Python 3.8 or newer
- pip (Python package manager)

## 2. Install Dependencies
Navigate to the `api` directory and install the required packages:

```bash
cd api
pip install -r requirements.txt
```

## 3. Run the API Server
Start the FastAPI server using Uvicorn:

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 4. Example API Requests
- List all platforms:
  - `GET http://127.0.0.1:8000/platforms`
- Get details for a platform:
  - `GET http://127.0.0.1:8000/platforms/twitter`
- Validate a username:
  - `GET http://127.0.0.1:8000/platforms/twitter/validate/jack`
- Generate a profile link:
  - `GET http://127.0.0.1:8000/platforms/twitter/link/jack`

## 5. Contributing
See the [CONTRIBUTING.md](../.github/CONTRIBUTING.md) guide for how to add or update social link patterns.

---

If you have any questions, open an issue or join the community discussions! 