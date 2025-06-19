from src.models.user import db
from datetime import datetime

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    cpf_cnpj = db.Column(db.String(20), unique=True)
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    tipo = db.Column(db.String(50))  # Social Media, Gráfica, etc.
    forma_pagamento = db.Column(db.String(50))
    status = db.Column(db.String(20), default='ativo')
    responsavel_interno_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    responsavel = db.relationship('User', backref='clientes_responsavel')
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'cpf_cnpj': self.cpf_cnpj,
            'cidade': self.cidade,
            'estado': self.estado,
            'tipo': self.tipo,
            'forma_pagamento': self.forma_pagamento,
            'status': self.status,
            'responsavel_interno_id': self.responsavel_interno_id,
            'responsavel_nome': self.responsavel.username if self.responsavel else None,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

