package com.uninter.baozistore.controller;

import com.uninter.baozistore.model.Pedido;
import com.uninter.baozistore.repository.PedidoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {

    @Autowired
    private PedidoRepository pedidoRepository;

    // POST - Criar Pedido
    @PostMapping
    public ResponseEntity<Pedido> criar(@RequestBody Pedido pedido) {
        Pedido novoPedido = pedidoRepository.save(pedido);
        return ResponseEntity.status(HttpStatus.CREATED).body(novoPedido);
    }

    // GET - Listar todos os pedidos
    @GetMapping
    public ResponseEntity<List<Pedido>> listarTodos() {
        List<Pedido> lista = pedidoRepository.findAll();
        return ResponseEntity.ok(lista);
    }

    // GET /{id} - Consultar por ID
    @GetMapping("/{id}")
    public ResponseEntity<Pedido> consultarPorId(@PathVariable Long id) {
        return pedidoRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // DELETE /{id} - Apagar Pedido
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> apagar(@PathVariable Long id) {
        if (!pedidoRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        pedidoRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    // PUT /{id} - Atualizar Pedido (Endpoint opcional)
    @PutMapping("/{id}")
    public ResponseEntity<Pedido> atualizar(@PathVariable Long id, @RequestBody Pedido pedidoAtualizado) {
        return pedidoRepository.findById(id)
                .map(pedidoExistente -> {
                    pedidoExistente.setClienteId(pedidoAtualizado.getClienteId());
                    pedidoExistente.setProdutoId(pedidoAtualizado.getProdutoId());
                    pedidoExistente.setQuantidade(pedidoAtualizado.getQuantidade());
                    Pedido salvo = pedidoRepository.save(pedidoExistente);
                    return ResponseEntity.ok(salvo);
                })
                .orElse(ResponseEntity.notFound().build());
    }
}

