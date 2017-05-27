import os.path
import sys
import itertools
import random
from tabulate import tabulate
from colorama import init
from termcolor import colored
from .person_class import Person, Fellow, Staff
from .room_class import Room, OfficeSpace, LivingSpace
init()


class Amity(object):
    """
    This class contains all the methods/functions required for the
    entire amity system.
    """

    def __init__(self):
        self.people = []
        self.offices = []
        self.livingspaces = []
        self.office_waitinglist = []
        self.livingspace_waitinglist = []

    def create_room(self, room_type, room_name):
        """
        This method creates rooms based on a user's input.
        Rooms can either be an office or a living space.
        """
        if not isinstance(room_type, str) or not isinstance(room_name, str):
            raise TypeError(
                colored("\n\nUse input of type string only!\n\n", "red"))

        elif room_type.lower() != "office" and room_type.lower() != "livingspace":
            print(colored(
                "\n\nWrong room_type! rooms can only be offices or living spaces\n\n", "red"))
            return("Invalid room type!")

        else:

            if room_type.lower() == "office":
                new_office = OfficeSpace(room_type, room_name)
                if new_office.room_name.lower() in [room.room_name.lower() for room in itertools.chain(self.offices, self.livingspaces)]:
                    print (colored("\n\nThe room name " +
                                   room_name + " already exists!\n\n", "red"))
                else:
                    self.offices.append(new_office)
                    print (colored("\n\nAn office called " + room_name +
                                   " has been successfully created!\n\n", "blue"))
                    return new_office

            elif room_type.lower() == "livingspace":
                new_livingspace = LivingSpace(room_type, room_name)
                if new_livingspace.room_name.lower() in [room.room_name.lower() for room in itertools.chain(self.offices, self.livingspaces)]:
                    print (colored("\n\nThe room name " +
                                   room_name + " already exists!\n\n", "red"))
                else:
                    self.livingspaces.append(new_livingspace)
                    print (colored("\n\nA livingspace called " + room_name +
                                   " has been successfully created\n\n", "blue"))
                    return new_livingspace

    def add_person(self, person_id, name, person_type, wants_accom="N"):
        """
        This method adds a new fellow or staff into the system.
        It also calls the allocate_livingspace and allocate_office method to assign the new staff and fellow rooms.
        """
        if not isinstance(person_id, str) or not isinstance(name, str) or not isinstance(person_type, str):
            raise TypeError("\n\nUse input type of string only\n\n")
            return "Use input type of string only"

        elif person_id.lower() in [person.person_id.lower() for person in self.people]:
            print(colored("\n\nPerson id: " + person_id + " already exists.\n\n", "red"))

        elif person_type.lower() == "fellow":
            new_person = Fellow(person_id, name, person_type, wants_accom)
            self.people.append(new_person)
            print(colored("\n\nFellow " + name + " has been successfully added.\n\n", "blue"))
            self.allocate_office()
            if wants_accom.lower() == "y":
                self.allocate_livingspace()
            return "Added successfully"

        elif person_type.lower() == "staff":
            new_person = Staff(person_id, name, person_type)
            self.people.append(new_person)
            print (colored("\n\nStaff " + name + "  has been successfully added.\n\n", "blue"))
            self.allocate_office()
            return "Added successfully"
        else:
            print (colored("\n\nWrong person_type! A person can only be a staff or fellow\n\n", "red"))
            return "Wrong person_type! A person can only be a staff or fellow"

    def allocate_office(self):
        """
        This method allocates a random office to a new fellow or staff
        """
        person = self.people[-1]
        if len(self.offices) == 0:
            self.office_waitinglist.append(person)
            print (colored("\n\nThere are no offices created yet! Added to waiting list \n\n", "red"))
        elif len(self.offices) > 0:
            available_offices = []
            full_offices = []
            for office in self.offices:
                if len(office.occupants) < office.capacity:
                    available_offices.append(office)
            if available_offices:
                selected_office = random.choice(available_offices)
                selected_office.occupants.append(person)
                print (colored("\n\n" + person.name + " has been allocated the office " +
                               selected_office.room_name + ".\n\n", "blue"))
            else:
                self.office_waitinglist.append(person)
                print (colored("\n\nThere are no available offices! Added to waiting List.\n\n", "red"))

    def allocate_livingspace(self):
        """"
        This method allocates a living space to fellows who want accommodation
        """
        person = self.people[-1]
        if len(self.livingspaces) == 0:
            self.livingspace_waitinglist.append(person)
            print (colored("\n\nThere are no living spaces created yet! Added to waiting list.\n\n", "red"))
        elif len(self.livingspaces) > 0:
            available_livingspaces = []
            full_livingspaces = []
            for livingspace in self.livingspaces:
                if len(livingspace.occupants) < livingspace.capacity:
                    available_livingspaces.append(livingspace)
            if available_livingspaces:
                selected_livingspace = random.choice(available_livingspaces)
                selected_livingspace.occupants.append(person)
                print (colored("\n\n" + person.name + " has been allocated the livingspace " +
                               selected_livingspace.room_name + "\n\n", "blue"))
            else:
                self.livingspace_waitinglist.append(person)
                print (colored("\n\nThere are no available living spaces! Added to waiting List\n\n", "red"))

    def print_room(self, room_name):
        """
        This method prints a list of the specified room's occupants
        """
        if room_name.lower() not in [room.room_name.lower()
                                     for room in itertools.chain(self.offices, self.livingspaces)]:
            print(colored("\nThe room " + room_name + " does not exist!\n", "red"))

        else:
            for room in itertools.chain(self.offices, self.livingspaces):
                while room.room_name.lower() == room_name.lower():
                    if len(room.occupants) <= 0:
                        print(colored("\n\nThe room has no occupants\n\n", "yellow"))
                        return "The room has no occupants"
                    else:
                        names = []
                        for occupant in room.occupants:
                            names.append(occupant.name)
                        table = enumerate(names, start=1)
                        print ("\n\n" + tabulate(table, headers=[room.room_name + " |  \
" + room.room_type], tablefmt="fancy_grid"))
                        print("\n\n")
                    break

    def load_people(self, file_name):
        """
        This method adds people from a txt file.
        """

        if not os.path.isfile(file_name + ".txt"):
            print(colored("\n\nThe file " + file_name + ".txt does not exist!\n\n"))
        elif not os.stat(file_name + ".txt").st_size:
            print(colored("\n\nThe file " + file_name +
                          ".txt is empty!\n", "yellow"))

        else:
            with open(file_name + ".txt") as input_file:
                for line in input_file:
                    read_line = line.split()
                    if len(read_line) > 5 or len(read_line) < 4:
                        print(colored("\n\nInvalid input!\n PLease ensure if follows +\
                            the format: Id FirstName LastName Person_type +\
                            [Wants_Accommodation]\n\n", "yellow"))
                    else:
                        try:
                            person_id = read_line[0]
                            name = read_line[1] + " " + read_line[2]
                            person_type = read_line[3]
                            wants_accom = read_line[4]
                        except IndexError:
                            wants_accom = "N"

                        self.add_person(person_id, name,
                                        person_type, wants_accom=wants_accom)

            print(colored("\n\nData loaded successfully!\n\n", "green"))

    def print_allocations(self, filename=None):
        """
        This method prints a list of allocations onto the screen.
        Specifying the optional -o option ie, the file _name,
        outputs the registered allocations to a txt file.
        """
        output = ""
        if not self.offices and not self.livingspaces:
            print(colored("\n\nThere are no rooms in the Amity!\n\n", "red"))

        for room in itertools.chain(self.offices, self.livingspaces):
            if len(room.occupants) <= 0:
                print(colored("\n\n" + room.room_type + " " +
                              room.room_name + " has no occupants\n\n", "yellow"))
            else:
                if room.occupants:
                    output += ("\n\n" + room.room_name +
                               " - " + room.room_type)
                    output += ("\n" + "-" * 50 + "\n")
                    for occupant in room.occupants:
                        output += (occupant.name+ ", ")

        if filename is None:
            print(colored(output, "blue"))
            print("\n\n")

        else:
            print("\n\nSaving data to file...\n")
            txt_file = open(filename + ".txt", "w+")
            txt_file.write(output)
            txt_file.close()
            print("\n\nData has been successfully \
saved to " + filename + ".txt\n\n")

    def reallocate_person(self, person_id, new_room_name):
        """
        This method allows the facilities manager to reallocate a person \
        to a different room.
        """
        all_rooms = self.livingspaces + self.offices
        try:
            reallocating_person = [person for person in self.people if person.person_id.lower() == person_id.lower()][0]
        except IndexError:
            print(colored("\n\nThe person does not exist.\n\n", "red"))
            return "The person does not exist."

        try:
            new_room = [room for room in all_rooms if room.room_name.lower() == new_room_name.lower()][0]
        except IndexError:
            print(colored("\n\nThe room does not exist.\n\n", "red"))
            return "The room does not exist."

        if reallocating_person in new_room.occupants:
            print(colored("\n\nThe person is in the room! Reallocation can not be to same room.\n\n", "red"))

        elif len(new_room.occupants) == new_room.capacity:
            print(colored("\n\nThe new room is full!\n\n", "yellow"))

        # elif new_room.room_type != current_room.room_type:
        # print("Reallocation can only be office - office or livingspace - livingspace")

        else:
            try:
                current_room = [room for room in all_rooms if reallocating_person in room.occupants and new_room.room_type == room.room_type][0]
                if new_room.room_type == current_room.room_type:
                    new_room.occupants.append(reallocating_person)
                    current_room.occupants.remove(reallocating_person)
                    print(colored("\n\n" + reallocating_person.name + " successfully reallocated to " + new_room.room_type
                        + " " + new_room.room_name + "\n\n", "green"))
                    return"Successfully reallocated!"

                else:
                    print(colored("\n\nReallocation can only be office - office or livingspace - livingspace.\n\n", "red"))
            except IndexError:
                if reallocating_person.person_type.lower() == "staff" and new_room.room_type.lower() == "livingspace":
                    print(colored("\n\nStaff cannot be reallocated to a living space!\n\n", "red"))
                else:
                    print(colored("\n\nThe person does not have any room currently. Please use allocate_unallocted.\n\n", "yellow"))


    def print_unallocated(self, filename=None):
        output = ""

        if not self.office_waitinglist and not self.livingspace_waitinglist:
            print(colored("\n\nThere are no unallocated Fellows or Staff at the moment.\n\n", "yellow"))
            return "There are no unallocated Fellows or Staff at the moment."
        else:
            output = ("\n\n List Of Unallocated Fellows AND Staff\n"\
                + "-" * 40 + "\n")
            for person in self.office_waitinglist:
                output += ( "\n"+ person.person_id + " "
                           + person.name+ " " + person.person_type + " - Office\n\n")

            for person in self.livingspace_waitinglist:
                output += ("\n"+ person.person_id + " "
                           + person.name+ " " + person.person_type + " "
                           + person.wants_accom + " - Livingspace \n\n")

            if filename is None:
                print(colored("\n\n" + output + "\n\n", "blue"))
            else:
                print(colored("Saving unallocations to file...\n", "blue"))
                txt_file = open(filename + ".txt", "w+")
                txt_file.write(output)
                txt_file.close()
                print(colored("\n\nUnallocations successfully saved to " + filename + ".txt\n\n", "green"))
                return "Unallocations successfully saved"

    def allocate_unallocated(self, room_type):
        new_allocations = []

        if room_type.lower() == "office":
            for person in self.office_waitinglist:
                self.allocate_office()
                new_allocations.append(person)
                updated_office_waitinglist = list(set(self.office_waitinglist) - set(new_allocations))
                self.office_waitinglist = updated_office_waitinglist
            if self.office_waitinglist is None:
                print(colored("\n\nThere are no unallocted people.\n\n","yellow"))

        elif room_type.lower() == "livingspace":
            for person in self.livingspace_waitinglist:
                self.allocate_livingspace()
                new_allocations.append(person)
                updated_livingspace_waitinglist = list(set(self.livingspace_waitinglist) - set(new_allocations))
                self.livingspace_waitinglist = updated_livingspace_waitinglist
            if self.livingspace_waitinglist is None:
                print(colored("\n\nThere are no unallocted people.\n\n", "yellow"))

        else: print(colored("\n\nerror occured\n\n", "red"))


    def delete_person(self, person_id):
        pass

    def print_available_rooms(self):
        pass

    def disallocate_person(self, person_id, room):
        pass

    def delete_room(self, room_name):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass
