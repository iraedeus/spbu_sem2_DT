# Homeworks and practicies of the second semester

## Installation
```commandline
git clone https://github.com/iraedeus/spbu_sem2_DT.git
```
---
## Homeworks

1. - ``registry.py`` - the class registration system. You can register a class by name, and then use the same name to get it. For example:
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
   - ``treap.py`` - implementation of the Cartesian tree data structure  
&nbsp;
2. - ``actions.py`` - A module that allows you to perform many actions on an array, with the ability to roll back changes.  
&nbsp;
3. - ``orm.py``  - implements ORM (Object-Relational Mapping). <br/> ``script.py`` - shows the necessary information about the user's repository  
&nbsp;
4. - ``merge_sort.py`` - merge sorting using ``threading`` and ``multiprocessing`` libraries. <br/> ``main.py`` compares a multithreaded implementation and a regular one.  
&nbsp;
5. - ``Tic Tac Toe`` - A multiplayer game of tic tac toe. The architecture used is MVVM.

---
## Test works

---
## Dependencies
```commandline
pip install -r requirements.txt
```