#ifndef NODE_WALKER_HPP
#define NODE_WALKER_HPP

#include <memory>
#include <pybind11/pybind11.h>

// Forward declare Node to avoid circular dependency
class Node;

class NodeWalker
{
public:
    // Constructor
    explicit NodeWalker(std::shared_ptr<Node> root);

    // Methods
    std::pair<bool, std::shared_ptr<Node>> next();
    void resumeAt(std::shared_ptr<Node> node, bool entering);

    // Pybind11 binding method
    static void bind_node_walker(pybind11::module &m);

private:
    std::shared_ptr<Node> current;
    std::shared_ptr<Node> root;
    bool entering;
};

#endif // NODE_WALKER_HPP
