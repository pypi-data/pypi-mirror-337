# Streamlit Grid

Streamlit Grid is a **custom Streamlit component** that allows you to create interactive **grid layouts** in your Streamlit apps. It supports row and column spanning, custom colors, and dynamic layouts.

## Features
- 🟦 **Grid-based layout** for Streamlit
- 🔢 **Supports row and column spanning**
- 🎨 **Customizable cell colors**
- ⚡ **Easy integration** into Streamlit apps

---

## Installation

```sh
pip install streamlit-grid
```

---

## Usage

```python
import streamlit as st
from streamlit_grid import streamlit_grid, GridItem

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
```

---

## Parameters

| Parameter        | Type                 | Description                                 | 
|------------------|----------------------|---------------------------------------------|
| grid_layout      | List[List[GridItem]] | A **2D list** representing the grid layout. |
| columns          | int (Optional)       | Number of columns in the grid.              |
| gap              | int (Optional)       | Gap between grid items (in pixels).         |
| cell_height      | int (Optional)       | Height of each grid cell.                   |
| background_color | str (Optional)       | Background color of the grid container.     |
| key              | str (Optional)       | Unique key for the component state.         |

---

## GridItem Options

| Attribute        | Type           | Description                       |
|------------------|----------------|-----------------------------------|
| label            | str            | Text inside the cell.             |
| background_color | str (Optional) | Background color of the cell.     |
| text_color       | str (Optional) | Text color inside the cell.       |
| row_span         | int (Optional) | Number of rows the cell spans.    |
| col_span         | int (Optional) | Number of columns the cell spans. |

---

## Example Output
The following example creates a calculator-style grid:

![Example Grid](https://via.placeholder.com/600x400)

---

## Contributing
We welcome contributions! To contribute:

1. **Ensure you have the necessary dependencies installed:**
   - [Python 3.6+](https://www.python.org/downloads/)
   - [Node.js](https://nodejs.org)
   - [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

2. **Clone the repository:**
   ```sh
   git clone https://github.com/syedahoorainali/streamlit-grid-component.git
   ```

3. **Set up the Python environment:**
   ```sh
   cd streamlit-grid-component
   python3 -m venv venv  # Create virtual environment
   . venv/bin/activate   # Activate virtual environment
   pip install streamlit  # Install Streamlit
   pip install -e .  # Install package in editable mode
   ```

4. **Run the Streamlit app:**
   ```sh
   streamlit run streamlit_grid/example.py
   ```

5. **Set up and run the frontend component:**
   ```sh
   cd streamlit_grid/frontend
   npm install  # Install dependencies
   npm run start  # Start Webpack dev server
   ```

6. **Make changes to the component:**
   - Modify the **frontend** code in `streamlit_grid/frontend/src/StreamlitGrid.tsx`
   - Modify the **backend** Python code in `streamlit_grid/__init__.py`

7. **Build the frontend:**
   ```sh
   npm run build
   ```

8. **Submit a pull request** 🚀

---

## License
This project is licensed under the **MIT License**.

