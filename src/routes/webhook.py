from flask import Blueprint, request, jsonify
from src.models.user import db
import requests
import json
from datetime import datetime

webhook_bp = Blueprint('webhook', __name__)

# Configurações para integrações
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Configurar via variável de ambiente
N8N_WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL"  # Configurar via variável de ambiente

@webhook_bp.route('/webhooks/telegram/send-message', methods=['POST'])
def send_telegram_message():
    """
    Endpoint para enviar mensagens via Telegram
    Usado para notificações automáticas do sistema
    """
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        message = data.get('message')
        
        if not chat_id or not message:
            return jsonify({'error': 'chat_id e message são obrigatórios'}), 400
        
        # Simular envio de mensagem (em produção, usar API real do Telegram)
        telegram_response = {
            'ok': True,
            'result': {
                'message_id': 123,
                'date': int(datetime.now().timestamp()),
                'text': message
            }
        }
        
        # Log da atividade
        print(f"[TELEGRAM] Mensagem enviada para {chat_id}: {message}")
        
        return jsonify({
            'success': True,
            'telegram_response': telegram_response
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@webhook_bp.route('/webhooks/n8n/trigger', methods=['POST'])
def trigger_n8n_workflow():
    """
    Endpoint para disparar workflows no n8n
    Usado para automações complexas
    """
    try:
        data = request.get_json()
        workflow_type = data.get('workflow_type')
        payload = data.get('payload', {})
        
        if not workflow_type:
            return jsonify({'error': 'workflow_type é obrigatório'}), 400
        
        # Simular disparo de workflow n8n
        n8n_response = {
            'success': True,
            'workflow_id': f"wf_{workflow_type}_{int(datetime.now().timestamp())}",
            'status': 'triggered',
            'payload': payload
        }
        
        # Log da atividade
        print(f"[N8N] Workflow {workflow_type} disparado com payload: {payload}")
        
        return jsonify({
            'success': True,
            'n8n_response': n8n_response
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@webhook_bp.route('/webhooks/automation/new-order', methods=['POST'])
def automation_new_order():
    """
    Automação disparada quando um novo pedido é criado
    """
    try:
        data = request.get_json()
        pedido_id = data.get('pedido_id')
        cliente_nome = data.get('cliente_nome')
        servico_nome = data.get('servico_nome')
        responsavel_id = data.get('responsavel_id')
        
        automations_triggered = []
        
        # 1. Enviar notificação via Telegram
        telegram_message = f"🆕 Novo pedido criado!\n\nCliente: {cliente_nome}\nServiço: {servico_nome}\nResponsável: ID {responsavel_id}"
        
        telegram_result = {
            'type': 'telegram_notification',
            'status': 'simulated',
            'message': telegram_message
        }
        automations_triggered.append(telegram_result)
        
        # 2. Criar tarefa automaticamente se for design
        if servico_nome and 'design' in servico_nome.lower():
            task_result = {
                'type': 'auto_task_creation',
                'status': 'simulated',
                'task_title': f"Criar {servico_nome} - {cliente_nome}"
            }
            automations_triggered.append(task_result)
        
        # 3. Disparar workflow n8n para integração com sistemas externos
        n8n_result = {
            'type': 'n8n_workflow',
            'status': 'simulated',
            'workflow': 'new_order_processing'
        }
        automations_triggered.append(n8n_result)
        
        # Log das automações
        print(f"[AUTOMATION] Automações disparadas para pedido {pedido_id}: {len(automations_triggered)} ações")
        
        return jsonify({
            'success': True,
            'pedido_id': pedido_id,
            'automations_triggered': automations_triggered
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@webhook_bp.route('/webhooks/automation/task-completed', methods=['POST'])
def automation_task_completed():
    """
    Automação disparada quando uma tarefa é concluída
    """
    try:
        data = request.get_json()
        tarefa_id = data.get('tarefa_id')
        tarefa_titulo = data.get('tarefa_titulo')
        responsavel_nome = data.get('responsavel_nome')
        cliente_nome = data.get('cliente_nome')
        
        automations_triggered = []
        
        # 1. Notificar cliente via Telegram/WhatsApp
        client_message = f"✅ Tarefa concluída!\n\n{tarefa_titulo}\nResponsável: {responsavel_nome}"
        
        client_notification = {
            'type': 'client_notification',
            'status': 'simulated',
            'message': client_message,
            'cliente': cliente_nome
        }
        automations_triggered.append(client_notification)
        
        # 2. Atualizar status do pedido relacionado
        order_update = {
            'type': 'order_status_update',
            'status': 'simulated',
            'action': 'check_completion'
        }
        automations_triggered.append(order_update)
        
        # 3. Gerar relatório de produtividade
        productivity_report = {
            'type': 'productivity_tracking',
            'status': 'simulated',
            'responsavel': responsavel_nome
        }
        automations_triggered.append(productivity_report)
        
        print(f"[AUTOMATION] Automações disparadas para tarefa {tarefa_id}: {len(automations_triggered)} ações")
        
        return jsonify({
            'success': True,
            'tarefa_id': tarefa_id,
            'automations_triggered': automations_triggered
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@webhook_bp.route('/webhooks/automation/payment-received', methods=['POST'])
def automation_payment_received():
    """
    Automação disparada quando um pagamento é recebido
    """
    try:
        data = request.get_json()
        financeiro_id = data.get('financeiro_id')
        valor = data.get('valor')
        cliente_nome = data.get('cliente_nome')
        
        automations_triggered = []
        
        # 1. Atualizar status financeiro
        financial_update = {
            'type': 'financial_status_update',
            'status': 'simulated',
            'action': 'mark_as_paid'
        }
        automations_triggered.append(financial_update)
        
        # 2. Enviar recibo por email
        receipt_email = {
            'type': 'receipt_email',
            'status': 'simulated',
            'cliente': cliente_nome,
            'valor': valor
        }
        automations_triggered.append(receipt_email)
        
        # 3. Atualizar KPIs em tempo real
        kpi_update = {
            'type': 'kpi_update',
            'status': 'simulated',
            'metrics': ['receita_mes', 'lucro_mes']
        }
        automations_triggered.append(kpi_update)
        
        # 4. Notificar equipe financeira
        team_notification = {
            'type': 'team_notification',
            'status': 'simulated',
            'message': f"💰 Pagamento recebido: R$ {valor} de {cliente_nome}"
        }
        automations_triggered.append(team_notification)
        
        print(f"[AUTOMATION] Automações disparadas para pagamento {financeiro_id}: {len(automations_triggered)} ações")
        
        return jsonify({
            'success': True,
            'financeiro_id': financeiro_id,
            'automations_triggered': automations_triggered
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@webhook_bp.route('/webhooks/automation/deadline-alert', methods=['POST'])
def automation_deadline_alert():
    """
    Automação para alertas de prazo
    """
    try:
        data = request.get_json()
        alert_type = data.get('alert_type')  # 'task_due', 'payment_due', etc.
        items = data.get('items', [])
        
        automations_triggered = []
        
        for item in items:
            # Enviar alerta personalizado baseado no tipo
            if alert_type == 'task_due':
                alert = {
                    'type': 'task_deadline_alert',
                    'status': 'simulated',
                    'message': f"⚠️ Tarefa vencendo: {item.get('titulo')}",
                    'responsavel': item.get('responsavel_nome')
                }
            elif alert_type == 'payment_due':
                alert = {
                    'type': 'payment_deadline_alert',
                    'status': 'simulated',
                    'message': f"💳 Conta vencendo: R$ {item.get('valor')}",
                    'cliente': item.get('cliente_nome')
                }
            else:
                alert = {
                    'type': 'generic_alert',
                    'status': 'simulated',
                    'message': f"📅 Alerta: {item}"
                }
            
            automations_triggered.append(alert)
        
        print(f"[AUTOMATION] Alertas de prazo disparados: {len(automations_triggered)} alertas")
        
        return jsonify({
            'success': True,
            'alert_type': alert_type,
            'alerts_sent': len(automations_triggered),
            'automations_triggered': automations_triggered
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

