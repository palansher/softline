from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.calculator import Calculator, CalculatorError
from app.schemas.payload import (
    CalculateErrorResponse,
    CalculateRequest,
    CalculateSuccessResponse,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Windows Calculator API",
    description="Веб-калькулятор на FastAPI и Python 3.12",
    version="1.0.0",
)

# Подключение статических файлов (CSS, JS)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Настройка шаблонизатора Jinja2
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Инициализируем сервис вычислений
calc_service = Calculator()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> HTMLResponse:
    """Отображает главную страницу калькулятора."""
    return templates.TemplateResponse(request=request, name="index.html")


# include_in_schema=False скрывает этот роут из документации Swagger (/docs)
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    svg_content = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <rect width="100" height="100" rx="22" fill="#0078D4"/>
        <text x="50" y="68" font-size="55" text-anchor="middle" fill="white" font-family="sans-serif">🧮</text>
    </svg>
    """
    return Response(content=svg_content, media_type="image/svg+xml")


@app.post(
    "/api/calculate",
    response_model=CalculateSuccessResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": CalculateErrorResponse},
    },
)
async def calculate(
    payload: CalculateRequest,
) -> CalculateSuccessResponse | JSONResponse:
    """API эндпоинт для безопасного вычисления математических выражений."""
    try:
        result = calc_service.evaluate(payload.expression)
        return CalculateSuccessResponse(status="success", result=result)
    except CalculatorError as err:
        """
        Перехватит и DivisionByZeroError, и InvalidExpressionError!
        Возвращаем понятный JSON клиенту с кодом 400 Bad Request.
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CalculateErrorResponse(status="error", message=str(err)).model_dump(),
        )
