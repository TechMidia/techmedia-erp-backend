from src.models.user import db
from datetime import datetime

class Grafica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    custo_unitario = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    custo_total = db.Column(db.Float)  # calculado automaticamente
    preco_venda = db.Column(db.Float, nullable=False)
    prazo = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='orcamento')  # orcamento, aprovado, producao, entregue
    link_arte = db.Column(db.String(500))
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = db.relationship('Cliente', backref='graficas')
    fornecedor = db.relationship('Fornecedor', backref='graficas')

    def __repr__(self):
        return f'<Grafica {self.produto}>'

    def calculate_custo_total(self):
        self.custo_total = self.custo_unitario * self.quantidade

    def to_dict(self):
        return {
            'id': self.id,
            'produto': self.produto,
            'categoria': self.categoria,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'pedido_id': self.pedido_id,
            'pedido_codigo': self.pedido.codigo if self.pedido else None,
            'fornecedor_id': self.fornecedor_id,
            'fornecedor_nome': self.fornecedor.nome if self.fornecedor else None,
            'custo_unitario': self.custo_unitario,
            'quantidade': self.quantidade,
            'custo_total': self.custo_total,
            'preco_venda': self.preco_venda,
            'prazo': self.prazo.isoformat() if self.prazo else None,
            'status': self.status,
            'link_arte': self.link_arte,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

