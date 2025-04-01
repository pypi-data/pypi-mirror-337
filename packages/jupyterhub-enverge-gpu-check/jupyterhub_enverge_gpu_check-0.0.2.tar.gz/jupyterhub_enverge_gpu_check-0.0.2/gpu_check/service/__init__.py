import json
import logging
import os
from tornado import web, ioloop
from jupyterhub.services.auth import HubAuthenticated

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/srv/gpu_check_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from .. import analyze_resource_usage

class GPUCheckHandler(HubAuthenticated, web.RequestHandler):
    async def get(self):
        self.finish(json.dumps({
            "status": "healthy",
            "service": "gpu_check",
            "version": "1.0.0"
        }))

    async def post(self):
        try:
            data = json.loads(self.request.body)
            code = data.get('code')
            
            if not code:
                self.set_status(400)
                self.finish(json.dumps({
                    "error": "Missing code parameter",
                    "has_resource_usage": False
                }))
                return
                
            result = analyze_resource_usage(code)
            # Convert enum values to strings for JSON serialization
            if 'operations' in result:
                result['operations'] = {k.value: v for k, v in result['operations'].items()}
            self.finish(json.dumps(result))
            
        except Exception as e:
            logger.error(f"Error analyzing code: {str(e)}", exc_info=True)
            self.set_status(500)
            self.finish(json.dumps({
                "error": str(e),
                "has_resource_usage": False
            }))

def main():
    prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')
    if not prefix.endswith('/'):
        prefix = prefix + '/'
    
    logger.info(f"Starting GPU check service with prefix: {prefix}")
    
    app = web.Application([
        (f"{prefix}", GPUCheckHandler),
    ], cookie_secret=os.environ.get('JUPYTERHUB_API_TOKEN', 'secret'))
    
    port = int(os.environ.get('JUPYTERHUB_SERVICE_PORT', 8005))
    logger.info(f"Listening on port: {port}")
    app.listen(port)
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main() 
