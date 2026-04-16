# Autobot de Atendimento

Bot de atendimento automatizado que monitora um chat de suporte em tempo real, encaminha mensagens para um fluxo de IA no **N8N** e responde automaticamente com base em uma base de conhecimento configurada.

---

## Sobre o Projeto

O Autobot de Atendimento é uma solução de automação desenvolvida em Python com Selenium que simula um atendente humano em um widget de chat ao vivo. O bot:

1. Acessa o site de suporte automaticamente
2. Preenche o formulário de início de conversa
3. Seleciona a opção de **Suporte**
4. Monitora novas mensagens em tempo real
5. Encaminha cada mensagem recebida para um **webhook no N8N**
6. O N8N processa a mensagem consultando uma base de dados configurada e retorna a resposta
7. O bot envia a resposta de volta ao chat automaticamente

---

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal |
| Selenium | Automação do navegador (Chrome) |
| Requests | Comunicação HTTP com o webhook |
| N8N | Orquestração do fluxo de IA e base de conhecimento |

---

## Pré-requisitos

- Python 3.8+
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/downloads) compatível com a versão do seu Chrome
- N8N configurado com o fluxo e base de conhecimento
- Acesso ao site de suporte alvo

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/KevenDebug/Autobot-de-Atendimento.git
   cd Autobot-de-Atendimento
   ```

2. **Instale as dependências:**
   ```bash
   pip install selenium requests
   ```

3. **Configure o ChromeDriver:**

   Certifique-se de que o `chromedriver` está no seu PATH ou na raiz do projeto.

---

## Configuração

No arquivo principal do bot, localize e ajuste as seguintes variáveis:

```python
# URL do webhook configurado no N8N
webhook_url = "SUA_URL_DO_WEBHOOK_AQUI"

# Dados do formulário de início de conversa
campo_nome.send_keys("Seu Nome")
campo_email.send_keys("seuemail@exemplo.com")
campo_cnpj.send_keys("00.000.000/0001-00")
campo_telefone.send_keys("00000000000")
```

>  **Importante:** O webhook do N8N deve estar configurado para receber um JSON com o campo `"mensagem"` e retornar um JSON com o campo `"output"` contendo a resposta gerada pela IA.

### Exemplo de payload enviado ao N8N:
```json
{
  "mensagem": "Preciso de ajuda com meu boleto"
}
```

### Exemplo de resposta esperada do N8N:
```json
{
  "output": "Olá! Para dúvidas sobre boletos, acesse a área financeira do seu painel."
}
```

---

## Como Executar

```bash
python autobot.py
```

O bot irá:
- Abrir o Chrome automaticamente
- Navegar até o site de suporte
- Preencher e iniciar a conversa
- Entrar em modo de monitoramento contínuo

Todas as mensagens trocadas serão salvas no arquivo `log_mensagens.txt`.

---

## Estrutura do Projeto

```
Autobot-de-Atendimento/
│
├── autobot.py            # Script principal do bot
├── log_mensagens.txt     # Log gerado automaticamente em execução
└── README.md
```

---

## Fluxo de Funcionamento

```
Site de Suporte (Chat)
        │
        │ Nova mensagem detectada
        ▼
   Bot (Selenium)
        │
        │ POST { "mensagem": "..." }
        ▼
   Webhook N8N
        │
        │ Consulta base de conhecimento
        ▼
   Resposta { "output": "..." }
        │
        │ Envia resposta ao chat
        ▼
   Site de Suporte (Chat)
```

---

## Logs

O bot registra todas as ações no arquivo `log_mensagens.txt`:

```
Enviando ao webhook: Preciso de ajuda com meu boleto
Resposta enviada: Olá! Para dúvidas sobre boletos...
Erro no monitoramento: Message: no such element
```

---

## Observações

- O bot mantém um **controle de mensagens já enviadas** para evitar duplicatas.
- Em caso de erro durante o monitoramento, o bot registra o erro e continua operando.
- O intervalo de verificação padrão é de **5 segundos**.
- O fluxo N8N deve ser configurado **separadamente** com a base de dados e a lógica de resposta desejada.

---

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

---

## Autor

Desenvolvido por [KevenDebug](https://github.com/KevenDebug)
