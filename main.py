from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import functions.excel_functions.reader_excel as funcao_planilha

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/encomendas/planilhas")
async def load_planilha(planilha: UploadFile = File(...)):
    contents = await planilha.read()
    """
    O método load_workbook espera um caminho de arquivo como argumento, não o conteúdo da planilha.
    Para carregar uma planilha a partir de um conteúdo em memória, podemos usar BytesIO para criar um arquivo temporário
    em memória e então passar esse arquivo para o load_workbook.

     O conteúdo da planilha é lido e passado para BytesIO para criar um arquivo temporário em memória. 
     Esse arquivo temporário é então passado para o load_workbook para carregar a planilha.
    """
    try:
        with BytesIO(contents) as planilha_temporaria:
            dados_planilha = funcao_planilha.pegar_dados_intervalo_planilha(planilha_temporaria, 'A1:E18')
        # print({"filename": planilha.filename})
        # print(planilha.filename)
        # print(planilha.headers["content-disposition"])
        return dados_planilha
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})
