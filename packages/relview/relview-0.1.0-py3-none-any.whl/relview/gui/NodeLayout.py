class NodeLayout(object):
    """A doer-of-node-layouts - so not sure this is the best name for it, but
    it is what it is... Idea is RelationshipScene will create an instance of
    a subclass of this, passing in itself, and will call doNodeLayout() to
    perform the layout of nodes on the scene. See ForceSimulationNodeLayout,
    as an example. Separating out like this so different clients/studios/etc.
    can do their node layouts differently, for whatever reason.
    """

    def __init__(self, relationshipScene):
        self._scene = relationshipScene

    def willTakeAWhile(self):
        # subclasses can implement this to answer True if the laying out of the
        # nodes will take more than a fraction of a second (RelationshipScene
        # calls this to determine if a wait cursor should be used or not)
        return False

    def doNodeLayout(self):
        raise NotImplementedError("doNodeLayout() must be implemented!")
