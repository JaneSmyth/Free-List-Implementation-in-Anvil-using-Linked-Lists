from ._anvil_designer import StartMenuTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StartMenu(StartMenuTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)

  @handle("submit_menu", "click")
  def submit_menu_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    print(self.drop_down_menu.selected_value)
    menu_item = self.drop_down_menu.selected_value
    if(menu_item == "Display Free Memory List"):
      open_form("DisplayList")
    if(menu_item == "Allocate Memory - First Fit"):
      pass
    if(menu_item == "Allocate Memory - Worst Fit"):
      pass
    if(menu_item == "Deallocate Memory"):
      open_form('DeAllocateMemory')
