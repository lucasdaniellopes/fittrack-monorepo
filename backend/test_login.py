#!/usr/bin/env python3
"""
Teste simples para verificar se o login JWT customizado está funcionando
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_login():
    """Testa o endpoint de login customizado"""
    
    # Dados de teste (você pode ajustar com credenciais reais)
    login_data = {
        "username": "admin",  # Altere para um usuário existente
        "password": "admin123"  # Altere para a senha correta
    }
    
    print("🔑 Testando login JWT customizado...")
    print(f"URL: {BASE_URL}/api/v1/token/")
    print(f"Dados: {login_data}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/token/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login realizado com sucesso!")
            print("\n📝 Dados retornados:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verificar se os dados do usuário estão presentes
            if 'user' in data:
                print("\n✅ Dados do usuário encontrados no token!")
                user_data = data['user']
                print(f"   - ID: {user_data.get('id')}")
                print(f"   - Username: {user_data.get('username')}")
                print(f"   - Email: {user_data.get('email')}")
                
                if 'perfil' in user_data:
                    print(f"   - Tipo de perfil: {user_data['perfil'].get('tipo')}")
                    
                    # Verificar dados específicos do tipo
                    perfil_tipo = user_data['perfil'].get('tipo')
                    if perfil_tipo in user_data:
                        print(f"   - Dados do {perfil_tipo}: {user_data[perfil_tipo]}")
            else:
                print("❌ Dados do usuário não encontrados na resposta!")
                
        elif response.status_code == 401:
            print("❌ Credenciais inválidas!")
            print("💡 Dica: Verifique se o usuário existe e a senha está correta")
            
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao servidor!")
        print("💡 Dica: Verifique se o servidor Django está rodando em http://localhost:8000")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_me_endpoint():
    """Testa o endpoint /me com token JWT"""
    
    print("\n" + "="*50)
    print("🔍 Testando endpoint /me...")
    
    # Primeiro fazer login para obter o token
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        # Fazer login
        login_response = requests.post(
            f"{BASE_URL}/api/v1/token/",
            json=login_data
        )
        
        if login_response.status_code != 200:
            print("❌ Não foi possível fazer login para testar o endpoint /me")
            return
            
        token_data = login_response.json()
        access_token = token_data.get('access')
        
        if not access_token:
            print("❌ Token de acesso não encontrado na resposta do login")
            return
            
        # Testar endpoint /me
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        me_response = requests.get(
            f"{BASE_URL}/api/v1/users/me/",
            headers=headers
        )
        
        print(f"📊 Status Code: {me_response.status_code}")
        
        if me_response.status_code == 200:
            data = me_response.json()
            print("✅ Endpoint /me funcionando!")
            print("\n📝 Dados do usuário atual:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erro no endpoint /me: {me_response.status_code}")
            print(f"Resposta: {me_response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar endpoint /me: {e}")

if __name__ == "__main__":
    test_login()
    test_me_endpoint()
    
    print("\n" + "="*50)
    print("📚 Como usar no frontend:")
    print("""
    // Fazer login
    const response = await fetch('/api/v1/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin', password: 'admin123' })
    });
    
    const data = await response.json();
    
    // Agora você tem:
    // - data.access (token JWT)
    // - data.refresh (token de refresh)
    // - data.user (dados completos do usuário)
    
    // Armazenar no localStorage/sessionStorage
    localStorage.setItem('token', data.access);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    // Para requests autenticadas
    const authResponse = await fetch('/api/v1/users/me/', {
        headers: { 'Authorization': `Bearer ${data.access}` }
    });
    """)