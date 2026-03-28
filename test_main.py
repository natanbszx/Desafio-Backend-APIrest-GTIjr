from fastapi.testclient import TestClient
from main import app


client = TestClient(app)



def test_criar_pedido_com_sucesso():
    payload = {
        "nome_cliente": "Cliente Teste Automatizado",
        "itens": "1x Hambúrguer de Teste, 1x Refrigerante",
        "valor_total": 45.90
    }
    
    response = client.post("/pedidos/", json=payload)
    
    assert response.status_code == 200
    
    pedido_criado = response.json()
    
    
    assert pedido_criado["nome_cliente"] == payload["nome_cliente"]
    assert pedido_criado["valor_total"] == payload["valor_total"]
    

    assert "id" in pedido_criado
    assert pedido_criado["status_do_pedido"] == "Pendente"


def test_rota_listar_pedidos_obedece_a_paginacao():
    
    response = client.get("/pedidos/?skip=0&limit=2")
    
    assert response.status_code == 200
    pedidos = response.json()
    
    
    assert isinstance(pedidos, list)
    

    assert len(pedidos) <= 2