import streamlit as st
from __init__ import streamlit_grid, GridItem
# from streamlit_grid import streamlit_grid, GridItem

st.set_page_config(
    page_title="Streamlit Grid Example",
    page_icon=":material/space_dashboard:",
    layout="centered",
)


st.subheader("Streamlit Grid Example")

grid = [
    [GridItem("C", col_span=2, background_color="red", text_color="white"), GridItem("/"), GridItem("*")],
    [GridItem("7"), GridItem("8"), GridItem("9"), GridItem("-")],
    [GridItem("4"), GridItem("5"), GridItem("6"), GridItem("+", row_span=2)],
    [GridItem("1"), GridItem("2"), GridItem("3")],
    [GridItem("0"), GridItem("00"), GridItem("."), GridItem("=", background_color="#2B90DE", text_color="white")],
]


selected_value = streamlit_grid(
    grid_layout=grid, 
    columns=4, 
    gap=5, 
    cell_height=20,
    background_color="#ccc",
)

st.write(f"#### You clicked: {selected_value}")

