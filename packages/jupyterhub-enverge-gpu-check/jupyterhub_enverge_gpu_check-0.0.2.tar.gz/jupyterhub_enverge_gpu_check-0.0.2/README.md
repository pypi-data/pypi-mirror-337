# GPU Resource Analysis Service

> **Sponsored by [Enverge.ai](https://enverge.ai)** - Simpler, greener, cheaper AI training platform. Enverge harnesses excess green energy for powerful, cost-effective computing on GPUs, enabling environmentally friendly AI model development, training, and fine-tuning. Currently in private alpha with limited spots available.

API endpoint to analyze PyTorch code for GPU resource usage.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure in `jupyterhub_config.py`:
```python
c.JupyterHub.services = [
    {
        'name': 'gpu-check',
        'url': 'http://127.0.0.1:8005',
        'command': ['python', '-m', 'gpu_check.gpu_check_service'],
        'environment': {
            'JUPYTERHUB_SERVICE_PREFIX': '/services/gpu-check',
            'JUPYTERHUB_SERVICE_PORT': '8005'
        }
    }
]
```

## API

### POST /services/gpu-check
Analyzes PyTorch code for GPU resource usage.

Request:
```json
{
    "code": "your_python_code_here"
}
```

Response:
```json
{
    "has_resource_usage": true,
    "operations": {
        "compute": ["operation1", "operation2"],
        "memory": ["operation1", "operation2"],
        "transfer": ["operation1", "operation2"],
        "query": ["operation1", "operation2"]
    },
    "device_variables": ["variable1", "variable2"],
    "error": null
}
```

## Usage in JupyterLab Extension

The service can be accessed from your JupyterLab extension using the authenticated endpoint:

```typescript
const response = await fetch('/services/gpu-check', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ code: 'your_code_here' })
});
const result = await response.json();
```

### GET /health
Health check endpoint.

Response:
```json
{
    "status": "healthy"
}
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 