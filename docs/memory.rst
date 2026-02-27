Memory management library
=========================

Smart pointers
--------------

Smart pointers enable automatic, exception-safe, object lifetime management.

Pointer categories
..................

.. csv-table:: What

   "unique_ptr", "C++11", "smart pointer with unique object ownership semantics"
   "shared_ptr", "C++11", "smart pointer with shared object ownership semantics"
   "weak_ptr", "C++11", "weak reference to an object managed by std::shared_ptr"
   "auto_ptr", "deprecated in C++11", "smart pointer with strict object ownership semantics"