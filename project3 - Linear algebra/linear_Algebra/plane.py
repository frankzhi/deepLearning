from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = n.coordinates[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n.coordinates[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n.coordinates[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)

    def planesAreParallel(self, other):
        return self.normal_vector.isParallel(other.normal_vector)

    def linesAreParallel(self, other):
        return self.normal_vector.isParallel(other.normal_vector)


    def __eq__(self,other):
        if self.normal_vector.isZero():
            if not other.normal_vector.isZero():
                return False
            else:
                diff =self.constant_term - other.constant_term
                return MyDecimal(diff).is_near_zero()
        elif other.normal_vector.isZero():
            return False

        if not self.linesAreParallel(other):
            return False

        b1 = self.basepoint
        b2 = other.basepoint

        v = b1.minus(b2)
        n = self.normal_vector   #2 lines have already parallel, no need to compare to normal vector to v

        return n.isOrthogonal(v)

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


p1 = Plane(normal_vector = Vector(['-0.412','3.806','0.728']),constant_term = '-3.46')
p2 = Plane(normal_vector = Vector(['1.03','-9.515','-1.82']),constant_term = '8.65')
print p1.planesAreParallel(p2)
print 'Are them equal? :{}'.format(p1 == p2)

p3 = Plane(normal_vector = Vector(['2.611','5.528','0.283']),constant_term = '4.6')
p4 = Plane(normal_vector = Vector(['7.715','8.306','5.342']),constant_term = '3.76')
print p3.planesAreParallel(p4)
print p3 == p4

p5 = Plane(normal_vector = Vector(['-7.926','8.625','-7.212']),constant_term = '-7.952')
p6 = Plane(normal_vector = Vector(['-2.642','2.875','-2.404']),constant_term = '2.443')
print p5.planesAreParallel(p6)
print p5 == p6
