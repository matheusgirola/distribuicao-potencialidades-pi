import re, unicodedata

SECOES = {
 'A': 'A - Agricultura, pecuária, produção florestal, pesca e aquicultura',
 'B': 'B - Indústrias extrativas',
 'C': 'C - Indústrias de transformação',
 'D': 'D - Eletricidade e gás',
 'E': 'E - Água, esgoto, resíduos e descontaminação',
 'F': 'F - Construção',
 'G': 'G - Comércio; reparação de veículos',
 'H': 'H - Transporte, armazenagem e correio',
 'I': 'I - Alojamento e alimentação',
 'J': 'J - Informação e comunicação',
 'K': 'K - Atividades financeiras e de seguros',
 'L': 'L - Atividades imobiliárias',
 'M': 'M - Atividades profissionais, científicas e técnicas',
 'N': 'N - Atividades administrativas e serviços complementares',
 'O': 'O - Administração pública, defesa e seguridade social',
 'P': 'P - Educação',
 'Q': 'Q - Saúde humana e serviços sociais',
 'R': 'R - Artes, cultura, esporte e recreação',
 'S': 'S - Outras atividades de serviços',
 'T': 'T - Serviços domésticos',
 'U': 'U - Organismos internacionais',
 'Z': 'Z - Não classificado',
}

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode()
    return re.sub(r'\s+', ' ', s.lower()).strip()

# ordered (regex, secao). First match wins -> most specific first.
RULES = [
    (r'aluguel de imoveis proprios|corretagem na compra e venda|corretagem no aluguel|gestao e administracao da propriedade imobiliaria|compra e venda de imoveis proprios|loteamento de imoveis proprios', 'L'),
    (r'^aluguel de |^locacao de ', 'N'),
    (r'^fabricacao |^confeccao|^conservas de|^producao de |^preparacao de |^beneficiamento de (arroz|cafe|trigo|castanha|leite)|^moagem|^torrefacao|^abate de|^laticinios|^curtimento|^serrarias|^desdobramento de madeira|^impressao|^metalurgia|^fundicao|^usinagem|^panificacao|^lapidacao', 'C'),
    (r'atividades de condicionamento fisico', 'R'),
    # --- Comércio (G) : capturar antes de indústria/serviços ---
    (r'comercio (varejista|atacadista|a varejo)|representantes comerciais|intermediarios do comercio|manutencao e reparacao de (veiculos automotores|motocicletas)|comercio de (pecas|veiculos|automoveis|motocicletas)|comercio por atacado|servicos de manutencao e reparacao mecanica de veiculos|lanternagem|funilaria|borracharia|lavagem, lubrificacao e polimento|reparacao de (pneumaticos|tanques|radiadores)|servicos de lanternagem|recauchutagem|comercio ambulante|representacao comercial', 'G'),
    # --- Agropecuária (A) ---
    (r'^cultivo|criacao de|producao de (mudas|sementes|lavouras)|apicultura|aquicultura|aqcultura|piscicultura|pesca|horticultura|floricultura|cultivo|producao florestal|extracao de (madeira|produtos nao-madeireiros|latex)|silvicultura|reflorestamento|servico de preparacao de terreno|atividades de apoio a (agricultura|pecuaria|producao florestal|aqicultura|aquicultura)|atividades de pos-colheita|atividades de apoio a aqicultura|criacao|coleta de produtos nao-madeireiros|carvao vegetal - florestas plantadas|producao de carvao vegetal - florestas plantadas', 'A'),
    # --- Extrativas (B) ---
    (r'extracao (de|e) |atividades de apoio a extracao|beneficiamento de minerio|beneficiamento de minerios|britamento de pedras|aparelhamento de pedras para construcao|extracao de sal|garimp', 'B'),
    # --- Eletricidade e gás (D) ---
    (r'geracao de energia|transmissao de energia|distribuicao de energia|comercio atacadista de energia|producao de gas|distribuicao de combustiveis gasosos|coordenacao e controle da operacao da geracao', 'D'),
    # --- Água, esgoto, resíduos (E) ---
    (r'captacao, tratamento e distribuicao de agua|distribuicao de agua por caminhoes|gestao de redes de esgoto|relacionadas a esgoto|coleta de residuos|tratamento e disposicao de residuos|recuperacao de materiais|descontaminacao|tratamento e disposicao|servicos de coleta|recuperacao de sucatas', 'E'),
    # --- Construção (F) ---
    (r'construcao de (edificios|rodovias|ferrovias|obras|redes|estacoes|instalacoes)|obras de |incorporacao de empreendimentos imobiliarios|instalacao e manutencao (eletrica|de sistemas)|instalacoes (hidraulicas|eletricas|de sistema|em construcao)|montagem de estruturas metalicas|demolicao|preparacao de canteiro|perfuracao e construcao de pocos|servicos especializados para construcao|obras portuarias|aplicacao de revestimentos e de resinas|impermeabilizacao em obras|instalacao de portas|servicos de pintura de edificios|administracao de obras|obras de acabamento|terraplenagem|servico de pintura de edificios', 'F'),
    # --- Transporte / correio (H) ---
    (r'transporte (rodoviario|ferroviario|aquaviario|aereo|dutoviario|maritimo|por navegacao)|armazenamento|armazens gerais|deposito de mercadorias|carga e descarga|operadores portuarios|gestao de portos|atividades auxiliares dos transportes|terminais rodoviarios|estacionamento de veiculos|correio nacional|atividades de correio|servicos de entrega|servicos de malote|agenciamento maritimo|despachantes aduaneiros|organizacao logistica do transporte|administracao da infra-estrutura portuaria|concessionarias de rodovias|transporte de valores|atividades de agenciamento maritimo|gestao de terminais aquaviarios|operacao dos aeroportos', 'H'),
    # --- Alojamento e alimentação (I) ---
    (r'hoteis|apart-hoteis|motéis|moteis|albergues|campings|pensoes \(alojamento\)|alojamento|restaurantes|lanchonetes|casas de cha|bares e outros|servicos ambulantes de alimentacao|fornecimento de alimentos preparados|cantinas|servicos de alimentacao para eventos|sorveterias|padaria e confeitaria com predominancia de revenda', 'I'),
    # --- Informação e comunicação (J) ---
    (r'edicao de|edicao integrada|producao cinematografica|pos-producao cinematografica|distribuicao cinematografica|exibicao cinematografica|gravacao de som|atividades de radio|atividades de televisao|televisao por assinatura|telecomunicacoes|operadoras de televisao|provedores de acesso|desenvolvimento (de programas|e licenciamento)|consultoria em tecnologia da informacao|suporte tecnico, manutencao e outros servicos em tecnologia|tratamento de dados|portais, provedores|agencias de noticias|servicos de telefonia|programadoras|reproducao de videos|reproducao de som|hospedagem na internet|servicos de comunicacao multimidia|web design', 'J'),
    # --- Financeiras e seguros (K) ---
    (r'bancos|caixas economicas|cooperativas de credito|agencias de fomento|sociedades de credito|arrendamento mercantil|cartoes de credito|fundos de investimento|corretoras|seguros|previdencia complementar|planos de saude|resseguros|atividades auxiliares dos servicos financeiros|administracao de fundos|corretores e agentes de seguros|peritos e avaliadores de seguros|auditoria e consultoria atuarial|holdings|caixas de financiamento|servicos de custodia|clubes de investimento|atividades de cobranca e informacoes cadastrais|bolsa de valores|gestao de ativos|correspondentes de instituicoes financeiras|planos de assistencia', 'K'),
    # --- Imobiliárias (L) ---
    (r'aluguel de imoveis proprios|corretagem na compra e venda|corretagem no aluguel|gestao e administracao da propriedade imobiliaria|compra e venda de imoveis proprios|imobiliari', 'L'),
    # --- Profissionais, científicas e técnicas (M) ---
    (r'atividades juridicas|cartorios|atividades de contabilidade|consultoria e auditoria contabil|consultoria em gestao empresarial|servicos de arquitetura|servicos de engenharia|atividades tecnicas relacionadas a (arquitetura|engenharia)|testes e analises tecnicas|pesquisa e desenvolvimento|agencias de publicidade|agenciamento de espacos para publicidade|marketing direto|consultoria em publicidade|pesquisas de mercado|design|atividades fotograficas|producao de fotografias|atividades veterinarias|atividades profissionais, cientificas e tecnicas nao especificadas|estudos geologicos|mapeamento|servicos de agronomia|servico de assessoria|atividades de intermediacao e agenciamento de servicos e negocios|atividades de publicidade nao especificadas|atividades de artistas plasticos, jornalistas independentes e escritores|atividades de sonorizacao e de iluminacao', 'M'),
    # --- Administrativas e serviços complementares (N) ---
    (r'aluguel de (maquinas|equipamentos|moveis|outros|palcos|andaimes|aparelhos|objetos|material|fitas|automoveis|embarcacoes|aeronaves|meios de transporte|veiculos)|locacao de (automoveis|mao-de-obra)|selecao e agenciamento de mao-de-obra|fornecimento e gestao de recursos humanos|agencias de viagens|operadores turisticos|servicos de reservas|vigilancia e seguranca privada|monitoramento de sistemas de seguranca|servicos de investigacao|limpeza em predios|imunizacao e controle de pragas|atividades paisagisticas|servicos combinados de escritorio|fotocopias|preparacao de documentos|atividades de teleatendimento|call center|organizacao de feiras|servicos de escritorio|atividades de cobranca|envasamento e empacotamento|atividades de servicos prestados principalmente as empresas|atividades de limpeza|servicos de organizacao de feiras|leiloeiros|apoio administrativo|gestao de ativos intangiveis|centros de contato|atividades de franqueadas', 'N'),
    # --- Administração pública (O) ---
    (r'administracao publica|seguridade social obrigatoria|defesa|justica|policia|regulacao das atividades|atividades auxiliares da justica|fiscalizacao profissional|servico publico', 'O'),
    # --- Educação (P) ---
    (r'educacao (infantil|de jovens|profissional|superior|pre-escola|fundamental|media)|ensino |escolas |cursos |atividades de apoio a educacao|treinamento em desenvolvimento profissional|educacao', 'P'),
    # --- Saúde e serviços sociais (Q) ---
    (r'atividade medica|atividade odontologica|atendimento hospitalar|pronto-socorro|atencao ambulatorial|servicos de (complementacao diagnostica|dialise|quimioterapia|radioterapia|hemoterapia|vacinacao|remocao de pacientes)|laboratorios (clinicos|de anatomia)|atividades de (enfermagem|fisioterapia|fonoaudiologia|psicologia|nutricao|terapia|podologia|praticas integrativas|assistencia social|assistencia psicossocial|profissionais da area de saude|centros de assistencia psicossocial|apoio a gestao de saude|fornecimento de infra-estrutura de apoio e assistencia a paciente)|assistencia social|atividades de atendimento|clinicas|banco de|condicionamento fisico|atividades de atencao|servicos de assistencia social|acolhimento|abrigo', 'Q'),
    # --- Artes, cultura, esporte e recreação (R) ---
    (r'artes cenicas|producao (teatral|musical|de espetaculos)|gestao de espacos para artes cenicas|atividades de museus|jardins botanicos|zoologicos|bibliotecas|arquivos|clubes sociais, esportivos|atividades de (organizacoes associativas ligadas a cultura|condicionamento)|gestao de instalacoes de esportes|exploracao de (jogos|apostas|boliche|bilhar)|parques de diversao|discotecas, danceterias|atividades esportivas|atividades de recreacao|atividades desportivas|artistica e cultural|atividades de exibicao|festas', 'R'),
    # --- Outras atividades de serviços (S) ---
    (r'atividades de organizacoes (religiosas|politicas|sindicais|associativas|patronais)|atividades associativas|associacoes de defesa de direitos|reparacao e manutencao de (computadores|equipamentos de comunicacao|objetos|calcados|moveis|eletrodomesticos)|cabeleireiros|atividades de estetica|lavanderias|tinturarias|toalheiros|servicos de somatoconservacao|funerarias|atividades funerarias|servicos de tatuagem|alojamento de animais domesticos|higiene e embelezamento de animais|servicos pessoais nao especificados|servicos de lavanderia|manutencao e reparacao de (equipamentos|maquinas) de uso pessoal|atividades de manutencao e reparacao|servicos domesticos|chaveiros|servicos de organizacoes|clinicas de estetica', 'S'),
    # --- Indústria de transformação (C) - amplo, deixar por último ---
    (r'fabricacao|abate|frigorifico|preparacao de|producao de (laticinios|derivados|oleo|acucar|biocombust|alcool|malte|cerveja|refrigerantes|artefatos)|moagem|torrefacao|beneficiamento de (arroz|cafe|trigo|castanha|sal)|laticinios|fiacao|tecelagem|confeccao|curtimento|serrarias|desdobramento de madeira|impressao|servicos de pre-impressao|acabamentos graficos|refino|producao de |metalurgia|siderurgia|fundicao|usinagem|tratamento e revestimento em metais|manutencao e reparacao de (maquinas|motores|equipamentos|aeronaves|embarcacoes|veiculos ferroviarios|tratores|geradores)|instalacao de maquinas|producao de artefatos|aparelhamento de placas|producao de joias|panificacao|padaria|producao de sucos|obtencao de|cortes de|producao grafica|servicos de usinagem|recondicionamento|montagem de moveis|producao de pecas', 'C'),
]

def classify(nome):
    n = norm(nome)
    for pat, sec in RULES:
        if re.search(pat, n):
            return sec
    return 'Z'

OVERRIDES = {
 'Aluguel de outras máquinas e equipamentos comerciais e industriais não especificados anteriormente, sem operador':'N',
 'Atividades de profissionais da nutrição':'Q','Casas lotéricas':'R',
 'Comércio sob consignação de motocicletas e motonetas':'G','Comércio sob consignação de veículos automotores':'G',
 'Condomínios prediais':'N','Estamparia e texturização em fios, tecidos, artefatos têxteis e peças do vestuário':'C',
 'Estúdios cinematográficos':'J','Exploração de máquinas de serviços pessoais acionadas por moeda':'S',
 'Facção de peças do vestuário, exceto roupas íntimas':'C','Facção de roupas profissionais':'C',
 'Formação de condutores':'P','Instalação de painéis publicitários':'M',
 'Instituições de longa permanência para idosos':'Q','Laboratórios fotográficos':'M','Lapidação de gemas':'C',
 'Locação de outros meios de transporte não especificados anteriormente, sem condutor':'N',
 'Lojas de departamentos ou magazines (Desativado)':'G','Lojas de departamentos ou magazines, exceto lojas francas (Duty free)':'G',
 'Lojas de variedades, exceto lojas de departamentos ou magazines':'G','Loteamento de imóveis próprios':'L',
 'Manutenção e reparação de aparelhos eletromédicos e eletroterapêuticos e equipamentos de irradiação':'C',
 'Manutenção e reparação de outras máquinas e equipamentos para usos industriais não especificados anteriormente':'C',
 'Montagem e desmontagem de andaimes e outras estruturas temporárias':'F',
 'Montagem e instalação de sistemas e equipamentos de iluminação e sinalização em vias públicas, portos e aeroportos':'F',
 'Operadoras de cartões de débito':'K','Orfanatos':'Q',
 'Organização de excursões em veículos rodoviários próprios, intermunicipal, interestadual e internacional':'H',
 'Outras atividades de prestação de serviços de informação não especificadas anteriormente':'J',
 'Outras atividades de serviços de segurança':'N','Outras atividades de serviços pessoais não especificadas anteriormente':'S',
 'Outros serviços de acabamento em fios, tecidos, artefatos têxteis e peças do vestuário':'C',
 'Peixaria':'G','Perfurações e sondagens':'F','Pintura para sinalização em pistas rodoviárias e aeroportos':'F',
 'Preservação de peixes, crustáceos e moluscos':'C','Produção e promoção de eventos esportivos':'R','Promoção de vendas':'M',
 'Provedores de voz sobre protocolo internet - VOIP':'J','Recarga de cartuchos para equipamentos de informática':'N',
 'Reforma de pneumáticos usados':'C','Reparação de artigos do mobiliário':'S','Reparação de bicicletas, triciclos e outros veículos não-motorizados':'S',
 'Reparação de calçados, bolsas e artigos de viagem':'S','Reparação de jóias':'S','Reparação de relógios':'S',
 'Reparação e manutenção de equipamentos eletroeletrônicos de uso pessoal e doméstico':'S',
 'Reparação e manutenção de outros objetos e equipamentos pessoais e domésticos não especificados anteriormente':'S',
 'Restauração e conservação de lugares e prédios históricos':'R','Salas de acesso à internet':'N','Securitização de créditos':'K',
 'Serviço de inseminação artificial em animais':'A','Serviço de laboratório óptico':'C','Serviço de manejo de animais':'A',
 'Serviço de pulverização e controle de pragas agrícolas':'A','Serviço de táxi aéreo e locação de aeronaves com tripulação':'H',
 'Serviço móvel especializado - SME':'J','Serviços advocatícios':'M','Serviços combinados para apoio a edifícios, exceto condomínios prediais':'N',
 'Serviços de alinhamento e balanceamento de veículos automotores':'G','Serviços de capotaria':'G',
 'Serviços de cartografia, topografia e geodésia':'M','Serviços de cremação':'S',
 'Serviços de desenho técnico relacionados à arquitetura e engenharia':'M',
 'Serviços de diagnóstico por imagem com uso de radiação ionizante, exceto tomografia':'Q',
 'Serviços de diagnóstico por imagem sem uso de radiação ionizante, exceto ressonância magnética':'Q',
 'Serviços de diagnóstico por métodos ópticos - endoscopia e outros exames análogos':'Q',
 'Serviços de diagnóstico por registro gráfico - ECG, EEG e outros exames análogos':'Q',
 'Serviços de encadernação e plastificação':'C',
 'Serviços de instalação, manutenção e reparação de acessórios para veículos automotores':'G',
 'Serviços de levantamento de fundos sob contrato':'N','Serviços de manutenção e reparação elétrica de veículos automotores':'G',
 'Serviços de operação e fornecimento de equipamentos para transporte e elevação de cargas e pessoas para uso em obras':'F',
 'Serviços de perícia técnica relacionados à segurança do trabalho':'M','Serviços de prótese dentária':'C',
 'Serviços de reboque de veículos':'H','Serviços de ressonância magnética':'Q','Serviços de sepultamento':'S',
 'Serviços de tomografia':'Q','Telefonia móvel celular':'J','Transporte escolar':'H',
 'Tratamentos térmicos, acústicos ou de vibração':'F','Treinamento em informática':'P','UTI móvel':'Q',
}

OVERRIDES.update({'Atividade médica ambulatorial com recursos para realização de exames complementares': 'Q', 'Atividade médica ambulatorial com recursos para realização de procedimentos cirúrgicos': 'Q', 'Atividade odontológica com recursos para realização de procedimentos cirúrgicos': 'Q', 'Atividade odontológica sem recursos para realização de procedimentos cirúrgicos': 'Q', 'Alojamento de animais domésticos': 'S', 'Alojamento, higiene e embelezamento de animais': 'S', 'Serviços de assistência social sem alojamento': 'Q', 'Preparação de canteiro e limpeza de terreno': 'F', 'Preparação de documentos e serviços especializados de apoio administrativo não especificados anteriormente': 'N', 'Produção de espetáculos de dança': 'R', 'Produção de filmes para publicidade': 'J', 'Produção de carvão vegetal - florestas nativas': 'A', 'Produção de carvão vegetal - florestas plantadas': 'A', 'Produção de mudas e outras formas de propagação vegetal, certificadas': 'A', 'Produção de ovos': 'A', 'Produção de pintos de um dia': 'A', 'Produção de sementes certificadas, exceto de forrageiras para pasto': 'A', 'Atividades de associações de defesa de direitos sociais': 'S', 'Atividades de atividades de fiscalização profissional': 'S', 'Manutenção e reparação de máquinas e equipamentos de terraplenagem, pavimentação e construção, exceto tratores': 'C', 'Filmagem de festas e eventos': 'M'})

def secao(nome):
    if nome in OVERRIDES: return OVERRIDES[nome]
    return classify(nome)
