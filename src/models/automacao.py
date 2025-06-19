from src.models.user import db
from datetime import datetime

class Automacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    tipo_automacao = db.Column(db.String(100))  # bot_whatsapp, email_marketing, etc.
    nome_projeto = db.Column(db.String(200), nullable=False)
    escopo = db.Column(db.Text)
    status = db.Column(db.String(50), default='planejamento')  # planejamento, desenvolvimento, teste, ativo, pausado
    responsavel_tecnico_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complexidade = db.Column(db.String(20), default='media')  # baixa, media, alta
    prazo = db.Column(db.DateTime)
    link_fluxo = db.Column(db.String(500))  # link para n8n ou outro sistema
    webhook_url = db.Column(db.String(500))
    api_keys = db.Column(db.Text)  # JSON com chaves de API necessárias
    observacoes_tecnicas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = db.relationship('Cliente', backref='automacoes')
    responsavel_tecnico = db.relationship('User', backref='automacoes_responsavel')

    def __repr__(self):
        return f'<Automacao {self.nome_projeto}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'tipo_automacao': self.tipo_automacao,
            'nome_projeto': self.nome_projeto,
            'escopo': self.escopo,
            'status': self.status,
            'responsavel_tecnico_id': self.responsavel_tecnico_id,
            'responsavel_tecnico_nome': self.responsavel_tecnico.username if self.responsavel_tecnico else None,
            'complexidade': self.complexidade,
            'prazo': self.prazo.isoformat() if self.prazo else None,
            'link_fluxo': self.link_fluxo,
            'webhook_url': self.webhook_url,
            'api_keys': self.api_keys,
            'observacoes_tecnicas': self.observacoes_tecnicas,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

