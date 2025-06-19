from src.models.user import db
from datetime import datetime

class SocialMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    tipo_conteudo = db.Column(db.String(100))  # post, stories, reels, etc.
    tema_titulo = db.Column(db.String(200))
    briefing = db.Column(db.Text)
    status = db.Column(db.String(50), default='pendente')  # pendente, aprovado, publicado
    data_publicacao = db.Column(db.DateTime)
    link_arte = db.Column(db.String(500))
    responsavel_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = db.relationship('Cliente', backref='social_medias')
    responsavel = db.relationship('User', backref='social_medias_responsavel')

    def __repr__(self):
        return f'<SocialMedia {self.tema_titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'tipo_conteudo': self.tipo_conteudo,
            'tema_titulo': self.tema_titulo,
            'briefing': self.briefing,
            'status': self.status,
            'data_publicacao': self.data_publicacao.isoformat() if self.data_publicacao else None,
            'link_arte': self.link_arte,
            'responsavel_id': self.responsavel_id,
            'responsavel_nome': self.responsavel.username if self.responsavel else None,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

