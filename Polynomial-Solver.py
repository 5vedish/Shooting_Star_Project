sign_strings = { 1 : '+' , -1 : '-'}
degree_strings = { 0 : '' , 1 : 'x' , 2 : 'x^' , -1 : 'x'}

class Term:

    def __init__(self, coeff, degree):

        self.coeff = coeff
        self.degree = degree

    def __str__(self):

        coeff_str = '' if self.coeff == 1 and self.degree != 0 else str(self.coeff) # x
        coeff_str = coeff_str[0] if self.coeff == -1 and self.degree != 0 else coeff_str # -x
        deg_decision = 2 if self.degree > 1 or self.degree < 0 else self.degree # x^ or ''/x
        format_str = degree_strings[deg_decision]
        deg_str = str(self.degree) if self.degree > 1 or self.degree < 0 else '' # degree

        return coeff_str + format_str + deg_str

class Polynomial:

    def __init__(self, poly):

        self.terms = []

        str_terms = poly.split('+')

        for str_term in str_terms:

            self.terms.append(Term(self.coeff(str_term), self.degree(str_term)))

    def coeff(self, term):

        negative = -1 if term[0] == '-' else 1 
        term = term[1:] if negative == -1 else term
        x = term.find('x')

        if x == -1:
            return negative * int(term) # constant
        elif x == 0:
            return negative * 1 # x
        else: 
            return negative * int(term[:x]) # coefficient
 
    def degree(self, term):
    
        caret = term.find('^')

        if term.find('x') == -1: # constant
            return 0
        elif term.find('^') == -1: # x
            return 1
        elif term[caret+1]  == '-': # negative degree
            return -1 * int(term[caret+2:])
        else:
             return int(term[caret+1:]) # degree

    def __str__(self):

        canonical = ''

        for term in self.terms:
            canonical += '+' + str(term)

        canonical = canonical[1:]

        return canonical

    def add_poly(self, other_poly):

        sum_hash = {}
        new_terms = []

        self_degrees = [term.degree for term in self.terms]
        other_degrees = [term.degree for term in other_poly.terms]

        set_degrees = set(self_degrees + other_degrees)

        for degree in set_degrees:
            sum_hash[degree] = 0

        for term in self.terms:
            sum_hash[term.degree] += term.coeff

        for term in other_poly.terms:
            sum_hash[term.degree] += term.coeff

        for x in sum_hash:

            if sum_hash[x] is not 0:

                new_terms.append(Term(sum_hash[x], x))

        if len(new_terms) == 0:
            return '0'

        new_terms = sorted(new_terms, key= lambda term : term.degree, reverse= True)
    
        new_poly = ''.join(['+' + str(term) for term in new_terms])
        new_poly = new_poly[1:]
    
        return Polynomial(new_poly)

    def negate_poly(self):

        for term in self.terms:

            term.coeff = -1 * term.coeff

    def sub_poly(self, other_poly):

        other_poly.negate_poly()

        return self.add_poly(other_poly)

    def mult_poly(self, other_poly):

        prod_hash = {}
        new_terms = []
        set_degrees = []

        self_degrees = [term.degree for term in self.terms]
        other_degrees = [term.degree for term in other_poly.terms]

        for x in self_degrees:
            for y in other_degrees:
                set_degrees.append(x+y)

        set_degrees = list(set(set_degrees))

        for degree in set_degrees:
            prod_hash[degree] = 0

        for t1 in self.terms:
            for t2 in other_poly.terms:

                prod_hash[t1.degree + t2.degree] += t1.coeff * t2.coeff

        for x in prod_hash:

            if prod_hash[x] is not 0:

                new_terms.append(Term(prod_hash[x], x))

        if len(new_terms) == 0:
            return '0'
            
        new_terms = sorted(new_terms, key= lambda term : term.degree, reverse= True)
    
        new_poly = ''.join(['+' + str(term) for term in new_terms])
        new_poly = new_poly[1:]
    
        return Polynomial(new_poly)
        
print('Polynomials must be in canonical form where its terms are separated by addition.')
print('Type (Add/Sub/Mult)')
op = input()
print('Enter polynomial 1')
poly1 = input()
print('Enter polynomial 2')
poly2 = input()

a = Polynomial(poly1)
b = Polynomial(poly2)

print('The answer is')
if op == 'Add':
    print(a.add_poly(b))
elif op == 'Sub':
    print(a.sub_poly(b))
elif op == 'Mult':
    print(a.mult_poly(b))
else:
    print('Invalid Operation, restart script')