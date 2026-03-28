from pydantic import BaseModel
from datetime import date


class PedidoCriar(BaseModel):
    nome_cliente: str
    itens: str
    valor_total: float


class PedidoRetorno(BaseModel):
    id: str
    nome_cliente: str
    itens: str
    valor_total: float
    status_do_pedido: str
    data_do_pedido: date

    
    class Config:
        from_attributes = True
    