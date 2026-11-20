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
    try: #try to convert the input to integer
      requested_memory = int(self.size_textbox.text)
    except ValueError: #if it isnt possible due to invalid input, throw error
      Notification("Please enter a valid whole number").show()
      return
    if requested_memory <= 0: 
      Notification("Memory size must be greater than 0").show()
      return
    response = anvil.server.call('firstFitAlloc',requested_memory)
    Notification(response).show()
    open_form('DisplayList')
    
  @handle("menu_btn", "click")
  def menu_btn_click(self, **event_args):
    open_form('StartMenu') 
