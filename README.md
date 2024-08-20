# Homeworks and practicies of the second semester

## Installation
```commandline
git clone https://github.com/iraedeus/spbu_sem2_DT.git
```
---
## Homeworks

1. - ``registry.py`` - the class registration system. You can register a class by name, and then use the same name to get it. For example:  
&nbsp;
   ```python
    class ParentClass:
        pass

    parent = Registry[ParentClass](default=None)

    @parent.register(name="AVL")
    class AVLTree(ParentClass):
        pass

    @parent.register(name="Treap")
    class CartesianTree(ParentClass):
        pass
   ```  
   &nbsp;
   - ``treap.py`` - implementation of the Cartesian tree data structure  
&nbsp;
2. - ``actions.py`` - A module that allows you to perform many actions on an array, with the ability to roll back changes.  
&nbsp;
3. - ``orm.py``  - implements ORM (Object-Relational Mapping). <br/> ``script.py`` - shows the necessary information about the user's repository  
&nbsp;
4. - ``merge_sort.py`` - merge sorting using ``threading`` and ``multiprocessing`` libraries. <br/> ``main.py`` compares a multithreaded implementation and a regular one.  
&nbsp;
5. - ``Tic Tac Toe`` - A multiplayer game of tic tac toe. The architecture used is MVVM. <br/> For starting server run ``server.py``.

---
## Test works
1. - ``university.py`` - implementation of the internal structure of the university. It is able to store each student, teacher, as well as subjects taught by teachers and for which each student has a grade
   - ``matrix.py`` - implementation of the matrix class, with all operations, as well as a subclass of matrices consisting of integers  
&nbsp;
2. - ``Quotes`` - application that shows quotes from the site ``https://башорг.рф/``  
&nbsp;
3. - ``Wikipedia Path Finder`` - multithreaded path search in a graph. The application itself can find the way from the starting point (the points are Wikipedia pages) by hyperlinks to the end point, while going through the pages that the user specifies. <br/> Usage: ```main.py pages processor_count```. <br/> Example: ```main.py Outer_Wilds Adolf_Hitler Skibidi_Toilet 10```
---
## Dependencies
```commandline
pip install -r requirements.txt
```