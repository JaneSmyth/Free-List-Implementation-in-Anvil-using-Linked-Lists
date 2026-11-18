from ._anvil_designer import DeAllocateMemoryTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DeAllocateMemory(DeAllocateMemoryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      size = int(self.size_textbox.text)
      address = int(self.address_textbox.text)
    except ValueError:
      alert("Please enter valid whole numbers in both boxes")
      return
    if size <= 0 or address < 0:
      alert("Size must be greater than 0 and address cannot be negative")
      return
    response = anvil.server.call('deallocate', address, size)
    alert(response)
    open_form('DisplayList')

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('StartMenu')
