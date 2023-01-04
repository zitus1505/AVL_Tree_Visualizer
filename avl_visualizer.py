from tkinter import *

class Node:
    def __init__(self, value) -> None:
        self.data = value
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self) -> None:
        self.root = None

    def insert(self, value):
        def insert_tree(current, value):
            if current == None:
                return Node(value)
            # Traversal (mencari lokasi yang benar)
            if value < current.data:
                current.left = insert_tree(current.left, value)

            elif value > current.data:
                current.right = insert_tree(current.right, value)
            else:
                display_2.config(text="Duplicated Value in Tree, Try with other value !")

            # = Update height
            current.height = 1 + max(self.getNodeheight(current.left), self.getNodeheight(current.right))

            #  Cek balance
            # Kalo -1 atau 1 = Balance
            balance = self.getNodeheight(current.left) - self.getNodeheight(current.right)
            
            isDoubleRot = False
            # cek apakah perlu rotate
            if balance > 1: #Rotate Right
                balanceL = self.getNodeheight(current.left.left) - self.getNodeheight(current.left.right)
                if balanceL < 0:    #if negative then double rotation
                    current.left = self.rotateLeft(current.left)
                    isDoubleRot = True
                    
                current = self.rotateRight(current)
                if isDoubleRot:
                    L2.config(text="LR Rotation on " + str(current.data))
                else:
                    L2.config(text="RR Rotation on " + str(current.data))
            elif balance < -1:  #Rotate Left
                balanceR = self.getNodeheight(current.right.left) - self.getNodeheight(current.right.right)
                if balanceR > 0:    #if positive then double rotation
                    current.right = self.rotateRight(current.right)
                    isDoubleRot = True
                current = self.rotateLeft(current)
                if isDoubleRot:
                    L2.config(text="LR Rotation on " + str(current.data))
                else:
                    L2.config(text="RR Rotation on " + str(current.data))
            return current

        if self.root == None:
            self.root = Node(value)
        else:
            self.root = insert_tree(self.root, value)

    def rotateLeft(self, x: Node):    #x=root
        newRoot=x.right
        #replace root
        x.right=None
        #posisikan original left of new root di right of x
        if newRoot.left is not None:
            x.right=newRoot.left
        #replace left of new root dengan x
        newRoot.left=x
        #update height
        x.height=max(self.getNodeheight(x.left),self.getNodeheight(x.right))+1
        newRoot.height=max(self.getNodeheight(newRoot.left),self.getNodeheight(newRoot.right))+1
        return newRoot

    def rotateRight(self, x: Node):
        newRoot = x.left
        # replace root
        x.left = None
        # posisikan original right of new root di left of x
        if newRoot.right is not None:
            x.left = newRoot.right
        # replace right of new root dengan x
        newRoot.right = x
        # update height
        x.height = max(self.getNodeheight(x.left), self.getNodeheight(x.right)) + 1
        newRoot.height = max(self.getNodeheight(newRoot.left), self.getNodeheight(newRoot.right)) + 1
        return newRoot

    def getNodeheight(self, node: Node):
        if node is not None:
            return node.height
        else:
            return 0

    def search(self,value):
        if self.root is None:
            return
        queue = []
        queue.append(self.root)
        temp = []
        
        while len(queue) != 0:
            cur: Node = queue.pop(0)
            temp.append(cur.data)
                
            if cur.left != None:
                queue.append(cur.left)

            
            if cur.right != None:
                queue.append(cur.right)
        
        if value not in temp:
            return False
        else:
            return True

    def print_tree(self, val="data", left="left", right="right"):
        if self.root is None:
            # KOSONG ROOT
            return
        def display(root, val=val, left=left, right=right):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            
            # No child.
            if getattr(root, right) is None and getattr(root, left) is None:
                line = '%s' % getattr(root, val)
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if getattr(root, right) is None:
                lines, n, p, x = display(getattr(root, left))
                s = '%s' % getattr(root, val)
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if getattr(root, left) is None:
                lines, n, p, x = display(getattr(root, right))
                s = '%s' % getattr(root, val)
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = display(getattr(root, left))
            right, m, q, y = display(getattr(root, right))
            s = '%s' % getattr(root, val)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * \
                '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + \
                (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + \
                [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2

        lines, *_ = display(self.root, val, left, right)
        temp = ""
        for line in lines:
            temp += line + "\n"
        return temp

    def printInorder(self):
        if self.root is None:
            return 'Tree is empty'
        hasil = []
        def DFS(cur):
            if not cur:
                return

            DFS(cur.left)
            hasil.append(str(cur.data))
            DFS(cur.right)
            return hasil

        output = DFS(self.root)
        return output

    def postOrder(self):
        temp = []
        if self.root is None:
            return 'Tree is empty'
        def DFS(cur):
            if not cur:
                return
            DFS(cur.left)
            DFS(cur.right)
            temp.append(cur.data)
        DFS(self.root)
        return temp

    def preOrder(self):
        temp = []
        if self.root is None:
            return 'Tree is empty'
        def DFS(cur):
            if not cur:
                return
            temp.append(cur.data)
            DFS(cur.left)
            DFS(cur.right)
        DFS(self.root)
        return temp

    def printBFS(self):
        if self.root is None:
            print('Tree is empty')
            return
        queue = []
        temp = []

        queue.append(self.root)
        while len(queue) != 0:
            cur: Node = queue.pop(0)  # = Dequeue

            # Hasil
            temp.append(cur.data)

            if cur.left != None:
                queue.append(cur.left)

            if cur.right != None:
                queue.append(cur.right)
            
        return temp
        
    def delete(self, value):
        def deleteValue(current: Node, value: int) -> Node:
            if current is None:
                return current

            elif value < current.data:
                current.left = deleteValue(current.left, value)

            elif value > current.data:
                current.right = deleteValue(current.right, value)
            # Kalo ketemu datanya
            else:
                # child kiri kosong, digantikan child di kanannya
                if current.left is None:
                    temp = current.right
                    current = None
                    return temp
                
                # child kanan kosong, digantikan child kiri nya
                elif current.right is None:
                    temp = current.left
                    current = None
                    return temp

                # Kedua child tidak kosong
                temp = min_value_node(current.right)
                current.data = temp.data
                # delete temp
                current.right = deleteValue(current.right, temp.data)

            
            # Update height
            if current is None:
                return current

            current.height = 1 + max(self.getNodeheight(current.left), self.getNodeheight(current.right))

            # cek balance
            balance = get_balance(current)

            # Ada 4 case
            # Case LL
            if balance > 1 and get_balance(current.left) >= 0:
                L2.config(text="LL Rotation on " + str(current.data))
                return self.rotateRight(current)

            # Case LR
            if balance > 1 and get_balance(current.left) < 0:
                L2.config(text="LR Rotation on " + str(current.data))
                current.left = self.rotateLeft(current.left)
                return self.rotateRight(current)

            # case RR
            if balance < -1 and get_balance(current.right) <= 0:
                L2.config(text="RR Rotation on " + str(current.data))
                return self.rotateLeft(current)

            # Case RL
            if balance < -1 and get_balance(current.right) > 0:
                L2.config(text="RL Rotation on " + str(current.data))
                current.right = self.rotateRight(current.right)
                return self.rotateLeft(current)
            return current

        def min_value_node(node: Node) -> Node:
            current = node

            # cari yg paling kiri
            while current.left is not None:
                current = current.left

            return current

        def get_balance(node: Node) -> int:
            if not node:
                return 0

            return self.getNodeheight(node.left) - self.getNodeheight(node.right)
        
        if self.search(value) == True:
            root = deleteValue(self.root, value)
            self.root = root
        
    def search(self,value):
        if self.root is None:
            return
        queue = []
        queue.append(self.root)
        temp = []
        
        while len(queue) != 0:
            cur: Node = queue.pop(0)
            temp.append(cur.data)
            
            if cur.data == value:
                return True
                
            if cur.left != None:
                queue.append(cur.left)

            
            if cur.right != None:
                queue.append(cur.right)
        
        if value not in temp:
            return False

#  GUI
root = Tk()
root.config(bg="#222222")
root.resizable(False,False)

avl = AVL()

L1 = Label(root, text="AVL TREE VISUALIZATION", bg="#222222", fg="white", font=("Arial",12,"bold"))
L1.pack()

# display with textbox
display = Text(root, width=105, height=30)
# set textbox cant edited
display.configure(state='disabled')
display.tag_configure("Display", justify='center')
display.tag_add("Display", "1.0", "end")
display.pack()

L2 = Label(root, text="", bg="#222222", fg="white")
L2.pack()

# Display box 2
display_2 = Label(root, text="None", width=120, height=3, borderwidth=2, relief="sunken", fg="black",bg="white")
display_2.pack()

# input textbox
input_box = Entry(root, borderwidth=2, relief="sunken", fg="black",bg="white")
input_box.place(x= 216, y=600)

# Function click
def click_insert():
    angka = int(input_box.get())    
    display_2.config(text=str(angka) + " | Status : Inserted")
    avl.insert(angka)
    L2.config()
    hasilTree = avl.print_tree()
    
    display.configure(state='normal')
    display.delete('1.0', END)
    display.insert(INSERT, hasilTree)
    display.configure(state='disabled')
    display.tag_add("Display", "1.0", "end")
    
    
 
def click_delete():
    angka = int(input_box.get()) 

    if avl.search(angka) == True:
        avl.delete(angka)
        
        display_2.config(text=str(angka) + " | Status : Deleted")
    else:
        L2.config(text="")
        display_2.config(text="Nothing can be deleted")   

    hasilTree = avl.print_tree()
    
    if hasilTree == None:
        display.configure(state='normal')
        display.delete('1.0', END)
        display.insert(INSERT,"None")
        display.configure(state='disabled')
        display.tag_add("Display", "1.0", "end")
    else:
        display.configure(state='normal')
        display.delete('1.0', END)
        display.insert(INSERT, hasilTree)
        display.configure(state='disabled') 
        display.tag_add("Display", "1.0", "end")
    
def click_BFS():
   
    L2.config(text="BFS")
     
    output = avl.printBFS()
    display_2.config(text=output)
    
def click_Preorder():
    output = avl.preOrder()
    L2.config(text="Pre order")
    display_2.config(text=output)
    
def click_Inorder():
    output = avl.printInorder()
    L2.config(text="In order")
    display_2.config(text=output)    
    
def click_Postorder():
    output = avl.postOrder()
    L2.config(text="Post order")
    display_2.config(text=output)
    
def click_search():
    angka = int(input_box.get())    
    L2.config(text="Searching " + str(angka))
    
    if avl.search(angka) == True:
        display_2.config(text=str(angka)+" is found")
    else:
        display_2.config(text=str(angka)+" is not found")
    
def click_Clear():
   
    L2.config(text="Cleared")
    avl.root = None
    display.configure(state='normal')
    display.delete('1.0', END)
    display.insert(INSERT,"None")
    display.configure(state='disabled')
    display.tag_add("Display", "1.0", "end")
    display_2.config(text="")

# BUTTON
btnInsert = Button(root, text="Insert", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_insert)
btnInsert.place(x=346, y=597)

btnDelete = Button(root, text="Delete", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_delete)
btnDelete.place(x=396, y=597)

btnSearch = Button(root, text="Search", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_search)
btnSearch.place(x=446, y=597)

btnBFS = Button(root, text="BFS", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_BFS)
btnBFS.place(x=500, y=597)

btnPre = Button(root, text="PreOrder", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_Preorder)
btnPre.place(x=536, y=597)

btnIn = Button(root, text="InOrder", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_Inorder)
btnIn.place(x=604, y=597)

btnPost = Button(root, text="PostOrder", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_Postorder)
btnPost.place(x=662, y=597)

btnClear = Button(root, text="Clear", font=("Arial",8,"bold"),bg="#434242",fg="white", command=click_Clear)
btnClear.place(x=737, y=597)

root.title("AVL Tree Visualizer")
root.geometry("1280x720")
root.mainloop()