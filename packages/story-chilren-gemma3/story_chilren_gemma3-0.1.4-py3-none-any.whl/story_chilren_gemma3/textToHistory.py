from ollama import Client
import json
import os
import regex as re


def safeTextUnicodeYoutube(texto):
    # Substitui aspas duplas por uma string vazia
    texto_sem_aspas = texto.replace('"', '')
    # Substitui quebras de linha por uma string vazia
    texto_limpo = texto_sem_aspas.replace('\n', '')
    return texto_limpo

def safeTextUnicodeSpeak(texto):
    # Substitui caracteres que não sejam letras, vírgulas, pontos de interrogação, pontos de exclamação ou espaços
    return re.sub(r'[^\p{L},¡¿!? ]+', '', texto) 

def safeTextUnicodeScene(texto):
    # Substitui caracteres que não sejam letras, vírgulas, pontos de interrogação, pontos de exclamação ou espaços
    return re.sub(r'[^\p{L},¡¿!? .:]+', '', texto) 


def formatPromptYoutube(history, tema, licao):
    """
    Gera o prompt para criação de conteúdo para YouTube baseado na história infantil.

    Parâmetros:
        history (str): A história infantil completa.
        tema (str): O tema utilizado para gerar a história.
        licao (str): A lição ou moral da história.

    Retorna:
        str: Um prompt formatado que solicita a geração de título, descrição e tags 
             para o vídeo no YouTube, estruturado em JSON.
    """
    return "Considere a história infantil: "+ history +". Gerado pelo tema '"+ tema + "' com a lição da história '" + licao + """'
    Gere para o youtube:

    [title] Um ótimo título incrível para história.
     
    [description] Também gere uma ótima descrição.
    
    [tags] Gere ótimas tag/palavras chaves no formato "tag, tag, tag,..." para youtube, ou seja, apenas as palavras chaves separado por virgula com máximo de 400 caracteres, elabore para vídeo no YouTube, adicione ícones interessantes sobre o tema, hashtag na descrição.

    responda apenas como TEXT extritamente nesta estrutura JSON:

    {
        "title": "....",
        "tags": ["tag1","tag2",...],
        "description":"..."    

    }"""


def formatPromptNarracao(tema, licao):
    """
    Gera o prompt para criação de uma história infantil narrada.

    Parâmetros:
        tema (str): O tema da história.
        licao (str): A lição ou moral da história.

    Retorna:
        str: Um prompt formatado que solicita a geração de uma narração da história,
             com frases de aproximadamente 120 caracteres cada e cerca de 12 frases, 
             estruturado em JSON.
    """
    return """
    
    Gere uma história infantil com o tema " 
    
    
    """ + tema + """ 
    
    " com a lição da história " 
    
    
    """ + licao + """ 
    
    " . Quero o formato da seguinte forma:

    [narration] Narração frase a frase de aproximadamente 120 caracteres, e aproximadamente 12 frases.
    responda apenas como TEXT extritamente nesta estrutura JSON:

    {
        "narration":[ "frase1 ....", "frase2 ...", ...]

    }"""

def formatPromptDescriptionScenes(scene,history,person):
    """
    Gera o prompt para a descrição de uma cena específica da história infantil.

    Parâmetros:
        scene (str): A parte ou frase da narração que descreve a cena.
        history (str): A história completa, utilizada para fornecer contexto.
        person (str): A descrição do personagem principal que deverá ser incorporada na cena.

    Retorna:
        str: Um prompt formatado que solicita a geração de uma descrição resumida da cena 
             (aproximadamente 100 caracteres), enfatizando o cenário, os personagens e suas ações.
    """
    return "Considerando a historia "+ history+ ". Focando apenas nesse trecho '"+ scene +"'." + """""' 

    [scenes] Gerar uma descrição da cena, descrevendo um cenário incrível com personagens e suas ações e o ambiente/local onde se passa a cena, importante, substitua a menção do personagem esse texto: '
    
    """+ person +"""

    '
    
    , e repita a descrição dos personagens em todas as cenas. Resuma em aproximadamente 100 caracteres

    responda apenas como TEXT extritamente:

    "...."


    """

def formatPromptDescriptionPerson(history):
    """
    Gera o prompt para a descrição completa do personagem principal da história.

    Parâmetros:
        history (str): A história completa, que servirá de base para a descrição do personagem.

    Retorna:
        str: Um prompt formatado que solicita uma descrição resumida e completa do personagem principal,
             incluindo detalhes como vestimenta e aparência.
    """
    return "Considerando a historia '"+ history+ """

    ' Gere uma descrição completa do personagem principal, como o que veste, sua aparência, resuma.
    responda apenas como TEXT extritamente:

    "...."


    """

def formatPromptTranslate(conteudo, idioma):
    """
    Gera o prompt para tradução de um conteúdo para o idioma especificado.

    Parâmetros:
        conteudo (str): O texto que deverá ser traduzido.
        idioma (str): O idioma para o qual o conteúdo deverá ser traduzido.

    Retorna:
        str: Um prompt formatado que solicita a tradução do conteúdo, respondida apenas como TEXT.
    """
    return "Traduza para a lingua '"+ idioma+ """

    ' o conteudo:

    "
    """+ conteudo +"""
    "

    Responda apenas como TEXT.

    """

def sendPrompt(prompt):
    """
    Envia o prompt para o serviço de chat utilizando o Client da biblioteca 'ollama' e retorna a resposta.

    Parâmetros:
        prompt (str): O prompt a ser enviado para o modelo de chat.

    Retorna:
        str: A resposta do modelo, com formatações indesejadas (como marcação de JSON) removidas, se necessário.
    """
       
    print("Prompt:", prompt)
    client = Client(
    host='http://127.0.0.1:11434/',
    headers={'x-some-header': 'some-value'}
    )
    response = client.chat(model='gemma3', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])

    resposta = response.message.content
    if "json" in resposta:
        resposta = (response.message.content).replace("```json","")
        resposta = resposta.replace("```","")
    return resposta


def create_storys(temas, licoes):

    """
    Função principal que orquestra a criação, tradução e armazenamento de uma história infantil.

    O fluxo de execução é o seguinte:
      1. Seleciona um índice (exemplo: i = 10) e gera a narração da história utilizando 'formatPromptNarracao'.
      2. Processa a resposta JSON para extrair a narração e gera, para cada frase, uma descrição de cena usando 'formatPromptDescriptionScenes'.
      3. Gera o prompt para criação do conteúdo para YouTube com 'formatPromptYoutube' e processa a resposta JSON.
      4. Realiza traduções para múltiplos idiomas (lista de idiomas e siglas definidas) para título, tags, descrição, narração e (para inglês) cenas utilizando 'formatPromptTranslate'.
      5. Armazena o resultado final em um arquivo JSON no caminho especificado.

    Parâmetros:
        temas (list): Lista de temas para a geração de histórias.
        licoes (list): Lista de lições correspondentes aos temas.

    Retorna:
        (None)
        SAVE PATH_HISTORY:
        "lan" = {
        "title": "....",
        "scenes": ["scenes1","scenes2",...,"scenes N"],
        "narration": ["narration1","narration2",...,"narration N"],
        "tags": ["tag1","tag2",...],
        "description":"..."    

        }
    """

    print("Carregando configs!")

    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o caminho para salvar: uma pasta acima do script e dentro de "config/"
    path_config = os.path.join(script_dir, "config")

    file_path = os.path.join(path_config, "config.json")

    if file_path :
        # Lê o JSON existente
        with open(file_path, 'r', encoding='utf-8') as arquivo:
            config = json.load(arquivo)
    else:
        print("Erro config não existe")
    for i in range(len(temas)):
        resposta = sendPrompt(formatPromptNarracao(temas[i], licoes[i]))
        print(resposta)
        try:
            dados_json = json.loads(resposta)
            print(dados_json['narration'])
            narracao = dados_json['narration']

            narracao_safe = []
            for safenarration in narracao:
                narracao_safe.append(safeTextUnicodeSpeak(safenarration)+ ", ")
            narracao = narracao_safe

            dados_json['narration'] = narracao
            scenes = []
            history = "".join(narracao)
            for scene in narracao:
                resposta_scene = sendPrompt(formatPromptDescriptionScenes(scene, history, formatPromptDescriptionPerson(history)))
                print(resposta_scene)
                scenes.append(safeTextUnicodeScene(resposta_scene))
            print(scenes)
            
            resposta_youtube = sendPrompt(formatPromptYoutube(history, temas[i], licoes[i]))
            print(resposta_youtube)
            try:
                dados_json_final = json.loads(resposta_youtube)

                dados_json_final["title"] = safeTextUnicodeYoutube(dados_json_final["title"]) 
                dados_json_final["tags"] = safeTextUnicodeYoutube(dados_json_final["tags"]) 
                dados_json_final["description"] = safeTextUnicodeYoutube(dados_json_final["description"]) 
                dados_json_final["narration"]=narracao
                dados_json_final["scenes"]=scenes
                print(dados_json_final)
                
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                print(f"Conteúdo da resposta: {resposta_youtube}")
            
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            print(f"Conteúdo da resposta: {resposta_scene}")

        languages = ["árabe","inglês", "espanhol", "francês", "alemão", "italiano", "polonês", "turco", "russo", "holandês", "tcheco", "chinês", "japonês", "húngaro", "coreano", "hindi"]
        siglas = ["ar", "en", "es", "fr", "de", "it", "pl", "tr", "ru", "nl", "cs",  "zh-cn", "ja", "hu", "ko", "hi"]
        dados_multlanguage = {}
        dados_multlanguage["pt"] = dados_json_final
        for j in range(len(languages)):
            temp = {}
            resposta_lang = sendPrompt(formatPromptTranslate(dados_json_final["title"], languages[j]))
            print(resposta_lang)
            temp['title'] = safeTextUnicodeYoutube(resposta_lang)
            resposta_lang = sendPrompt(formatPromptTranslate(dados_json_final["tags"], languages[j]))
            print(resposta_lang)
            temp['tags'] = safeTextUnicodeYoutube(resposta_lang)
            resposta_lang = sendPrompt(formatPromptTranslate(dados_json_final["description"], languages[j]))
            print(resposta_lang)
            temp['description'] = safeTextUnicodeYoutube(resposta_lang)
            aux = []
            for n in dados_json_final["narration"]:
                resposta_lang = sendPrompt(formatPromptTranslate(n, languages[j]))
                print(resposta_lang)
                aux.append(safeTextUnicodeSpeak(resposta_lang)+ ", ")
            temp['narration'] = aux
            aux = []
            if siglas[j] == "en":
                for n in dados_json_final["scenes"]:
                    resposta_lang = sendPrompt(formatPromptTranslate(n, languages[j]))
                    print(resposta_lang)
                    aux.append(safeTextUnicodeScene(resposta_lang))
                temp['scenes'] = aux
            dados_multlanguage[siglas[j]] = temp     
             
       
        with open(config["path_history"]+str(i)+"_history.json", 'w', encoding='utf-8') as f:
                    json.dump(dados_multlanguage, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":


    temas_criancas = [
    "Menina Júlia com vestido de bolinhas vermelho e uma gatinha Ana preta com olhos verdes",
    "Menino João vestido de bombeiro com capacete brilhante",
    "Menina Clara explorando uma floresta encantada com coelhinhos",
    "Menino Pedro pilotando um avião mágico entre as nuvens",
    "Menina Sofia pintando um mural colorido em uma cidade encantada",
    "Menino Lucas com uniforme de astronauta em uma aventura espacial",
    "Menina Isabela em um castelo encantado com um dragão amigável",
    "Menino Miguel jogando futebol com amigos na rua",
    "Menina Valentina cuidando de um jardim mágico com flores falantes",
    "Menino Gabriel com capa de super-herói salvando a cidade",
    "Menina Beatriz com mochila cheia de livros em uma aventura escolar",
    "Menino Henrique em uma corrida de carros de brinquedo no parque",
    "Menina Mariana navegando num barco de papel em um rio encantado",
    "Menino Rafael com capa de pirata em busca de tesouros escondidos",
    "Menina Laura em um laboratório de ciências com experimentos mágicos",
    "Menino Thiago brincando com robôs em um mundo futurista",
    "Menina Camila em um festival de balões coloridos",
    "Menino Gustavo em uma aventura de dinossauros no museu",
    "Menina Fernanda cuidando de um animalzinho de estimação mágico",
    "Menino Vitor em uma expedição pela savana africana",
    "Menina Alice descobrindo um livro encantado em uma biblioteca misteriosa",
    "Menino Daniel construindo uma torre com blocos gigantes",
    "Menina Nicole dançando em um baile de máscaras colorido",
    "Menino Eduardo em uma missão para salvar animais em perigo",
    "Menina Elisa explorando um castelo flutuante no céu",
    "Menino André participando de uma oficina de música com instrumentos mágicos",
    "Menina Paula em uma corrida de bicicletas num parque encantado",
    "Menino Roberto em uma aventura submarina com peixes falantes",
    "Menina Gabriela fazendo um piquenique com fadas no bosque",
    "Menino Felipe com traje de detetive resolvendo mistérios na vizinhança",
    "Menina Carolina em um circo mágico com palhaços divertidos",
    "Menino Matheus pilotando um trem encantado por paisagens maravilhosas",
    "Menina Luana construindo um castelo de areia na praia dourada",
    "Menino André em uma aventura com dinossauros no parque jurássico",
    "Menina Marina pintando o arco-íris num dia chuvoso",
    "Menino Igor jogando xadrez com um robô sábio",
    "Menina Helena em uma viagem de trem por cidades encantadas",
    "Menino Bruno em um acampamento sob as estrelas",
    "Menina Luna explorando uma caverna de cristais brilhantes",
    "Menino Caio em uma missão para salvar o planeta",
    "Menina Rita em um espetáculo de marionetes mágicas",
    "Menino Sérgio em uma corrida de carrinhos de controle remoto",
    "Menina Clara em uma aventura na cidade dos doces encantados",
    "Menino Fábio construindo uma ponte com blocos coloridos",
    "Menina Silvia em uma expedição ao topo de uma montanha mágica",
    "Menino Jorge explorando um jardim de borboletas encantadas",
    "Menina Rafaela em uma festa de aniversário no mundo dos sonhos",
    "Menino Leandro com uniforme de médico em uma clínica encantada",
    "Menina Elisa em um passeio de balão sobre paisagens encantadoras",
    "Menino Ricardo em uma jornada por trilhas misteriosas na floresta",
    "Menina Tainá com vestido de princesa em um baile real",
    "Menino Alexandre explorando um laboratório de invenções futuristas",
    "Menina Estela em uma aventura noturna com vaga-lumes mágicos",
    "Menino Vinícius em uma expedição pelo deserto encantado",
    "Menina Lorena em uma festa de máscaras em um jardim encantado",
    "Menino Otávio em uma jornada de bicicleta por vilarejos coloridos",
    "Menina Fabiana explorando uma caverna de segredos mágicos",
    "Menino Caetano em uma aventura de trem com paisagens surreais",
    "Menina Denise em um parque de diversões encantado",
    "Menino Eduardo em uma viagem ao centro da Terra",
    "Menina Renata em uma expedição de bicicleta por trilhas mágicas",
    "Menino Marcos em um espetáculo de mágica e ilusionismo",
    "Menina Lúcia com um vestido de fada em um bosque encantado",
    "Menino Gustavo em uma aventura de barco pelo rio encantado",
    "Menina Silvia em uma jornada pelo mundo dos sonhos com unicórnios",
    "Menino Rafael em uma missão de resgate com dinossauros amigáveis",
    "Menina Carina em uma aventura mágica por uma cidade de cristal",
    "Menino Sérgio em uma competição de patins em uma pista brilhante",
    "Menina Lara em um festival de cores com pinturas vivas",
    "Menino André em uma jornada de exploração por florestas encantadas",
    "Menina Bianca com vestido de bolinhas e laços em um parque encantado",
    "Menino Roberto em uma aventura de carro de corrida com pistas mágicas",
    "Menina Melissa em uma viagem de trem por cidades encantadas",
    "Menino Felipe em um laboratório de invenções com brinquedos interativos",
    "Menina Aline em um passeio por um mundo de contos de fadas",
    "Menino Igor em uma expedição pelo espaço em uma nave brilhante",
    "Menina Julia em uma festa de aniversário com personagens mágicos",
    "Menino Caio em uma corrida de skate com obstáculos divertidos",
    "Menina Rosa em um jardim encantado com flores falantes",
    "Menino Daniel em uma aventura de balão sobre montanhas encantadas",
    "Menina Isadora em uma viagem mágica com pôneis e arco-íris",
    "Menino Leonardo em uma jornada de bicicleta por estradas encantadas",
    "Menina Estefânia em uma expedição pelo mar em um barco encantado",
    "Menino Vítor em uma aventura na floresta com animais falantes",
    "Menina Patrícia em uma festa temática com personagens de contos de fadas",
    "Menino Samuel em uma corrida de carrinhos de brinquedo num mundo mágico",
    "Menina Rafaela em uma viagem pelo espaço com estrelas brilhantes",
    "Menino Francisco em uma expedição para descobrir segredos do oceano",
    "Menina Agatha em uma aventura num reino encantado de fadas",
    "Menino Eduardo em uma missão para salvar uma cidade mágica",
    "Menina Olívia em um passeio de barco por lagos encantados",
    "Menino Rodrigo em uma competição de skate em uma pista mágica",
    "Menina Vitória em uma festa de máscaras num baile encantado",
    "Menino André em uma aventura de trem por paisagens surreais",
    "Menina Eduarda em uma expedição por trilhas encantadas na floresta",
    "Menino Luan em uma corrida de carros em um circuito encantado",
    "Menina Nicole em um mundo de fantasias com princesas e dragões",
    "Menino Miguel em uma aventura por um planeta distante",
    "Menina Camila em um cenário de inverno com neve encantada",
    "Menino Bruno em uma missão de resgate em uma cidade futurista"
    ]

    licoes_criancas = [
        "Economizar dinheiro",
        "Estudar é importante para a prosperidade",
        "Cuidar da natureza",
        "Sonhar grande",
        "A criatividade transforma o mundo",
        "A educação abre portas para o universo",
        "A coragem vence desafios",
        "O trabalho em equipe é fundamental",
        "O respeito pela natureza é essencial",
        "A bondade faz a diferença",
        "O conhecimento é poder",
        "A persistência leva ao sucesso",
        "A imaginação abre horizontes",
        "A honestidade é o melhor caminho",
        "A curiosidade impulsiona a inovação",
        "A tecnologia com responsabilidade",
        "Compartilhar alegrias fortalece amizades",
        "Aprender sobre o passado constrói o futuro",
        "A empatia transforma relações",
        "Respeitar as diferenças culturais",
        "Ler é viajar sem sair do lugar",
        "A paciência constrói grandes realizações",
        "A autoestima brilha de dentro para fora",
        "A compaixão salva vidas",
        "A imaginação não tem limites",
        "A harmonia une corações",
        "O exercício é essencial para a saúde",
        "A preservação dos oceanos é vital",
        "A amizade enriquece a vida",
        "A curiosidade leva à descoberta",
        "A alegria é contagiante",
        "A persistência abre caminhos",
        "A criatividade transforma o simples em especial",
        "O respeito pelo passado é fundamental",
        "A beleza está na diversidade",
        "O raciocínio lógico é a chave do sucesso",
        "A aventura ensina sobre o mundo",
        "A amizade fortalece a jornada",
        "O conhecimento ilumina a escuridão",
        "A sustentabilidade é responsabilidade de todos",
        "A imaginação transforma histórias",
        "A competição saudável estimula o crescimento",
        "O equilíbrio entre o prazer e a saúde é essencial",
        "A cooperação constrói futuros brilhantes",
        "A determinação supera obstáculos",
        "O cuidado com a natureza gera harmonia",
        "Celebrar a vida é importante",
        "A empatia cura feridas",
        "A liberdade inspira conquistas",
        "A coragem é o primeiro passo para a mudança",
        "A gentileza abre portas",
        "A inovação transforma o mundo",
        "A luz da esperança nunca se apaga",
        "A resiliência é a chave do sucesso",
        "A diversidade torna o mundo mais rico",
        "O esforço leva à recompensa",
        "A curiosidade é o primeiro passo para o conhecimento",
        "A determinação conquista sonhos",
        "A diversão ensina lições valiosas",
        "O aprendizado é uma aventura sem fim",
        "A superação nasce da prática",
        "A imaginação é uma ferramenta poderosa",
        "A fé transforma os desafios",
        "A cooperação torna tudo possível",
        "A imaginação liberta o espírito",
        "A coragem e a responsabilidade caminham juntas",
        "A persistência conquista horizontes",
        "A disciplina é o caminho para o sucesso",
        "A arte é uma forma de expressão",
        "O respeito pela natureza ensina sabedoria",
        "A alegria se multiplica com a amizade",
        "A determinação supera barreiras",
        "A aventura é um aprendizado constante",
        "A criatividade gera soluções inovadoras",
        "A imaginação é a chave dos sonhos",
        "O universo se revela para os curiosos",
        "Celebrar as conquistas inspira novas jornadas",
        "A persistência transforma desafios em vitórias",
        "A natureza ensina lições de vida",
        "A liberdade e a coragem andam juntas",
        "A bondade cria laços duradouros",
        "O esforço vale cada pedalada",
        "A cooperação conquista mares",
        "O respeito pelos seres vivos é fundamental",
        "A imaginação nos ensina a ser felizes",
        "A determinação vence desafios",
        "O conhecimento ilumina a escuridão",
        "A curiosidade abre portas para o saber",
        "A empatia transforma o mundo",
        "A solidariedade constrói pontes",
        "A paciência colhe os frutos",
        "A determinação é o segredo do sucesso",
        "A diversidade enriquece a convivência",
        "A imaginação impulsiona a criatividade",
        "A persistência leva a grandes conquistas",
        "A disciplina e o foco trazem resultados",
        "O respeito à diversidade é essencial",
        "O conhecimento é a base para um futuro brilhante",
        "A união aquece os corações",
        "A solidariedade constrói um mundo melhor"
    ]

    temas_animais = [
        "Tartaruguinha Júlia bancária e gatinha Ana com olhos verdes",
        "Macaquinho Pedro bombeiro de macacão",
        "Coelhinho Lucas jardineiro de cenouras encantadas",
        "Passarinha Marina mensageira de boas vibrações",
        "Peixinho Bruno pescador de histórias mágicas",
        "Cachorrinho Rafael professor de matemática divertida",
        "Porquinho Gabriel artista pintando sonhos",
        "Borboletinha Isabela exploradora do arco-íris",
        "Elefantinho Thiago guardião da selva encantada",
        "Girafinha Helena aventureira em safári de cores",
        "Leãozinho Eduardo rei da floresta sorridente",
        "Ursozinho Caio contador de estrelas brilhantes",
        "Canguru Lara saltitante em prados coloridos",
        "Panda Sofia mensageira da paz e harmonia",
        "Tigrezinho Felipe guardião dos segredos da selva",
        "Rena Júlia viajante pelo reino gelado",
        "Macaco Bento músico das árvores encantadas",
        "Pinguim Léo explorador dos polos congelados",
        "Zebrinha Rita dançarina das planícies",
        "Hipopótamo Ítalo nadador das águas mágicas",
        "Rinoceronte Sara aventureira no deserto encantado",
        "Flamingo Clara dançarina das lagoas brilhantes",
        "Cavalo Miguel corredor dos campos dourados",
        "Ovelhinha Lúcia tricoteira de sonhos fofinhos",
        "Girafa Alice colecionadora de sorrisos mágicos",
        "Jacaré Vinicius guardião dos pântanos misteriosos",
        "Ganso Marcos viajante dos lagos encantados",
        "Lobo Pedro protetor das montanhas serenas",
        "Raposa Luna contadora de contos encantados",
        "Guaxinim André caçador de aventuras noturnas",
        "Esquilo Lara colecionadora de nozes mágicas",
        "Tartaruga Bianca viajante do tempo encantado",
        "Coala Fernanda exploradora dos eucaliptos",
        "Baleia Clara cantora dos oceanos profundos",
        "Golfinho Rafael mensageiro das ondas felizes",
        "Caracol Mateus pensador das trilhas místicas",
        "Abelhinha Vitória cuidadora das flores encantadas",
        "Borboleta Catarina pintora do jardim encantado",
        "Joaninha Sofia portadora de sorte e alegria",
        "Formiguinha Isabel trabalhadora em comunidade unida",
        "Sapo Marcos saltitante no lago encantado",
        "Pato Daniel nadador dos lagos de cristal",
        "Gatinho Otávio aventureiro pelas noites mágicas",
        "Cãozinho Marcos amigo leal e corajoso",
        "Vaca Marta leiteira dos campos floridos",
        "Cabra Júlia escaladora das montanhas encantadas",
        "Bode Pedro saltitante pelo vale da amizade",
        "Pavão Felipe exibicionista do jardim mágico",
        "Periquito Ana mensageira dos segredos do vento",
        "Papagaio Lucas contador de histórias tropicais",
        "Rato Miguel explorador dos queijos mágicos",
        "Hamster Bianca corredora do labirinto encantado",
        "Cervo Henrique protetor das florestas místicas",
        "Javali Rafael aventureiro pelos bosques secretos",
        "Alce Sofia navegante dos rios serenos",
        "Bicho-preguiça Léo calmante das tardes lentas",
        "Tamanduá Laura detetive dos segredos da floresta",
        "Morceguinho Igor voador na noite encantada",
        "Lêmure Paula saltitante pelas copas das árvores",
        "Paca Roberto aventureiro nas trilhas da selva",
        "Capivara Clara amiga das águas serenas",
        "Mico Dourado André explorador das matas",
        "Arara Júlia colorida nas alturas do saber",
        "Marimbondo Pedro mensageiro das colmeias",
        "Morcego Lúcio aventureiro do céu estrelado",
        "Pandazinho Rafael guardião dos bambuzais",
        "Foca Camila nadadora das ondas geladas",
        "Tubarão Bruno protetor dos recifes mágicos",
        "Estrela-do-mar Luna exploradora dos mares",
        "Polvo Igor inventor das águas misteriosas",
        "Caranguejo Mateus caminhante das praias douradas",
        "Camarão Sara saltitante nos recifes encantados",
        "Águia Valentina voadora sobre os cumes",
        "Coruja Henrique sábio das noites silentes",
        "Gavião Lucas vigilante dos céus brilhantes",
        "Falcão Bruno mensageiro dos ventos livres",
        "Mariposa Ana dançarina do luar mágico",
        "Besouro Rafael explorador dos bosques coloridos",
        "Cigarra Sofia cantora das tardes de verão",
        "Grilo Miguel mensageiro das canções da natureza",
        "Formiga Ana trabalhadora das trilhas de cooperação",
        "Abelha Pedro cuidadora do jardim vibrante",
        "Mariposa Júlia dançarina das luzes noturnas",
        "Vespa Lucas aventureiro dos campos ensolarados",
        "Cigarra Lúcia mensageira das melodias da vida",
        "Lagartinha Helena transformadora dos jardins",
        "Gafanhoto Gabriel saltitante pelos campos",
        "Besouro Camila colecionadora de tesouros naturais",
        "Joaninha Pedro mensageiro da sorte e alegria",
        "Borboleta Rafael voador pelos prados encantados",
        "Caterpilar Sofia transformadora dos sonhos",
        "Caracol Pedro aventureiro pelas trilhas suaves",
        "Rena Ana viajante pelo mundo congelado",
        "Alce Rafael guardião das florestas antigas",
        "Tartaruguinha Lúcia viajante dos segredos do tempo",
        "Macaquinho Bruno explorador das árvores mágicas",
        "Coelhinho Júlia jardineira dos campos floridos",
        "Passarinha Daniel mensageiro dos ventos suaves",
        "Peixinho Ana nadadora dos recifes encantados",
        "Cachorrinho Lucas amigo leal dos corações"
    ]

    licoes_animais = [
        "Economizar dinheiro",
        "Estudar é importante para prosperidade",
        "Cuidar da natureza",
        "Valorizar a amizade",
        "Compartilhar é se importar",
        "Respeitar as diferenças",
        "A honestidade constrói confiança",
        "A coragem enfrenta desafios",
        "A persistência gera resultados",
        "Aprender com os erros",
        "Ser gentil com os outros",
        "Trabalhar em equipe",
        "Valorizar o esforço",
        "Respeitar os animais",
        "Cuidar do meio ambiente",
        "Aprender a perdoar",
        "O respeito gera harmonia",
        "A criatividade transforma o mundo",
        "A educação abre portas",
        "A paciência traz resultados",
        "Valorizar a família",
        "Aprender com os mais velhos",
        "Ter empatia com os outros",
        "Ser grato pelo que se tem",
        "Investir no conhecimento",
        "Respeitar as tradições",
        "Cuidar dos amigos",
        "A bondade gera sorrisos",
        "Ouvir os conselhos",
        "Compartilhar os bons momentos",
        "Valorizar cada conquista",
        "Ser responsável",
        "A perseverança vence obstáculos",
        "A honestidade é a melhor política",
        "Valorizar o trabalho",
        "Respeitar a natureza",
        "A cooperação fortalece a comunidade",
        "Aprender a lidar com desafios",
        "A gentileza transforma o dia",
        "Ser solidário",
        "Valorizar a diversidade",
        "Aprender com a imaginação",
        "O esforço traz recompensas",
        "Cuidar do planeta",
        "A amizade é um tesouro",
        "O respeito começa em casa",
        "Aprender com o esporte",
        "Valorizar a criatividade",
        "Cuidar do bem-estar",
        "A empatia constrói pontes",
        "Aprender com a natureza",
        "Valorizar a simplicidade",
        "A persistência é fundamental",
        "Compartilhar responsabilidades",
        "Ser gentil com o meio ambiente",
        "Valorizar o tempo",
        "Aprender a trabalhar em conjunto",
        "A cooperação faz a diferença",
        "A determinação leva ao sucesso",
        "Valorizar cada oportunidade",
        "Ser honesto",
        "A importância da disciplina",
        "Aprender com o respeito",
        "Cuidar dos sentimentos",
        "Valorizar os pequenos gestos",
        "O esforço gera progresso",
        "Aprender a ajudar",
        "A bondade é contagiante",
        "Ser humilde",
        "Valorizar o conhecimento",
        "Aprender a compartilhar sonhos",
        "A determinação vence desafios",
        "Cuidar do coração",
        "Valorizar a amizade verdadeira",
        "Aprender a ser perseverante",
        "A união faz a força",
        "Valorizar a imaginação",
        "Aprender com os erros",
        "O respeito é a base de tudo",
        "Ser agradecido",
        "Valorizar a saúde",
        "Aprender a ser resiliente",
        "Cuidar da comunidade",
        "Valorizar o trabalho em equipe",
        "Aprender com a experiência",
        "A importância da ética",
        "Valorizar a diversidade cultural",
        "Aprender a se expressar",
        "Cuidar dos sentimentos alheios",
        "Valorizar as tradições",
        "Aprender com a paciência",
        "A perseverança gera resultados",
        "Valorizar o respeito mútuo",
        "Aprender a ser compassivo",
        "Cuidar da natureza com amor",
        "Valorizar os laços de amizade",
        "Aprender a ter coragem",
        "A importância da disciplina",
        "Valorizar cada momento",
        "Aprender a ser um amigo leal"
    ]
    temas_concat = temas_criancas+ temas_animais
    licoes_concat = licoes_criancas + licoes_animais
    temas = []
    licoes = []

    ordem = [96, 119, 153, 13, 172, 31, 177, 100, 112, 70, 5, 123, 136, 150, 197, 113, 48, 37, 26, 183, 11, 103, 154, 127, 184, 56, 106, 12, 110, 156, 74, 188, 85, 14, 133, 41, 198, 45, 134, 107, 47, 18, 174, 159, 114, 51, 146, 21, 164, 93, 59, 7, 22, 176, 44, 64, 49, 160, 94, 116, 168, 46, 170, 67, 139, 2, 166, 158, 126, 173, 180, 118, 87, 60, 53, 187, 0, 195, 165, 138, 73, 23, 135, 42, 109, 43, 122, 171, 24, 15, 52, 10, 125, 62, 83, 72, 140, 38, 79, 9, 35, 6, 151, 147, 131, 92, 104, 111, 82, 189, 191, 30, 1, 40, 141, 80, 8, 63, 29, 77, 175, 178, 17, 75, 91, 25, 149, 192, 55, 142, 58, 89, 179, 61, 152, 128, 145, 98, 161, 84, 186, 99, 27, 4, 193, 137, 19, 57, 97, 3, 54, 148, 196, 194, 121, 132, 69, 71, 105, 34, 86, 167, 68, 129, 50, 16, 143, 182, 117, 20, 108, 28, 130, 120, 33, 66, 144, 181, 81, 39, 199, 76, 65, 90, 102, 124, 162, 157, 169, 78, 32, 163, 36, 88, 155, 115, 190, 101, 95, 185]

    num = 0
    for i in ordem:
        num = num + 1
        if i > 199 or i < 0:
            print(i)
        temas.append(temas_concat[i])
        licoes.append(licoes_concat[i])
        if num == 2:
            break


    create_storys(temas, licoes)
        