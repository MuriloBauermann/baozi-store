import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\Murilo\.gemini\antigravity\scratch\baozi-store\prints"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_use_case_diagram_perfect(filename="caso_de_uso_uml.png"):
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
    font_mod = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 15)
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 13)
    font_uc = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 12)

    width = 1200
    height = 920
    img = Image.new("RGB", (width, height), "#FFFFFF")
    d = ImageDraw.Draw(img)

    # Borda externa
    d.rectangle([(15, 15), (width - 15, height - 15)], outline="#B0BEC5", width=2)

    # Título do Diagrama
    d.text((40, 30), "DIAGRAMA DE CASOS DE USO UML - API REST BAOZI STORE", fill="#003366", font=font_title)
    d.line([(40, 65), (width - 40, 65)], fill="#003366", width=2)

    # Limite do Sistema (System Boundary)
    sys_x1, sys_y1, sys_x2, sys_y2 = 300, 85, width - 35, height - 30
    d.rectangle([(sys_x1, sys_y1), (sys_x2, sys_y2)], fill="#F8FAFC", outline="#1976D2", width=2)
    
    # Cabeçalho do Sistema
    d.rectangle([(sys_x1, sys_y1), (sys_x1 + 320, sys_y1 + 35)], fill="#1976D2")
    d.text((sys_x1 + 15, sys_y1 + 8), "Sistema: Baozi Store API REST", fill="#FFFFFF", font=font_mod)

    # Ator: Usuário da API (boneco UML)
    actor_cx = 140
    actor_top = 370
    
    # Cabeça
    d.ellipse([(actor_cx - 25, actor_top), (actor_cx + 25, actor_top + 50)], outline="#263238", width=3, fill="#ECEFF1")
    # Tronco
    d.line([(actor_cx, actor_top + 50), (actor_cx, actor_top + 150)], fill="#263238", width=3)
    # Braços
    d.line([(actor_cx - 45, actor_top + 85), (actor_cx + 45, actor_top + 85)], fill="#263238", width=3)
    # Pernas
    d.line([(actor_cx, actor_top + 150), (actor_cx - 40, actor_top + 240)], fill="#263238", width=3)
    d.line([(actor_cx, actor_top + 150), (actor_cx + 40, actor_top + 240)], fill="#263238", width=3)
    # Legenda do Ator
    d.text((actor_cx - 30, actor_top + 255), "«actor»", fill="#546E7A", font=font_small)
    bbox_act = font_bold.getbbox("Usuário da API")
    d.text((actor_cx - (bbox_act[2] - bbox_act[0]) // 2, actor_top + 275), "Usuário da API", fill="#003366", font=font_bold)
    bbox_sub = font_small.getbbox("(Postman / Cliente REST)")
    d.text((actor_cx - (bbox_sub[2] - bbox_sub[0]) // 2, actor_top + 295), "(Postman / Cliente REST)", fill="#546E7A", font=font_small)

    actor_hand = (actor_cx + 45, actor_top + 85)

    # Três blocos funcionais (Cliente, Produto, Pedido)
    secoes = [
        {
            "titulo": "1. MÓDULO CLIENTE",
            "y": 140,
            "cor": "#E3F2FD",
            "borda": "#1565C0",
            "ucs": [
                "Cadastrar Cliente (POST)",
                "Listar Todos os Clientes (GET)",
                "Consultar Cliente por ID (GET/{id})",
                "Excluir Cliente (DELETE/{id})"
            ]
        },
        {
            "titulo": "2. MÓDULO PRODUTO",
            "y": 390,
            "cor": "#E8F5E9",
            "borda": "#2E7D32",
            "ucs": [
                "Cadastrar Produto (POST)",
                "Listar Todos os Produtos (GET)",
                "Consultar Produto por ID (GET/{id})",
                "Excluir Produto (DELETE/{id})"
            ]
        },
        {
            "titulo": "3. MÓDULO PEDIDO",
            "y": 640,
            "cor": "#FFF3E0",
            "borda": "#E65100",
            "ucs": [
                "Registrar Pedido (POST)",
                "Listar Todos os Pedidos (GET)",
                "Consultar Pedido por ID (GET/{id})",
                "Excluir Pedido (DELETE/{id})"
            ]
        }
    ]

    for sec in secoes:
        sy = sec["y"]
        # Caixa de fundo do módulo
        d.rectangle([(sys_x1 + 15, sy), (sys_x2 - 15, sy + 225)], fill="#FFFFFF", outline="#CFD8DC", width=1)
        # Faixa do módulo
        d.rectangle([(sys_x1 + 25, sy - 12), (sys_x1 + 220, sy + 14)], fill=sec["borda"])
        d.text((sys_x1 + 35, sy - 10), sec["titulo"], fill="#FFFFFF", font=font_bold)

        # 4 Casos de Uso em 2 colunas dentro de cada módulo
        col1_x = sys_x1 + 210
        col2_x = sys_x1 + 610

        posicoes = [
            (col1_x, sy + 65),
            (col2_x, sy + 65),
            (col1_x, sy + 155),
            (col2_x, sy + 155)
        ]

        rx, ry = 175, 26
        for i, text in enumerate(sec["ucs"]):
            cx, cy = posicoes[i]
            # Desenha elipse UML
            d.ellipse([(cx - rx, cy - ry), (cx + rx, cy + ry)], fill=sec["cor"], outline=sec["borda"], width=2)
            
            # Centraliza o texto
            bbox = font_uc.getbbox(text)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            d.text((cx - tw // 2, cy - th // 2 - 2), text, fill="#1A237E", font=font_uc)

            # Linha de comunicação do Ator com o caso de uso
            # Para col1, liga diretamente na borda esquerda da elipse
            if i % 2 == 0:
                ponto_elipse = (cx - rx, cy)
                d.line([actor_hand, ponto_elipse], fill="#78909C", width=1)
            else:
                # Para col2, conecta a partir da elipse da esquerda correspondente
                cx_col1 = col1_x
                d.line([(cx_col1 + rx, cy), (cx - rx, cy)], fill="#B0BEC5", width=1)

    out_file = os.path.join(OUTPUT_DIR, filename)
    img.save(out_file)
    print("Salvo diagrama aprimorado:", out_file)

if __name__ == "__main__":
    render_use_case_diagram_perfect()

