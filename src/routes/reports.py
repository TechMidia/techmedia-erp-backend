from flask import Blueprint, jsonify
from src.models.user import db
from src.models.cliente import Cliente
from src.models.pedido import Pedido
from src.models.tarefa import Tarefa
from src.models.financeiro import Financeiro
from src.models.social_media import SocialMedia
from src.models.design import Design
from src.models.grafica import Grafica
from src.models.automacao import Automacao
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta
import json

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/dashboard-complete', methods=['GET'])
def get_complete_dashboard():
    """
    Relatório completo do dashboard com todos os KPIs e métricas
    """
    try:
        hoje = datetime.now()
        mes_atual = hoje.strftime('%Y-%m')
        
        # KPIs principais
        kpis = {
            'total_clientes': Cliente.query.filter_by(status='ativo').count(),
            'total_pedidos': Pedido.query.count(),
            'pedidos_andamento': Pedido.query.filter(Pedido.status.in_(['pendente', 'em_andamento'])).count(),
            'tarefas_ativas': Tarefa.query.filter(Tarefa.status.in_(['pendente', 'em_andamento'])).count(),
        }
        
        # Métricas financeiras
        financeiro_mes = db.session.query(
            func.sum(Financeiro.valor).label('receita'),
            func.sum(Financeiro.custo).label('custo'),
            func.sum(Financeiro.lucro).label('lucro')
        ).filter(
            Financeiro.tipo_registro == 'receita',
            Financeiro.referencia_mensal == mes_atual
        ).first()
        
        kpis.update({
            'faturamento_mes': financeiro_mes.receita or 0,
            'custo_mes': financeiro_mes.custo or 0,
            'lucro_mes': financeiro_mes.lucro or 0
        })
        
        # Contas a receber e pagar
        contas_receber = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro == 'receita',
            Financeiro.status == 'pendente'
        ).scalar() or 0
        
        contas_pagar = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro.in_(['despesa_variavel', 'custo_fixo']),
            Financeiro.status == 'pendente'
        ).scalar() or 0
        
        kpis.update({
            'contas_receber': contas_receber,
            'contas_pagar': contas_pagar
        })
        
        # Distribuição por status
        pedidos_status = dict(db.session.query(
            Pedido.status, func.count(Pedido.id)
        ).group_by(Pedido.status).all())
        
        tarefas_prioridade = dict(db.session.query(
            Tarefa.prioridade, func.count(Tarefa.id)
        ).group_by(Tarefa.prioridade).all())
        
        # Faturamento histórico (últimos 6 meses)
        faturamento_historico = []
        for i in range(6):
            data_mes = hoje - timedelta(days=30*i)
            mes_ref = data_mes.strftime('%Y-%m')
            valor = db.session.query(func.sum(Financeiro.valor)).filter(
                Financeiro.tipo_registro == 'receita',
                Financeiro.referencia_mensal == mes_ref
            ).scalar() or 0
            faturamento_historico.append({
                'mes': mes_ref,
                'valor': float(valor)
            })
        
        # Produtividade por usuário
        produtividade = db.session.query(
            Tarefa.responsavel_id,
            func.count(Tarefa.id).label('total_tarefas'),
            func.sum(Tarefa.tempo_gasto).label('tempo_total')
        ).group_by(Tarefa.responsavel_id).all()
        
        produtividade_data = []
        for prod in produtividade:
            if prod.responsavel_id:
                from src.models.user import User
                user = User.query.get(prod.responsavel_id)
                produtividade_data.append({
                    'usuario': user.username if user else 'Desconhecido',
                    'total_tarefas': prod.total_tarefas,
                    'tempo_total': prod.tempo_total or 0
                })
        
        # Clientes mais ativos
        clientes_ativos = db.session.query(
            Cliente.nome,
            func.count(Pedido.id).label('total_pedidos'),
            func.sum(Pedido.valor).label('valor_total')
        ).join(Pedido).group_by(Cliente.id, Cliente.nome).order_by(
            func.count(Pedido.id).desc()
        ).limit(10).all()
        
        clientes_data = []
        for cliente in clientes_ativos:
            clientes_data.append({
                'nome': cliente.nome,
                'total_pedidos': cliente.total_pedidos,
                'valor_total': float(cliente.valor_total or 0)
            })
        
        return jsonify({
            'kpis': kpis,
            'distribuicoes': {
                'pedidos_status': pedidos_status,
                'tarefas_prioridade': tarefas_prioridade
            },
            'historicos': {
                'faturamento': faturamento_historico
            },
            'analises': {
                'produtividade': produtividade_data,
                'clientes_ativos': clientes_data
            },
            'gerado_em': hoje.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/financial-summary', methods=['GET'])
def get_financial_summary():
    """
    Relatório financeiro detalhado
    """
    try:
        hoje = datetime.now()
        mes_atual = hoje.strftime('%Y-%m')
        
        # Resumo mensal
        resumo_mensal = db.session.query(
            Financeiro.tipo_registro,
            func.sum(Financeiro.valor).label('total'),
            func.count(Financeiro.id).label('quantidade')
        ).filter(
            Financeiro.referencia_mensal == mes_atual
        ).group_by(Financeiro.tipo_registro).all()
        
        resumo_data = {}
        for item in resumo_mensal:
            resumo_data[item.tipo_registro] = {
                'total': float(item.total),
                'quantidade': item.quantidade
            }
        
        # Fluxo de caixa por categoria
        fluxo_categoria = db.session.query(
            Financeiro.categoria,
            func.sum(Financeiro.valor).label('total')
        ).filter(
            Financeiro.referencia_mensal == mes_atual
        ).group_by(Financeiro.categoria).all()
        
        categoria_data = []
        for item in fluxo_categoria:
            if item.categoria:
                categoria_data.append({
                    'categoria': item.categoria,
                    'total': float(item.total)
                })
        
        # Contas em atraso
        contas_atraso = Financeiro.query.filter(
            Financeiro.data_vencimento < hoje,
            Financeiro.status == 'pendente'
        ).all()
        
        atraso_data = []
        for conta in contas_atraso:
            dias_atraso = (hoje - conta.data_vencimento).days
            atraso_data.append({
                'id': conta.id,
                'tipo': conta.tipo_registro,
                'valor': float(conta.valor),
                'dias_atraso': dias_atraso,
                'cliente_fornecedor': conta.cliente_fornecedor
            })
        
        # Previsão de recebimentos
        previsao_recebimentos = Financeiro.query.filter(
            Financeiro.tipo_registro == 'receita',
            Financeiro.status == 'pendente',
            Financeiro.data_vencimento >= hoje
        ).order_by(Financeiro.data_vencimento).limit(20).all()
        
        previsao_data = []
        for item in previsao_recebimentos:
            previsao_data.append({
                'data_vencimento': item.data_vencimento.isoformat() if item.data_vencimento else None,
                'valor': float(item.valor),
                'cliente': item.cliente_fornecedor,
                'pedido_codigo': item.pedido.codigo if item.pedido else None
            })
        
        return jsonify({
            'resumo_mensal': resumo_data,
            'fluxo_categoria': categoria_data,
            'contas_atraso': atraso_data,
            'previsao_recebimentos': previsao_data,
            'mes_referencia': mes_atual,
            'gerado_em': hoje.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/productivity', methods=['GET'])
def get_productivity_report():
    """
    Relatório de produtividade da equipe
    """
    try:
        hoje = datetime.now()
        inicio_mes = hoje.replace(day=1)
        
        # Produtividade por usuário no mês
        produtividade_mes = db.session.query(
            Tarefa.responsavel_id,
            func.count(Tarefa.id).label('tarefas_total'),
            func.sum(case([(Tarefa.status == 'concluida', 1)], else_=0)).label('tarefas_concluidas'),
            func.avg(Tarefa.progresso).label('progresso_medio'),
            func.sum(Tarefa.tempo_gasto).label('tempo_total')
        ).filter(
            Tarefa.created_at >= inicio_mes
        ).group_by(Tarefa.responsavel_id).all()
        
        from src.models.user import User
        produtividade_data = []
        for prod in produtividade_mes:
            if prod.responsavel_id:
                user = User.query.get(prod.responsavel_id)
                if user:
                    eficiencia = (prod.tarefas_concluidas / prod.tarefas_total * 100) if prod.tarefas_total > 0 else 0
                    produtividade_data.append({
                        'usuario': user.username,
                        'role': user.role,
                        'tarefas_total': prod.tarefas_total,
                        'tarefas_concluidas': prod.tarefas_concluidas or 0,
                        'eficiencia_percent': round(eficiencia, 2),
                        'progresso_medio': round(float(prod.progresso_medio or 0), 2),
                        'tempo_total_horas': prod.tempo_total or 0
                    })
        
        # Tarefas por área
        tarefas_area = db.session.query(
            Tarefa.area_relacionada,
            func.count(Tarefa.id).label('total'),
            func.avg(Tarefa.tempo_gasto).label('tempo_medio')
        ).filter(
            Tarefa.created_at >= inicio_mes
        ).group_by(Tarefa.area_relacionada).all()
        
        area_data = []
        for area in tarefas_area:
            if area.area_relacionada:
                area_data.append({
                    'area': area.area_relacionada,
                    'total_tarefas': area.total,
                    'tempo_medio_horas': round(float(area.tempo_medio or 0), 2)
                })
        
        # Tarefas em atraso
        tarefas_atraso = Tarefa.query.filter(
            Tarefa.data_entrega < hoje,
            Tarefa.status.in_(['pendente', 'em_andamento'])
        ).all()
        
        atraso_data = []
        for tarefa in tarefas_atraso:
            dias_atraso = (hoje - tarefa.data_entrega).days if tarefa.data_entrega else 0
            atraso_data.append({
                'id': tarefa.id,
                'titulo': tarefa.titulo,
                'responsavel': tarefa.responsavel.username if tarefa.responsavel else 'Não atribuído',
                'dias_atraso': dias_atraso,
                'prioridade': tarefa.prioridade,
                'cliente': tarefa.cliente.nome if tarefa.cliente else None
            })
        
        return jsonify({
            'produtividade_equipe': produtividade_data,
            'distribuicao_areas': area_data,
            'tarefas_atraso': atraso_data,
            'periodo': {
                'inicio': inicio_mes.isoformat(),
                'fim': hoje.isoformat()
            },
            'gerado_em': hoje.isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/reports/client-analysis', methods=['GET'])
def get_client_analysis():
    """
    Análise detalhada de clientes
    """
    try:
        # Clientes por valor total
        clientes_valor = db.session.query(
            Cliente.id,
            Cliente.nome,
            Cliente.tipo,
            Cliente.cidade,
            func.count(Pedido.id).label('total_pedidos'),
            func.sum(Pedido.valor).label('valor_total'),
            func.avg(Pedido.valor).label('ticket_medio')
        ).join(Pedido).group_by(
            Cliente.id, Cliente.nome, Cliente.tipo, Cliente.cidade
        ).order_by(func.sum(Pedido.valor).desc()).all()
        
        clientes_data = []
        for cliente in clientes_valor:
            clientes_data.append({
                'id': cliente.id,
                'nome': cliente.nome,
                'tipo': cliente.tipo,
                'cidade': cliente.cidade,
                'total_pedidos': cliente.total_pedidos,
                'valor_total': float(cliente.valor_total or 0),
                'ticket_medio': float(cliente.ticket_medio or 0)
            })
        
        # Distribuição por tipo de cliente
        tipos_cliente = db.session.query(
            Cliente.tipo,
            func.count(Cliente.id).label('quantidade'),
            func.sum(Pedido.valor).label('valor_total')
        ).join(Pedido).group_by(Cliente.tipo).all()
        
        tipos_data = []
        for tipo in tipos_cliente:
            if tipo.tipo:
                tipos_data.append({
                    'tipo': tipo.tipo,
                    'quantidade_clientes': tipo.quantidade,
                    'valor_total': float(tipo.valor_total or 0)
                })
        
        # Clientes inativos (sem pedidos nos últimos 90 dias)
        data_limite = datetime.now() - timedelta(days=90)
        clientes_inativos = db.session.query(Cliente).filter(
            ~Cliente.id.in_(
                db.session.query(Pedido.cliente_id).filter(
                    Pedido.created_at >= data_limite
                )
            )
        ).all()
        
        inativos_data = []
        for cliente in clientes_inativos:
            ultimo_pedido = Pedido.query.filter_by(cliente_id=cliente.id).order_by(
                Pedido.created_at.desc()
            ).first()
            
            inativos_data.append({
                'id': cliente.id,
                'nome': cliente.nome,
                'tipo': cliente.tipo,
                'ultimo_pedido': ultimo_pedido.created_at.isoformat() if ultimo_pedido else None,
                'responsavel': cliente.responsavel.username if cliente.responsavel else None
            })
        
        return jsonify({
            'ranking_clientes': clientes_data,
            'distribuicao_tipos': tipos_data,
            'clientes_inativos': inativos_data,
            'total_clientes_ativos': len(clientes_data),
            'total_clientes_inativos': len(inativos_data),
            'gerado_em': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

