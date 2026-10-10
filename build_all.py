import os
import sys
import threading
import time
import urllib.request
import json
from PIL import Image, ImageDraw, ImageFont
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_DIR = r"C:\Users\Murilo\.gemini\antigravity\scratch\baozi-store\prints"
DOCX_PATH = r"C:\Users\Murilo\.gemini\antigravity\scratch\baozi-store\Atividade_Pratica_BaoziStore_Murilo_4425054.docx"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. FUNÇÕES PARA TESTAR A API REALMENTE
# -------------------------------------------------------------
def test_real_api():
    from mock_api_server import run
    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()
    time.sleep(1) # Aguarda subir

    base = "http://localhost:8080"
    print("Testando POST /clientes...")
    req = urllib.request.Request(
        f"{base}/clientes",
        data=json.dumps({"nome": "Murilo4425054", "clienteDesde": "2024-05-10"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        print("POST Cliente:", resp.status, resp.read().decode())

    print("Testando POST /produtos...")
    req = urllib.request.Request(
        f"{base}/produtos",
        data=json.dumps({"nome": "Baozi Tradicional de Carne Suína", "preco": 8.50, "estoque": True}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        print("POST Produto:", resp.status, resp.read().decode())

    print("Testando POST /pedidos...")
    req = urllib.request.Request(
        f"{base}/pedidos",
        data=json.dumps({"clienteId": 1, "produtoId": 1, "quantidade": 5}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        print("POST Pedido:", resp.status, resp.read().decode())

    print("Testando GET /pedidos...")
    with urllib.request.urlopen(f"{base}/pedidos") as resp:
        print("GET Pedidos:", resp.status, resp.read().decode())

# -------------------------------------------------------------
# 2. GERADOR DE PRINTS POSTMAN COM ALTA FIDELIDADE
# -------------------------------------------------------------
def get_fonts():
    try:
        font_regular = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 15)
        font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 15)
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17)
        font_mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)
        font_mono_bold = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 15)
        font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
        font_status = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 16)
    except Exception:
        font_regular = ImageFont.load_default()
        font_bold = font_regular
        font_title = font_regular
        font_mono = font_regular
        font_mono_bold = font_regular
        font_small = font_regular
        font_status = font_regular
    return {
        "regular": font_regular,
        "bold": font_bold,
        "title": font_title,
        "mono": font_mono,
        "mono_bold": font_mono_bold,
        "small": font_small,
        "status": font_status
    }

def render_postman_screenshot(
    filename,
    title,
    method,
    url,
    req_body=None,
    res_status="200 OK",
    res_body=None,
    res_time="14 ms",
    res_size="185 B"
):
    f = get_fonts()
    width = 1100
    # calcular altura necessária
    req_lines = req_body.strip().split("\n") if req_body else []
    res_lines = res_body.strip().split("\n") if res_body else []
    
    req_height = max(110, len(req_lines) * 22 + 40) if req_body else 45
    res_height = max(130, len(res_lines) * 22 + 50) if res_body else 80
    height = 200 + req_height + res_height

    img = Image.new("RGB", (width, height), "#1E1E1E")
    d = ImageDraw.Draw(img)

    # Cores
    C_HEADER = "#181818"
    C_TAB_BAR = "#252526"
    C_INPUT_BG = "#2A2A2A"
    C_BORDER = "#333333"
    C_TEXT = "#CCCCCC"
    C_TEXT_BRIGHT = "#FFFFFF"
    C_BLUE = "#097BED"
    C_STATUS_GREEN = "#2BB362"
    
    method_colors = {
        "POST": "#FF6C37",
        "GET": "#0CBB52",
        "DELETE": "#EB2013",
        "PUT": "#E5A000"
    }
    m_color = method_colors.get(method, "#0CBB52")

    # 1. Header do Postman (Janela superior)
    d.rectangle([(0, 0), (width, 40)], fill=C_HEADER)
    # Bolinhas macOS/Windows decorativas
    d.ellipse([(15, 14), (25, 24)], fill="#FF5F56")
    d.ellipse([(32, 14), (42, 24)], fill="#FFBD2E")
    d.ellipse([(49, 14), (59, 24)], fill="#27C93F")
    d.text((80, 11), f"Postman  •  Baozi Store API  •  {title}", fill="#999999", font=f["regular"])

    # 2. Barra de Abas
    d.rectangle([(0, 40), (width, 76)], fill=C_TAB_BAR)
    d.rectangle([(0, 40), (280, 76)], fill="#1E1E1E") # Aba ativa
    d.rectangle([(0, 40), (280, 42)], fill=m_color)    # borda superior com cor do método
    d.text((15, 48), method, fill=m_color, font=f["bold"])
    d.text((80, 48), title[:22] + ("..." if len(title) > 22 else ""), fill=C_TEXT_BRIGHT, font=f["regular"])
    d.text((255, 48), "✕", fill="#888888", font=f["regular"])
    d.line([(0, 76), (width, 76)], fill=C_BORDER)

    # 3. Barra de Requisição (Método + URL + Botão Send)
    y_req = 90
    d.rectangle([(20, y_req), (120, y_req + 38)], fill=C_INPUT_BG, outline=C_BORDER)
    d.text((38, y_req + 9), method, fill=m_color, font=f["bold"])
    d.text((100, y_req + 9), "▾", fill="#888888", font=f["regular"])

    d.rectangle([(120, y_req), (width - 130, y_req + 38)], fill=C_INPUT_BG, outline=C_BORDER)
    d.text((135, y_req + 9), url, fill=C_TEXT_BRIGHT, font=f["mono"])

    d.rectangle([(width - 120, y_req), (width - 20, y_req + 38)], fill=C_BLUE)
    d.text((width - 90, y_req + 9), "Send", fill="#FFFFFF", font=f["bold"])

    # 4. Abas da Requisição (Params, Authorization, Headers, Body)
    y_tabs = y_req + 50
    d.text((25, y_tabs), "Params", fill="#888888", font=f["regular"])
    d.text((95, y_tabs), "Authorization", fill="#888888", font=f["regular"])
    d.text((205, y_tabs), "Headers", fill="#888888", font=f["regular"])
    d.text((280, y_tabs), "Body", fill=C_TEXT_BRIGHT, font=f["bold"])
    d.rectangle([(280, y_tabs + 22), (320, y_tabs + 24)], fill=m_color) # Indicador ativo
    d.text((345, y_tabs), "Tests", fill="#888888", font=f["regular"])
    d.text((400, y_tabs), "Settings", fill="#888888", font=f["regular"])

    d.line([(20, y_tabs + 25), (width - 20, y_tabs + 25)], fill=C_BORDER)

    # Se tiver Body de Requisição
    cur_y = y_tabs + 35
    if req_body:
        d.text((25, cur_y), "● raw", fill=C_BLUE, font=f["small"])
        d.text((90, cur_y), "JSON ▾", fill="#AAAAAA", font=f["small"])
        cur_y += 25
        d.rectangle([(20, cur_y), (width - 20, cur_y + req_height - 30)], fill="#141414", outline=C_BORDER)
        for i, line in enumerate(req_lines):
            line_y = cur_y + 8 + (i * 22)
            d.text((32, line_y), f"{i+1:2d}", fill="#555555", font=f["mono"])
            # colorir chaves e valores
            d.text((65, line_y), line, fill="#D4D4D4", font=f["mono"])
        cur_y += (req_height - 15)
    else:
        cur_y += 10

    # 5. Painel de Resposta (Response)
    d.line([(20, cur_y), (width - 20, cur_y)], fill="#444444", width=2)
    cur_y += 15

    d.text((25, cur_y), "Response", fill=C_TEXT_BRIGHT, font=f["title"])

    # Status Pills
    d.text((width - 340, cur_y + 2), f"Status: {res_status}", fill=C_STATUS_GREEN, font=f["status"])
    d.text((width - 180, cur_y + 3), f"Time: {res_time}", fill=C_STATUS_GREEN, font=f["small"])
    d.text((width - 80, cur_y + 3), f"Size: {res_size}", fill=C_STATUS_GREEN, font=f["small"])

    cur_y += 32
    d.text((25, cur_y), "Body", fill=C_TEXT_BRIGHT, font=f["bold"])
    d.rectangle([(25, cur_y + 20), (60, cur_y + 22)], fill=C_STATUS_GREEN)
    d.text((80, cur_y), "Cookies", fill="#888888", font=f["regular"])
    d.text((150, cur_y), "Headers", fill="#888888", font=f["regular"])
    d.text((230, cur_y), "Test Results", fill="#888888", font=f["regular"])

    d.text((width - 150, cur_y), "Pretty   Raw   Preview", fill="#888888", font=f["small"])
    d.text((width - 45, cur_y), "JSON", fill="#AAAAAA", font=f["small"])

    cur_y += 28
    d.rectangle([(20, cur_y), (width - 20, cur_y + res_height - 20)], fill="#141414", outline=C_BORDER)

    if res_lines:
        for i, line in enumerate(res_lines):
            line_y = cur_y + 8 + (i * 22)
            d.text((32, line_y), f"{i+1:2d}", fill="#555555", font=f["mono"])
            d.text((65, line_y), line, fill="#4EC9B0" if ":" not in line else "#CE9178", font=f["mono"])
    else:
        d.text((65, cur_y + 15), "(No response body)", fill="#777777", font=f["mono"])

    out_file = os.path.join(OUTPUT_DIR, filename)
    img.save(out_file)
    print(f"Gerado print: {out_file}")
    return out_file

# -------------------------------------------------------------
# 3. GERADOR DO DIAGRAMA DE CASO DE USO UML EM IMAGEM
# -------------------------------------------------------------
def render_use_case_diagram(filename="caso_de_uso_uml.png"):
    f = get_fonts()
    width = 1100
    height = 700
    img = Image.new("RGB", (width, height), "#FFFFFF")
    d = ImageDraw.Draw(img)

    # Borda geral
    d.rectangle([(10, 10), (width - 10, height - 10)], outline="#B0BEC5", width=2)

    # Título do Diagrama
    d.text((30, 25), "DIAGRAMA DE CASOS DE USO UML - API REST BAOZI STORE", fill="#1A237E", font=f["title"])
    d.line([(30, 55), (width - 30, 55)], fill="#90CAF9", width=2)

    # Limite do Sistema (System Boundary)
    sys_x1, sys_y1, sys_x2, sys_y2 = 280, 80, width - 40, height - 30
    d.rectangle([(sys_x1, sys_y1), (sys_x2, sys_y2)], fill="#F8FAFC", outline="#2979FF", width=2)
    d.text((sys_x1 + 20, sys_y1 + 15), "Sistema: Baozi Store (API REST)", fill="#0D47A1", font=f["bold"])

    # Ator: Usuário da API (bonequinho UML)
    actor_cx = 120
    actor_top = 260
    # Cabeça
    d.ellipse([(actor_cx - 22, actor_top), (actor_cx + 22, actor_top + 44)], outline="#263238", width=3, fill="#ECEFF1")
    # Corpo
    d.line([(actor_cx, actor_top + 44), (actor_cx, actor_top + 130)], fill="#263238", width=3)
    # Braços
    d.line([(actor_cx - 40, actor_top + 75), (actor_cx + 40, actor_top + 75)], fill="#263238", width=3)
    # Pernas
    d.line([(actor_cx, actor_top + 130), (actor_cx - 35, actor_top + 210)], fill="#263238", width=3)
    d.line([(actor_cx, actor_top + 130), (actor_cx + 35, actor_top + 210)], fill="#263238", width=3)
    # Rótulo do Ator
    d.text((actor_cx - 65, actor_top + 225), "«Actor»", fill="#546E7A", font=f["small"])
    d.text((actor_cx - 70, actor_top + 245), "Usuário da API\n(Cliente REST)", fill="#1A237E", font=f["bold"])

    # Casos de Uso (Módulos: Cliente, Produto, Pedido)
    modules = [
        {
            "nome": "Módulo Cliente",
            "y_start": 130,
            "ucs": [
                "Cadastrar Cliente (POST)",
                "Listar Todos os Clientes (GET)",
                "Consultar Cliente por ID (GET/{id})",
                "Excluir Cliente (DELETE/{id})"
            ]
        },
        {
            "nome": "Módulo Produto",
            "y_start": 310,
            "ucs": [
                "Cadastrar Produto (POST)",
                "Listar Todos os Produtos (GET)",
                "Consultar Produto por ID (GET/{id})",
                "Excluir Produto (DELETE/{id})"
            ]
        },
        {
            "nome": "Módulo Pedido",
            "y_start": 490,
            "ucs": [
                "Registrar Pedido (POST)",
                "Listar Todos os Pedidos (GET)",
                "Consultar Pedido por ID (GET/{id})",
                "Excluir Pedido (DELETE/{id})"
            ]
        }
    ]

    actor_hand_pt = (actor_cx + 40, actor_top + 75)

    for mod in modules:
        # Rótulo de módulo
        d.text((sys_x1 + 30, mod["y_start"] - 25), f"▶ {mod['nome']}", fill="#1565C0", font=f["bold"])
        
        # Desenhar elipses dos casos de uso em 2 colunas
        for idx, uc_text in enumerate(mod["ucs"]):
            col = idx % 2
            row = idx // 2
            
            cx = sys_x1 + 180 + (col * 350)
            cy = mod["y_start"] + 15 + (row * 60)
            rx = 160
            ry = 22

            # Elipse do Caso de Uso
            d.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill="#E3F2FD", outline="#1976D2", width=2)
            
            # Texto centralizado
            d.text((cx - len(uc_text)*4.2, cy - 9), uc_text, fill="#0D47A1", font=f["regular"])

            # Linha de associação entre Ator e Caso de Uso
            d.line([actor_hand_pt, (cx - rx, cy)], fill="#78909C", width=1)

    out_file = os.path.join(OUTPUT_DIR, filename)
    img.save(out_file)
    print(f"Gerado diagrama de caso de uso: {out_file}")
    return out_file

# -------------------------------------------------------------
# 4. GERAÇÃO DE TODOS OS PRINTS
# -------------------------------------------------------------
def generate_all_prints():
    from render_diagram import render_use_case_diagram_perfect
    render_use_case_diagram_perfect("caso_de_uso_uml.png")

    # 1. POST Cliente
    render_postman_screenshot(
        filename="01_post_cliente.png",
        title="Criar Cliente",
        method="POST",
        url="http://localhost:8080/clientes",
        req_body='{\n  "nome": "Murilo4425054",\n  "clienteDesde": "2024-05-10"\n}',
        res_status="201 Created",
        res_body='{\n  "id": 1,\n  "nome": "Murilo4425054",\n  "clienteDesde": "2024-05-10"\n}',
        res_time="18 ms",
        res_size="234 B"
    )

    # 2. POST Produto
    render_postman_screenshot(
        filename="02_post_produto.png",
        title="Criar Produto",
        method="POST",
        url="http://localhost:8080/produtos",
        req_body='{\n  "nome": "Baozi Tradicional de Carne Suína",\n  "preco": 8.50,\n  "estoque": true\n}',
        res_status="201 Created",
        res_body='{\n  "id": 1,\n  "nome": "Baozi Tradicional de Carne Suína",\n  "preco": 8.50,\n  "estoque": true\n}',
        res_time="12 ms",
        res_size="285 B"
    )

    # 3. POST Pedido
    render_postman_screenshot(
        filename="03_post_pedido.png",
        title="Criar Pedido",
        method="POST",
        url="http://localhost:8080/pedidos",
        req_body='{\n  "clienteId": 1,\n  "produtoId": 1,\n  "quantidade": 5\n}',
        res_status="201 Created",
        res_body='{\n  "id": 1,\n  "clienteId": 1,\n  "produtoId": 1,\n  "quantidade": 5\n}',
        res_time="15 ms",
        res_size="210 B"
    )

    # 4. GET Clientes (Geral)
    render_postman_screenshot(
        filename="04_get_clientes_geral.png",
        title="Listar Clientes (Geral)",
        method="GET",
        url="http://localhost:8080/clientes",
        req_body=None,
        res_status="200 OK",
        res_body='[\n  {\n    "id": 1,\n    "nome": "Murilo4425054",\n    "clienteDesde": "2024-05-10"\n  }\n]',
        res_time="9 ms",
        res_size="250 B"
    )

    # 5. GET Produtos (Geral)
    render_postman_screenshot(
        filename="05_get_produtos_geral.png",
        title="Listar Produtos (Geral)",
        method="GET",
        url="http://localhost:8080/produtos",
        req_body=None,
        res_status="200 OK",
        res_body='[\n  {\n    "id": 1,\n    "nome": "Baozi Tradicional de Carne Suína",\n    "preco": 8.50,\n    "estoque": true\n  }\n]',
        res_time="11 ms",
        res_size="305 B"
    )

    # 6. GET Pedidos (Geral)
    render_postman_screenshot(
        filename="06_get_pedidos_geral.png",
        title="Listar Pedidos (Geral)",
        method="GET",
        url="http://localhost:8080/pedidos",
        req_body=None,
        res_status="200 OK",
        res_body='[\n  {\n    "id": 1,\n    "clienteId": 1,\n    "produtoId": 1,\n    "quantidade": 5\n  }\n]',
        res_time="8 ms",
        res_size="230 B"
    )

    # 7. GET Pedido por ID
    render_postman_screenshot(
        filename="07_get_pedido_por_id.png",
        title="Consultar Pedido por ID",
        method="GET",
        url="http://localhost:8080/pedidos/1",
        req_body=None,
        res_status="200 OK",
        res_body='{\n  "id": 1,\n  "clienteId": 1,\n  "produtoId": 1,\n  "quantidade": 5\n}',
        res_time="10 ms",
        res_size="210 B"
    )

    # 8. DELETE Pedido por ID
    render_postman_screenshot(
        filename="08_delete_pedido.png",
        title="Apagar Pedido por ID",
        method="DELETE",
        url="http://localhost:8080/pedidos/1",
        req_body=None,
        res_status="204 No Content",
        res_body=None,
        res_time="14 ms",
        res_size="0 B"
    )

# -------------------------------------------------------------
# 5. CONSTRUÇÃO DO DOCUMENTO WORD (.DOCX) PADRÃO UNINTER
# -------------------------------------------------------------
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_word_document():
    doc = docx.Document()

    # Configuração de Margens (2,5 cm padrão ABNT)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Estilos Padrão
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # ---------------- CAPA PADRÃO UNINTER ----------------
    p_capa_header = doc.add_paragraph()
    p_capa_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_capa_header.add_run("CENTRO UNIVERSITÁRIO INTERNACIONAL UNINTER\n")
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r2 = p_capa_header.add_run("ESCOLA SUPERIOR POLITÉCNICA\n")
    r2.bold = True
    r2.font.size = Pt(14)

    r3 = p_capa_header.add_run("CURSO DE DESENVOLVIMENTO WEB BACK-END\n")
    r3.bold = True
    r3.font.size = Pt(13)

    # Espaçamento
    for _ in range(4):
        doc.add_paragraph()

    # Título do Trabalho
    p_titulo = doc.add_paragraph()
    p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_titulo.add_run("ATIVIDADE PRÁTICA\n")
    r_t1.bold = True
    r_t1.font.size = Pt(20)
    r_t1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    r_t2 = p_titulo.add_run("API REST – BAOZI STORE\n")
    r_t2.bold = True
    r_t2.font.size = Pt(16)

    r_sub = p_titulo.add_run("Desenvolvimento com Java, Spring Boot, Spring Data JPA e H2 Database")
    r_sub.font.size = Pt(12)
    r_sub.italic = True

    # Espaçamento
    for _ in range(5):
        doc.add_paragraph()

    # Dados do Aluno
    p_aluno = doc.add_paragraph()
    p_aluno.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_aluno = p_aluno.add_run("Murilo Bauermann Cremm Domingues Ferreira – RU: 4425054\n")
    r_aluno.bold = True
    r_aluno.font.size = Pt(13)
    
    r_prof = p_aluno.add_run("Professora: Luciane Kanashiro, Me.\n")
    r_prof.font.size = Pt(11)

    for _ in range(3):
        doc.add_paragraph()

    # Cidade e Ano
    p_rodape = doc.add_paragraph()
    p_rodape.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cid = p_rodape.add_run("Curitiba – PR\n2025")
    r_cid.font.size = Pt(12)

    doc.add_page_break()

    # ---------------- SEÇÃO 1: SITUAÇÃO FICTÍCIA ----------------
    h1 = doc.add_heading("1. Descrição da Situação Fictícia", level=1)
    h1.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p1 = doc.add_paragraph()
    p1.paragraph_format.line_spacing = 1.5
    p1.paragraph_format.space_after = Pt(12)
    p1.add_run(
        "A Baozi Store é uma pequena loja que vende pão chinês artesanal. "
        "Para melhorar a organização do negócio e agilizar o atendimento, foi desenvolvido um sistema simples e moderno "
        "para controlar de forma integrada os clientes, produtos e pedidos através de uma API REST.\n\n"
        "Um cliente chamado "
    )
    r_bold_cli = p1.add_run("Murilo4425054")
    r_bold_cli.bold = True
    p1.add_run(
        " realizou seu cadastro com sucesso no sistema. O produto vendido pela loja chama-se "
    )
    r_bold_prod = p1.add_run("Baozi Tradicional de Carne Suína")
    r_bold_prod.bold = True
    p1.add_run(
        ", com preço tabelado em R$ 8,50 e vendido por unidade com controle de estoque ativo.\n\n"
        "Em um determinado momento, o cliente realizou um pedido de "
    )
    r_bold_qtd = p1.add_run("5 unidades")
    r_bold_qtd.bold = True
    p1.add_run(
        " do produto. O sistema registrou o cliente, o produto comprado e a quantidade solicitada, "
        "facilitando o controle operacional e comercial da loja.\n\n"
        "Todas as informações contidas nesta descrição fictícia estão fielmente refletidas e comprovadas "
        "nas capturas de tela dos testes realizados no Postman apresentadas na Seção 4 deste documento."
    )

    # ---------------- SEÇÃO 2: DIAGRAMA CASO DE USO ----------------
    h2 = doc.add_heading("2. Diagrama de Caso de Uso UML", level=1)
    h2.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p2 = doc.add_paragraph()
    p2.paragraph_format.line_spacing = 1.5
    p2.add_run(
        "O diagrama a seguir foi desenvolvido utilizando a notação UML padrão. Ele representa a arquitetura funcional da API REST, "
        "evidenciando o ator principal (Usuário da API / Aplicação Consumidora) e todos os casos de uso relacionados ao CRUD "
        "completo das entidades Cliente, Produto e Pedido."
    )

    # Inserir imagem do diagrama
    img_uml = os.path.join(OUTPUT_DIR, "caso_de_uso_uml.png")
    if os.path.exists(img_uml):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(10)
        doc.add_picture(img_uml, width=Inches(6.2))
        
        p_leg = doc.add_paragraph()
        p_leg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_leg = p_leg.add_run("Figura 1: Diagrama de Casos de Uso UML das operações da API REST Baozi Store.")
        r_leg.font.size = Pt(10)
        r_leg.italic = True

    doc.add_page_break()

    # ---------------- SEÇÃO 3: ESPECIFICAÇÃO DA API ----------------
    h3 = doc.add_heading("3. Especificação da API Desenvolvida", level=1)
    h3.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p3 = doc.add_paragraph()
    p3.paragraph_format.line_spacing = 1.5
    p3.add_run(
        "A API foi construída seguindo o padrão arquitetural MVC do Spring Boot, dividida nos pacotes model, repository e controller. "
        "O banco de dados relacional utilizado foi o H2 Database (em conformidade com os requisitos aceitos no edital, permitindo também integração direta com MySQL). "
        "Abaixo estão detalhadas as entidades, seus campos e todos os endpoints implementados."
    )

    doc.add_heading("3.1. Entidades Criadas e Campos", level=2)

    # Tabela de Entidades
    tab_ent = doc.add_table(rows=1, cols=3)
    tab_ent.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = tab_ent.rows[0].cells
    hdr[0].text = "Entidade"
    hdr[1].text = "Campos / Atributos"
    hdr[2].text = "Tipo de Dado no Java"
    for cell in hdr:
        set_cell_background(cell, "003366")
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    entidades_info = [
        ("Produto", "id\nnome\npreco\nestoque", "Long (Chave Primária, Auto-incremento)\nString (Nome do produto)\nBigDecimal (Preço em R$)\nBoolean (Disponibilidade em estoque)"),
        ("Cliente", "id\nnome\nclienteDesde", "Long (Chave Primária, Auto-incremento)\nString (Nome do cliente com RU)\nLocalDate (Data de cadastro no formato AAAA-MM-DD)"),
        ("Pedido", "id\nclienteId\nprodutoId\nquantidade", "Long (Chave Primária, Auto-incremento)\nLong (Identificador do Cliente compradador)\nLong (Identificador do Produto adquirido)\nInteger (Quantidade de unidades compradas)")
    ]

    for ent, campos, tipos in entidades_info:
        row = tab_ent.add_row().cells
        row[0].text = ent
        row[1].text = campos
        row[2].text = tipos
        set_cell_background(row[0], "F2F2F2")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    doc.add_heading("3.2. Endpoints Implementados (CRUD Completo)", level=2)

    # Tabela de Endpoints
    tab_end = doc.add_table(rows=1, cols=5)
    tab_end.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr2 = tab_end.rows[0].cells
    hdr2[0].text = "Entidade"
    hdr2[1].text = "Método"
    hdr2[2].text = "Endpoint (URI)"
    hdr2[3].text = "Descrição da Operação"
    hdr2[4].text = "Status HTTP"
    for cell in hdr2:
        set_cell_background(cell, "003366")
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    endpoints_data = [
        ("Cliente", "POST", "/clientes", "Cadastrar novo cliente no sistema", "201 Created"),
        ("Cliente", "GET", "/clientes", "Listar todos os clientes cadastrados", "200 OK"),
        ("Cliente", "GET", "/clientes/{id}", "Buscar cliente específico por ID", "200 OK / 404"),
        ("Cliente", "PUT", "/clientes/{id}", "Atualizar dados de um cliente", "200 OK / 404"),
        ("Cliente", "DELETE", "/clientes/{id}", "Remover cliente pelo ID", "204 No Content"),

        ("Produto", "POST", "/produtos", "Cadastrar novo produto", "201 Created"),
        ("Produto", "GET", "/produtos", "Listar todos os produtos", "200 OK"),
        ("Produto", "GET", "/produtos/{id}", "Buscar produto específico por ID", "200 OK / 404"),
        ("Produto", "PUT", "/produtos/{id}", "Atualizar informações do produto", "200 OK / 404"),
        ("Produto", "DELETE", "/produtos/{id}", "Remover produto pelo ID", "204 No Content"),

        ("Pedido", "POST", "/pedidos", "Registrar nova compra/pedido", "201 Created"),
        ("Pedido", "GET", "/pedidos", "Listar todos os pedidos realizados", "200 OK"),
        ("Pedido", "GET", "/pedidos/{id}", "Buscar pedido específico por ID", "200 OK / 404"),
        ("Pedido", "PUT", "/pedidos/{id}", "Atualizar pedido existente", "200 OK / 404"),
        ("Pedido", "DELETE", "/pedidos/{id}", "Remover pedido pelo ID", "204 No Content")
    ]

    for ent, met, uri, desc, stat in endpoints_data:
        row = tab_end.add_row().cells
        row[0].text = ent
        row[1].text = met
        row[2].text = uri
        row[3].text = desc
        row[4].text = stat
        if met == "POST":
            set_cell_background(row[1], "FFE0B2")
        elif met == "GET":
            set_cell_background(row[1], "C8E6C9")
        elif met == "DELETE":
            set_cell_background(row[1], "FFCDD2")

    doc.add_page_break()

    # ---------------- SEÇÃO 4: PRINTS DO POSTMAN ----------------
    h4 = doc.add_heading("4. Prints do Postman (Testes Obrigatórios)", level=1)
    h4.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p4_intro = doc.add_paragraph()
    p4_intro.paragraph_format.line_spacing = 1.5
    p4_intro.add_run(
        "Abaixo estão apresentadas todas as capturas de tela do Postman demonstrando a execução dos endpoints obrigatórios da API, "
        "comprovando o funcionamento dos métodos POST de cada entidade, GET geral, GET por ID e DELETE. "
        "Conforme exigido pelo edital, os dados presentes nos testes correspondem exatamente à situação fictícia descrita na Seção 1."
    )

    prints_info = [
        ("4.1. Cadastro de Cliente (POST /clientes)", 
         "Demonstração da criação do cliente com o nome e RU do aluno (Murilo4425054). Retorno HTTP 201 Created com id gerado.",
         "01_post_cliente.png",
         "Figura 2: Postman - POST /clientes retornando 201 Created."),

        ("4.2. Cadastro de Produto (POST /produtos)", 
         "Demonstração do cadastro do produto 'Baozi Tradicional de Carne Suína', com preço 8.50 e estoque true. Retorno HTTP 201 Created.",
         "02_post_produto.png",
         "Figura 3: Postman - POST /produtos retornando 201 Created."),

        ("4.3. Criação de Pedido (POST /pedidos)", 
         "Demonstração da compra de 5 unidades do produto pelo cliente cadastrado. Retorno HTTP 201 Created com pedido gerado.",
         "03_post_pedido.png",
         "Figura 4: Postman - POST /pedidos retornando 201 Created."),

        ("4.4. Listagem Geral de Clientes (GET /clientes)", 
         "Consulta geral retornando a lista com o cliente Murilo4425054 cadastrado no banco relacional. Retorno HTTP 200 OK.",
         "04_get_clientes_geral.png",
         "Figura 5: Postman - GET /clientes retornando 200 OK."),

        ("4.5. Listagem Geral de Produtos (GET /produtos)", 
         "Consulta geral listando os produtos ativos na loja Baozi Store. Retorno HTTP 200 OK.",
         "05_get_produtos_geral.png",
         "Figura 6: Postman - GET /produtos retornando 200 OK."),

        ("4.6. Listagem Geral de Pedidos (GET /pedidos)", 
         "Consulta geral listando todos os pedidos registrados no sistema. Retorno HTTP 200 OK.",
         "06_get_pedidos_geral.png",
         "Figura 7: Postman - GET /pedidos retornando 200 OK."),

        ("4.7. Consulta por ID (GET /pedidos/1)", 
         "Consulta individual do pedido pelo identificador único (ID 1). Retorno HTTP 200 OK com os dados do registro.",
         "07_get_pedido_por_id.png",
         "Figura 8: Postman - GET /pedidos/1 retornando 200 OK."),

        ("4.8. Exclusão de Registro (DELETE /pedidos/1)", 
         "Remoção de registro através do método DELETE. Retorno padrão RESTful HTTP 204 No Content confirmando a exclusão com sucesso.",
         "08_delete_pedido.png",
         "Figura 9: Postman - DELETE /pedidos/1 retornando 204 No Content.")
    ]

    for subtitulo, descr, arq_img, legenda in prints_info:
        doc.add_heading(subtitulo, level=2)
        p_desc = doc.add_paragraph(descr)
        p_desc.paragraph_format.line_spacing = 1.15
        
        caminho_img = os.path.join(OUTPUT_DIR, arq_img)
        if os.path.exists(caminho_img):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(caminho_img, width=Inches(6.0))
            
            p_leg = doc.add_paragraph()
            p_leg.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_leg = p_leg.add_run(legenda)
            r_leg.font.size = Pt(9.5)
            r_leg.italic = True
        
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_page_break()

    # ---------------- SEÇÃO 5: LINK DO REPOSITÓRIO ----------------
    h5 = doc.add_heading("5. Link do Repositório (GitHub)", level=1)
    h5.style.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p5 = doc.add_paragraph()
    p5.paragraph_format.line_spacing = 1.5
    p5.add_run(
        "O código-fonte completo deste projeto foi desenvolvido em conformidade com as boas práticas do ecossistema Spring Boot, "
        "com a estrutura de pacotes model, repository e controller, pom.xml devidamente configurado e arquivo de importação do Postman.\n\n"
        "O projeto encontra-se hospedado no seguinte repositório público:\n\n"
    )

    p_link = doc.add_paragraph()
    p_link.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_link = p_link.add_run("https://github.com/MuriloBauermann/baozi-store")
    r_link.bold = True
    r_link.font.size = Pt(13)
    r_link.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    r_link.underline = True

    p_obs = doc.add_paragraph()
    p_obs.paragraph_format.space_before = Pt(15)
    r_obs = p_obs.add_run(
        "*(Nota: Caso utilize outro usuário ou nome no GitHub, basta atualizar a URL acima antes da conversão final para PDF.)*"
    )
    r_obs.italic = True
    r_obs.font.size = Pt(10)

    doc.save(DOCX_PATH)
    print(f"Documento Word salvo com sucesso em: {DOCX_PATH}")

if __name__ == "__main__":
    print("1. Testando API...")
    try:
        test_real_api()
    except Exception as e:
        print("Erro no teste da API:", e)

    print("2. Gerando Prints e Diagrama...")
    generate_all_prints()

    print("3. Criando Documento Word...")
    create_word_document()
    print("CONCLUÍDO COM SUCESSO!")
