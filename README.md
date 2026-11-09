# 🔎 Checa Aí!

> **Antes de compartilhar, verifique.**
> Um jogo em PyGame sobre combater a desinformação.

Atividade A3 — Desenvolvimento de Jogos (PyGame) · UC de UDWMJ

**Integrantes:** `Ruan Vitor Moreno Oliveira - 323132532 | Daniel Luca saraiva da Silva - 323112685 | Mariana martins costa coimbra pessoa - 323125572`

---

## 🎮 Sobre o jogo

`Checa aí é um jogo sobre combate a desinformação. Na era digital cada vez mais em grupos de whatsapp, e em redes sociais, se tornou cada vez mais facil espalhar mentiras, esse jogo foca na ideia de analisar, e classificar essas noticias, como verdadeiras ou falsas, investigando cada noticia, e utilizando do raciocinio logico em conjunto com as dicas para identificar rapidamente o que pode ser uma fake news. Nos baseamos bastante na ideia de gameplay de jogos como paper please, e thats not my neighbor, onde você precisa validar informações pra determinar se aquele "item" é legitimo, ou falso.`

## ▶️ Como rodar

Requisitos: Python 3.14 e PyGame-ce.

```bash
pip install -r requirements.txt
python checa_ai.py
```

## ⌨️ Controles

| Tecla | Ação |
|---|---|
| `ESPAÇO` | Investigar: revela uma pista (a mensagem desce um pouco) |
| `D` | Desmentir: você acha que a mensagem é falsa |
| `C` | Confirmar: você acha que a mensagem é verdadeira |
| `ESC` | Sair |

## 🧠 Respostas às perguntas do enunciado

**Quem é impactado pelo jogo?**
`Pessoas que utilizam diariamente grupos massivos de mensagem, como canais no whatsapp ou grupos do telegram, onde mensagens falsas são facilmente repassadas`
**Qual problema ou necessidade está sendo abordado?**
`O problema que abordamos e o da desinformação, que pode causar desde uma desconfiança infundada, até a mesmo uma morte por acreditar em uma mentira perigosamente falsa.` 

**Como as ações do jogador contribuem para esse impacto?**
`O jogador atua como um checador de fatos, a pessoa que traz credibilidade para essas noticias, e dependendo do seu resultado, pode influenciar a vida da vizinhaça para melhor, ou pior.` 

**Que tipo de experiência queremos provocar?**
`Queremos que o jogador sinta o peso que noticias falsas tem, e o quanto de estrago podemos evitar, ao checar os fatos, e alertar a comunidade.` 

**Como a mecânica reforça esse objetivo?**
`As mecanicas fazem uma alusão a realidade, checar uma noticia leva tempo, mas traz mais evidencias da sua veracidade ou falsidade. Tratar uma noticia falsa como verdadeira, e vice e versa, também impactam na sua credibilidade, pois alguem que valida informações falsas, não é confiavel. As mensagens de status também trazem um breve vislumbre do que sua atitude pode mudar na vida das pessoas.` 

### 🪧 O teste do "cartaz"

*"Se eu remover o controle do jogador e deixar só texto, o jogo ainda cumpre o objetivo?"*

`Quando o jogador nao toma nenhuma ação, as noticias, tanto verdadeiras, quanto falsas, passam sem nenhuma checagem, podendo trazer consequencias irreversiveis para a população do bairro.`

## ✅ Requisitos técnicos

| Requisito | Onde está |
|---|---|
| Python + PyGame | `checa_ai.py` |
| Game loop `input → update → draw` | `main()` chama `processar_eventos()`, `atualizar()` e `desenhar()` |


## 🤖 Uso de Inteligência Artificial

A IA gerou a estrutura inicial do código em pygame com base em uma versão inicial só com a estrutura logica pronta, nos ajudou a criar as mensagens de noticia e revisou nosso código. O grupo implementou as regras do jogo, tomou as decisões de design como oque iria ocorrer caso uma noticia falsa fosse validada, passasse sem nenhuma analise, etc, testou e documentou o projeto.
