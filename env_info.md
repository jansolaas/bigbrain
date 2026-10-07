

#### 1. **Backend Host (`BACKEND_HOST`)**
The **backend host** is the IP address or hostname on which the FastAPI application will run and listen for incoming requests. It determines **where the application will be accessible**.
- **Default Value**: FastAPI defaults the host to `127.0.0.1` (localhost), which ensures the application is accessible **only from the same machine** where it is running.
- **Common Use Cases**:
    - **Local Development**: Keep `BACKEND_HOST=127.0.0.1` to restrict access to your local machine.
    - **Production**:
        - Use `BACKEND_HOST=0.0.0.0` to allow the application to listen on **all network interfaces**, making it accessible externally (e.g., via a public IP or domain).
        - Attach a proxy/load balancer (e.g., Nginx or AWS ALB) and limit external access.





- Instead of relying on `.env` for setting the `PYTHONPATH`, you can set this explicitly in your `pytest.ini` for tests. This keeps test configuration separate from runtime logic.
Example `pytest.ini`:
``` ini
  [pytest]
  testpaths = tests/
  pythonpaths = backend/
```
### Examples in Context
#### Backend Host Example
1. **Local Development**:
``` 
   BACKEND_HOST=127.0.0.1
   BACKEND_PORT=8000
```
Uvicorn will start and respond only to requests made from the same machine:
``` 
   uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Access the API by visiting:
``` 
   http://127.0.0.1:8000
```
1. **Production Deployment**:
``` 
   BACKEND_HOST=0.0.0.0
   BACKEND_PORT=9000
   UVICORN_WORKERS=5
```
Uvicorn will listen on all network interfaces:
``` 
   uvicorn app.main:app --host 0.0.0.0 --port 9000 --workers 5
```
This makes the app accessible externally. For example:
- Public IP: `http://<your-public-IP-or-domain>:9000`
- For security, put this behind an HTTPS proxy like Nginx or a cloud-based load balancer.

#### Workers Example
- **Single Worker (Default)**:
``` bash
  uvicorn app.main:app --host 127.0.0.1 --port 8000
```
- Only one worker process serves all requests.
- Good for light workloads or dev environments.

- **Multiple Workers**:
``` bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
- With 4 workers, the application can serve more requests concurrently across different CPU cores.
- Useful for scaling in production environments.
