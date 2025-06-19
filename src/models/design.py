from src.models.user import db
from datetime import datetime

class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_arte = db.Column(db.String(100))  # logomarca, cartão, banner, etc.
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    status = db.Column(db.String(50), default='pendente')  # pendente, em_producao, aprovado, entregue
    responsavel_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    link_arte = db.Column(db.String(500))
    prazo = db.Column(db.DateTime)
    observacoes = db.Column(db.Text)
    briefing_criativo = db.Column(db.Text)
    revisoes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = db.relationship('Cliente', backref='designs')
    responsavel = db.relationship('User', backref='designs_responsavel')

    def __repr__(self):
        return f'<Design {self.tipo_arte}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tipo_arte': self.tipo_arte,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'pedido_id': self.pedido_id,
            'pedido_codigo': self.pedido.codigo if self.pedido else None,
            'status': self.status,
            'responsavel_id': self.responsavel_id,
            'responsavel_nome': self.responsavel.username if self.responsavel else None,
            'link_arte': self.link_arte,
            'prazo': self.prazo.isoformat() if self.prazo else None,
            'observacoes': self.observacoes,
            'briefing_criativo': self.briefing_criativo,
            'revisoes': self.revisoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

