from src.models.user import db
from datetime import datetime

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    area_relacionada = db.Column(db.String(100))  # design, social_media, grafica, etc.
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    data_entrega = db.Column(db.DateTime)
    prioridade = db.Column(db.String(20), default='media')  # baixa, media, alta, urgente
    status = db.Column(db.String(50), default='pendente')  # pendente, em_andamento, concluida, cancelada
    progresso = db.Column(db.Integer, default=0)  # 0-100%
    tempo_estimado = db.Column(db.Integer)  # em horas
    tempo_gasto = db.Column(db.Integer, default=0)  # em horas
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    responsavel = db.relationship('User', backref='tarefas_responsavel')
    cliente = db.relationship('Cliente', backref='tarefas')

    def __repr__(self):
        return f'<Tarefa {self.titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'responsavel_id': self.responsavel_id,
            'responsavel_nome': self.responsavel.username if self.responsavel else None,
            'area_relacionada': self.area_relacionada,
            'pedido_id': self.pedido_id,
            'pedido_codigo': self.pedido.codigo if self.pedido else None,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'prioridade': self.prioridade,
            'status': self.status,
            'progresso': self.progresso,
            'tempo_estimado': self.tempo_estimado,
            'tempo_gasto': self.tempo_gasto,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

