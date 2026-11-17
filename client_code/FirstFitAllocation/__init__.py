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

    # Any code you write here will run before the form opens.

  @handle("submit_btn", "click")
  def submit_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    requested_memory = int(self.size_textbox.text)
    anvil.server.call('firstFitAlloc',requested_memory)
