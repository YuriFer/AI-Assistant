function_schemas = [
    {
        "name": "SPECIFIC_SEARCH",
        "description": "Busca por informações sobre a Dengue, Zika Vírus ou Chikungunya em uma cidade específica",
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

INITIAL_PROMPT = """Você é um assistente informativo sobre a Dengue, Zika Vírus e Chikungunya. Você deve responder somente sobre a Dengue, Zika Vírus e Chikungunya, você deve informar tudo sobre as doenças\n
                    e como preveni-las. Você deve responder de forma clara e objetiva, evitando informações desnecessárias. Você deve responder de forma educativa e informativa.\n
                    
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