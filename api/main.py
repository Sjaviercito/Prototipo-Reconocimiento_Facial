from fastapi import FastAPI
from datos.visita_datos import obtener_visitas_abiertas, obtener_todas_las_visitas
from fastapi.responses import HTMLResponse

app = FastAPI()
@app.get("/adentro")
def quien_esta_adentro():
    visitas = obtener_visitas_abiertas()
    return {"adentro": visitas}


@app.get("/visitas")
def ver_todas_las_visitas():
    visitas = obtener_todas_las_visitas()
    return {"visitas": visitas}



@app.get("/", response_class=HTMLResponse)
def panel():
    with open("api/static/index.html", "r", encoding="utf-8") as f:
        return f.read()