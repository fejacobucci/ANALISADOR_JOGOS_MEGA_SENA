from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Concurso(Base):
    __tablename__ = "concursos"

    id = Column(Integer, primary_key=True, index=True)
    numero_concurso = Column(Integer, unique=True, nullable=False, index=True)
    data_sorteio = Column(Date, nullable=False, index=True)
    ganhadores_sena = Column(Integer, default=0)
    rateio_sena = Column(Numeric(15, 2))
    ganhadores_quina = Column(Integer, default=0)
    rateio_quina = Column(Numeric(15, 2))
    ganhadores_quadra = Column(Integer, default=0)
    rateio_quadra = Column(Numeric(15, 2))
    acumulado = Column(Numeric(15, 2))
    arrecadacao_total = Column(Numeric(15, 2))
    estimativa_premio = Column(Numeric(15, 2))
    acumulado_mega_virada = Column(Numeric(15, 2))
    observacao = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    dezenas = relationship("DezenaSorteada", back_populates="concurso", cascade="all, delete-orphan")
    cidades = relationship("CidadeGanhadora", back_populates="concurso", cascade="all, delete-orphan")


class DezenaSorteada(Base):
    __tablename__ = "dezenas_sorteadas"
    __table_args__ = (
        CheckConstraint('dezena >= 1 AND dezena <= 60', name='check_dezena_range'),
        CheckConstraint('posicao >= 1 AND posicao <= 6', name='check_posicao_range'),
    )

    id = Column(Integer, primary_key=True, index=True)
    concurso_id = Column(Integer, ForeignKey("concursos.id", ondelete="CASCADE"), nullable=False, index=True)
    dezena = Column(Integer, nullable=False, index=True)
    posicao = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento
    concurso = relationship("Concurso", back_populates="dezenas")


class CidadeGanhadora(Base):
    __tablename__ = "cidades_ganhadoras"

    id = Column(Integer, primary_key=True, index=True)
    concurso_id = Column(Integer, ForeignKey("concursos.id", ondelete="CASCADE"), nullable=False, index=True)
    cidade = Column(String(100))
    uf = Column(String(2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento
    concurso = relationship("Concurso", back_populates="cidades")
