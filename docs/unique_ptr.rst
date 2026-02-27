``std::unique_ptr``
===================

.. version-added:: C++11

Defined in header `\<memory\> <header/memory.md>`_

.. code-block::

  template<class T, class Deleter = std::default_delete<T>>      // (1)
  class unique_ptr;

  template <class T, class Deleter>                              // (2)
  class unique_ptr<T[], Deleter>;

``std::unique_ptr`` is a smart pointer that owns (is responsible for) and manages another object via a pointer and subsequently disposes of that object when the ``unique_ptr`` goes out of scope.

The object is disposed of, using the associated deleter, when either of the following happens:

* the managing unique_ptr object is destroyed.
* the managing unique_ptr object is assigned another pointer via operator= or reset().

The object is disposed of, using a potentially user-supplied deleter, by calling ``get_deleter()(ptr)``.
The default deleter (``std::default_delete``) uses the delete operator, which destroys the object and deallocates the memory.

A ``unique_ptr`` may alternatively own no object, in which case it is described as empty.

There are two versions of ``unique_ptr``:

#. Manages a single object (e.g., allocated with ``new``).
#. Manages a dynamically-allocated array of objects (e.g., allocated with ``new[]``).

The class satisfies the requirements of `*MoveConstructible* <>`_ and `*MoveAssignable* <>`_, but of neither `*CopyConstructible* <>`_ nor `*CopyAssignable* <>`_.

If ``T*`` was not a valid type (e.g., ``T`` is a reference type), a program that instantiates the definition of ``std::unique_ptr<T, Deleter>`` is ill-formed.

Type requirements
-----------------

- Deleter must be `*FunctionObject* <>`_ or lvalue reference to a `*FunctionObject* <>`_ or lvalue reference to function, callable with an argument of type ``unique_ptr<T, Deleter>::pointer``.

Notes
-----

Only non-const ``unique_ptr`` can transfer the ownership of the managed object to another ``unique_ptr``.
If an object's lifetime is managed by a ``const std::unique_ptr``, it is limited to the scope in which the pointer was created.

``unique_ptr`` is commonly used to manage the lifetime of objects, including:

* providing exception safety to classes and functions that handle objects with dynamic lifetime, by guaranteeing deletion on both normal exit and exit through exception.
* passing ownership of uniquely-owned objects with dynamic lifetime into functions.
* acquiring ownership of uniquely-owned objects with dynamic lifetime from functions.
* as the element type in move-aware containers, such as `std::vector <>`_, which hold pointers to dynamically-allocated objects (e.g. if polymorphic behavior is desired).

unique_ptr may be constructed for an `incomplete type <>`_ T, such as to facilitate the use as a handle in the `pImpl idiom <>`_.
If the default deleter is used, T must be complete at the point in code where the deleter is invoked, which happens in the destructor, move assignment operator, and reset member function of unique_ptr.
(In contrast, `std::shared_ptr <>`_ cannot be constructed from a raw pointer to incomplete type, but can be destroyed where T is incomplete).
Note that if T is a class template specialization, use of unique_ptr as an operand, e.g. ``!p`` requires T's parameters to be complete due to `ADL <>`_.

If T is a `derived class <>`_ of some base B, then unique_ptr\<T\> is `implicitly convertible <>`_ to unique_ptr\<B\>.
The default deleter of the resulting unique_ptr\<B\> will use `operator delete <>`_ for B, leading to `undefined behavior <>`_ unless the destructor of B is `virtual <>`_.
Note that `std::shared_ptr <>`_ behaves differently: `std::shared_ptr\<B\> <>`_ will use the `operator delete <>`_ for the type T and the owned object will be deleted correctly even if the destructor of B is not `virtual <>`_.

Unlike `std::shared_ptr <>`_, unique_ptr may manage an object through any custom handle type that satisfies `*NullablePointer* <>`_.
This allows, for example, managing objects located in shared memory, by supplying a Deleter that defines ``typedef boost::offset_ptr pointer;`` or another `fancy pointer <>`_.

.. csv-table::
  :header: "`Feature-test <>`_ macro", "Value", "Std", "Feature"

  "`\_\_cpp_lib_constexpr_memory <>`_", `202202L <>`_", "C++23", "``constexpr std::unique_ptr``"

Nested types
------------

================ ===============================================================================================================================
Type             Definition
================ ===============================================================================================================================
``pointer``      `std::remove_reference<Deleter>::type::pointer <>`_ if that type exists, otherwise ``T*``. Must satisfy `*NullablePointer* <>`_
``element_type`` ``T``, the type of the object managed by this ``unique_ptr``
``deleter_type`` ``Deleter``, the function object or lvalue reference to function or to function object, to be called from the destructor
================ ===============================================================================================================================

Member functions
----------------

.. list-table::

  * - `(constructor) <>`_
    - constructs a new ``unique_ptr``</br>(public member function)
  * - `(destructor) <>`_
    - destructs the managed object if such is present</br>(public member function)
  * - ``operator=``
    - assigns the ``unique_ptr``</br>(public member function)

Modifiers
^^^^^^^^^

.. list-table::

  * - ``release``
    - returns a pointer to the managed object and releases the ownership</br>(public member function)
  * - ``reset``
    - replaces the managed object</br>(public member function)
  * - ``swap``
    - swaps the managed objects</br>(public member function)

Observers
^^^^^^^^^

.. list-table::

  * - ``get``
    - returns a pointer to the managed object</br>(public member function)
  * - ``get_deleter``
    - returns the deleter that is used for destruction of the managed object</br>(public member function)
  * - ``operator bool``
    - checks if there is an associated managed object</br>(public member function)

Single-object version, ``unique_ptr<T>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::

  * - ``operator*``
      ``operator->``
    - dereferences pointer to the managed object</br>(public member function)

Array version, ``unique_ptr<T[]>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::

  * - ``operator[]``
    - provides indexed access to the managed array</br>(public member function)

Non-member functions
--------------------

.. list-table::

  * - ``make_unique`` (C++14)
      ``make_unique_for_overwrite`` (C++20)
    - creates a unique pointer that manages a new object</br>(function template)
  * - ``operator==`` (removed in C++20)
      ``operator!=``
      ``operator<``
      ``operator<=``
      ``operator>``
      ``operator>=``
      ``operator<=>`` (C++20)
    - compares to another ``unique_ptr`` or with ``nullptr``</br>(function template)
  * - ``operator<<(std::unique_ptr)`` (C++20)
    - outputs the value of the managed pointer to an output stream</br>(function template)
  * - ``std::swap(std::unique_ptr)`` (C++11)
    - specializes the ``std::swap`` algorithm
      (function template)

Helper classes
--------------

.. list-table::

  * - ``std::hash<std::unique_ptr>`` (C++11)
    - hash support for ``std::unique_ptr``
      (class template specialization)

Example
-------

`Run this code <>`_

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

Possible output:

``````text
1) Unique ownership semantics demo
D::D
D::bar
D::~D

2) Runtime polymorphism demo
D::D
D::bar
D::~D

3) Custom deleter demo
x

4) Custom lambda-expression deleter and exception safety demo
D::D
destroying from a custom deleter...
D::~D
Caught exception

5) Array form of unique_ptr demo
D::D
D::D
D::D
D::~D
D::~D
D::~D

6) Linked list demo
1,000,000 bottles of beer on the wall...
``````

## Defect reports

The following behavior-changing defect reports were applied retroactively to previously published C++ standards.

|      DR      | Applied to |           Behavior as published           | Correct behavior |
| :----------: | :--------: | :---------------------------------------: | :--------------: |
| [LWG 4144]() |   C++11    | T\* was not required to form a valid type |     required     |

## See also

|                  |       |                                                                                                  |
| :--------------- | :---: | :----------------------------------------------------------------------------------------------- |
| [``shared_ptr``]() | C++11 | smart pointer with shared object ownership semantics</br>(class template)                        |
| [``weak_ptr``]()   | C++11 | weak reference to an object managed by [``std::shared_ptr``]()</br>(class template)                |
| [``indirect``]()   | C++26 | a wrapper containing dynamically-allocated object with value-like semantics</br>(class template) |
| [``any``]()        | C++17 | objects that hold instances of any [_CopyConstructible_]() type</br>(class)                      |
