from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


\\webhook_url = "webwook"
mensagens_enviadas = set()
log_file = "log_mensagens.txt"


def escrever_log(texto):
    with open(log_file, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{texto}\n")
    print(texto)


navegador = webdriver.Chrome()
wait = WebDriverWait(navegador, 30)

navegador.get("https://impactoautomacao.com.br/suporte")


def entrar_no_iframe_chat(driver, timeout=30):
    wait_local = WebDriverWait(driver, timeout)
    iframe = wait_local.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
    )
    driver.switch_to.frame(iframe)


def enviar_mensagem(texto):
    campo = wait.until(EC.presence_of_element_located((By.ID, "msgarea")))
    campo.click()
    campo.clear()
    campo.send_keys(texto)

    botao = wait.until(EC.element_to_be_clickable((By.ID, "sqico-send")))
    botao.click()


# ===================== INICIAR CHAT =====================
# botão flutuante
botao_chat = wait.until(
    EC.element_to_be_clickable((By.ID, "woot-widget--expanded__text"))
)
botao_chat.click()

# entrar no iframe
entrar_no_iframe_chat(navegador)

# botão "Iniciar Conversa"
botao_iniciar = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Iniciar Conversa')]"))
)
botao_iniciar.click()


campo_nome = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[@name='fullName']")
    )
)
campo_nome.click()
campo_nome.send_keys("Carlos")


campo_email = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[@name='emailAddress']")
    )
)
campo_email.click()
campo_email.send_keys("carlo.eduardo@gmail.com")

campo_cnpj = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[@name='cnpj_consulta']")
    )
)
campo_cnpj.click()
campo_cnpj.send_keys("31.282.650/0001-09")


campo_telefone = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[@name='phoneNumber']")
    )
)
campo_telefone.click()
campo_telefone.send_keys("40028922")
campo_mesage = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//textarea[@placeholder='Por favor, digite sua mensagem']")

    )
)
campo_mesage.click()
campo_mesage.send_keys("Preciso de Ajuda")


def esperar_botao_habilitar():
    wait.until(
        lambda d: d.find_element(
            By.XPATH, "//button[.//text()[contains(., 'Iniciar Conversa')]]"
        ).is_enabled()
    )

esperar_botao_habilitar()

botao = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Iniciar Conversa')]"))
)
botao.click()


def esperar_botao_suporte():
    wait.until(
        lambda d: d.find_element(
            By.XPATH, "//button[.//text()[contains(., '🛠️ Suporte')]]"
        ).is_enabled()
    )

esperar_botao_suporte()

opcao_suporte = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., '🛠️ Suporte')]"))
)
opcao_suporte.click()

print("Monitorando mensagens...")


# ===================== MONITORAMENTO =====================
def aguardar_nova_mensagem(driver, qtd_atual, timeout=90):
    WebDriverWait(driver, timeout).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "span.siq-message")) > qtd_atual
    )


while True:
    try:
        mensagens = navegador.find_elements(By.CSS_SELECTOR, "span.siq-message")
        qtd_atual = len(mensagens)

        aguardar_nova_mensagem(navegador, qtd_atual)

        mensagens = navegador.find_elements(By.CSS_SELECTOR, "span.siq-message")
        ultima = mensagens[-1].text.strip()

        if ultima and ultima not in mensagens_enviadas:
            escrever_log(f"Enviando ao webhook: {ultima}")

            resposta = requests.post(webhook_url, json={"mensagem": ultima})
            mensagens_enviadas.add(ultima)

            retorno = resposta.json()
            resposta_texto = retorno.get("output", "").strip()

            if resposta_texto:
                enviar_mensagem(resposta_texto)
                escrever_log(f"Resposta enviada: {resposta_texto}")

    except Exception as e:
        escrever_log(f"Erro no monitoramento: {e}")

    time.sleep(5)

