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

#Function removes the memory from the first node that has space. Takes it from end of the block not the start
@anvil.server.callable
def firstFitAlloc(size): 
  current = get_head()
  previous = None
  while(current is not None):
    if(current['Size'] > size): #located node with enough memory for allocation
      newSize = current['Size'] - size #new size of remaining node
      addOfBlock = current['Address'] + newSize #address of block of memory allocated to the user
      current.update(Size = newSize) #set current.size = new size
      return f"Allocated memory address: {addOfBlock}\nsize: {size}"
    if (current['Size'] == size): #located node with exactly the right amount of memory
      addOfBlock = current['Address'] 
      if previous is None: #if we are at the start of the list update head node to current.next
        app_tables.memorytablehead.get().update(HeadID =current['Next']) 
      else:
        previous.update(Next = current['Next']) #set previous nodes 'next' to current.next
      current.delete()
      return f"Allocated memory address: {addOfBlock}\nsize: {size}"
    previous = current #move previous forward one node
    current = app_tables.memorytable.get(ID=current['Next']) #move current forward one node
  return "There is not enough memory available"

#This functions removes the memory from the largest block in the list. Takes it from end of the block not the start
@anvil.server.callable
def worstFitAlloc(size):
  current = get_head()
  if(current is None): #checks if list is empty. Otherwise largestNode['size'] will throw an error
    return "There is not enough memory available"
  previous = None
  largestNode = current
  largestPrev = None
  while(current is not None):
    if(current['Size'] > largestNode['Size']): #finds the node with the most memory
      largestNode = current
      largestPrev = previous #keeps track of the node directly before the largest
    previous = current #current and previous move forward one node for loop to continue
    current = app_tables.memorytable.get(ID=current['Next'])
  if(largestNode['Size'] > size): #if the node has more memory than we need
    newSize = largestNode['Size'] - size #calculate memory leftover
    addOfBlock = largestNode['Address'] + newSize #calculate address of allocated block
    largestNode.update(Size = newSize) #update the size of the remaining node
    return f"Allocated memory address: {addOfBlock}\nsize: {size}"
  if (largestNode['Size'] == size): #if the node has exactly the amount of memory needed
    addOfBlock = largestNode['Address']
    if largestPrev is None: #if we are at the head of the list
      app_tables.memorytablehead.get().update(HeadID =largestNode['Next']) #head is updated to the node after the largest
    else:
      largestPrev.update(Next = largestNode['Next']) #otherwise set the node before the largests to point to the node after the largest
    largestNode.delete()
    return f"Allocated memory address: {addOfBlock}\nsize: {size}"
  return "There is not enough memory available"