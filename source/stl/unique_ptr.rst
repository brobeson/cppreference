:orphan:

.. role:: cpp-entity-type

``std::unique_ptr``
===================

#. .. cpp:class:: template<class T, class Deleter = std::default_delete<T>> unique_ptr
#. .. cpp:class:: template<class T[], class Deleter> unique_ptr

Defined in header :doc:`/headers/memory`

.. .. code-block::

..   template<class T, class Deleter = std::default_delete<T>>      // (1)
..   class unique_ptr;

..   template <class T, class Deleter>                              // (2)
..   class unique_ptr<T[], Deleter>;

:cpp:class:`std::unique_ptr <unique_ptr>` is a smart pointer that owns (is responsible for) and manages another object via a pointer and subsequently disposes of that object when the :cpp:class:`unique_ptr` goes out of scope.

The object is disposed of, using the associated deleter, when either of the following happens:

* the managing :cpp:class:`unique_ptr` object is destroyed.
* the managing :cpp:class:`unique_ptr` object is assigned another pointer via :cpp:func:`operator=` or :cpp:func:`reset`.

The object is disposed of, using a potentially user-supplied deleter, by calling :cpp:func:`get_deleter`.
The default deleter (:cpp:class:`std::default_delete`) uses the ``delete`` operator, which destroys the object and deallocates the memory.

A :cpp:class:`unique_ptr` may alternatively own no object, in which case it is described as empty.

There are two versions of :cpp:class:`unique_ptr`:

#. Manages a single object (e.g., allocated with ``new``).
#. Manages a dynamically-allocated array of objects (e.g., allocated with ``new[]``).

The class satisfies the requirements of :doc:`/named_requirements/move_constructible` and :doc:`/named_requirements/move_assignable`, but of neither :doc:`/named_requirements/copy_constructible` nor :doc:`/named_requirements/copy_assignable`.

If ``T*`` is not a valid type (e.g., ``T`` is a reference type), a program that instantiates the definition of ``std::unique_ptr<T, Deleter>`` is ill-formed.

Type requirements
-----------------

- ``Deleter`` must be :doc:`/named_requirements/function_object` or lvalue reference to a :doc:`/named_requirements/function_object` or lvalue reference to function, callable with an argument of type ``unique_ptr<T, Deleter>::pointer``.

Notes
-----

Only non-const :cpp:class:`unique_ptr` can transfer the ownership of the managed object to another :cpp:class:`unique_ptr`.
If an object's lifetime is managed by a :cpp:class:`const unique_ptr <unique_ptr>`, it is limited to the scope in which the pointer was created.

:cpp:class:`unique_ptr` is commonly used to manage the lifetime of objects, including:

* providing exception safety to classes and functions that handle objects with dynamic lifetime, by guaranteeing deletion on both normal exit and exit through exception.
* passing ownership of uniquely-owned objects with dynamic lifetime into functions.
* acquiring ownership of uniquely-owned objects with dynamic lifetime from functions.
* as the element type in move-aware containers, such as :cpp:class:`std::vector <vector>`, which hold pointers to dynamically-allocated objects (e.g. if polymorphic behavior is desired).

:cpp:class:`unique_ptr` may be constructed for an incomplete type ``T``, such as to facilitate the use as a handle in the pImpl idiom.
If the default deleter is used, ``T`` must be complete at the point in code where the deleter is invoked, which happens in the destructor, move assignment operator, and reset member function of unique_ptr.
(In contrast, :cpp:class:`std::shared_ptr <shared_ptr>` cannot be constructed from a raw pointer to incomplete type, but can be destroyed where ``T`` is incomplete).
Note that if ``T`` is a class template specialization, use of :cpp:class:`unique_ptr` as an operand, e.g. ``!p`` requires ``T``'s parameters to be complete due to ADL.

If ``T`` is a derived class of some base ``B``, then :cpp:class:`unique_ptr\<T\> <unique_ptr>` is implicitly convertible to :cpp:class:`unique_ptr\<B\> <unique_ptr>`.
The default deleter of the resulting :cpp:class:`unique_ptr\<B\> <unique_ptr>` will use operator delete for ``B``, leading to undefined behavior unless the destructor of ``B`` is virtual.
Note that :cpp:class:`std::shared_ptr <shared_ptr>` behaves differently: :cpp:class:`std::shared_ptr\<B\> <shared_ptr>` will use the operator delete for the type ``T`` and the owned object will be deleted correctly even if the destructor of ``B`` is not virtual.

Unlike :cpp:class:`std::shared_ptr <shared_ptr>`, :cpp:class:`unique_ptr` may manage an object through any custom handle type that satisfies :doc:`/named_requirements/nullable_pointer`.
This allows, for example, managing objects located in shared memory, by supplying a Deleter that defines ``typedef boost::offset_ptr pointer;`` or another fancy pointer.

.. csv-table::
  :header: "Feature-test macro", "Value", "Std", "Feature"

  :cpp:var:`\_\_cpp_lib_constexpr_memory`, ``202202L``, C++23, :cpp:class:`constexpr std::unique_ptr <unique_ptr>`

Nested types
------------

================ ========================================================================================================================
Type             Definition
================ ========================================================================================================================
``pointer``      :cpp:class:`std::remove_reference<Deleter>::type::pointer` if that type exists, otherwise ``T*``. Must satisfy :doc:`/named_requirements/nullable_pointer`
``element_type`` ``T``, the type of the object managed by this :cpp:class:`unique_ptr`
``deleter_type`` ``Deleter``, the function object or lvalue reference to function or to function object, to be called from the destructor
================ ========================================================================================================================

Member functions
----------------

.. .. rst-class:: member-list

.. .. list-table::

..   * - :cpp:func:`(constructor) <constructor>`
..     - constructs a new :cpp:class:`unique_ptr` :cpp-entity-type:`(public member function)`
..   * - :cpp:func:`(destructor) <destructor>`
..     - destructs the managed object if such is present :cpp-entity-type:`(public member function)`
..   * - :cpp:func:`operator=`
..     - assigns the :cpp:class:`unique_ptr` :cpp-entity-type:`(public member function)`

.. .. rst-class:: member-list

.. .. list-table::

..   * - :cpp:func:`(constructor) <constructor>`
..     - :cpp-entity-type:`(public member function)`
..     - constructs a new :cpp:class:`unique_ptr`
..   * - :cpp:func:`(destructor) <destructor>`
..     - :cpp-entity-type:`(public member function)`
..     - destructs the managed object if such is present
..   * - :cpp:func:`operator=`
..     - :cpp-entity-type:`(public member function)`
..     - assigns the :cpp:class:`unique_ptr`

.. rst-class:: member-list

.. list-table::

  * - :cpp:func:`(constructor) <constructor>`
    - constructs a new :cpp:class:`unique_ptr`
    - :cpp-entity-type:`(public member function)`
  * - :cpp:func:`(destructor) <destructor>`
    - destructs the managed object if such is present
    - :cpp-entity-type:`(public member function)`
  * - :cpp:func:`operator=`
    - assigns the :cpp:class:`unique_ptr`
    - :cpp-entity-type:`(public member function)`

Modifiers
^^^^^^^^^

.. rst-class:: member-list

.. list-table::

  * - :cpp:func:`release`
    - returns a pointer to the managed object and releases the ownership
    - :cpp-entity-type:`(public member function)`
  * - :cpp:func:`reset`
    - replaces the managed object
    - :cpp-entity-type:`(public member function)`
  * - :cpp:func:`swap`
    - swaps the managed objects
    - :cpp-entity-type:`(public member function)`

Observers
^^^^^^^^^

.. rst-class:: member-list

.. list-table::

  * - :cpp:func:`get`
    - returns a pointer to the managed object
    - :cpp-entity-type:`(public member function)`
  * - :cpp:func:`get_deleter`
    - returns the deleter that is used for destruction of the managed object
    - :cpp-entity-type:`(public member function)`
  * - :cpp:func:`operator bool`
    - checks if there is an associated managed object
    - :cpp-entity-type:`(public member function)`

Single-object version, :cpp:class:`unique_ptr<T>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. rst-class:: member-list

.. list-table::

  * - | :cpp:func:`operator*`
      | :cpp:func:`operator->`
    - dereferences pointer to the managed object
    - :cpp-entity-type:`(public member function)`

Array version, ``unique_ptr<T[]>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. rst-class:: member-list

.. list-table::

  * - :cpp:func:`operator[]`
    - provides indexed access to the managed array
    - :cpp-entity-type:`(public member function)`

Non-member functions
--------------------

.. rst-class:: member-list

.. list-table::

  * - | :cpp:func:`make_unique`
      | :cpp:func:`make_unique_for_overwrite`
    - creates a unique pointer that manages a new object
    - :cpp-entity-type:`(function template)`
  * - | :cpp:func:`operator==`
      | :cpp:func:`operator!=`
      | :cpp:func:`operator<`
      | :cpp:func:`operator<=`
      | :cpp:func:`operator>`
      | :cpp:func:`operator>=`
      | :cpp:func:`operator\<=\>`
    - compares to another :cpp:class:`unique_ptr` or with ``nullptr``
    - :cpp-entity-type:`(function template)`
  * - :cpp:func:`operator\<\<(std::unique_ptr) <operator\<\<>`
    - outputs the value of the managed pointer to an output stream
    - :cpp-entity-type:`(function template)`
  * - :cpp:func:`std::swap(unique_ptr) <swap>`
    - specializes the ``std::swap`` algorithm
    - :cpp-entity-type:`(function template)`


Helper classes
--------------

.. rst-class:: member-list

.. list-table::

  * - :cpp:func:`std::hash<std::unique_ptr>` :cpp-entity-type:`(C++11)`
    - hash support for ``std::unique_ptr``
    - :cpp-entity-type:`(class template specialization)`

Example
-------

`Run this code in Compiler Explorer <https://godbolt.org/z/G4q16b1MK>`_

.. code-block::

  #include <cassert>
  #include <cstdio>
  #include <fstream>
  #include <iostream>
  #include <locale>
  #include <memory>
  #include <stdexcept>

  // helper class for runtime polymorphism demo below
  struct B
  {
      virtual ~B() = default;

      virtual void bar() { std::cout << "B::bar\n"; }
  };

  struct D : B
  {
      D() { std::cout << "D::D\n"; }
      ~D() { std::cout << "D::~D\n"; }

      void bar() override { std::cout << "D::bar\n"; }
  };

  // a function consuming a unique_ptr can take it by value or by rvalue reference
  std::unique_ptr<D> pass_through(std::unique_ptr<D> p)
  {
      p->bar();
      return p;
  }

  // helper function for the custom deleter demo below
  void close_file(std::FILE* fp)
  {
      std::fclose(fp);
  }

  // unique_ptr-based linked list demo
  struct List
  {
      struct Node
      {
          int data;
          std::unique_ptr<Node> next;
      };

      std::unique_ptr<Node> head;

      ~List()
      {
          // destroy list nodes sequentially in a loop, the default destructor
          // would have invoked its “next”'s destructor recursively, which would
          // cause stack overflow for sufficiently large lists.
          while (head)
          {
              auto next = std::move(head->next);
              head = std::move(next);
          }
      }

      void push(int data)
      {
          head = std::unique_ptr<Node>(new Node{data, std::move(head)});
      }
  };

  int main()
  {
      std::cout << "1) Unique ownership semantics demo\n";
      {
          // Create a (uniquely owned) resource
          std::unique_ptr<D> p = std::make_unique<D>();

          // Transfer ownership to “pass_through”,
          // which in turn transfers ownership back through the return value
          std::unique_ptr<D> q = pass_through(std::move(p));

          // “p” is now in a moved-from 'empty' state, equal to nullptr
          assert(!p);
      }

      std::cout << "\n" "2) Runtime polymorphism demo\n";
      {
          // Create a derived resource and point to it via base type
          std::unique_ptr<B> p = std::make_unique<D>();

          // Dynamic dispatch works as expected
          p->bar();
      }

      std::cout << "\n" "3) Custom deleter demo\n";
      std::ofstream("demo.txt") << 'x'; // prepare the file to read
      {
          using unique_file_t = std::unique_ptr<std::FILE, decltype(&close_file)>;
          unique_file_t fp(std::fopen("demo.txt", "r"), &close_file);
          if (fp)
              std::cout << char(std::fgetc(fp.get())) << '\n';
      } // “close_file()” called here (if “fp” is not null)

      std::cout << "\n" "4) Custom lambda expression deleter and exception safety demo\n";
      try
      {
          std::unique_ptr<D, void(*)(D*)> p(new D, [](D* ptr)
          {
              std::cout << "destroying from a custom deleter...\n";
              delete ptr;
          });

          throw std::runtime_error(""); // “p” would leak here if it were a plain pointer
      }
      catch (const std::exception&)
      {
          std::cout << "Caught exception\n";
      }

      std::cout << "\n" "5) Array form of unique_ptr demo\n";
      {
          std::unique_ptr<D[]> p(new D[3]);
      } // “D::~D()” is called 3 times

      std::cout << "\n" "6) Linked list demo\n";
      {
          List wall;
          const int enough{1'000'000};
          for (int beer = 0; beer != enough; ++beer)
              wall.push(beer);

          std::cout.imbue(std::locale("en_US.UTF-8"));
          std::cout << enough << " bottles of beer on the wall...\n";
      } // destroys all the beers
  }

Possible output::

  1) Unique ownership semantics demo
  D::D
  D::bar
  D::~D

  1) Runtime polymorphism demo
  D::D
  D::bar
  D::~D

  1) Custom deleter demo
  x

  1) Custom lambda-expression deleter and exception safety demo
  D::D
  destroying from a custom deleter...
  D::~D
  Caught exception

  1) Array form of unique_ptr demo
  D::D
  D::D
  D::D
  D::~D
  D::~D
  D::~D

  1) Linked list demo
  1,000,000 bottles of beer on the wall...

Defect reports
--------------

The following behavior-changing defect reports were applied retroactively to previously published C++ standards.

.. list-table::
  :header-rows: 1

  * - DR
    - Applied to
    - Behavior as published
    - Correct behavior
  * - `LWG 4144 <https://cplusplus.github.io/LWG/issue4144>`_
    - C++11
    - ``T*`` was not required to form a valid type
    - required

See also
--------

.. rst-class:: member-list

.. list-table::

  * - :cpp:class:`shared_ptr`
    - smart pointer with shared object ownership semantics
    - :cpp-entity-type:`(class template)`
  * - :cpp:class:`weak_ptr`
    - weak reference to an object managed by ``std::shared_ptr``
    - :cpp-entity-type:`(class template)`
  * - :cpp:class:`indirect`
    - a wrapper containing dynamically-allocated object with value-like semantics
    - :cpp-entity-type:`(class template)`
  * - :cpp:class:`any`
    - objects that hold instances of any *CopyConstructible* type
    - :cpp-entity-type:`(class)`
