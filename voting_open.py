import pickle
import datetime

x = datetime.datetime.now()

class VotingOpen:
    def __init__(self, theme):
        self.theme = theme
        self.contenders = {}
        self.voters = {}
        self.fase_2 = False

        themes_file = open ("data/themes/themes", "a")
        themes_file.write(" # %s, %s/%s/%s; "%(theme, x.strftime("%d"), x.strftime("%m"), x.strftime("%Y")))
        themes_file.close()


    def update_data(self): 
            contenders_file = open("data/contenders/%s"%(self.theme), "wb")
            pickle.dump(self.contenders,contenders_file)
            contenders_file.close()

            voters_file = open("data/voters/%s"%(self.theme), "wb")
            pickle.dump(self.voters,voters_file)
            voters_file.close()

            print(self.contenders, self.voters)

            print("data updated \n")

            # contenders_test = open("data/contenders/%s"%(self.theme), "rb")
            # data = pickle.load(contenders_test)
            # print(data)
            # contenders_test.close()

            # voters_file = open("data/voters/%s"%(self.theme), "rb")
            # data = pickle.load(voters_file)
            # print(data)
            # voters_file.close()


    def check_contender(self, contendr):
        for key in self.contenders.keys():
            if contendr.lower() == self.contenders[key][0].lower():
                return True
    

    def get_contender_id(self, contendr):
        for key in self.contenders.keys():
            if contendr.lower() == self.contenders[key][0].lower():
                return key

    
    def check_contender_id(self, id):
        if id in self.contenders:
            return True

    
    def check_voter(self, id):
        if id in self.voters:
            return True


#actual commands --------------------------------------------------------------------------------------
    
    def add_contender(self, contendr, name, id):
        if self.fase_2 == False:
            if self.check_contender(contendr) == True:
                msg = "ERROR: <@%s> There is already a contender with the same name."%(id)
                print(msg)
                return msg

            else:
                print("Adding %s"%(contendr))
                self.contenders.update({id : [str(contendr), str(name), 0, str(id)]})
                self.update_data()
                msg = "<@%s> Added: %s."%(name, contendr)
                return msg
        else:
            msg = "ERROR: <@%s> We aren't in the adding phase anymore. You can't add contenders anymore."%(id)
            print(msg)
            return msg
            
    
    def vote_contender(self, contendr, voter_name, voter_id):
        if self.fase_2 == True:
            if self.check_contender(contendr) != True:
                msg = "ERROR: There is no contender by the name of: %s."%(contendr)
                print(msg)
                return msg
            
            elif self.check_voter(voter_id) == True:
                msg = "ERROR: <@%s> you have already Voted."%(voter_id)
                print(msg)
                return msg

            elif self.get_contender_id(contendr) == voter_id:
                msg = "ERROR: <@%s> you cannot vote for yourself."%(id)
                print(msg)
                return msg

            else:
                contendr_key = self.get_contender_id(contendr)

                print("%s voting for %s"%(voter_name, self.contenders[contendr_key][0]))

                self.contenders[contendr_key][2] += 1

                self.voters.update({voter_id : [str(contendr), str(voter_name), str(voter_id), str(contendr_key)]})

                msg = "%s voted for: %s"%(voter_name, contendr)

                self.update_data()
                
                print(msg)
                return msg
        
        else:
            msg = "We are still adding contenders."
            print(msg)
            return msg

    
    def vote_id(self, contender_id, voter_name, voter_id):
        if self.fase_2 == True:
            if self.check_contender_id(contender_id) != True:
                msg = "ERROR: <@%s> this person didnt add a contender."%(voter_id)
                print(msg)
                return msg
            
            elif self.check_voter(voter_id) == True:
                msg = "ERROR: <@%s> you have already Voted."%(voter_id)
                print(msg)
                return msg

            elif contender_id == voter_id:
                msg = "ERROR: <@%s> you cannot vote for yourself."%(voter_id)
                print(msg)
                return msg

            else:
                print("%s voting for %s"%(voter_name, self.contenders[contender_id][0]))

                self.contenders[contender_id][2] += 1

                self.voters.update({voter_id : [str(self.contenders[contender_id][0]), str(voter_name), str(voter_id), str(contender_id)]})

                msg = "%s voted for: %s"%(voter_name, self.contenders[contender_id][0])

                self.update_data()
                
                print(msg)
                return msg
        else:
            msg = "We are still adding contenders."
            print(msg)
            return msg

        
    def del_contender(self, contender_id):
        if self.check_contender_id(contender_id) != True:
            msg = "ERROR: <@%s> didnt add a contender."%(contender_id)
            print(msg)
            return msg

        else:
            print("deleting %s"%(self.contenders[contender_id][0]))

            msg_name = self.contenders[contender_id][0]

            keys_to_remove = []
            
            for key in self.voters.keys():
                if str(self.voters[key][3]) == str(contender_id):
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.voters[key]

            del self.contenders[contender_id]

            self.update_data()

            return "%s has been removed."%(msg_name)


    def del_voter(self, voter_id):
        if voter_id not in self.voters:
            msg = "ERROR: <@%s> hasn't voted yet"%(voter_id)
            print(msg)
            return msg

        else:
            print("deleting voter %s"%(self.voters[voter_id][1]))

            msg = "%s Your vote has been removed."%(self.voters[voter_id][1])

            self.contenders[int(self.voters[voter_id][3])][2] -= 1

            del self.voters[voter_id]

            self.update_data()

            return msg


    def join_contenders(self, id_1, id_2):
        if id_1 not in self.contenders or id_2 not in self.contenders:
            if id_1 not in self.contenders and id_2 in self.contenders:
                msg = "ERROR: <@%s> didn't add a contender."%(id_1)
                print(msg)
                return msg
            
            elif id_2 not in self.contenders and id_1 in self.contenders:
                msg = "ERROR: <@%s> didn't add a contender."%(id_2)
                print(msg)
                return msg

            else:
                msg = "ERROR: <@%s> and <@%s> didn't add a contender."%(id_1, id_2)
                print(msg)
                return msg
        
        else:
            print("joining %s with %s"%(self.contenders[id_1][0], self.contenders[id_2][0]))

            keys_to_change = []
            for key in self.voters.keys():
                if str(id_2) == str(self.voters[key][3]):
                    keys_to_change.append(int(key))
            print(keys_to_change)
            
            print("rearranging voters")
            for keys in keys_to_change:
                key_int = int(keys)
                if key_int == id_1:
                    self.del_voter(key_int)

                else:
                    self.voters.update({key_int : [self.contenders[id_1][0], self.voters[key_int][1], self.voters[key_int][2], self.contenders[id_1][3]]})
                    self.contenders[id_1][2] += 1

            msg = "%s joined with %s."%(self.contenders[id_1][0], self.contenders[id_2][0])

            del self.contenders[id_2]
            self.update_data()
            print(msg)
            return msg
            

    def decide_winner(self):
        if len(self.contenders) < 3:
            msg = "Not enough contenders, there must be at least 3."
            print(msg)
            return msg
        else:
            print("deciding winners")
            contenders_sorted = sorted(self.contenders.items(), key=lambda x: x[1][2], reverse=True)

            msg = [
                ("#1 %s by:"%(contenders_sorted[0][1][0]), "<@%s> with %s votes."%(contenders_sorted[0][0], contenders_sorted[0][1][2]), True),
                ("#2 %s by:"%(contenders_sorted[1][1][0]), "<@%s> with %s votes."%(contenders_sorted[1][0], contenders_sorted[1][1][2]), True),
                ("#3 %s by:"%(contenders_sorted[2][1][0]), "<@%s> with %s votes."%(contenders_sorted[2][0], contenders_sorted[2][1][2]), True),
            ]
            print(msg)
            return msg


    def recover_themes(self):
        contenders_pickled = open("data/contenders/%s"%(self.theme), "rb")
        self.contenders = pickle.load(contenders_pickled)
        contenders_pickled.close()

        voters_pickled = open("data/voters/%s"%(self.theme), "rb")
        self.voters = pickle.load(voters_pickled)
        voters_pickled.close()

        msg = "Recovered the theme: %s"%(self.theme)
        print(msg)
        return msg


    def change_fase(self):
        if self.fase_2 == True:
            msg = "The phase has already been changed."
            print(msg)
            return msg
        else:
            msg = "Changing to the voting phase."
            print(msg)
            
            self.fase_2 = True
            return msg


def print_themes():
    themes_file = open("data/themes/themes", "rt")
    themes_file_splitted = themes_file.read().split(";")
    themes_file.close()
    print(themes_file_splitted)
    return themes_file_splitted


#creates the class
test = VotingOpen("test")

#tests add_contender
print("\n -----add_contender")
test_1 = test.add_contender("GOH", "Yuri", 123)#should normally
print(test_1)
# test.add_contender("GOH", "Yuri", 123)#should normally
test.add_contender("hxh", "Vlad", 321)#should normally
test.add_contender("DBZ", "Wolf", 432)#should normally
print("---errors")
test.add_contender("hxh", "Vlad", 321)#should return error: same as other contender
test.add_contender("hvh", "Vlad", 321)#should return error: you already added

#test change_fase
print("\n ------change_fase")

test.vote_id(123, "Vlad", 321)#should return error
test.change_fase()
test.change_fase()
test.add_contender("hvh", "Vlad", 321)#should return error

#tests vote_contender
print("\n ------vote_contender")

test.vote_contender("hvh", "Yuri", 123)#should return error: no contender
test.vote_contender("GOH", "Yuri", 123)#should return error: vote yourself
test.vote_contender("HXH", "Yuri", 123)#should normally
test.vote_contender("hxh", "Yuri", 123)#should return error: vote again

#tests vote_id
print("\n ------vote_id")

test.vote_id(333, "Vlad", 321)#should return error: no id
test.vote_id(321, "Vlad", 321)#should return error: vote yourself
test.vote_id(123, "Vlad", 321)#should normally
test.vote_id(123, "Vlad", 321)#should return error: vote again
test.vote_id(123, "Wolf", 432)#should normally
test.vote_id(123, "Dimi", 234)#should normally
test.vote_id(123, "Frie", 543)#should normally

#test del_contender
print("\n -------del_contender")

test.del_contender(321)#should normally
test.del_contender(321)#should return error: no contender

#tests del_voter
print("\n ------del_voter")

# test.del_voter(321)#should normally
# test.del_voter(321)#should return error: no vote

#tests join_contenders
print("\n ------join_contenders")

# test.join_contenders(333, 111)#should return error: both bad
# test.join_contenders(333, 123)#should return error: only one bad
# test.join_contenders(321, 111)#should return error: only one bad
# test.join_contenders(321, 123)#should normally

#tests decide_winner
print("\n ------decide_winner")

test.decide_winner()#should error IF: 2 or less contenders

#tests recover_themes
print("\n ------print_themes")

# recover_themes()
# test.recover_themes()
# print(test.contenders)
# print(test.voters)
# test.decide_winner()