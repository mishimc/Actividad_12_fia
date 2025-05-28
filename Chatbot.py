from openai import OpenAI
import streamlit as st
import pandas as pd

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 My ChatBot")
st.caption("🚀 Preguntas y respuestas ")

# Cargar datos
df = pd.read_csv("https://raw.githubusercontent.com/mishimc/Actividad_12_fia/refs/heads/main/Fish.csv")

# Mostrar TODA la tabla (con opción de scroll)
st.subheader("📊 Dataset completo de peces")
st.dataframe(df)  # Muestra la tabla completa con scroll

# Mensaje del sistema (para forzar respuestas solo sobre los datos)
system_prompt = f"""
Eres un analista de datos especializado en el dataset 'Fish'. 
Solo responde preguntas estrictamente relacionadas con estos datos. 

Si te preguntan algo no relacionado, responde:
"❌ Solo puedo responder preguntas sobre el dataset de peces. Ejemplos:"
- "¿Cuál es el peso promedio de las especies?"
- "¿Qué especie tiene la mayor longitud vertical?"

Columnas disponibles: {', '.join(df.columns)}
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Hola 👋, pregúntame sobre el dataset de peces. ¡Tengo todos los datos aquí!"}
    ]

# Mostrar historial de chat
for msg in st.session_state.messages:
    if msg["role"] != "system":  # No mostrar el prompt del sistema
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Por favor, ingresa tu API key de OpenAI en la barra lateral.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        msg = response.choices[0].message.content
    except Exception as e:
        msg = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)