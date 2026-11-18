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
  current = get_head()
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
  #insert a block back into the free list
  newNodeId = next_available_ID()
  current = get_head()
  successMsg = "Memory block deallocated"
  if current is None: #empty list insertion
    app_tables.memorytable.add_row(ID=1, Address=address, Size=size, Next=None)
    app_tables.memorytablehead.add_row(HeadID=1)
    return successMsg
  if address == current['Address']:
    return "Memory location already in use"
  if address < current['Address']: #insertion at head of list
    app_tables.memorytable.add_row(ID=newNodeId, Address=address, Size=size, Next=current['ID'])
    app_tables.memorytablehead.get().update(HeadID = newNodeId)
    return successMsg
    
  while(current['Next'] is not None): #traversing to find where it should slot in, in order. Looking one place ahead. 
    nextNode = app_tables.memorytable.get(ID=current['Next'])
    if nextNode['Address'] == address:
      return "Memory location already in use"
    if nextNode['Address'] > address:
      break
    current = nextNode
  #inserting block in to its ordered place in the list  
  app_tables.memorytable.add_row(ID=newNodeId, Address=address, Size=size, Next=current['Next'])
  current.update(Next=newNodeId) #set next value to the new node we inserted 
  return successMsg
  
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
      return ("Address of allocated memory block:", addOfBlock, " of size:", size)
    if (current['Size'] == size):
      addOfBlock = current['Address']
      print("equal to")
      if previous is None:
        app_tables.memorytablehead.get().update(HeadID =current['Next'])
      else:
        previous.update(Next = current['Next'])
      current.delete()
      return ("Address of allocated memory block:", addOfBlock, " of size:", size)
    previous = current
    current = app_tables.memorytable.get(ID=current['Next'])
  return "There is not enough memory available"

@anvil.server.callable
def worstFitAlloc(size):
  head = get_head()
  current = head
  if(current is None):
    return "There is not enough memory available"
  previous = None
  largestNode = current
  largestPrev = None
  while(current is not None):
    if(current['Size'] > largestNode['Size']):
      largestNode = current
      largestPrev = previous
    previous = current
    current = app_tables.memorytable.get(ID=current['Next'])
  if(largestNode['Size'] > size):
    #removing it from the end
    newSize = largestNode['Size'] - size
    addOfBlock = largestNode['Address'] + newSize
    largestNode.update(Size = newSize)
    return ("Address of allocated memory block:", addOfBlock, " of size:", size)

  elif (largestNode['Size'] == size):
    addOfBlock = largestNode['Address']
    if largestPrev is None:
      app_tables.memorytablehead.get().update(HeadID =largestNode['Next'])
    else:
      largestPrev.update(Next = largestNode['Next'])
    largestNode.delete()
    return ("Address of allocated memory block:", addOfBlock, " of size:", size)