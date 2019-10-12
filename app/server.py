import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='app/static'), name='static')

@app.route('/')
async def index(request):
    context = {'request': request}
    return templates.TemplateResponse('index.html', context)
