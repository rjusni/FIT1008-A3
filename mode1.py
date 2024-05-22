from landsites import Land
from data_structures.heap import MaxHeap
from algorithms.mergesort import mergesort
from data_structures.referential_array import ArrayR


class Mode1Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """
   

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Student-TODO: Best/Worst Case
        Complexity: best/worst O(n log n)
        """
        self.sites = sites 
        self.adventurers = adventurers
        
        #site_order holds lands in list ordered from most valuable to least
        self.site_order = self.heapsort_land()

    def heapsort_land(self):
        """Sorts the lands from best ratio to worst using heapsort
    
        Complexity:
        First loop iterates through all sites and creates a tuple with the reward ratio and land, which is then appended to array - O(n)
        The array is then converted to a maxheap using heapify - O(n)
        The lands are then spat back out in order using heap get_max() (log n) and then appended. This loop runs n times for each land - O(n log n)

        Final Complexity:
        O(n) + O(n) + O(n log n)
        = O(n log n) where n is the number of lands

        Completeness of a heap means 
        """

        value_array = []

        #O(n)
        for site in self.sites:
            #Finds the value of gold to adventure sent for each island and adds to a max heap
            value = (site.get_gold()/site.get_guardians(), site)
            value_array.append(value)        

        #Heapify O(n)
        site_heap = MaxHeap.heapify(value_array)

        res = []

        while len(site_heap) != 0:
            val, land_val = site_heap.get_max()
            res.append(land_val)

        return res 


    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Student-TODO: Best/Worst Case

        Complexity:
        Loop runs maximum n times where n is the number off lands. If after the first iteration,  there are no more adventurers, the loop enters the final if statment and breaks.
            Best Case: First island uses all troops for best value
                O(1)
            Worst Case: Need to go through all islands which had value calculated during init
                O(n)
        """
        res = []

        adventurers_left = self.adventurers

        #O(n)
        for item in self.site_order:
            guardians_cost = item.get_guardians()

            if guardians_cost < adventurers_left:
                res.append((item, guardians_cost))
            else:
                res.append((item, adventurers_left))

            adventurers_left -= guardians_cost
            if adventurers_left < 0:
                break

        return res


    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Complexity:
            Best and Worst Case of last two loops add up to be O(A) for both cases.
            Mergesort of A log A dominates O(A)
            Complexity also scales with O(n)
        Final Complexity:
            O(A log A) + O(N) where A is length of adventure_numbers and N is number of lands
        """
        res = [None] * len(adventure_numbers)

        #Used to remember original order to reformat result
        arr_remember = []
        #O(A)
        for i in range(len(adventure_numbers)):
            val = (adventure_numbers[i], i)
            arr_remember.append(val)
        
        #O(A log A)
        sorted_arr_remb = mergesort(arr_remember)
        
        curr_index = 0
        curr_largest = sorted_arr_remb[curr_index][0]
        curr_total = 0

        adventurers_used = 0

        #O(n)
        for item in self.site_order:

            guardians_cost = item.get_guardians()

            #Use of counter means while loop runs independent to the for loop and will run maximum A times
            #Best Case: curr largest is already bigger than cost so while loop is never entered O(1)
            #Worst case: needs to run for each adventure_number O(A)
            while curr_largest - adventurers_used <= guardians_cost:
                #While current adventuers cannot fully ransack an island
                res[sorted_arr_remb[curr_index][1]] = ((curr_largest-adventurers_used)/guardians_cost)*item.get_gold() + curr_total
                curr_index += 1
                try:
                    curr_largest = sorted_arr_remb[curr_index][0]
                except:
                    #filled all of list
                    break

            adventurers_used += guardians_cost
            curr_total += item.get_gold()


        #Check if any adventure numbers are over the total of all lands
        #Best Case All items were filled in previous loop O(1)
        #Worst Case: all items need to be filled here O(A)
        while curr_index < len(adventure_numbers):
            res[sorted_arr_remb[curr_index][1]] = curr_total
            curr_index += 1

        return res

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Complexity: O(1)
        """
        land.set_gold(new_reward)
        land.set_guardians(new_guardians)
