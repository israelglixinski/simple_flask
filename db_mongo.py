from pymongo import MongoClient
from datetime import datetime
import os


# Conexão com o Mongo
mongopass = os.getenv('MONGO_PASS')

if not mongopass:
    raise ValueError("A variável de ambiente 'MONGO_PASS' não está definida!")

client = MongoClient(f"mongodb+srv://israelglixinski:{mongopass}@cluster0.kzkzrs2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["licitacao"]
colecao = db["pncp"]

# Configurar locale para formato monetário brasileiro



def encontrar_pertinentes():

    agora = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    filtro = {
        "objetoCompra": { 
            "$regex": "(software)", 
            "$options": "i"
        },
        "dataEncerramentoProposta": { 
            "$gt": agora
        }
    }
    
    chaves_selecionadas = {
        "objetoCompra": 1,
        "dataEncerramentoProposta": 1,
        "valorTotalEstimado": 1
        # "_id": 0  # Oculta o campo "_id"
    }
    

    total_registros = colecao.count_documents(filtro)
    # print('\n')
    # print(total_registros)
    # print('\n')



    consulta = colecao.find(filtro)
    list_registros = []
    for documento in consulta:

        # documento['valorTotalEstimado']         = locale.currency(documento['valorTotalEstimado'], grouping=True, symbol="R$ ")
        # documento['dataEncerramentoProposta']   = str(documento['dataEncerramentoProposta']).replace('T',' ')

        # valor_formatado = locale.currency(documento['valorTotalEstimado'], grouping=True, symbol="R$ ")        
        # datahora_formatada = str(documento['dataEncerramentoProposta']).replace('T',' ')

        # print('\n')
        # print(f'valorTotalEstimado       - '+valor_formatado                             ) 
        # print(f'dataEncerramentoProposta - '+datahora_formatada                          ) 
        # print(f'_id                      - '+str(documento['_id'                       ])) 
        # print(f'objetoCompra             - '+str(documento['objetoCompra'              ])) 
        # print('\n')    
        
        ano_CtPNCP = str(documento['numeroControlePNCP']).split('/')[-1]
        cli_CtPNCP = str(documento['numeroControlePNCP']).split('-')[0]
        num_CtPNCP = int(str(documento['numeroControlePNCP']).split('-')[-1].split('/')[0])
        link = f'https://pncp.gov.br/app/editais/{cli_CtPNCP}/{ano_CtPNCP}/{num_CtPNCP}'
        
        list_registros.append({
            'valorTotalEstimado': str(documento['valorTotalEstimado'])
            ,'dataEncerramentoProposta':str(documento['dataEncerramentoProposta']).replace('T',' ')
            ,'objetoCompra':documento['objetoCompra']
            ,'link':link
            ,'interesse':documento['interesse']
        })

    return {"total_registros":total_registros,"list_registros":list_registros}


def atualizar_interesse(licitacao_id, novo_interesse):
    colecao.update_one({"id": licitacao_id}, {"$set": {"interesse": novo_interesse}})


if __name__ == "__main__":
    dados = encontrar_pertinentes()
    print(dados)
       
    
    # for registro in dados["list_registros"]:
    #     print('\n')
    #     print(registro)
    #     print('\n')
    
    
    
    # print(dados["total_registros"])

    pass