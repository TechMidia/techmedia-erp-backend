from flask import Blueprint, jsonify
from src.models.user import db
from src.models.cliente import Cliente
from src.models.pedido import Pedido
from src.models.tarefa import Tarefa
from src.models.financeiro import Financeiro
from sqlalchemy import func, extract
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/kpis', methods=['GET'])
def get_dashboard_kpis():
    try:
        # Data atual
        hoje = datetime.now()
        mes_atual = hoje.strftime('%Y-%m')
        
        # Total de clientes
        total_clientes = Cliente.query.filter_by(status='ativo').count()
        
        # Total de pedidos
        total_pedidos = Pedido.query.count()
        
        # Pedidos em andamento
        pedidos_andamento = Pedido.query.filter(
            Pedido.status.in_(['pendente', 'em_andamento'])
        ).count()
        
        # Tarefas ativas
        tarefas_ativas = Tarefa.query.filter(
            Tarefa.status.in_(['pendente', 'em_andamento'])
        ).count()
        
        # Faturamento do mês
        faturamento_mes = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro == 'receita',
            Financeiro.referencia_mensal == mes_atual
        ).scalar() or 0
        
        # Custos do mês
        custos_mes = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro.in_(['despesa_variavel', 'custo_fixo']),
            Financeiro.referencia_mensal == mes_atual
        ).scalar() or 0
        
        # Lucro do mês
        lucro_mes = faturamento_mes - custos_mes
        
        # Contas a receber
        contas_receber = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro == 'receita',
            Financeiro.status == 'pendente'
        ).scalar() or 0
        
        # Contas a pagar
        contas_pagar = db.session.query(func.sum(Financeiro.valor)).filter(
            Financeiro.tipo_registro.in_(['despesa_variavel', 'custo_fixo']),
            Financeiro.status == 'pendente'
        ).scalar() or 0
        
        # Pedidos por status
        pedidos_status = db.session.query(
            Pedido.status, func.count(Pedido.id)
        ).group_by(Pedido.status).all()
        
        # Tarefas por prioridade
        tarefas_prioridade = db.session.query(
            Tarefa.prioridade, func.count(Tarefa.id)
        ).group_by(Tarefa.prioridade).all()
        
        # Faturamento últimos 6 meses
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
                'valor': valor
            })
        
        return jsonify({
            'total_clientes': total_clientes,
            'total_pedidos': total_pedidos,
            'pedidos_andamento': pedidos_andamento,
            'tarefas_ativas': tarefas_ativas,
            'faturamento_mes': faturamento_mes,
            'custos_mes': custos_mes,
            'lucro_mes': lucro_mes,
            'contas_receber': contas_receber,
            'contas_pagar': contas_pagar,
            'pedidos_status': dict(pedidos_status),
            'tarefas_prioridade': dict(tarefas_prioridade),
            'faturamento_historico': faturamento_historico
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/dashboard/atividades-recentes', methods=['GET'])
def get_atividades_recentes():
    try:
        # Últimos 10 pedidos
        pedidos_recentes = Pedido.query.order_by(Pedido.created_at.desc()).limit(10).all()
        
        # Últimas 10 tarefas
        tarefas_recentes = Tarefa.query.order_by(Tarefa.created_at.desc()).limit(10).all()
        
        # Últimas 10 movimentações financeiras
        financeiro_recente = Financeiro.query.order_by(Financeiro.created_at.desc()).limit(10).all()
        
        return jsonify({
            'pedidos_recentes': [pedido.to_dict() for pedido in pedidos_recentes],
            'tarefas_recentes': [tarefa.to_dict() for tarefa in tarefas_recentes],
            'financeiro_recente': [fin.to_dict() for fin in financeiro_recente]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/dashboard/alertas', methods=['GET'])
def get_alertas():
    try:
        alertas = []
        
        # Tarefas vencidas
        tarefas_vencidas = Tarefa.query.filter(
            Tarefa.data_entrega < datetime.now(),
            Tarefa.status.in_(['pendente', 'em_andamento'])
        ).count()
        
        if tarefas_vencidas > 0:
            alertas.append({
                'tipo': 'warning',
                'titulo': 'Tarefas Vencidas',
                'mensagem': f'{tarefas_vencidas} tarefa(s) vencida(s)',
                'link': '/tarefas?status=vencidas'
            })
        
        # Contas a vencer em 7 dias
        data_limite = datetime.now() + timedelta(days=7)
        contas_vencer = Financeiro.query.filter(
            Financeiro.data_vencimento <= data_limite,
            Financeiro.status == 'pendente'
        ).count()
        
        if contas_vencer > 0:
            alertas.append({
                'tipo': 'info',
                'titulo': 'Contas a Vencer',
                'mensagem': f'{contas_vencer} conta(s) vencem em 7 dias',
                'link': '/financeiro?status=a_vencer'
            })
        
        # Pedidos sem responsável
        pedidos_sem_responsavel = Pedido.query.filter(
            Pedido.responsavel_id.is_(None),
            Pedido.status == 'pendente'
        ).count()
        
        if pedidos_sem_responsavel > 0:
            alertas.append({
                'tipo': 'error',
                'titulo': 'Pedidos sem Responsável',
                'mensagem': f'{pedidos_sem_responsavel} pedido(s) sem responsável',
                'link': '/pedidos?status=sem_responsavel'
            })
        
        return jsonify({'alertas': alertas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

