import pymel.core as pmc
import pymel.core.datatypes as dt

##### Basic Functions #####

def get_vector_vertex_bounds(vertices, upVector=dt.Vector(0,1,0)):
    startVert = vertices[0]
    endVert = vertices[0]
    for vert in vertices:
        value = get_vector_value(vert.getPosition(), upVector)
        startValue = get_vector_value(startVert.getPosition(), upVector)
        endValue = get_vector_value(endVert.getPosition(), upVector)
        if value < startValue:
            startVert = vert
        if value > endValue:
            endVert = vert

    return startVert, endVert

def get_vector_value(point, upVector=dt.Vector(0,1,0)):
    '''
    Uses dot product to project a point onto a vector.
    Returns the a float value on that vector.
    :param point: The point to project.
    :param upVector: The normalized vector to project along.
    :return: A float value representing the projected position on the vector.
    '''

    return point * upVector

def get_normalized_value_in_range(value, startValue, endValue):
    ''' Remaps a value based on an arbitrary range to a 0 - 1 range '''
    length = endValue - startValue
    position = value - startValue
    return position / length

def apply_vertex_color(vertex, value):
    color = dt.Color(value, value, value)
    vertex.setColor(color)

def get_furthest_vert(vertices, point):
    furthestVert = vertices[0]
    for vert in vertices:
        vertDistance = vert.getPosition().distanceTo(point)
        furthestDistance = furthestVert.getPosition().distanceTo(point)
        if vertDistance > furthestDistance:
            furthestVert = vert
    return furthestVert

def get_verts_from_selection():
    '''
    Grabs the selection, and returns vertices.
    :return: A MeshVertex List
    '''

    # Grab the selection
    selection = pmc.selected()

    # Check if the selection contains any of the supported types
    # Otherwise raise a not implemented error
    if isinstance(selection[0], pmc.MeshVertex):

        # Filter through the selection for PolyVerts
        filtered = pmc.filterExpand(ex=True, sm=31)

        # Convert filtered list to a list of MeshVertex's
        verts = [pmc.PyNode(vert) for vert in filtered]

    elif isinstance(selection[0], pmc.MeshFace):
        shape = selection[0].node().getParent()

    elif selection[0].nodeType() == 'transform':

        # Just grab the shapes verts
        verts = selection[0].getShape().verts

    else:
        raise NotImplementedError('The selection does not contain a supported type')

    print verts
    return verts

def get_center_point(verts):
    '''
    Returns the center of a list of verts.
    :param verts: A list of MeshVertices
    :return: The center vector position
    '''

    # The return average vector, for now its the zero vector
    average = dt.Vector()

    # A counter
    count = 0

    # Iterate through vert list
    for vert in verts:

        # Add the vert position to
        average += vert.getPosition()

        # Add to the counter
        count += 1

    # Divide by the number of vectors
    average = average / count

    return average

def enable_color_display(vert):
    '''
    Enables the display colors of a vertices parent shape
    :param vert: A vert from the shape
    '''
    shape = vert.node().getParent()
    shape.setDisplayColors(True)


##### Application Functions #####

def apply_vector_gradient(vertices, vector):
    '''
    Applies a vertex color gradient along a specified vector
    :param vertices: The vertices to paint
    :param vector: The normalized vector to paint along
    '''

    # Enable color display for shape node
    enable_color_display(vertices[0])

    # Get the vertex bounds along the vector
    # The bounds are the furthest vertices along that vector
    start, end = get_vector_vertex_bounds(vertices, vector)

    # Get the projected position along the vector
    # (Is a single float value)
    startValue = get_vector_value(start.getPosition(), vector)
    endValue = get_vector_value(end.getPosition(), vector)

    # Iterate through the vertices
    for vert in vertices:

        # Get the vector value of the vert
        value = get_vector_value(vert.getPosition(), vector)

        # Remap the value to the value range
        value = get_normalized_value_in_range(value, startValue, endValue)

        # Apply a vertex color based on that value
        apply_vertex_color(vert, value)

def apply_radial_gradient(vertices, point):
    '''
    Applies a vertex color gradient radiating out from a specified point.
    :param vertices: The vertices to paint
    :param point: The point to center the gradient on
    '''

    # Enable color display for shape node
    enable_color_display(vertices[0])

    # Grab the start and end point
    # The end point for now is the furthest vertex from the point
    start = point
    end = get_furthest_vert(vertices, point)

    # Get the normalized direction from the point to the furthest point
    vector = end.getPosition() - start
    vector = vector.normal()

    # Get the value along that vector of the start and end point
    startValue = get_vector_value(start, vector)
    endValue = get_vector_value(end.getPosition(), vector)

    for vert in vertices:
        # Get the direction vector from the vert to the center point
        vertVector = vert.getPosition() - start
        vertVector = vertVector.normal()

        # Get the vert's value along that vector
        value = get_vector_value(vert.getPosition(), vertVector)

        # Normalize that value to the start and end value
        value = get_normalized_value_in_range(value, startValue, endValue)

        # Apply the vertex color to the vert
        apply_vertex_color(vert, 1 - value)

def apply_distance_gradient(vertices, point1, point2):
    '''
    Finds the vector between two points and applys a vector gradient to the specified verts
    :param vertices: The vertices to paint
    :param point1: The start point
    :param point2: The end point
    :return: 
    '''

    # Enable color display for shape node
    enable_color_display(vertices[0])

    # Find the direction between the specified points
    direction = point2 - point1

    # Normalize the direction
    directionN = direction.normal()

    # Apply a vector gradient
    apply_vector_gradient(vertices, directionN)


# from vertexcolortools import gradientTool; reload(gradientTool_ui); gradientTool._testtool();

def _testtool():
    verts = get_verts_from_selection()
    center = get_center_point(verts)
    print center
    apply_radial_gradient(verts, center)
    #apply_vector_gradient(verts, dt.Vector(0,-1,0))

