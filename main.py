# -*- coding: utf-8 -*-

import hashlib
import requests
import json


alfabeto = [letra for letra in 'abcdefghijklmnopqrstuvwxyz']
TOKEN = '505e6e4d981bd4320689f57334c2e9928396fd8b'


def descriptografar(texto, chave, resultado=''):
    for letra in texto:
        
        if letra not in alfabeto:
            resultado += letra

        else:
            indice = alfabeto.index(letra)
            indice_nova_letra = indice - chave

            resultado += alfabeto[indice_nova_letra]          
    
    return resultado


def resumo_criptografico(texto):
    hash = hashlib.sha1()

    hash.update(texto)

    return hash.hexdigest()


def requsicao():
    resposta = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}'.format(TOKEN))
    
    conteudo = {
        "numero_casas": resposta.json()['numero_casas'],
        "token": resposta.json()['token'],
        "cifrado": resposta.json()['cifrado'],
        "decifrado": resposta.json()['decifrado'],
        "resumo_criptografico": resposta.json()['resumo_criptografico']
    }

    return conteudo


def postar(arquivo):

    multipart_form_data = {
        'answer': arquivo
    }

    r = requests.post(
        url='https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}'.format(TOKEN),
        files=multipart_form_data
    )
    
    if r.ok:
        print(r.content)
    else:
        print("Falha na conexão!")


def montar(conteudo):
    novo_conteudo = conteudo

    texto_descriptografado = descriptografar(
                                texto=conteudo['cifrado'], 
                                chave=conteudo['numero_casas']
                                )

    novo_conteudo['decifrado'] = texto_descriptografado
    novo_conteudo['resumo_criptografico'] = resumo_criptografico(
                                                    texto=texto_descriptografado
                                                    )

    with open('answer.json', 'w') as f:
        json.dump(novo_conteudo, f)


if __name__ == "__main__":
    montar(conteudo=requsicao())
    arquivo = open('answer.json', 'r')
    postar(arquivo)