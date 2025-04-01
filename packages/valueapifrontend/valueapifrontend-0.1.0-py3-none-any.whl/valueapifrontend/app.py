import sys
import os
import signal
import urllib.parse
import streamlit as st
from valueapiconnector import ValueDataType, ValueAPIConnector
import json
import pandas as pd


if len(sys.argv) < 2:
    print("Call this streamlit application with 2 paramters:")
    print("1. URL of the value api: see https://github.com/ValueAPI/Server")
    print("2. A root context")
    os.kill(os.getpid(), signal.SIGKILL)

base_url = sys.argv[1]
root_context = sys.argv[2]

api = ValueAPIConnector(base_url)

hide_menu_style = "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stAppDeployButton {visibility: hidden}</style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)

with st.spinner():
    c_context_config = api.get_context(f"{root_context}_context_config")
    v_contextes = c_context_config.get_value("contextes", ValueDataType.STRING_LIST)
    contextes = v_contextes.pull()
    if contextes.is_error:
        st.error(f"No connection to the server: {contextes.error}")
        st.stop()
    else:
        contextes = contextes.unwrap()
    with st.sidebar:
        st.header(f"Root Context: `{root_context}`")
        selected_context = st.selectbox("Context", contextes, key="context_selection")

        def reset():
            st.session_state.context_selection = None

        if selected_context:
            selected_context = selected_context.replace("/", "-")
            st.button("Reset", on_click=reset)
            st.write(
                f"Context: `{root_context}_{urllib.parse.quote(selected_context)}`"
            )
            delete_context = st.button("Delete Context")
            if delete_context:
                contextes = tuple([c for c in contextes if c != selected_context])
                v_contextes.push(tuple(sorted(set(contextes))))
                st.toast("Deleted")
                st.rerun()
        else:
            new_context = st.text_input("New Context", key="new_context_input")
            if new_context:
                contextes += (new_context,)
                v_contextes.push(list(sorted(set(contextes))))
                st.rerun()
    if not selected_context:
        st.warning("Please select a context")
        st.stop()

selected_value = None
auth_token = None
# TODO: handle auth_token for the selected context
with st.spinner():
    v_available_values = c_context_config.get_value(
        selected_context + "_available_values", ValueDataType.STRING_LIST
    )
    c_value_context = api.get_context(f"{root_context}_{selected_context}")
    values = v_available_values.pull().unwrap()
    with st.sidebar:
        with st.form("new-value-form", clear_on_submit=True):
            st.write("Add new value")
            f_value_name = st.text_input("Value Name")
            f_data_type = st.selectbox(
                "Data type",
                [
                    "String",
                    "Integer",
                    "Float",
                    "Boolean",
                    # "Datetime", # FUTURE VERSION!
                    "Date",
                    "Time",
                    "String List",
                    "Integer List",
                    "Float List",
                    "Boolean List",
                    "Json",
                ],
            )
            submitted = st.form_submit_button("Submit")
            if submitted and len(f_value_name) > 0:
                values += (f_value_name + " - - " + f_data_type,)
                v_available_values.push(tuple(sorted(set(values))))

st.header("Values")
if len(values) == 0:
    st.warning("No values in this context. Add a new value.")
else:
    selected_value = st.selectbox("Select a value", values)

if selected_value:
    val_name, val_type = selected_value.split(" - - ")
    val_data_type = {
        "Integer": ValueDataType.INTEGER,
        "Float": ValueDataType.FLOAT,
        "Boolean": ValueDataType.BOOLEAN,
        "Date": ValueDataType.DATE,
        "Time": ValueDataType.TIME,
        "String": ValueDataType.STRING,
        "String List": ValueDataType.STRING_LIST,
        "Integer List": ValueDataType.INTEGER_LIST,
        "Float List": ValueDataType.FLOAT_LIST,
        "Boolean List": ValueDataType.BOOLEAN_LIST,
        "Json": ValueDataType.JSON,
    }[val_type]
    v_value = c_value_context.get_value(val_name, val_data_type)
    val_container = st.container(border=True)
    value = v_value.pull().unwrap()
    val_new = None
    error = False
    match val_type:
        case "String":
            val_new = val_container.text_input(val_name, value)
        case "Integer":
            val_new = val_container.number_input(val_name, None, None, value, step=1)
        case "Float":
            val_new = val_container.number_input(val_name, None, None, value, step=0.01)
        case "Boolean":
            val_new = val_container.checkbox(val_name, value=value)
        case "Date":
            val_new = val_container.date_input(
                val_name, value=value if value is not None else "today"
            )
        case "Time":
            val_new = val_container.time_input(
                val_name, value=value if value is not None else "now"
            )
        case "Json":
            val_new = val_container.text_area(
                val_name, value=json.dumps(value, indent=2), height=300
            )
            try:
                val_new = json.loads(val_new)
            except Exception as e:
                error = True
            val_container.json(val_new)

        case w if w in (
            "String List",
            "Integer List",
            "Boolean List",
            "Float List",
        ):
            val_new = val_container.data_editor(
                pd.DataFrame(
                    [{val_name: val_el} for val_el in value], columns=[val_name]
                ),
                hide_index=True,
                num_rows="dynamic",
            )
            val_new = tuple(val_new[val_name])
    if not error:
        v_value.push(val_new)
    t_plain, t_python_requests, t_python_value_api, t_bash = val_container.tabs([
        "plain",
        "python requests",
        "python value api",
        "bash",
    ])

    t_plain.markdown(f"""
                           ```
                           {v_value.url}
                           ```
                           [Open in a new tab.]({v_value.url})
                           """)
    t_python_requests.markdown(f"""
                           ```python
                           requests.get("{v_value.url}")
                           ```
                           """)
    t_python_value_api.markdown(f"""
                           ```python
                           connector = ValueAPIConnector("{base_url}")
                           context = connector.get_context("{root_context}_{selected_context}")
                           value = context.get_value("{val_name}", {val_data_type}).pull().unwrap()
                           ```
                           """)
    t_bash.markdown(f"""
                           ```shell
                           x=$(curl -s {v_value.url})
                           ```
                           """)
    if auth_token is not None:
        val_container.warning("You need to pass the auth token as well!")
    btn_delete_val = val_container.button("Delete", key=f"delete-val-{val_name}")
    if btn_delete_val:
        v_value.delete()
        values = tuple([v for v in values if v != selected_value])
        v_available_values.push(tuple(sorted(set(values))))
        st.rerun()
