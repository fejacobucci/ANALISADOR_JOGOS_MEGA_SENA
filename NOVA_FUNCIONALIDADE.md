# Nova Funcionalidade: Intervalo entre Repetições por Posição

## 📊 O que foi adicionado?

Uma nova métrica que analisa o **intervalo em dias** entre as repetições de números em cada posição (1ª a 6ª) do sorteio.

---

## 🎯 Objetivo

Identificar padrões temporais de repetição dos números, permitindo entender:
- Com que frequência (em dias) um número se repete em determinada posição
- Qual o intervalo mínimo e máximo observado
- Quando foi o último sorteio de cada número

---

## 🔧 Implementação

### Backend (Python)

**Arquivo:** `backend/app/services/analytics_service.py`

Novo método criado:
```python
def intervalo_repeticoes_por_posicao(self, posicao: int = 1, limite: int = 20)
```

**O que faz:**
1. Busca todos os sorteios de uma posição específica ordenados por data
2. Agrupa por dezena
3. Calcula intervalos em dias entre cada aparição
4. Retorna estatísticas: média, mínimo, máximo

**Retorno:**
```json
{
  "dezena": 1,
  "frequencia": 288,
  "intervalo_medio": 37.8,
  "intervalo_minimo": 2,
  "intervalo_maximo": 217,
  "ultimo_sorteio": "2025-12-20",
  "total_intervalos": 287
}
```

### API Endpoint

**Rota:** `GET /api/v1/analytics/intervalo-repeticoes-posicao`

**Parâmetros:**
- `posicao` (int): Posição a analisar (1-6)
- `limite` (int): Quantidade de números a retornar (padrão: 20)

**Exemplo de chamada:**
```bash
curl "http://localhost:8000/api/v1/analytics/intervalo-repeticoes-posicao?posicao=1&limite=10"
```

### Frontend (React)

**Arquivo:** `frontend/src/pages/FrequenciaPosicao.tsx`

**Novidades:**
1. Adicionado seletor de visualização com 2 opções:
   - **Frequência de Aparições** (visualização original)
   - **Intervalo entre Repetições** (nova visualização)

2. Nova tabela com 6 colunas:
   - Dezena
   - Frequência
   - Intervalo Médio (dias)
   - Intervalo Mínimo
   - Intervalo Máximo
   - Último Sorteio

3. Card explicativo sobre como interpretar os intervalos

---

## 📈 Exemplo de Dados Reais

### Posição 1 - Top 5:

| Dezena | Frequência | Int. Médio | Int. Mínimo | Int. Máximo | Último Sorteio |
|--------|------------|------------|-------------|-------------|----------------|
| 1      | 288x       | 37.8 dias  | 2 dias      | 217 dias    | 20/12/2025     |
| 2      | 269x       | 39.8 dias  | 2 dias      | 280 dias    | 21/08/2025     |
| 4      | 248x       | 44.0 dias  | 2 dias      | 343 dias    | 09/12/2025     |
| 3      | 226x       | 47.9 dias  | 2 dias      | 315 dias    | 18/10/2025     |
| 5      | 215x       | 50.2 dias  | 2 dias      | 301 dias    | 18/12/2025     |

### Posição 3 - Top 5:

| Dezena | Frequência | Int. Médio | Int. Mínimo | Int. Máximo |
|--------|------------|------------|-------------|-------------|
| 28     | 121x       | 89.1 dias  | 4 dias      | 483 dias    |
| 24     | 116x       | 91.8 dias  | 3 dias      | 385 dias    |
| 30     | 111x       | 98.8 dias  | 2 dias      | 561 dias    |
| 23     | 111x       | 97.8 dias  | 3 dias      | 578 dias    |
| 19     | 105x       | 102.7 dias | 3 dias      | 636 dias    |

---

## 💡 Como Interpretar os Intervalos

### Intervalo Médio Baixo (< 40 dias)
- O número tende a se repetir com mais frequência
- Exemplo: Dezena 1 na posição 1 (37.8 dias)

### Intervalo Médio Alto (> 100 dias)
- O número demora mais para se repetir
- Menos frequente, mas quando sai pode ter padrão

### Intervalo Mínimo de 2 dias
- Indica que o número já saiu em concursos **consecutivos**
- Mostra que repetições rápidas são possíveis

### Intervalo Máximo Alto
- Mostra a maior "seca" que o número já teve
- Exemplo: Dezena 25 na posição 3 ficou 1040 dias sem aparecer

### Último Sorteio Recente
- Número apareceu recentemente nesta posição
- Pode indicar tendência ou apenas coincidência

---

## 🎯 Casos de Uso

### 1. Identificar Números "Regulares"
Números com intervalo médio baixo tendem a aparecer mais consistentemente.

**Exemplo:** Dezena 1 na posição 1
- Intervalo médio: 37.8 dias
- Interpretação: Aparece aproximadamente a cada 5-6 semanas

### 2. Detectar Números "Atrasados"
Compare o último sorteio com o intervalo médio.

**Exemplo:** Se um número tem intervalo médio de 40 dias e não sai há 100 dias, está "atrasado".

### 3. Validar Estratégias
Use os intervalos para:
- Escolher números que estão dentro do intervalo médio
- Evitar números que acabaram de sair (se considerar improvável repetição rápida)
- Focar em números "atrasados" (se acreditar em compensação)

---

## 🔄 Como Usar no Sistema

### 1. Acesse a Interface
```
http://localhost:3000/frequencia-posicao
```

### 2. Selecione a Posição
Escolha qual posição analisar (1ª a 6ª)

### 3. Selecione a Visualização
- **Frequência de Aparições**: Visão clássica (quantas vezes apareceu)
- **Intervalo entre Repetições**: Nova visão temporal (a cada quantos dias)

### 4. Analise os Dados
- Veja os números ordenados por frequência
- Compare intervalos médios
- Identifique padrões

### 5. Use na Geração de Jogos
Combine esta informação com outras métricas para criar jogos mais informados.

---

## 📊 Insights Descobertos

### Posição 1 (números baixos)
- Números menores (1-5) têm intervalos mais curtos
- Média geral: ~40 dias
- Repetições consecutivas são raras mas acontecem (mín: 2 dias)

### Posição 3 (meio-baixo)
- Números entre 19-34 dominam
- Intervalos maiores (~90-110 dias)
- Mais variabilidade nos padrões

### Posição 6 (números altos)
- Números maiores (45-60) predominam
- Padrões similares à posição 1
- Intervalos médios baixos para números frequentes

---

## 🚀 Melhorias Futuras Sugeridas

1. **Gráfico de Linha do Tempo**
   - Visualizar quando cada número saiu ao longo do tempo
   - Identificar "clusters" de aparições

2. **Predição de Próxima Aparição**
   - Baseado no intervalo médio e último sorteio
   - "Número X tem 70% de chance de sair nos próximos 30 dias"

3. **Correlação entre Posições**
   - Analisar se números em posições diferentes têm correlação temporal

4. **Alertas Automáticos**
   - Notificar quando número está muito "atrasado"
   - Alertar sobre padrões anormais

---

## 📝 Arquivos Modificados

### Backend
- ✅ `backend/app/services/analytics_service.py` - Novo método
- ✅ `backend/app/api/routes.py` - Novo endpoint

### Frontend
- ✅ `frontend/src/services/api.ts` - Nova função de API
- ✅ `frontend/src/pages/FrequenciaPosicao.tsx` - Interface atualizada

### Documentação
- ✅ `NOVA_FUNCIONALIDADE.md` - Este arquivo

---

## 🧪 Como Testar

### Via API (cURL)
```bash
# Posição 1, top 5
curl "http://localhost:8000/api/v1/analytics/intervalo-repeticoes-posicao?posicao=1&limite=5"

# Posição 3, top 10
curl "http://localhost:8000/api/v1/analytics/intervalo-repeticoes-posicao?posicao=3&limite=10"

# Posição 6, top 15
curl "http://localhost:8000/api/v1/analytics/intervalo-repeticoes-posicao?posicao=6&limite=15"
```

### Via Interface Web
1. Inicie o frontend (se ainda não estiver rodando):
   ```bash
   cd frontend
   npm run dev
   ```

2. Acesse: http://localhost:3000/frequencia-posicao

3. Selecione uma posição

4. Mude a visualização para "Intervalo entre Repetições"

5. Explore os dados!

---

## ✅ Status

**Implementação:** ✅ Completa
**Testes:** ✅ Passando
**Documentação:** ✅ Atualizada
**Deploy:** ✅ Backend rodando
**Frontend:** ⏳ Aguardando inicialização (execute `npm run dev`)

---

## 📞 Feedback

Esta funcionalidade foi criada com base no seu pedido!

Sugestões de melhorias são bem-vindas. 🎯

---

*Desenvolvido em 03/01/2026*
*Claude Code + FastAPI + React*
