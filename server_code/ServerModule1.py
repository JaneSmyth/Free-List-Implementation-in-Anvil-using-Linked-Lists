import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_head():
  

  
@anvil.server.callable
def get_nodes():
  linked_list = []
  #the head of the list is the nodes whos "prev" points to null
  head = app_tables.memorytable.get(Prev=None)

  if head is None:
    return linked_list 
  current = head
  
  while(current is not None):
    linked_list.append(current)
    next = current['Next']
    if next is None:
      break
    current = app_tables.memorytable.get(ID=next)
  return linked_list

@anvil.server.callable
def deallocate(address,size):
  head = app_tables.memorytable.get(Prev=None)
  while(current is not None):
    linked_list.append(current)
    next = current['Next']
    if next is None:
      break
    current = app_tables.memorytable.get(ID=next)
  return linked_list
  