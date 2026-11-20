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
    #Drop down menu opens the corresponding pages when selected
    menu_item = self.drop_down_menu.selected_value
    if(menu_item == "Display Free Memory List"):
      open_form("DisplayList")
    if(menu_item == "Allocate Memory - First Fit"):
      open_form('FirstFitAllocation')
    if(menu_item == "Allocate Memory - Worst Fit"):
      open_form('WorstFitAllocation')
    if(menu_item == "Deallocate Memory"):
      open_form('DeAllocateMemory')
