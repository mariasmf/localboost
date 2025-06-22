mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"mfernandahelpdesk@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
enableCORS = false\n\
headless = true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
