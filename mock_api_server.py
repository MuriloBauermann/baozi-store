import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import re

clientes = []
produtos = []
pedidos = []

next_cliente_id = 1
next_produto_id = 1
next_pedido_id = 1

class BaoziHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))

    def _send_empty(self, status):
        self.send_response(status)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self._send_empty(200)

    def do_GET(self):
        path = self.path.split('?')[0].rstrip('/')
        if not path:
            self._send_json(200, {"message": "Baozi Store API REST está ativa!", "aluno": "Murilo4425054"})
            return

        m_cli = re.match(r'^/clientes(?:/(\d+))?$', path)
        if m_cli:
            cid = m_cli.group(1)
            if cid:
                c = next((item for item in clientes if item["id"] == int(cid)), None)
                if c:
                    self._send_json(200, c)
                else:
                    self._send_empty(404)
            else:
                self._send_json(200, clientes)
            return

        m_prod = re.match(r'^/produtos(?:/(\d+))?$', path)
        if m_prod:
            pid = m_prod.group(1)
            if pid:
                p = next((item for item in produtos if item["id"] == int(pid)), None)
                if p:
                    self._send_json(200, p)
                else:
                    self._send_empty(404)
            else:
                self._send_json(200, produtos)
            return

        m_ped = re.match(r'^/pedidos(?:/(\d+))?$', path)
        if m_ped:
            ped_id = m_ped.group(1)
            if ped_id:
                ped = next((item for item in pedidos if item["id"] == int(ped_id)), None)
                if ped:
                    self._send_json(200, ped)
                else:
                    self._send_empty(404)
            else:
                self._send_json(200, pedidos)
            return

        self._send_empty(404)

    def do_POST(self):
        global next_cliente_id, next_produto_id, next_pedido_id
        path = self.path.split('?')[0].rstrip('/')
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        data = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}

        if path == '/clientes':
            data['id'] = next_cliente_id
            next_cliente_id += 1
            clientes.append(data)
            self._send_json(201, data)
            return

        if path == '/produtos':
            data['id'] = next_produto_id
            next_produto_id += 1
            produtos.append(data)
            self._send_json(201, data)
            return

        if path == '/pedidos':
            data['id'] = next_pedido_id
            next_pedido_id += 1
            pedidos.append(data)
            self._send_json(201, data)
            return

        self._send_empty(404)

    def do_DELETE(self):
        path = self.path.split('?')[0].rstrip('/')
        m_cli = re.match(r'^/clientes/(\d+)$', path)
        if m_cli:
            cid = int(m_cli.group(1))
            idx = next((i for i, item in enumerate(clientes) if item["id"] == cid), None)
            if idx is not None:
                clientes.pop(idx)
                self._send_empty(204)
            else:
                self._send_empty(404)
            return

        m_prod = re.match(r'^/produtos/(\d+)$', path)
        if m_prod:
            pid = int(m_prod.group(1))
            idx = next((i for i, item in enumerate(produtos) if item["id"] == pid), None)
            if idx is not None:
                produtos.pop(idx)
                self._send_empty(204)
            else:
                self._send_empty(404)
            return

        m_ped = re.match(r'^/pedidos/(\d+)$', path)
        if m_ped:
            ped_id = int(m_ped.group(1))
            idx = next((i for i, item in enumerate(pedidos) if item["id"] == ped_id), None)
            if idx is not None:
                pedidos.pop(idx)
                self._send_empty(204)
            else:
                self._send_empty(404)
            return

        self._send_empty(404)

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, BaoziHandler)
    print("Servidor Baozi Store ativo na porta 8080...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

