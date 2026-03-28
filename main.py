from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from datetime import date

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/pedidos/", response_model=schemas.PedidoRetorno, tags=["Pedidos"], summary="Criar um novo pedido")
def criar_pedido(pedido: schemas.PedidoCriar, db: Session = Depends(get_db)):

    novo_pedido = models.Pedido (
        nome_cliente = pedido.nome_cliente,
        itens = pedido.itens,
        valor_total = pedido.valor_total
    )
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido

@app.get("/pedidos/", response_model=list[schemas.PedidoRetorno], tags=["Pedidos"], summary="Lista todos os pedidos")
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    
    pedidos = db.query(models.Pedido).order_by(models.Pedido.id).offset(skip).limit(limit).all()
    
    return pedidos

@app.get("/pedidos/{pedido_id}", response_model=schemas.PedidoRetorno, tags=["Pedidos"], summary="Buscar um pedido específico pelo ID")
def buscar_pedido(pedido_id: str, db: Session = Depends(get_db)):
    
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Erro! Pedido não encontrado")

    return pedido

@app.patch("/pedidos/{pedido_id}/status", response_model=schemas.PedidoRetorno, tags=["Pedidos"], summary="Atualizar o status de um pedido")
def atualizacao_status_pedido(pedido_id : str, pedido_novo_status: str, db: Session = Depends(get_db)):

    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

    if pedido:
        pedido.status_do_pedido = pedido_novo_status.capitalize()
        db.commit()
        db.refresh(pedido)
        return pedido
    else:
        raise HTTPException(status_code= 404, detail="Erro! Pedido não encontrado.")
    
@app.delete("/pedidos/{pedido_id}", response_model=schemas.PedidoRetorno, tags=["Pedidos"], summary="Deletar um pedido permanentemente")
def deletar_pedido(pedido_id: str, db: Session = Depends(get_db)):

    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

    if pedido:
        db.delete(pedido)
        db.commit()
        return pedido
    else:
        raise HTTPException(status_code=404, detail="Erro! Pedido não encontrado")

## ABA DE NOTICIAS

@app.get("/noticias", tags=["Dashboard"], summary="Feed de atualizações e notícias do sistema")
def ultimas_noticias():
    return [
        {
            "data": "2023-10-25",
            "titulo": "Novo sistema de Pedidos",
            "mensagem": "Nossa nova API de criação de pedidos entrou no ar com sucesso!"
        },
        {
            "data": "2023-10-26",
            "titulo": "Atualização de Status",
            "mensagem": "Agora os clientes podem acompanhar se o pedido está 'Pendente' ou 'Concluído'."
        },
        {
            "data": "2023-10-27",
            "titulo": "Migração para UUID",
            "mensagem": "Melhoramos a segurança do sistema alterando as chaves de identificação para UUIDs universais."
        }
    ]


## APRESENTAÇÃO DA EMPRESA

@app.get("/empresa", tags=["Dashboard"], summary="Relatório Financeiro e apresentação da empresa")
def sobre_a_empresa(db: Session = Depends(get_db)):
    hoje = date.today()

    # 1. CONTAGEM DE STATUS (GERAL, MÊS, ANO)

    # Geral
    total_concluidos = db.query(models.Pedido).filter(models.Pedido.status_do_pedido == "Concluído").count()
    total_pendentes = db.query(models.Pedido).filter(models.Pedido.status_do_pedido == "Pendente").count()

    # Mês
    total_concluidos_mes = db.query(models.Pedido).filter(
        models.Pedido.status_do_pedido == "Concluído",
        extract('month', models.Pedido.data_do_pedido) == hoje.month,
        extract('year', models.Pedido.data_do_pedido) == hoje.year
    ).count()
    
    total_pendentes_mes = db.query(models.Pedido).filter(
        models.Pedido.status_do_pedido == "Pendente",
        extract('month', models.Pedido.data_do_pedido) == hoje.month,
        extract('year', models.Pedido.data_do_pedido) == hoje.year
    ).count()

    # Ano
    total_concluidos_ano = db.query(models.Pedido).filter(
        models.Pedido.status_do_pedido == "Concluído",
        extract('year', models.Pedido.data_do_pedido) == hoje.year
    ).count()
    
    total_pendentes_ano = db.query(models.Pedido).filter(
        models.Pedido.status_do_pedido == "Pendente",
        extract('year', models.Pedido.data_do_pedido) == hoje.year
    ).count()


    # 2. CONTAGEM DE PEDIDOS ALTOS, MEDIOS E BAIXOS DO MÊS E ANO (QUANTIDADE)

    # MÊS
    altos_mes = db.query(models.Pedido).filter(models.Pedido.valor_total >= 2000, extract('month', models.Pedido.data_do_pedido) == hoje.month, extract('year', models.Pedido.data_do_pedido) == hoje.year).count()
    medios_mes = db.query(models.Pedido).filter(models.Pedido.valor_total >= 500, models.Pedido.valor_total < 2000, extract('month', models.Pedido.data_do_pedido) == hoje.month, extract('year', models.Pedido.data_do_pedido) == hoje.year).count()
    baixos_mes = db.query(models.Pedido).filter(models.Pedido.valor_total < 500, extract('month', models.Pedido.data_do_pedido) == hoje.month, extract('year', models.Pedido.data_do_pedido) == hoje.year).count()

    # ANO
    altos_ano = db.query(models.Pedido).filter(models.Pedido.valor_total >= 2000, extract('year', models.Pedido.data_do_pedido) == hoje.year).count()
    medios_ano = db.query(models.Pedido).filter(models.Pedido.valor_total >= 500, models.Pedido.valor_total < 2000, extract('year', models.Pedido.data_do_pedido) == hoje.year).count()
    baixos_ano = db.query(models.Pedido).filter(models.Pedido.valor_total < 500, extract('year', models.Pedido.data_do_pedido) == hoje.year).count()

    # 3. FATURAMENTO REAL 

    # Geral
    faturamento_geral = db.query(func.sum(models.Pedido.valor_total)).scalar() or 0.0
    
    # Mês
    faturamento_mes = db.query(func.sum(models.Pedido.valor_total)).filter(
        extract('month', models.Pedido.data_do_pedido) == hoje.month,
        extract('year', models.Pedido.data_do_pedido) == hoje.year
    ).scalar() or 0.0
    
    # Ano
    faturamento_ano = db.query(func.sum(models.Pedido.valor_total)).filter(
        extract('year', models.Pedido.data_do_pedido) == hoje.year
    ).scalar() or 0.0

    # 4. RETORNO ORGANIZADO E LIMPO
    return {
        "nome": "GTI Tech Store",
        "descricao": "O melhor Shopping Virtual Tech da região. Focado em entregas rápidas e sistemas eficientes.",
        "versao_api": "1.0.0",
        "visao_geral": {
            "total_pedidos_finalizados": total_concluidos,
            "total_pedidos_pendentes": total_pendentes,
            "faturamento_total_acumulado": round(faturamento_geral, 2)
        },
        "estatisticas_este_mes": {
            "status": {
                "finalizados": total_concluidos_mes,
                "pendentes": total_pendentes_mes
            },
            "quantidade_por_ticket": {
                "altos_mais_2000": altos_mes,
                "medios_500_a_2000": medios_mes,
                "baixos_menos_500": baixos_mes
            },
            "faturamento_do_mes": round(faturamento_mes, 2)
        },
        "estatisticas_este_ano": {
            "status": {
                "finalizados": total_concluidos_ano,
                "pendentes": total_pendentes_ano
            },
            "quantidade_por_ticket": {
                "altos_mais_2000": altos_ano,
                "medios_500_a_2000": medios_ano,
                "baixos_menos_500": baixos_ano
            },
            "faturamento_do_ano": round(faturamento_ano, 2)
        }
    }







