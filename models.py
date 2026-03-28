from sqlalchemy import Column, Integer, String, Float,  DATE
from database import Base
from datetime import date
import uuid

class Pedido(Base):
    __tablename__ = "Pedidos"

    id = Column(String(150), primary_key = True, index = True, nullable= True, default=lambda: str(uuid.uuid4()))
    nome_cliente = Column(String(100), nullable=False)
    itens = Column(String(255), nullable=False)
    valor_total = Column(Float, nullable=False)
    data_do_pedido = Column(DATE, nullable= True, default= date.today)
    status_do_pedido = Column(String(100), nullable= True, default = "Pendente")

