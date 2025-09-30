"""
Local development entrypoint.

Run:
    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

Note:
    This file is optional; prefer invoking uvicorn directly.
"""
import uvicorn


# PUBLIC_INTERFACE
def main():
    """Run the FastAPI app with uvicorn reloader."""
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
