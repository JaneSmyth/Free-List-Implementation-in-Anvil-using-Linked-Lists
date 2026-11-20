from ._anvil_designer import FirstFitAllocationTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class FirstFitAllocation(FirstFitAllocationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

  @handle("submit_btn", "click")
  def submit_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      requested_memory = int(self.size_textbox.text)
    except ValueError:
      alert("Please enter a valid whole number")
      return
    if requested_memory <= 0:
      alert("Memory size must be greater than 0")
      return
    response = anvil.server.call('firstFitAlloc',requested_memory)
    alert(response.strip())
    open_form('DisplayList')
    
  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('StartMenu')
