from collections import defaultdict
from functools import cmp_to_key
import numpy as np
import random

from .NodeLayout import NodeLayout
from .PrimNodeItem import PrimNodeItem


class ForceSimulationNodeLayout(NodeLayout):
    """Performs node layout according to a "force simulation."

    TODO 1: Cap Forces
    TODO 2: Make starting position spiral
    """

    #
    # configuration options
    #

    # Number of times to run the simulation
    SIMULATION_TICKS = 3000
    # During the simulation, at what time to bring in the left & right walls
    WALL_TICKS = 400

    # How much time to step forward per loop
    DT = 0.04
    # How much time to step forward towards the middle of the simulation
    MID_DT = 0.03
    # How much time to step forward towards the end of the simulation
    LATE_DT = 0.02

    # At what percentage of the simulation to start using midDt
    MID_DT_PCT = 0.66
    # At what percentage of the simulation to start using lateDt
    LATE_DT_PCT = 0.93

    # When a highly connected node is being simulated, we will choose this many
    # connections per tick to actually add forces for. Overtime, this balances out
    # to move the node to the correct position, but does not incur O(n) overhead
    # (i.e. a node connected to every other node does not ruin our scaling).
    MAX_CONNECTIONS = 5
    # Minimum number of nodes that trigger the grid cell optimization
    # (if <= this count, then we only use a 1x1 grid)
    GRID_MIN_NODE_COUNT = 100

    # How far nodes are away from each other
    DIST_SCALE = 500
    # As number of connected node increases, we expand the DIST_SCALE by n^DIST_SCALE_EXP.
    # A higher value means highly connected nodes will allow their connections to be farther.
    DIST_SCALE_EXP = 0.6
    # For a wide graph, we take its width and add this ratio to determine where the walls
    # should go
    WALL_DIST_RATIO = 0.8
    # How hard to pull the nodes to the wall
    WALL_CLOSENESS = 0.05
    # Tunes how strongly nodes are attracted to each other
    ATTRACTION_STRENGTH = 6.0
    # Repulsion factor for nodes that share out / in non-bidrectional edges
    REPULSION_FOR_CONNECTED = 1
    # Tunes how strongly nodes are repulsed from each other
    REPULSION_STRENGTH = 3000.0
    # How much we pull nodes to either wall
    # TODO: Consider making this work the same as MID_DT and LATE_DT (later in the
    #   simulation, use less strength to allow the nodes to spread out more on the
    #   wall)
    LEFT_STRENGTH = 0.1
    # How fast velocity decreases per iteration
    FRICTION = 0.95
    # Distance cutoff inside of the skewed universe that the nodes overlap
    NUDGE_CUTOFF = 100
    # Width of the node
    NODE_WIDTH = 4.0
    # Cap on how fast a node can move to make simulation more stable
    VELOCITY_LIMIT = 1000

    #
    # NodeLayout overrides
    #
    def willTakeAWhile(self):
        # TODO update this depending on number of nodes if we can make it faster
        # for lower node counts etc.
        return True

    def doNodeLayout(self):
        relationshipCollection = self._scene.getRelationshipCollection()
        assert (
            relationshipCollection
        ), "Need an active RelationshipCollection to do a node layout!"
        allRelationshipRecords = relationshipCollection.getAllRecords()
        # TODO: Consider caching these in the relRecs themselves
        # Prim path to input paths without bi dir
        relsNoBiDirIn = {}
        # Prim path to output paths without bi dir
        relsNoBiDirOut = {}
        numInputs = 0
        numOutputs = 0
        for currRel in allRelationshipRecords:
            primPath = currRel.getPrimPath()
            # Make sure clone to not modify if the set is cached later
            currIn_init = set(currRel.getPrimsWithFromRelationships())
            currOut_init = set(currRel.getPrimsWithToRelationships())

            # Remove nodes in IN that are also in OUT
            currIn = currIn_init.difference(currOut_init)
            # Remove nodes in OUT that are also in IN
            currOut = currOut_init.difference(currIn_init)

            # Count number of non-bidirectional
            if not currIn and currOut:
                numInputs += 1
            elif not currOut and currIn:
                numOutputs += 1

            relsNoBiDirIn[primPath] = currIn
            relsNoBiDirOut[primPath] = currOut

        numNodes = len(allRelationshipRecords)
        pathToIdx = {}
        positions = np.zeros(shape=(2, numNodes))

        def compare(first, second):
            def numConnectedPaths(currRel):
                inputPaths = currRel.getPrimsWithFromRelationships()
                outputPaths = currRel.getPrimsWithToRelationships()
                return len(inputPaths.union(outputPaths))

            return numConnectedPaths(second[1]) - numConnectedPaths(first[1])

        height = int(np.sqrt(numNodes)) + 1
        # Position the nodes in order of connections in a spiral pattern so that the most connected nodes
        # are in the center and there is as little stress as possible.
        sideLength = 1
        currSide = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dirIdx = 0
        col = 0
        row = 0
        count = 0
        isFirst = True
        for i, currRel in sorted(
            enumerate(allRelationshipRecords), key=cmp_to_key(compare)
        ):
            if isFirst:
                positions[:, i] = [
                    col * PrimNodeItem.NODE_WIDTH * 1.2,
                    row * PrimNodeItem.NODE_HEIGHT * 1.2,
                ]
                pathToIdx[currRel.getPrimPath()] = i
                isFirst = False
                continue

            row += directions[dirIdx][0]
            col += directions[dirIdx][1]

            positions[:, i] = [
                col * PrimNodeItem.NODE_WIDTH * 1.2,
                row * PrimNodeItem.NODE_HEIGHT * 1.2,
            ]
            pathToIdx[currRel.getPrimPath()] = i

            currSide += 1

            if currSide == sideLength:
                dirIdx += 1
                dirIdx %= len(directions)
                currSide = 0
                count += 1
                if count % 2 == 0:
                    sideLength += 1

        connectedNodes = [set() for _ in range(numNodes)]

        for i, currRel in enumerate(allRelationshipRecords):
            primPath = currRel.getPrimPath()
            inputPaths = currRel.getPrimsWithFromRelationships()
            outputPaths = currRel.getPrimsWithToRelationships()
            connectedPaths = inputPaths.union(outputPaths)
            for path in connectedPaths:
                pathIdx = pathToIdx[path]
                connectedNodes[i].add(pathIdx)
                connectedNodes[pathIdx].add(i)

        # Will be set to 1 if a pair of node is connected
        connections = np.zeros(shape=(numNodes, numNodes))
        # A factor to lower the repulsion strength for nodes that share out / in non-bidrectional edges
        repulsions = np.zeros(shape=(numNodes, numNodes))
        # Desired distance for the attraction force for each pair of nodes
        desiredDistancePerPair = np.zeros(shape=(numNodes, numNodes))
        desiredDistancePerPair[:, :] = self.DIST_SCALE
        # A node that has no inputs but has at least one output
        isConnectedInputNode = np.zeros(shape=(numNodes))
        # A node that has no outputs but has at least one input
        isConnectedOutputNode = np.zeros(shape=(numNodes))
        for i, currRel in enumerate(allRelationshipRecords):
            primPath = currRel.getPrimPath()
            inputPaths = currRel.getPrimsWithFromRelationships()
            outputPaths = currRel.getPrimsWithToRelationships()

            # Starts at distScale and scales with the sqrt of the number of nodes (rough guess for how much farther we
            # need to be)
            # TODO: separate input and output and assign to corresponding edges
            desiredDistance = self.DIST_SCALE * np.clip(
                (len(inputPaths) + len(outputPaths)) ** self.DIST_SCALE_EXP / 4, 1, None
            )

            for path in inputPaths.union(outputPaths):
                otherIdx = pathToIdx[path]
                # Since we don't know what order, we just set the desired distance to the max of what it is and
                # what we want
                desiredDistancePerPair[i, otherIdx] = max(
                    desiredDistancePerPair[i, otherIdx], desiredDistance
                )
                desiredDistancePerPair[otherIdx, i] = max(
                    desiredDistancePerPair[otherIdx, i], desiredDistance
                )

            inputPathsNoBiDir = relsNoBiDirIn[primPath]
            outputPathsNoBiDir = relsNoBiDirOut[primPath]

            if not inputPathsNoBiDir and outputPathsNoBiDir:
                isConnectedInputNode[i] = 1
            elif not outputPathsNoBiDir and inputPathsNoBiDir:
                isConnectedOutputNode[i] = 1

            connectedPaths = inputPaths.union(outputPaths)
            for path in connectedPaths:
                pathIdx = pathToIdx[path]
                connections[i, pathIdx] = 1
                connections[pathIdx, i] = 1
            for j, otherRel in enumerate(allRelationshipRecords):
                if i == j:
                    continue
                otherPath = otherRel.getPrimPath()
                otherInputPathsNoBiDir = relsNoBiDirIn[otherPath]
                otherOutputPathsNoBiDir = relsNoBiDirOut[otherPath]

                repulsionStrength = 1
                if outputPathsNoBiDir.intersection(
                    otherOutputPathsNoBiDir
                ) or inputPathsNoBiDir.intersection(otherInputPathsNoBiDir):
                    repulsionStrength = self.REPULSION_FOR_CONNECTED

                repulsions[i, j] = repulsionStrength
                repulsions[j, i] = repulsionStrength

        # Scale right strength by how many of each input-only and output-only nodes there
        # are so that the graph doesn't drift more towards one wall over the other
        rightStrength = (
            self.LEFT_STRENGTH * numInputs / numOutputs if numOutputs != 0 else 1
        )

        addedWalls = False
        leftWall = 0
        rightWall = 0
        velocity = np.zeros(shape=(2, numNodes))

        gridTargetCellCount = 1
        if numNodes > self.GRID_MIN_NODE_COUNT:
            gridTargetCellCount = int(numNodes * 25 / 1000)
            if gridTargetCellCount < 1:
                print("gridMinNodeCount seems to be too low -- defaulting to 1x1 grid")
                gridTargetCellCount = 1

        for totalTime in range(self.SIMULATION_TICKS):
            gridShift = random.uniform(0, 1)
            minX = np.min(positions[0, :])
            minY = np.min(positions[1, :])
            maxX = np.max(positions[0, :])
            maxY = np.max(positions[1, :])

            # To determine which cell in the grid a node is part of, start with an
            # equation for the total number of cells we want to try to match:
            # T = total cells (gridTargetCellCount)
            # W = width of grid
            # H = height of grid
            # R = ratio of graph height / width = H_graph/W_graph
            # Force the relationship between W and H to be in terms of R to solve for
            # just one variable:
            # T = W * H
            # T = W * R * W  (R is aspect ratio of graph)
            # W^2 = T / R
            # W = sqrt(T / R) , H = R * W
            # Then we set gridWidth = W, gridHeight = H, when multiplied they are
            # approximately the gridTargetCellCount but can slightly more - the point
            # is that we fairly divided up the graph into that number of cells.
            graphWidth = max(maxX - minX, 1)
            graphHeight = max(maxY - minY, 1)
            graphRatio = graphHeight / graphWidth
            gridFairWidth = np.sqrt(gridTargetCellCount / graphRatio)
            gridFairHeight = gridFairWidth * graphRatio

            gridWidth = int(gridFairWidth) + 1
            gridHeight = int(gridFairHeight) + 1

            # This scale tells us how to convert from an absolute node position to a
            # grid cell.
            gridScaleX = gridWidth / graphWidth
            gridScaleY = gridHeight / graphHeight

            grid = defaultdict(set)
            for n in range(numNodes):
                # If the desired count is just 1 cell, the formula doesn't work; so we add
                # a special case to force all the nodes to (0, 0)
                if gridTargetCellCount == 1:
                    x = 0
                    y = 0
                else:
                    x = int(((positions[0, n] - minX) * gridScaleX) + gridShift)
                    y = int(((positions[1, n] - minY) * gridScaleY) + gridShift)
                grid[(x, y)].add(n)

                # TODO: Consider if attraction should be separated somehow.
                # For now, did not pursue this because it would make things
                # a lot more complicated (having only one matrix to deal with is a lot easier).
                # Not even sure whether it would help performance.
                currConnections = connectedNodes[n]
                if len(connectedNodes[n]) > self.MAX_CONNECTIONS:
                    currConnections = random.sample(
                        connectedNodes[n], self.MAX_CONNECTIONS
                    )
                for attractedNode in currConnections:
                    grid[(x, y)].add(attractedNode)

            grid = {k: list(v) for (k, v) in grid.items()}

            dt = self.DT
            if totalTime > self.SIMULATION_TICKS * self.LATE_DT_PCT:
                dt = self.LATE_DT
            elif totalTime > self.SIMULATION_TICKS * self.MID_DT_PCT:
                dt = self.MID_DT
            if totalTime > self.WALL_TICKS and not addedWalls:
                addedWalls = True
                # Once the graph spreads out a bit, calculate max and min x and use those as left and right walls
                leftWall = np.min(positions[0, :])
                rightWall = np.max(positions[0, :])
                wallDist = abs(rightWall - leftWall)
                leftWall -= self.WALL_DIST_RATIO * wallDist
                rightWall += self.WALL_DIST_RATIO * wallDist

            if addedWalls:
                xPositions = positions[0, :]
                leftForces = leftWall - xPositions
                rightForces = rightWall - xPositions
                leftForcesAbs = np.abs(leftForces)
                rightForcesAbs = np.abs(rightForces)
                wallForces = (
                    self.LEFT_STRENGTH * isConnectedInputNode * leftForces
                    + rightStrength * isConnectedOutputNode * rightForces
                )
                wallThreshold = wallDist * self.WALL_CLOSENESS
                wallForces[leftForcesAbs < wallThreshold] = 0
                wallForces[rightForcesAbs < wallThreshold] = 0
                velocity[0, :] += wallForces * dt

            for cell, nodes in grid.items():
                cellPositions = positions[:, nodes]
                localRepulsions = repulsions[:, nodes][nodes, :]
                localConnections = connections[:, nodes][nodes, :]
                localDesiredDistancePerPair = desiredDistancePerPair[:, nodes][nodes, :]

                # allDiffs[:, i, j] = vector from node j to node i.
                allDiffs = (
                    cellPositions[:, :, np.newaxis] - cellPositions[:, np.newaxis, :]
                )
                # allDist2[i, j] = distance squared between node i and node j.
                allDist2 = np.sum(allDiffs**2, axis=0)
                # allDist = distance
                allDist = np.sqrt(allDist2)

                # By squishing x by 4.0, we convert the ellipse shape of the node into
                # a circle in the "squished universe". This means a regular distance check
                # and cutoff in the "squished universe" causes an elliptical distance check
                # in the real world.
                skewDiff = np.array(allDiffs)
                skewDiff[0, :, :] /= self.NODE_WIDTH
                skewDist2 = np.sum(skewDiff**2, axis=0)
                skewDist = np.sqrt(skewDist2)

                # allDir[:, i, j] = unit vector from node j to node i.
                allDir = allDiffs / (allDist + 0.01)

                # Calculate repulsion by distance squared
                allRepulsionIntensity = self.REPULSION_STRENGTH / (allDist + 0.01)
                # For any node and itself, make sure it doesn't have any repulsion
                allRepulsionIntensity[allDist2 == 0] = 0
                allRepulsion = (
                    allDir
                    * allRepulsionIntensity[np.newaxis, :, :]
                    * localRepulsions[np.newaxis, :, :]
                )
                # Sum up all the repulsion forces of the other nodes
                sumRepulsion = np.sum(allRepulsion, axis=2)

                velocity[:, nodes] += sumRepulsion * dt

                # While distance is bigger than desired, apply attraction towards
                # other node
                attractionIntensity = self.ATTRACTION_STRENGTH * np.clip(
                    allDist - localDesiredDistancePerPair, 0, None
                )
                # For any node and itself, make sure it doesn't have any attraction
                attractionIntensity[allDist2 == 0] = 0
                allAttraction = (-1.0 * allDir) * attractionIntensity[np.newaxis, :, :]
                allAttraction[:, localConnections == 0] = 0
                # Sum up all the repulsion forces of the other nodes
                sumAttraction = np.sum(allAttraction, axis=2)
                velocity[:, nodes] += sumAttraction * dt

                # Apply a force that pushes overlapping nodes away from each other.
                # NOTE: Didn't find this too useful compared to the position-based approach below
                #       but keeping it in case we want to switch back for some reason.
                # border = np.array(allDir)
                # border[:, skewDist >= self.NUDGE_CUTOFF] = 0
                # border[:, skewDist < self.NUDGE_CUTOFF] *= 200
                # sumBorder = np.sum(border, axis=2)
                # velocity[:, nodes] += sumBorder * dt

                # TODO: Proper friction potentially scaled by dt
                velocity[:, nodes] *= self.FRICTION
                velocity[:, nodes] = np.clip(
                    velocity[:, nodes], -self.VELOCITY_LIMIT, self.VELOCITY_LIMIT
                )
                positions[:, nodes] += velocity[:, nodes] * dt

                # Border is the normalized away direction initially
                border = np.array(allDir)
                # How far away from the cutoff nodes i & j are
                nudgeDist = self.NUDGE_CUTOFF - skewDist
                # All nodes beyond the cutoff don't need any adjustment
                border[:, skewDist >= self.NUDGE_CUTOFF] = 0
                # Scale all away directions that are less than the cutoff to be as big as the amount we need
                # to move the node to be beyond the cutoff.
                border[:, skewDist < self.NUDGE_CUTOFF] *= nudgeDist[
                    skewDist < self.NUDGE_CUTOFF
                ]
                # Sum all the adjustments same as previous force calculations
                sumBorder = np.sum(border, axis=2)
                # Directly apply the adjustment instead of using a force -- since we have absolute distances
                # and this makes it much more stable
                positions[:, nodes] += sumBorder

        # Shift graph so that the minimum X and Y are 0's.
        # NOTE: To fit the entire graph on screen, we need to use the zoom feature (i.e. the scroll wheel)
        #       because if we scale the positions instead, that wouldn't make the node smaller.
        minX = np.min(positions[0, :])
        minY = np.min(positions[1, :])
        positions[0, :] -= minX
        positions[1, :] -= minY

        for i, currRel in enumerate(allRelationshipRecords):
            primPath = currRel.getPrimPath()
            currentNode = self._scene.getNodeItemForPrimPath(primPath)
            if not currentNode:
                print("node could not be found for prim path ", primPath)
                continue
            currentNode.setPos(positions[0, i], positions[1, i])
