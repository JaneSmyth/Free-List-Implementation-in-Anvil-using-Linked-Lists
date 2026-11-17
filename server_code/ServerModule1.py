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
  newNodeId = next_available_ID()
  head = get_head()
  current = head
  if current is None:
    app_tables.memorytable.add_row(ID=1, Address=address, Size=size, Next=None)
    app_tables.memorytablehead.add_row(HeadID=1)
    return 
  if address < current['Address']:
    app_tables.memorytable.add_row(ID=newNodeId, Address=address, Size=size, Next=current['ID'])
    app_tables.memorytablehead.get().update(HeadID = newNodeId)
    return
  while(current['Next'] is not None):
    nextNode = app_tables.memorytable.get(ID=current['Next'])
    if nextNode['Address'] >= address:
      break
    current = nextNode
    
  app_tables.memorytable.add_row(ID=newNodeId, Address=address, Size=size, Next=current['Next'])
  current.update(Next=newNodeId)
   # print("address", address, "currentNode", current, "currentaddress",currentAddress, "END")

@anvil.server.callable
def firstFitAlloc(size):
  head = get_head()
  current = head
  previous = None
  while(current is not None):
    if(current['Size'] > size):
      #removing it from the end
      newSize = current['Size'] - size
      addOfBlock = current['Address'] + newSize
      current.update(Size = newSize)
      return print("curent add:", current['Address'],"block add:", addOfBlock, "new size:", newSize)
    if (current['Size'] == size):
      addOfBlock = current['Address']
      print("equal to")
      if previous is None:
        app_tables.memorytablehead.get().update(HeadID =current['Next'])
      else:
        previous.update(Next = current['Next'])
      current.delete()
      return print(addOfBlock)
    previous = current
    current = app_tables.memorytable.get(ID=current['Next'])
  return print("There is not enough memory for this")

@anvil.server.callable
def worstFitAlloc(size):
  head = get_head()
  current = head
  previous = None
  largestNode = current
  while(current is not None):
    if(current['Size'] > largestNode):
      largestNode = current
    current = app_tables.memorytable.get(ID=current['Next'])
  if(size == largestNode['Size']):
    #if the node we want is the same size as the amount of mem we need
    addOfBlock = largestNode['Address']
    if(largestNode == head):
      if
      
