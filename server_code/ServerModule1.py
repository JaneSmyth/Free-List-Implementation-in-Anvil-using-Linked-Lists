import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_head():
  headIDRow = app_tables.memorytablehead.get()
  if headIDRow is None:
    return None
  return app_tables.memorytable.get(ID=headIDRow['HeadID'])
  
@anvil.server.callable
def get_nodes():
  linked_list = []
  head = get_head()
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

def next_available_ID():
  rows = app_tables.memorytable.search()
  existing_IDs = [row['ID'] for row in rows if row['ID'] is not None]
  if not existing_IDs:
    return 1
  else:
    return max(existing_IDs)+1
  
@anvil.server.callable
def deallocate(address,size):
  head = get_head()
  current = head
  if current is None:
    app_tables.memorytable.add_row(ID=1, Address=address, Size=size, Next=None)
    app_tables.memorytablehead.add_row(HeadID=1)
    return 
  #currentAddress = current['Address']
  while(current['Next'] is not None):
    nextNode = app_tables.memorytable.get(ID=current['Next'])
    if nextNode['Address'] >= address:
      break
    current = nextNode
    
  newNodeID = next_available_ID()
  app_tables.memorytable.add_row(ID=newNodeID, Address=address, Size=size, Next=current['Next'])
  current.update(Next=newNodeID)
   # print("address", address, "currentNode", current, "currentaddress",currentAddress, "END")


  