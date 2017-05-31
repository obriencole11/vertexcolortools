import pymel.core as pmc
import pymel.core.datatypes as dt
from collections import namedtuple


##### Basic Utils #####

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
    value = point * upVector
    return value

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

##### Application Tools #####

def get_selected_shape():
    ''' Returns the selected shape node. '''
    selection = pmc.ls(selection=True)
    return selection[0].getShapes()[0]

def apply_vector_gradient(vertices, vector):
    start, end = get_vector_vertex_bounds(vertices, vector)
    startValue = get_vector_value(start.getPosition(), vector)
    endValue = get_vector_value(end.getPosition(), vector)

    for vert in vertices:
        value = get_vector_value(vert.getPosition(), vector)
        value = get_normalized_value_in_range(value, startValue, endValue)
        apply_vertex_color(vert, value)

def apply_radial_gradient(vertices, point):
    start = point
    end = get_furthest_vert(vertices, point)
    vector = end.getPosition() - start

    vector = vector.normal()
    print vector
    startValue = get_vector_value(start, vector)
    endValue = get_vector_value(end.getPosition(), vector)

    for vert in vertices:
        value = get_vector_value(vert.getPosition(), vector)
        value = get_normalized_value_in_range(value, startValue, endValue)
        apply_vertex_color(vert, 1 - value)


def apply_distance_gradient(vertices, point1, point2):
    # Find the vector between points
    # Iterate through vertices, apply color based on value
    pass


def _testvegtool():
    selection = pmc.ls(selection=True)
    point = selection[0].getPosition()
    shape = pmc.ls(selection=True, o=True)[0]
    #shape = get_selected_shape()
    shape.setDisplayColors(True)
    vertices = shape.verts
    #vector = dt.Vector(0,0,1)
    #point = dt.Point(0,-1,0)

    #apply_vector_gradient(vertices, vector)
    apply_radial_gradient(vertices, point)