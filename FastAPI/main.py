# main.py

from fastapi import FastAPI, Request
from RAG import Rag
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve files from the static directory under /static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_content = """
    <html>
        <head>
            <title>Endringer Navigation</title>
        </head>
        <body>
            <button onclick="window.location.href='/endringer';">Go to Endringer</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


endring_systemvegg = """Beskrivelse av forholdet
Det er ikke medtatt systemvegger på høyde 3,4m.

Utredning og forslag til løsning
Det må bestilles plater på spesiallengde 3,4m.

Post 1: Minimumsantallet er 504 plater/ 1542m2. Plater på lengde 3,4m har en høyere pris med kr 9,30 pr m2.

Post 2: Det er rimeligere å benytte 3,4m platene til 3,3m enn å brenne inne med mye plater ekstra. Merkostnaden for nedkappet 3,3m plater er pr stk Kr 30,-. Det går med totalt 252plater på lengde 3,3m. F2 - 218 plater / D2 - 34 plater.

Post 3: Plater 3,4m som PT ikke benyttes i prosjektet blir 174stk.

Vederlagsjustering etter
 Justerte priser

 Eget pristilbud

Kostnadsoversikt
Postnr.	Beskrivelse	Firma	Enhet	Mengde	Enhetspris	Påslag	Totalbeløp	
1	Merkostnad pr m2 for spesiallengde plater	OBI	m2	1542	10,7	-	16 491,69	
2	Merkostnad nedkapping av 3,4 til 3,3	OBI	stk	252	34,5	-	8 694	
3	Merkostnad for 3,4m plater som PT ikke benyttes i prosjektet	OBI	stk	174	47,15	-	8 204,1	
Totalsum alle kostnader	33 389,79
"""


endring_himling = """
El.kanal gjennom himling

Beskrivelse av forholdet
Det skal monteres el-kanal gjennom himlingene

Utredning og forslag til løsning
Kappet vegglister for el-kanalene i bygg F 5-6-7-8 etg

Vederlagsjustering etter
 Regningsarbeid

Kostnadsoversikt
Postnr.	Beskrivelse	Firma	Enhet	Mengde	Enhetspris	Påslag	Totalbeløp	
1	arbeid	OBI	timer	8	660	-	5 280	

"""

endring_trespeilhimlinger = """Bygg DEG - trespilehimlinger i kommunikasjon

Beskrivelse av forholdet
Endret utførelse fra kontrakt post 10 EH.005

Mengder revidert da noe var uteglemt. endret fra 788m2 til 805,9m2

Utredning og forslag til løsning
Akustisk himlingsplate over trespilehimlinger

hvitpigmentering trespiler

Vederlagsjustering etter
 Kontraktens priser

 Eget pristilbud

Kostnadsoversikt
Postnr.	Beskrivelse	Firma	Enhet	Mengde	Enhetspris	Påslag	Totalbeløp	
1	Akustisk himlingsplate	OBI	m2	805.9	200	-	161 180	
2	hvitpigmentering trespiler	OBI	m2	805.9	41	-	33 041,9	
3	Prisregulering akustisk himlingsplate 1,3%	OBI	%	0.013	161 180	-	2 095,34	
4	R&D	OBI	%	0.05	196 316,9	-	9 815,85	
Totalsum alle kostnader	206 133,09"""




@app.get("/endringer", response_class=HTMLResponse)
async def get_endringer():
    # Example content for demonstration purposes

    html_content = f"""
    <html>
        <head>
            <title>Endringer Overview</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f0f0f0;
                }}
                .container {{
                    max-width: 800px;
                    margin: auto;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333;
                }}
                h2 {{
                    color: #666;
                }}
                pre {{
                    background-color: #eee;
                    padding: 15px;
                    overflow: auto;
                    border-radius: 5px;
                }}
                button {{
                    padding: 10px 20px;
                    font-size: 16px;
                    color: white;
                    background-color: #007bff;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Endringer</h1>
                <h2>Endring Systemvegg</h2>
                <pre id="systemvegg">{endring_systemvegg}</pre>
                <button onclick="executeMethod1('systemvegg')">SIM SALA BIM
                    <img src="/static/6056254-200.png" width="50" > 
                </button>
                <h2>Endring Himling</h2>
                <pre id="himling">{endring_himling}</pre>
                <button onclick="executeMethod1('himling')">SIM SALA BIM
                    <img src="/static/6056254-200.png" width="50" >                 
                </button>
                <h2>Endring Trespeilhimlinger</h2>
                <pre id="trespeilhimlinger">{endring_trespeilhimlinger}</pre>
                <button onclick="executeMethod1('trespeilhimlinger')">SIM SALA BIM
                    <img src="/static/6056254-200.png" width="50" > 
                </button>
            </div>
            <script>
                function executeMethod1(endringerId) {{
                    const endringerContent = document.getElementById(endringerId).innerText;
                    fetch('/execute-method1', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify({{ endringer: endringerContent }})
                    }})
                    .then(alert("AI is processing the contracts"))
                    .then(response => response.json())
                    .then(data => alert(data.message))
                    .catch((error) => {{
                        console.error('Error:', error);
                    }});
                }}
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/execute-method1")
async def execute_method1(request: Request):
    rag = Rag()
    body = await request.json()
    endringer_content = body.get("endringer")
    result_message = rag.method1(endringer_content)  # Assuming method1 exists and accepts the content as argument
    return JSONResponse(content={"message": result_message})