class Actor:

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name= None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__actor_colleague = list()

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        if self.__actor_full_name < other.__actor_full_name:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__actor_full_name)
        
    def add_actor_colleague(self, colleague):
       self.__actor_colleague.append(colleague)
       
    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.__actor_colleague:
            return True
        else:
            return False
