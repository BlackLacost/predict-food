import asyncio
from pathlib import Path
from io import BytesIO

import aiohttp
import uvicorn
from fastai.vision import open_image, load_learner
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

model_url = 'http://drive.google.com/uc?export=download&id=1HcWMnAoSbiUA2BhpQuEp8sj0V3tv7ojp'
model_name = 'lesson1-homework-food-50-step2-(12_cycle).pkl'
path = Path(__file__).parent # app folder

templates = Jinja2Templates(directory='app/templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='app/static'), name='static')

async def download_model(url, filename):
    if not filename.exists():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.read()
                with open(filename, 'wb') as f:
                    f.write(data)

async def setup_learner(url, path, filename):
    await download_model(url, path/filename)
    return load_learner(path, filename)

async def main():
    tasks = [asyncio.create_task(
        setup_learner(model_url, path, model_name)
    )]
    [learn] = await asyncio.gather(*tasks)
    return learn

learn = asyncio.run(main())

@app.route('/')
async def index(request):
    context = {'request': request}
    return templates.TemplateResponse('index.html', context)

@app.route('/predict', methods=['POST'])
async def predict(request):
    form = await request.form()
    filename = form['file'].filename
    content = await form['file'].read()
    img = open_image(BytesIO(content))
    prediction = learn.predict(img)[0]
    return JSONResponse({'result': str(prediction)})

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)
