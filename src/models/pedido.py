from src.models.user import db
from datetime import datetime

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    categoria = db.Column(db.String(100))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pendente')  # pendente, em_andamento, concluido, cancelado
    responsavel_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    valor = db.Column(db.Float, nullable=False)
    link_arquivo = db.Column(db.String(500))
    observacoes = db.Column(db.Text)
    briefing = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    responsavel = db.relationship('User', backref='pedidos_responsavel')
    tarefas = db.relationship('Tarefa', backref='pedido', lazy=True)
    financeiros = db.relationship('Financeiro', backref='pedido', lazy=True)

    def __repr__(self):
        return f'<Pedido {self.codigo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'servico_id': self.servico_id,
            'servico_nome': self.servico.nome if self.servico else None,
            'categoria': self.categoria,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'status': self.status,
            'responsavel_id': self.responsavel_id,
            'responsavel_nome': self.responsavel.username if self.responsavel else None,
            'valor': self.valor,
            'link_arquivo': self.link_arquivo,
            'observacoes': self.observacoes,
            'briefing': self.briefing,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

