import os
import streamlit.components.v1 as components
from typing import Optional

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True


if not _RELEASE:
    _streamlit_grid = components.declare_component(
        "streamlit-grid",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _streamlit_grid = components.declare_component("streamlit-grid", path=build_dir)



class GridItem:
    """
    Represents a single cell in the grid.
    """

    label: str
    row_span: Optional[int] = 1
    col_span: Optional[int] = 1
    text_color: Optional[str] = None
    background_color: Optional[str] = None

    def __init__(
            self, 
            label: str, *, 
            col_span: Optional[int] = 1,
            row_span: Optional[int] = 1, 
            text_color: Optional[str] = None, 
            background_color: Optional[str] = None, 
        ):
        self.label = label
        self.row_span = row_span
        self.col_span = col_span
        self.text_color = text_color
        self.background_color = background_color

        pass   
    

def streamlit_grid(
        grid_layout: list[list[GridItem]], 
        *,
        columns: Optional[int] = 4,  
        gap: Optional[int] = 10,  
        width: Optional[int] = 500,  
        cell_height: Optional[int] = 10,
        background_color: Optional[str] = None,
        use_container_width: Optional[bool] = False,
        key: Optional[str] = None,
    ) -> str:
    
    """
    Renders a grid layout with customizable cells in a Streamlit app.

    Args:
        grid_layout (List[List[GridItem]]): A 2D list representing rows of GridItem objects.
        columns (Optional[int]): Number of columns in the grid. Default is 4.
        gap (Optional[int]): Gap between grid items (in pixels). Default is 10.
        width (Optional[int]): Width of the grid container (in pixels). Default is 500.
        cell_height (Optional[int]): Height of each cell. Default is 10.
        background_color (Optional[str]): Background color for the grid container.
        use_container_width (Optional[bool]): Whether to override width with the width of the parent container.
        key (Optional[str]): A unique key for the component state.

    Returns:
        str: The last clicked or selected value from the grid.
    """
     
    return _streamlit_grid(
        grid_layout=[[item.__dict__ for item in row] for row in grid_layout], 
        columns=columns, 
        gap=gap, 
        wisth=width,
        cell_height=cell_height, 
        background_color=background_color,
        key=key,
        use_container_width=use_container_width,
        default='',
    )

