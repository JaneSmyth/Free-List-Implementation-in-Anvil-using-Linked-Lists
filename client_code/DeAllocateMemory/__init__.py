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

  @handle("submit_btn", "click")
  def submit_btn_click(self, **event_args):
    try: #try to convert the input to integer
      size = int(self.size_textbox.text)
      address = int(self.address_textbox.text)
    except ValueError: #if it isnt possible due to invalid input, throw error
      Notification("Please enter valid whole numbers",timeout=5).show()
      return
    if size <= 0 or address < 0:
      Notification("Size must be greater than 0",timeout=5).show()
      return
    response = anvil.server.call('deallocate', address, size)
    Notification(response,timeout=5).show()
    if response != "Memory location already in use":
      open_form('DisplayList')

  @handle("menu_btn", "click")
  def menu_btn_click(self, **event_args):
    open_form('StartMenu')
