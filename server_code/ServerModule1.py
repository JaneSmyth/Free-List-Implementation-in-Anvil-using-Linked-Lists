import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_head():
  #gets the first row of the table that stores what "head" is
  headIDRow = app_tables.memorytablehead.get()
  if headIDRow is None:
    return None #if there is no head, list is empty, returns null
  return app_tables.memorytable.get(ID=headIDRow['HeadID'])

@anvil.server.callable
def get_nodes():
  nodes_list = []
  current = get_head() 
  while(current is not None):
    #traverses through the database and appends each node to the nodes_list variable
    nodes_list.append(current)
    #checks the 'next' pointer of the current node, assigns it to the variable "next"
    next = current['Next']
    if next is None:
      break #checks if we are at the last node in the list
  #current is assigned to the node whos id is equal to the next pointer of current node
  #i.e. current = current.next
    current = app_tables.memorytable.get(ID=next) 
  return nodes_list

def next_available_ID():
  #rows contains all data in the memory table 
  rows = app_tables.memorytable.search()
  #gets all the id's of rows in the database
  existing_IDs = [row['ID'] for row in rows if row['ID'] is not None]
  if not existing_IDs:
    return 1 #if there are no id's then return 1.
    #This is used to make the first node in the table have an ID of 1
  else:
    return max(existing_IDs)+1 #otherwise gets the max ID, and adds 1 to it
    #This is used to give new nodes their ID 
  
@anvil.server.callable
def deallocate(address,size):
  #inserts a memory block back into the free list
  newNodeId = next_available_ID() 
  current = get_head()
  successMsg = "Memory block deallocated"
  if current is None: #Insert into empty list
    #Insert node into the table, setting 'next' to null
    app_tables.memorytable.add_row(ID=newNodeId, Address=address, Size=size, Next=None)
    #Update head variable to new node
    app_tables.memorytablehead.add_row(HeadID=1)
    return successMsg
  if address == current['Address']: #Deallocate an address that is already in the free list
    return "Memory location already in use"
  if address < current['Address']: #Insert at head of list
    app_tables.memorytable.add_row(ID=newNodeId, Address=address, Size=size, Next=current['ID'])
    app_tables.memorytablehead.get().update(HeadID = newNodeId) #head is set to new node
    return successMsg
  while(current['Next'] is not None): #Traverse to find insert slot, in order. Looking one place ahead. 
    nextNode = app_tables.memorytable.get(ID=current['Next'])
    if nextNode['Address'] == address:
      return "Memory location already in use"
    if nextNode['Address'] > address: 
      break  #loop breaks when the next address is greater than insertion address, proceeds to the node inserting process
    current = nextNode
  #Inserting process. New nodes next is set to current.next. This insertion also covers nodes at the end of the list
  app_tables.memorytable.add_row(ID=newNodeId, Address=address, Size=size, Next=current['Next'])
  current.update(Next=newNodeId) #sets current.next value to the new node we inserted 
  return successMsg
  
@anvil.server.callable
def firstFitAlloc(size):
  current = get_head()
  previous = None
  while(current is not None):
    if(current['Size'] > size):
      #removing it from the end
      newSize = current['Size'] - size
      addOfBlock = current['Address'] + newSize
      current.update(Size = newSize)
      return f"Allocated memory address: {addOfBlock}\nsize: {size}"
    if (current['Size'] == size):
      addOfBlock = current['Address']
      if previous is None:
        app_tables.memorytablehead.get().update(HeadID =current['Next'])
      else:
        previous.update(Next = current['Next'])
      current.delete()
      return f"Allocated memory address: {addOfBlock}\nsize: {size}"
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
    return f"Allocated memory address: {addOfBlock}\nsize: {size}"
  if (largestNode['Size'] == size):
    addOfBlock = largestNode['Address']
    if largestPrev is None:
      app_tables.memorytablehead.get().update(HeadID =largestNode['Next'])
    else:
      largestPrev.update(Next = largestNode['Next'])
    largestNode.delete()
    return f"Allocated memory address: {addOfBlock}\nsize: {size}"
  return "There is not enough memory available"