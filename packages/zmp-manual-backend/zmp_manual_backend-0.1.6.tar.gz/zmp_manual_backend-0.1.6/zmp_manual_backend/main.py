import logging
import os
import asyncio
from contextlib import asynccontextmanager
from logging.config import fileConfig
from pathlib import Path
from typing import Dict
import secrets
import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import subprocess

from zmp_manual_backend.api.auth_router import router as auth_router
from zmp_manual_backend.api.manual_router import router as manual_router

from starlette.middleware.sessions import SessionMiddleware
from starlette_csrf import CSRFMiddleware

# Try to import KeyCloak configuration
try:
    from zmp_manual_backend.api.oauth2_keycloak import (
        KEYCLOAK_SERVER_URL,
        KEYCLOAK_REALM,
        KEYCLOAK_CLIENT_ID,
        KEYCLOAK_AUTH_ENDPOINT,
        KEYCLOAK_TOKEN_ENDPOINT,
        KEYCLOAK_USER_ENDPOINT,
    )
except ImportError:
    # Set default values if import fails
    KEYCLOAK_SERVER_URL = os.environ.get(
        "KEYCLOAK_SERVER_URL", "https://keycloak.ags.cloudzcp.net/auth"
    )
    KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM", "ags")
    KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID", "zmp-client")
    # Construct endpoints directly
    KEYCLOAK_AUTH_ENDPOINT = (
        f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
    )
    KEYCLOAK_TOKEN_ENDPOINT = (
        f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    )
    KEYCLOAK_USER_ENDPOINT = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo"

# Load environment variables from the project root directory
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# Parse VSCODE_ENV_REPLACE for environment variables
vscode_env = os.environ.get("VSCODE_ENV_REPLACE", "")
if vscode_env:
    # Split by : and parse each key=value pair
    env_pairs = vscode_env.split(":")
    for pair in env_pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            # Only set if the value is not empty
            if value:
                os.environ[key] = value.replace("\\x3a", ":")  # Fix escaped colons

# Load .env file as fallback
load_dotenv(dotenv_path=env_path)

# Configure logging with absolute path
logging_conf_path = os.path.join(os.path.dirname(__file__), "..", "logging.conf")
if os.path.exists(logging_conf_path):
    fileConfig(logging_conf_path, disable_existing_loggers=False)

    # Update log levels based on LOG_LEVEL environment variable
    log_level_str = os.environ.get("LOG_LEVEL", "info").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Set log level for all configured loggers
    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).setLevel(log_level)

    # Also set root logger level
    logging.root.setLevel(log_level)

    logger = logging.getLogger("appLogger")
    logger.info(f"Set logging level to {log_level_str} for all loggers")
else:
    logging.basicConfig(level=logging.INFO)
    logging.warning(
        f"Logging config not found at {logging_conf_path}, using basic configuration"
    )

logger = logging.getLogger("appLogger")


def get_env_settings() -> Dict[str, str]:
    """Get environment settings with validation"""
    settings = {
        "HOST": os.environ.get("HOST", "0.0.0.0"),
        "PORT": os.environ.get("PORT", "8000"),
        "REPO_BASE_PATH": os.environ.get("REPO_BASE_PATH", "./repo"),
        "SOURCE_DIR": os.environ.get("SOURCE_DIR", "docs"),
        "TARGET_DIR": os.environ.get("TARGET_DIR", "i18n"),
        "DEBUG": os.environ.get("DEBUG", "True"),
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "info"),
        "ALLOWED_ORIGINS": os.environ.get("ALLOWED_ORIGINS", "*"),
        "APP_ROOT": os.environ.get("APP_ROOT", "/api/manual/v1"),
    }

    return settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Startup
        logger.info("Starting ZMP Manual Backend service")
        settings = get_env_settings()

        # Log configuration
        logger.info("Server configuration:")
        for key, value in settings.items():
            logger.info(f"- {key}: {value}")

        # Log environment variables status
        logger.info("Environment variables status:")
        logger.info(f"- .env file location: {env_path}")
        logger.info(f"- .env file exists: {env_path.exists()}")
        logger.info(
            f"- NOTION_TOKEN set: {'Yes' if os.environ.get('NOTION_TOKEN') else 'No'}"
        )

        # Log root page IDs for all solutions
        for solution in ["ZCP", "APIM", "AMDP"]:
            env_var = f"{solution}_ROOT_PAGE_ID"
            logger.info(
                f"- {env_var} set: {'Yes' if os.environ.get(env_var) else 'No'}"
            )

        # Initialize Keycloak with better error handling
        from zmp_manual_backend.api.oauth2_keycloak import PUBLIC_KEY

        if PUBLIC_KEY:
            logger.info("KeyCloak authentication initialized successfully")
        else:
            logger.warning(
                "KeyCloak authentication not properly initialized - "
                "authentication features may not work correctly"
            )
            # Don't abort startup, continue with degraded functionality

        # Log CORS configuration
        allowed_origins = settings["ALLOWED_ORIGINS"].split(",")
        logger.info(f"CORS configuration: allowing origins: {allowed_origins}")

        # Configure Git to use environment variables for authentication
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            logger.info("GitHub token found, configuring Git...")
            try:
                # Configure Git to use environment variables for auth
                subprocess.run(
                    ["git", "config", "--global", "credential.helper", ""], check=True
                )
                # Create a simple script that will echo the token as the password
                askpass_script = """#!/bin/sh
case "$1" in
  Username*) echo "oauth2" ;;
  Password*) echo "${GITHUB_TOKEN}" ;;
esac
"""
                # Save the script to a temporary file
                askpass_path = "/tmp/git-askpass.sh"
                with open(askpass_path, "w") as f:
                    f.write(askpass_script)
                os.chmod(askpass_path, 0o700)  # Make it executable

                # Set environment variables for Git
                os.environ["GIT_ASKPASS"] = askpass_path
                os.environ["GIT_TERMINAL_PROMPT"] = "0"

                logger.info("Git credential helper configured to use GitHub token")
            except Exception as e:
                logger.error(f"Failed to configure Git credentials: {str(e)}")
        else:
            logger.warning("GitHub token environment variable not found")

        # Log environment variables for debugging
        env_settings = get_env_settings()
        for key, value in env_settings.items():
            # Don't log sensitive values
            log_value = value
            if "TOKEN" in key or "SECRET" in key:
                log_value = value[:5] + "..." if value and len(value) > 5 else "[empty]"
            logger.info(f"- {key}: {log_value}")

        yield

        # After app setup, log all registered routes
        logger.info("Registered API routes:")
        for route in app.routes:
            logger.info(f"- {route.path} ({route.name})")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down ZMP Manual Backend service")

        # Clean up notification clients
        from zmp_manual_backend.api.manual_router import manual_service

        try:
            if manual_service:
                # Create a new event loop if needed
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    # Create a new event loop if the current one is closed or running
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                # Run the cleanup in the event loop
                try:
                    if loop.is_running():
                        # If loop is running, create a future and schedule it
                        future = asyncio.run_coroutine_threadsafe(
                            manual_service.unregister_all_clients(), loop
                        )
                        # Wait for a short time for the future to complete
                        try:
                            future.result(timeout=2.0)
                            logger.info(
                                "Successfully unregistered all notification clients"
                            )
                        except asyncio.TimeoutError:
                            logger.warning(
                                "Timeout while unregistering notification clients"
                            )
                        except Exception as e:
                            logger.error(
                                f"Error in notification client cleanup task: {str(e)}"
                            )
                    else:
                        # If loop is not running, run the coroutine directly
                        loop.run_until_complete(manual_service.unregister_all_clients())
                        logger.info(
                            "Successfully unregistered all notification clients"
                        )
                except Exception as e:
                    logger.error(f"Failed to run notification client cleanup: {str(e)}")
        except Exception as e:
            logger.error(f"Error cleaning up notification clients: {str(e)}")
            # Continue shutdown process despite errors


# Get environment settings
settings = get_env_settings()

# Create FastAPI application
app = FastAPI(
    title="ZMP Manual Backend",
    description="Backend service for ZMP manual management",
    version="0.1.0",
    docs_url=f"{settings['APP_ROOT']}/api-docs",
    openapi_url=f"{settings['APP_ROOT']}/openapi",
    redoc_url=f"{settings['APP_ROOT']}/api-redoc",
    default_response_class=JSONResponse,
    debug=True,
    root_path_in_servers=True,
    lifespan=lifespan,
)


# downgrading the openapi version to 3.0.0
def custom_openapi():
    # Always regenerate the schema to ensure we have the latest configuration
    app.openapi_schema = None

    # Get application root from settings for constructing URLs
    app_port = os.environ.get("PORT", "8001")
    app_url = f"http://localhost:{app_port}"

    # Define Keycloak endpoints
    auth_url = (
        f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
    )
    token_url = f"{KEYCLOAK_TOKEN_ENDPOINT}"
    userinfo_url = f"{KEYCLOAK_USER_ENDPOINT}"

    # Define redirect URL for Swagger UI - this needs to be the built-in Swagger UI redirect path
    swagger_redirect_url = f"{app_url}{settings['APP_ROOT']}/api-docs/oauth2-redirect"

    # Log the OAuth2 configuration
    logger.info("OAuth2 configuration for OpenAPI schema:")
    logger.info(f"- Authorization URL: {auth_url}")
    logger.info(f"- Token URL: {token_url}")
    logger.info(f"- Userinfo URL: {userinfo_url}")
    logger.info(f"- Client ID: {KEYCLOAK_CLIENT_ID}")
    logger.info(f"- Swagger Redirect URL: {swagger_redirect_url}")

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        openapi_version="3.0.0",
        servers=app.servers,
    )

    # Add security schemes
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Completely reset security schemes to avoid any default values
    openapi_schema["components"]["securitySchemes"] = {}

    # Add OAuth2 security scheme matching the sample application
    openapi_schema["components"]["securitySchemes"]["OAuth2AuthorizationCodeBearer"] = {
        "type": "oauth2",
        "flows": {
            "authorizationCode": {
                "refreshUrl": userinfo_url,
                "scopes": {},
                "authorizationUrl": auth_url,
                "tokenUrl": token_url,
            }
        },
    }

    # Add HTTP Basic security scheme like the sample
    openapi_schema["components"]["securitySchemes"]["HTTPBasic"] = {
        "type": "http",
        "scheme": "basic",
    }

    # Set the schema on the app
    app.openapi_schema = openapi_schema

    # Log that we've successfully set the OpenAPI schema
    logger.info("Successfully set custom OpenAPI schema with Keycloak security schemes")

    return app.openapi_schema


app.openapi = custom_openapi

logger.info(f"docs_url: {app.docs_url}")
logger.info(f"openapi_url: {app.openapi_url}")
logger.info(f"redoc_url: {app.redoc_url}")
logger.info(f"API routes will be mounted under: {settings['APP_ROOT']}")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Add basic health checks here
        repo_path = Path(settings["REPO_BASE_PATH"])
        if not repo_path.exists():
            raise HTTPException(
                status_code=503, detail="Repository directory not accessible"
            )

        return {
            "status": "healthy",
            "version": "0.1.0",
            "repository_path": str(repo_path.absolute()),
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))


# Create a prefixed API router
api_router = APIRouter(prefix=settings["APP_ROOT"])


# Add duplicated health check to the API router
@api_router.get("/health")
async def api_health_check():
    """Health check endpoint with prefix"""
    return await health_check()


# Add debug endpoint to API router
@api_router.get("/debug/schema")
async def api_debug_schema():
    """Debug endpoint to view the OpenAPI schema security schemes"""
    schema = app.openapi()
    security_schemes = schema.get("components", {}).get("securitySchemes", {})
    return {"securitySchemes": security_schemes}


# Include routers with the API prefix
api_router.include_router(manual_router, tags=["manuals"])
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])

# Include the API router in the app
app.include_router(api_router)


# Configure CORS
allowed_origins = settings["ALLOWED_ORIGINS"].split(",")

# If "*" is in allowed_origins, use that; otherwise, add specific origins including Keycloak
if "*" not in allowed_origins:
    # Add Keycloak URL to allowed origins
    keycloak_origin = KEYCLOAK_SERVER_URL.split("/auth")[
        0
    ]  # Get base URL without /auth
    if keycloak_origin not in allowed_origins:
        allowed_origins.append(keycloak_origin)

    # Add localhost with various ports for development
    for port in ["8000", "8001", "3000", "8080"]:
        local_origin = f"http://localhost:{port}"
        if local_origin not in allowed_origins:
            allowed_origins.append(local_origin)

logger.info(f"CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "X-Total-Count", "Authorization"],
    max_age=86400,  # 24 hours in seconds
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

__csrf_secret_key = secrets.token_urlsafe(16)
logger.info(f"CRSF Secret Key: {__csrf_secret_key}")
# references
# https://pypi.org/project/starlette-csrf/3.0.0/
# https://dev-in-seoul.tistory.com/44#CORS%20%EC%84%A4%EC%A0%95%EA%B3%BC%20CSRF%20%EA%B3%B5%EA%B2%A9%EC%9D%84%20%EB%A7%89%EA%B8%B0-1
app.add_middleware(
    CSRFMiddleware,
    secret=__csrf_secret_key,
    cookie_domain="localhost",
    cookie_name="csrftoken",
    cookie_path="/",
    cookie_secure=False,
    cookie_httponly=True,
    cookie_samesite="lax",
    header_name="x-csrf-token",
    safe_methods={"GET", "HEAD", "OPTIONS", "TRACE", "POST", "PUT", "DELETE", "PATCH"},
)

__session_secret_key = secrets.token_urlsafe(32)
logger.info(f"Session Secret Key: {__session_secret_key}")

app.add_middleware(
    SessionMiddleware,
    secret_key=__session_secret_key,
    session_cookie="session_id",
    max_age=1800,
    same_site="lax",
    https_only=True,
)

if __name__ == "__main__":
    try:
        settings = get_env_settings()
        uvicorn.run(
            "zmp_manual_backend.main:app",
            host=settings["HOST"],
            port=int(settings["PORT"]),
            reload=bool(settings["DEBUG"].lower() == "true"),
            log_level=settings["LOG_LEVEL"].lower(),
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
