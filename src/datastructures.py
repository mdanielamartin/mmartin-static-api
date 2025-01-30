
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        # example list of members
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        get_id = self._generateId()
        try:
            member_to_dict = {'id':member['id'],'first_name': member['first_name'], 
                          'last_name': self.last_name,'age':member['age'],
                          'lucky_numbers': member['lucky_numbers']}
            self._members.append(member_to_dict)
            return self._members
        except:
            return None


    def delete_member(self, id):
        member = self.get_member(id)
        if member:
            self._members = list(filter(lambda m: m['id'] != id,self._members))
            return self._members
        else:
            return None
        # fill this method and update the return

    def get_member(self, id):
        get_member = list(filter(lambda m: m['id'] == id,self._members))
        if get_member:
            return get_member[0]
        else:
            return None
        # fill this method and update the return
        
    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
