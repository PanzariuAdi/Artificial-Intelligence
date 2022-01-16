from abc import ABC, abstractmethod

class Constraint(ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        pass


class CSP():
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError('Error')

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)
    
    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def contains_constrain(self, constraint):
        for variable in self.variables:
            for value in self.constraints[variable]:
                if value.variables == constraint.variables:
                    return True
        return False

    def backtracking_search(self, assignment = {}):
        if len(assignment) == len(self.variables):
            return assignment
        
        # Variabilele neasignate
        unassigned = [v for v in self.variables if v not in assignment]
        min = 100
        for i in range(0, len(unassigned)):
            if len(self.domains[str(unassigned[i])]) < min:
                min = len(self.domains[str(unassigned[i])])
                position = i
        first = unassigned[position]

        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                self.forward_checking(first, local_assignment.get(first), self.domains)
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None
        
    def forward_checking(self, index, color, domains):
        domains_copy = domains.copy()
        while domains_copy:
            empty_domain = False
            for variable in self.variables:
                if variable != index:
                    constraint = MapColoringConstraint(index, variable)
                    if self.contains_constrain(constraint):
                        if color in domains_copy[variable]:
                            domains_copy[variable].remove(color)
                        # print(domains_copy[variable])
                if not domains_copy:
                    empty_domain = True
            if empty_domain:
                domains_copy = domains.copy()
            else: 
                return color
        

class MapColoringConstraint(Constraint):
    def __init__(self, place1, place2):
        super().__init__([place1, place2])
        self.place1 = place1
        self.place2 = place2

    def satisfied(self, assignment):
        if self.place1 not in assignment or self.place2 not in assignment:  
            return True
        return assignment[self.place1] != assignment[self.place2]


if __name__ == '__main__':

    file = open("date.txt", "r")
    number_of_nodes = int(file.readline())
    adj_matrix = []
    domains_matrix = []
    for i in range(0, number_of_nodes):
        line = file.readline().split(' ')
        del line[number_of_nodes]
        adj_matrix.append(line)

    for i in range(0, number_of_nodes):
        line = file.readline().split(' ')
        item = len(line)
        del line[item - 1]
        domains_matrix.append(line.copy())

    variables = [str(i) for i in range (0, number_of_nodes)]
    domains = {}
    for variable in variables:
        domains[variable] = domains_matrix[int(variable)]

    csp = CSP(variables, domains)
    for i in range (0, number_of_nodes):
        for j in range(0, number_of_nodes):
            if adj_matrix[i][j] == '1':
                csp.add_constraint(MapColoringConstraint(str(i), str(j)))

    solution = csp.backtracking_search()    
    if solution is None:
        print ("Nu exista solutie !")
    else:
        print(solution)
