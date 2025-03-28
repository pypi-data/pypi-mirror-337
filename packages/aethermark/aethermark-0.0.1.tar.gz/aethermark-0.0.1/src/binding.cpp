#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "Node.hpp"
#include "NodeWalker.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

PYBIND11_MODULE(aethermark, m)
{
    Node::bind_node(m);
    NodeWalker::bind_node_walker(m);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
