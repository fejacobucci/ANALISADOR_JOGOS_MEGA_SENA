-- Schema do Banco de Dados Mega Sena
-- Database: mega_sena_base

-- Tabela principal de concursos
CREATE TABLE IF NOT EXISTS concursos (
    id SERIAL PRIMARY KEY,
    numero_concurso INTEGER UNIQUE NOT NULL,
    data_sorteio DATE NOT NULL,
    ganhadores_sena INTEGER DEFAULT 0,
    rateio_sena DECIMAL(15, 2),
    ganhadores_quina INTEGER DEFAULT 0,
    rateio_quina DECIMAL(15, 2),
    ganhadores_quadra INTEGER DEFAULT 0,
    rateio_quadra DECIMAL(15, 2),
    acumulado DECIMAL(15, 2),
    arrecadacao_total DECIMAL(15, 2),
    estimativa_premio DECIMAL(15, 2),
    acumulado_mega_virada DECIMAL(15, 2),
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de dezenas sorteadas (normalizada)
CREATE TABLE IF NOT EXISTS dezenas_sorteadas (
    id SERIAL PRIMARY KEY,
    concurso_id INTEGER NOT NULL REFERENCES concursos(id) ON DELETE CASCADE,
    dezena INTEGER NOT NULL CHECK (dezena BETWEEN 1 AND 60),
    posicao INTEGER NOT NULL CHECK (posicao BETWEEN 1 AND 6),
    UNIQUE(concurso_id, posicao),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de cidades ganhadoras
CREATE TABLE IF NOT EXISTS cidades_ganhadoras (
    id SERIAL PRIMARY KEY,
    concurso_id INTEGER NOT NULL REFERENCES concursos(id) ON DELETE CASCADE,
    cidade VARCHAR(100),
    uf CHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para otimização de consultas
CREATE INDEX idx_concursos_data ON concursos(data_sorteio);
CREATE INDEX idx_concursos_numero ON concursos(numero_concurso);
CREATE INDEX idx_dezenas_concurso ON dezenas_sorteadas(concurso_id);
CREATE INDEX idx_dezenas_numero ON dezenas_sorteadas(dezena);
CREATE INDEX idx_dezenas_posicao ON dezenas_sorteadas(posicao);
CREATE INDEX idx_cidades_concurso ON cidades_ganhadoras(concurso_id);

-- View para facilitar consultas de concursos com todas as bolas
CREATE OR REPLACE VIEW vw_concursos_completos AS
SELECT
    c.numero_concurso,
    c.data_sorteio,
    MAX(CASE WHEN d.posicao = 1 THEN d.dezena END) as bola1,
    MAX(CASE WHEN d.posicao = 2 THEN d.dezena END) as bola2,
    MAX(CASE WHEN d.posicao = 3 THEN d.dezena END) as bola3,
    MAX(CASE WHEN d.posicao = 4 THEN d.dezena END) as bola4,
    MAX(CASE WHEN d.posicao = 5 THEN d.dezena END) as bola5,
    MAX(CASE WHEN d.posicao = 6 THEN d.dezena END) as bola6,
    c.ganhadores_sena,
    c.rateio_sena,
    c.ganhadores_quina,
    c.rateio_quina,
    c.ganhadores_quadra,
    c.rateio_quadra,
    c.acumulado,
    c.arrecadacao_total
FROM concursos c
LEFT JOIN dezenas_sorteadas d ON c.id = d.concurso_id
GROUP BY c.id, c.numero_concurso, c.data_sorteio, c.ganhadores_sena, c.rateio_sena,
         c.ganhadores_quina, c.rateio_quina, c.ganhadores_quadra, c.rateio_quadra,
         c.acumulado, c.arrecadacao_total
ORDER BY c.numero_concurso;

-- View para frequência de dezenas
CREATE OR REPLACE VIEW vw_frequencia_dezenas AS
SELECT
    dezena,
    COUNT(*) as frequencia,
    COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT concurso_id) FROM dezenas_sorteadas) as percentual
FROM dezenas_sorteadas
GROUP BY dezena
ORDER BY frequencia DESC;

-- View para frequência por posição
CREATE OR REPLACE VIEW vw_frequencia_por_posicao AS
SELECT
    posicao,
    dezena,
    COUNT(*) as frequencia
FROM dezenas_sorteadas
GROUP BY posicao, dezena
ORDER BY posicao, frequencia DESC;

-- View para análise de pares e ímpares
CREATE OR REPLACE VIEW vw_analise_pares_impares AS
SELECT
    c.numero_concurso,
    c.data_sorteio,
    SUM(CASE WHEN d.dezena % 2 = 0 THEN 1 ELSE 0 END) as qtd_pares,
    SUM(CASE WHEN d.dezena % 2 = 1 THEN 1 ELSE 0 END) as qtd_impares
FROM concursos c
JOIN dezenas_sorteadas d ON c.id = d.concurso_id
GROUP BY c.id, c.numero_concurso, c.data_sorteio
ORDER BY c.numero_concurso;

-- View para soma das dezenas
CREATE OR REPLACE VIEW vw_soma_dezenas AS
SELECT
    c.numero_concurso,
    c.data_sorteio,
    SUM(d.dezena) as soma_total
FROM concursos c
JOIN dezenas_sorteadas d ON c.id = d.concurso_id
GROUP BY c.id, c.numero_concurso, c.data_sorteio
ORDER BY c.numero_concurso;

-- Comentários nas tabelas
COMMENT ON TABLE concursos IS 'Tabela principal com informações dos concursos da Mega Sena';
COMMENT ON TABLE dezenas_sorteadas IS 'Tabela normalizada com as dezenas sorteadas em cada concurso';
COMMENT ON TABLE cidades_ganhadoras IS 'Tabela com as cidades que tiveram ganhadores';
