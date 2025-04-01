# Config App for the Value Api
This streamlit app provides a simple frontend application for the [Value Api](https://github.com/ValueAPI/Server) to store values (e.g., configs) in the web.

## Install

### Python package
```
pip install valueapifrontend 
```

### Docker
See [Deployment](https://github.com/ValueAPI/Deployment).

## Start the frontend app

### With the cli
```
valueapifrontend
```

### Directly with streamlit
```
streamlit run src/valueapifrontend/app.py <value-api-url> <context>
```
