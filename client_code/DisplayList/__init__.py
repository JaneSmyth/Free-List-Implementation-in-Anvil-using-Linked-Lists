from ._anvil_designer import DisplayListTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DisplayList(DisplayListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    #calls the function to get a list of the nodes, which are then displayed in a repeating panel
    self.repeating_panel_1.items = anvil.server.call('get_nodes')

  @handle("menu_btn", "click")
  def menu_btn_click(self, **event_args):
    open_form('StartMenu')
