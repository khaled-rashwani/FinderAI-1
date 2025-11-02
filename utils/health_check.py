import logging
from datetime import datetime
from aiohttp import web
import asyncio

logger = logging.getLogger(__name__)

health_status = {
    'status': 'healthy',
    'last_check': None,
    'uptime_start': datetime.now(),
    'checks': {
        'bot': False,
    }
}


def update_component_status(component: str, is_healthy: bool):
    """
    Update the health status of a component.
    
    Args:
        component: Component name ('bot', 'openai', 'database')
        is_healthy: Boolean indicating if component is healthy
    """
    if component in health_status['checks']:
        health_status['checks'][component] = is_healthy
        logger.debug(f"Health status updated for {component}: {is_healthy}")


def _calculate_uptime():
    """Calculate uptime in seconds."""
    uptime_delta = datetime.now() - health_status['uptime_start']
    return int(uptime_delta.total_seconds())


async def health_check_handler(request):
    """
    HTTP handler for health check endpoint.
    
    Returns:
        JSON response with health status
    """
    health_status['last_check'] = datetime.now().isoformat()
    
    all_healthy = all(health_status['checks'].values())
    health_status['status'] = 'healthy' if all_healthy else 'degraded'
    
    response_data = {
        'status': health_status['status'],
        'timestamp': health_status['last_check'],
        'uptime_seconds': _calculate_uptime(),
        'components': health_status['checks']
    }
    
    status_code = 200 if all_healthy else 503
    
    logger.info(f"Health check performed: {health_status['status']}")
    return web.json_response(response_data, status=status_code)


async def start_health_check_server(port: int = 8080):
    app = web.Application()
    app.router.add_get('/health', health_check_handler)
    app.router.add_get('/', health_check_handler)  
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    try:
        await site.start()
        logger.info(f"Health check server started on port {port}")
        logger.info(f"Access health endpoint at: http://0.0.0.0:{port}/health")
    except Exception as e:
        logger.error(f"Failed to start health check server: {e}", exc_info=True)


def initialize_health_status():

    health_status['checks']['bot'] = True
    
    logger.info(f"Health status initialized: {health_status['checks']}")