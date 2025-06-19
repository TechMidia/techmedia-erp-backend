from src.models.user import db
from datetime import datetime

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    custo = db.Column(db.Float, default=0)
    tempo_entrega = db.Column(db.Integer)  # em dias
    is_recorrente = db.Column(db.Boolean, default=False)
    fornecedor_externo = db.Column(db.Boolean, default=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    link_fornecedor = db.Column(db.String(500))
    status = db.Column(db.String(20), default='ativo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    fornecedor = db.relationship('Fornecedor', backref='servicos')
    pedidos = db.relationship('Pedido', backref='servico', lazy=True)

    def __repr__(self):
        return f'<Servico {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'preco': self.preco,
            'custo': self.custo,
            'tempo_entrega': self.tempo_entrega,
            'is_recorrente': self.is_recorrente,
            'fornecedor_externo': self.fornecedor_externo,
            'fornecedor_id': self.fornecedor_id,
            'fornecedor_nome': self.fornecedor.nome if self.fornecedor else None,
            'link_fornecedor': self.link_fornecedor,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

