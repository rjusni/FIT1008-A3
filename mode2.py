from landsites import Land
from data_structures.heap import MaxHeap


class Mode2Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, n_teams: int) -> None:
        """
        Complexity: O(1)
        """
        self.teams_count = n_teams
        self.sites = []


    def add_sites(self, sites: list[Land]) -> None:
        """
        Complexity of adding and copying two lists is the cost of iterating over both of them
        Complexity:
        O(N) + O(S) = O(N+S) where N is the size of pre-existing list and S is size of new list
        """
        self.sites = self.sites + sites


    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Complexity:
        Setting up the sites and ordering them in the heap is O(N) + O(N) which is just O(N)

        The day logic loop runs maximum K times where K is the number of teams and has important functions heap get_max and add which are O(log N) 

        Final Complexity:
            O(N) + O(K) * O(log N)
            = O(N + K log N) where N is the number of lands and K is the number of teams

        """

        #populate a max heap with all the lands
        #use heapify to maintain complexity requirement
        score_arr = []
        #O(N) 
        for land in self.sites:
            score = self.calculate_score(adventurer_size, land)
            score_arr.append(score)
        
        #O(N)
        score_heap = MaxHeap.heapify(score_arr)
        #The max element will be the most valuable that sends the most troops
        #most troops is better as it occupies potential lands for enemies

        res = []

        #O(K)
        for _ in range(self.teams_count):
            out = (None, 0)
            #O(log N)
            optimal = score_heap.get_max()
            #optimal is a tuple with (Gold, Troops sent, Land)
            opt_gold, opt_troop, opt_land = optimal
            out = (opt_land, opt_troop)
            res.append(out)

            #Replace land with ransacked land
            if opt_land is not None:
                opt_land.set_gold(opt_land.get_gold() - optimal[0])
                opt_land.set_guardians(opt_land.get_guardians() - optimal[1])
                new_land_score = self.calculate_score(adventurer_size, opt_land)
                #O(log N)
                score_heap.add(new_land_score)

        return res


    def calculate_score(self, adventurers_tot: int, land: Land):
        """Calculates the max score for a given land
        
            returns (optimal_score, troops required to send)

        Complexity:
        All operations are artithmetic or constant.
        Best case if only first if statement needs to be checked which is one arithmetic comparison
        Final Complexity: O(1)
        """

        "If a troop doesn't earn more than 2.5 it isn't worth to send."
        if land.get_guardians() == 0 or (land.get_gold()/land.get_guardians()) < 2.5:
            #Not worth to send, just stay all at home
            score = (2.5 * adventurers_tot, 0, None)
        elif adventurers_tot <= land.get_guardians():
            #Can send all troops to island
            score = ((adventurers_tot/land.get_guardians())*land.get_gold(), adventurers_tot, land)
        else:
            #Send what we can
            score = (land.get_gold() + 2.5*(adventurers_tot - land.get_guardians()),land.get_guardians(), land)
        return score




