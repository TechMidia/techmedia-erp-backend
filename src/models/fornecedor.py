from src.models.user import db
from datetime import datetime

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100))  # grafica, design, marketing, etc.
    contato = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    endereco = db.Column(db.Text)
    tabela_preco_link = db.Column(db.String(500))
    api_disponivel = db.Column(db.Boolean, default=False)
    api_endpoint = db.Column(db.String(500))
    api_key = db.Column(db.String(200))
    site = db.Column(db.String(200))
    status = db.Column(db.String(20), default='ativo')
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'contato': self.contato,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'tabela_preco_link': self.tabela_preco_link,
            'api_disponivel': self.api_disponivel,
            'api_endpoint': self.api_endpoint,
            'api_key': self.api_key,
            'site': self.site,
            'status': self.status,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

