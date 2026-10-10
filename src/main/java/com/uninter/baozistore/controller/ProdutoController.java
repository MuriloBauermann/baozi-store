package com.uninter.baozistore.controller;

import com.uninter.baozistore.model.Produto;
import com.uninter.baozistore.repository.ProdutoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/produtos")
public class ProdutoController {

    @Autowired
    private ProdutoRepository produtoRepository;

    // POST - Criar Produto
    @PostMapping
    public ResponseEntity<Produto> criar(@RequestBody Produto produto) {
        Produto novoProduto = produtoRepository.save(produto);
        return ResponseEntity.status(HttpStatus.CREATED).body(novoProduto);
    }

    // GET - Listar todos os produtos
    @GetMapping
    public ResponseEntity<List<Produto>> listarTodos() {
        List<Produto> lista = produtoRepository.findAll();
        return ResponseEntity.ok(lista);
    }

    // GET /{id} - Consultar por ID
    @GetMapping("/{id}")
    public ResponseEntity<Produto> consultarPorId(@PathVariable Long id) {
        return produtoRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // DELETE /{id} - Apagar Produto
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> apagar(@PathVariable Long id) {
        if (!produtoRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        produtoRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }

    // PUT /{id} - Atualizar Produto (Endpoint opcional)
    @PutMapping("/{id}")
    public ResponseEntity<Produto> atualizar(@PathVariable Long id, @RequestBody Produto produtoAtualizado) {
        return produtoRepository.findById(id)
                .map(produtoExistente -> {
                    produtoExistente.setNome(produtoAtualizado.getNome());
                    produtoExistente.setPreco(produtoAtualizado.getPreco());
                    produtoExistente.setEstoque(produtoAtualizado.getEstoque());
                    Produto salvo = produtoRepository.save(produtoExistente);
                    return ResponseEntity.ok(salvo);
                })
                .orElse(ResponseEntity.notFound().build());
    }
}

