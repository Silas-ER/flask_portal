import pywhatkit as whats

def enviar_mensagem(nome, telefone, email, tipo, setor, problema):
    telefone_destinatario = ["+5584999889418", "+5584988748879"]
    
    mensagem = f"Nova solicitação! {nome} do setor {setor}, precisa de {tipo} e está com seguinte relato: {problema}, os contatos dele são: {telefone}, {email}"

    # Envie a mensagem
    for destinatario in telefone_destinatario:
        whats.sendwhatmsg_instantly(destinatario, mensagem, 10) 
