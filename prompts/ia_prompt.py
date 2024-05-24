function_schemas = [
    {
        "name": "GENERAL_INFORMATION",
        "description": "Informações gerais sobre a Dengue, Zika Vírus e Chikungunya",
        "parameters": {
            "type": "object",
            "properties": {
                "pergunta_usuario": {
                    "type": "string",
                    "description": "Pergunta realizada pelo usuário"
                }
            }
        }
    },
    {
        "name": "SPECIFIC_SEARCH",
        "description": "Busca por informações sobre a Dengue, Zika Vírus ou Chikungunya em uma cidade específica do Brasil, um período específico e uma doença específica",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Nome da cidade"
                },
                "disease": {
                    "type": "string",
                    "description": "Nome da doença"
                },
                "start_date": {
                    "type": "string",
                    "description": "Data inicial no formato dd/mm/yyyy"
                },
                "end_date": {
                    "type": "string",
                    "description": "Data final no formato dd/mm/yyyy"
                }
            },
            "required": ["city", "disease", "start_date", "end_date"]
        }
    }
]

TOOLS = [{"type": "function", "function":function} for function in function_schemas]

INITIAL_TOOL_PROMPT = """AQUI VAI A PROMPT UTILIZADA PARA DEFINIR A FERRAMENTA ADEQUADA PARA USO E PEGAR OS DADOS(PARAMETROS) DA FERRAMENTA
                        buscar os dados na response e verificar a ferramenta pega, assim mandar o prompt de search específico dps de pegar os dados com a dengue api"""

SPECIFIC_SEARCH_PROMPT = """AQUI VAI A PROMPT PARA A BUSCA ESPECÍFICA, UTILIZANDO DADOS DA DENGUE API 'Você é um assistente de IA especializado em ciências de dados que responde às perguntas dos usuários com relação a Dengue, Zika Vírus e Chikungunya.
                    Abaixo você encontrará dados em formato JSON. Use-o para responder às perguntas do usuário. (Lembrar de adicionar no historico a role, tool_call_id, name, e content)"""



INITIAL_PROMPT = """Você é um assistente informativo sobre a Dengue, Zika Vírus e Chikungunya. Você deve responder somente sobre a Dengue, Zika Vírus e Chikungunya, você deve informar tudo sobre as doenças\n
                    e como preveni-las e outras informações. Você deve responder de forma clara e objetiva, evitando informações desnecessárias. Você deve responder de forma educativa e informativa.\n
                    
                    Você deve seguir algumas regras:\n
                    - Caso o usuário peça informações sobre alguma dessas doenças de um local específico, você deve informar a situação atual da doença nesse local. Para isso você deve ter as seguintes informações que o usuário deve te fornecer:\n
                        - Nome da cidade\n
                        - Nome da doença\n
                        - Data inicial no formato dd/mm/yyyy\n
                        - Data final no formato dd/mm/yyyy\n
                    - Caso ele não forneça as informações necessárias, peça para ele fornecê-las.\n
                    - Caso ele não forneça a data precisamente, calcule ela com base na data atual.\n
                    - Caso as informacões fornecidas pelo usuário não sejam válidas, informe que as informações fornecidas não são válidas e peça para ele fornecer as informações válidas.\n
                    - Caso as informações estejam corretas, você deve deve ler os seguintes dados 
                    """