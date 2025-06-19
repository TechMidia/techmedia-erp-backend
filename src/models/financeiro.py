from src.models.user import db
from datetime import datetime

class Financeiro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_registro = db.Column(db.String(50), nullable=False)  # receita, despesa_variavel, custo_fixo
    cliente_fornecedor = db.Column(db.String(200))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    valor = db.Column(db.Float, nullable=False)
    custo = db.Column(db.Float, default=0)
    lucro = db.Column(db.Float, default=0)  # calculado automaticamente
    status = db.Column(db.String(50), default='pendente')  # pendente, pago, vencido
    categoria = db.Column(db.String(100))
    forma_pagamento = db.Column(db.String(50))
    data_vencimento = db.Column(db.DateTime)
    data_pagamento = db.Column(db.DateTime)
    referencia_mensal = db.Column(db.String(7))  # YYYY-MM
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Financeiro {self.tipo_registro} - {self.valor}>'

    def calculate_lucro(self):
        if self.tipo_registro == 'receita':
            self.lucro = self.valor - self.custo
        else:
            self.lucro = 0

    def to_dict(self):
        return {
            'id': self.id,
            'tipo_registro': self.tipo_registro,
            'cliente_fornecedor': self.cliente_fornecedor,
            'pedido_id': self.pedido_id,
            'pedido_codigo': self.pedido.codigo if self.pedido else None,
            'valor': self.valor,
            'custo': self.custo,
            'lucro': self.lucro,
            'status': self.status,
            'categoria': self.categoria,
            'forma_pagamento': self.forma_pagamento,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'referencia_mensal': self.referencia_mensal,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

