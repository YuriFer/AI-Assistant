function_schemas = [
    # {
    #     "name": "GENERAL_INFORMATION",
    #     "description": "Informações gerais sobre a Dengue, Zika Vírus e Chikungunya. Geralmente são perguntas que o usuário pergunta sobre informações gerais dessas doenças.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "pergunta_usuario": {
    #                 "type": "string",
    #                 "description": "Pergunta realizada pelo usuário"
    #             }
    #         }
    #     }
    # },
    {
        "name": "SPECIFIC_SEARCH",
        "description": "Busca por informações sobre a Dengue, Zika Vírus ou Chikungunya em uma cidade específica do Brasil, um período específico e uma doença específica. É comum que os usuários enviem perguntas do tipo: 'Qual a situação da Dengue em <nome da cidade> entre <data inicial> e <data final>?', ou 'Quero saber a quantidade de casos de Dengue na cidade de <nome da cidade>",
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

INITIAL_TOOL_PROMPT = """
Você é um assistente informativo sobre a Dengue, Zika Vírus e Chikungunya. Sua função é responder somente sobre a Dengue, Zika Vírus e Chikungunya e ajudar os usuários com suas dúvidas

## Contexto
Estamos na data {date}

## Suas regras
- Se você não tiver certeza absoluta de qual ferramenta deve ser utilizada com base na pergunta do usuário, você deve confirmar com o usuário o que ele deseja fazer ou coletar mais informações até retirar todas suas dúvidas sobre qual ferramenta deve ser utilizada;
- Caso multiplas ferramentas possam ser utilizadas para responder a pergunta do usuário, SEMPRE escolha a ferramenta mais específica possível;
- Lembre-se de avaliar cada pergunta do usuário e escolher a ferramenta mais adequada a cada interação. Você SEMPRE deve tentar escolher uma das ferramentas disponíveis.
- Se o usuário não fornecer todas as informações necessárias para a ferramenta escolhida, você deve solicitar as informações necessárias para o usuário;
"""

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