"""
This program replicates the game of Blackjack.
"""


from tkinter import Tk, Label, Button, Entry, Frame, PhotoImage
from card import card # to import the card function from the card file
import random


class BlackJack:
    def __init__(self, master):
        # setting the measurements and background of the game window
        self.master = master
        master.title("BlackJack")
        master.geometry("850x550")
        self.bg = PhotoImage(file = "cards//BlackJack.png")
        self.photo_label = Label(master, image = self.bg)
        self.photo_label.place(x=0,y=0, relwidth = 1 , relheight =1)

        # the player and dealer both start off with no points and no cards(will be added later)
        self.player_points = []
        self.dealer_points = []
        self.playerhand = []
        self.dealerhand = []
        self.deck = [] # deck will be created 
        self.total_sum = 100 # inital amount is $100
        
        # this creates the deck by adding all the pictures to deck
        for letter in ["C","D","S","H"]:  
          for number in range(1,14): # 1 is ace 11 is jack 12 is Q 13 is K
            filename = "cards//%s%s.png" % (number,letter)
            value = number
            self.deck.append(card(filename,value))

        random.shuffle(self.deck)


        # Where the cards will appear
        self.cards_frame = Frame(master, bg = "white")
        self.cards_frame.grid(row=0, column=0,columnspan=2)
        # Where the player's cards will appear
        self.cards_frame_player = Frame(self.cards_frame, bg = "white")
        self.cards_frame_player.grid(row=0, column=1) 
        self.sum_label_player = Label(self.cards_frame_player,text="")
        self.sum_label_player.grid(row=1, column= 0) 
        # Where the dealer's cards will appear
        self.cards_frame_dealer = Frame(self.cards_frame, bg = "white")
        self.cards_frame_dealer.grid(row=2, column=1)
        self.sum_label_dealer = Label(self.cards_frame_dealer,text="")
        self.sum_label_dealer.grid(row=3, column= 0) 
        # to display the result of the round
        self.label_win = Label(master, text='',font = ("Times",9,"bold italic"),fg='white', bg = "#01321f") 
        self.label_win.place(x=382,y=275)
        # the buttons are the commands of the game
        self.deal_button = Button(master, text="Deal", command=self.deal,bg = "white",state='disabled')
        self.deal_button.place(x=40,y=235)
      
        self.hit_button = Button(master, text="Hit",bg = "white",command=self.hit,state='disabled')
        self.hit_button.place(x=100,y=235)
 
        self.stand_button = Button(master, text="Stand",bg = "white", command=self.stand,state='disabled')
        self.stand_button.place(x=150,y=235)

        # this displays the total amount at the time of playing
        self.current_total_label = Label(master, text = f"Current Total is ${self.total_sum}",font = ("Times",10,"bold"),fg='white', bg = '#963836')
        self.current_total_label.place(x=45,y=275)
        # this is to acccept the bet amount input by the user
        self.bet_amt_label = Label(text = "Enter Bet Amount",font = ("Times",11,"bold italic"),fg='white', bg = "#963836")
        self.bet_amt_label.place(x=47,y=105)
        self.bet_amt_entry = Entry()
        self.bet_amt_entry.place(x=42,y=135)
        self.bet_amt_button = Button(master, text = "Enter",bg = "white", command=self.bet,state='normal')
        self.bet_amt_button.place(x=90,y=165)
      
 
    def bet(self): # the betting function to manage the money being bet
      try: #initially converts input to an integer if possible
        self.bet_amt = int(self.bet_amt_entry.get())
        if self.bet_amt < 0:  # no negative amounts
          self.msg = "Enter A Valid Amount!"
        elif self.bet_amt > self.total_sum: # amount greater than what the player has is not possible
          self.msg = "Enter A Payable Amount!" 
        else:
          self.msg = "Press Deal To Start" # message upon appropriate entry
          self.deal_button.config(state='normal')
      except: # if input is not an integer then this message is dispalyed
        self.msg = "Enter A Valid Number!"
      self.bet_amt_label.config(text = self.msg) # this displays the appropriate message 

  
    def deal(self):
      self.new_bg = PhotoImage(file = "cards//green_bg.png") # playing background(blackjack table)
      self.photo_label.config(image=self.new_bg)
      self.deal_button.config(state='disabled')
      self.hit_button.config(state='normal')
      self.stand_button.config(state='normal')


      self.sum_label_player.config(bg = 'white')
      self.sum_label_dealer.config(bg = 'white')
      
      self.current_total_label.config(font = ("Times", 9,"bold"), bg = "#01321f")
      
      self.bet_amt_label.config(text = f"Current Bet Amount is ${self.bet_amt}",font = ("Times", 9,"bold"), bg = "#01321f") # displays the amount being bet this round
      self.bet_amt_label.place(x=25,y=305)
      # these are not required anymore so they are destroyed
      self.bet_amt_entry.destroy() 
      self.bet_amt_button.destroy()
      
      self.deal_button.place(x=340,y=305)
      self.hit_button.place(x=400,y=305)
      self.stand_button.place(x=450,y=305)
      # Button to restart the entire game
      self.restart_button = Button(self.master, text = "Start New Game", bg = 'white', command = self.restart)
      self.restart_button.place(x=360,y=340)
      
      # 2 cards are dealt to the player
      self.new_card_player()
      self.new_card_player()
      # 2 cards are dealt to the dealer but one is face down
      self.new_card_dealer()
      self.hidden_card()

      if sum(self.player_points) > 21: # if sum exceeds 21, player loses
        self.hit_button.config(state='disabled') 
        self.stand_button.config(state='disabled')
        self.label_win.config (text = "YOU LOSE!")
        self.dealer_win()
        root.after(2000, self.reset)
        
      elif sum(self.player_points) == 21: # if sum = 21, player gets Blackjack
        self.hit_button.config(state='disabled') 
        self.stand_button.config(state='disabled')
        self.label_win.config (text = "YOU WIN - BLACKJACK!")
        self.player_blackjack()
        root.after(2000, self.reset)

        
    def new_card_player(self): # function to deal a new card to the player and display the total
      new = self.deck[0]
      self.player_points.append(new.value)
      self.playerhand.append(new)
      self.deck.pop(0)   
        
      photo = PhotoImage(file=new.filename)
      new.label = Label(self.cards_frame_player, image=photo)
      new.label.photo = photo
      new.label.grid(row=0,column=self.playerhand.index(new))
      self.sum_label_player.config(text="Player's Total: %d" % sum(self.player_points))

    def new_card_dealer(self): # function to deal a face-up card to the dealer and display the total
      new_2 = self.deck[0]
      self.dealer_points.append(new_2.value)
      self.dealerhand.append(new_2)
      self.deck.pop(0)   
        
      photo = PhotoImage(file=new_2.filename)
      new_2.label = Label(self.cards_frame_dealer, image=photo)        
      new_2.label.photo = photo 
      new_2.label.grid(row=2,column=self.dealerhand.index(new_2))
      self.sum_label_dealer.config(text="Dealer's Total: %d" % sum(self.dealer_points))
      
    def hidden_card(self): # function to deal a hidden (face-down) card and add points to dealer's total
      new_2b = self.deck[0]
      self.dealerhand.append(new_2b)
      self.dealer_points.append(new_2b.value)
      self.deck.pop(0)   
     
      photo = PhotoImage(file="cards//back.png")
      new_2b.label = Label(self.cards_frame_dealer, image=photo)        
      new_2b.label.photo = photo
      new_2b.label.grid(row=2,column=self.dealerhand.index(new_2b))

    def reveal_card(self): # function that reveals the face-down cards of the dealer
      for x in range(1,len(self.dealerhand)):    
        new_3 = self.dealerhand[x]

        photo = PhotoImage(file= new_3.filename)
        new_3.label = Label(self.cards_frame_dealer, image=photo)        
        new_3.label.photo = photo
        new_3.label.grid(row=2,column=self.dealerhand.index(new_3))

  
    def hit(self): # to deal a new card to the player 
      self.new_card_player()
      
      if sum(self.player_points) == 21: # player blackjack
        self.label_win.config (text = "Player Wins - BLACKJACK!")
        self.player_blackjack()
        root.after(2500, self.reset) 
      elif sum(self.player_points) > 21: # player excess points
        self.hit_button.config(state='disabled') 
        self.stand_button.config(state='disabled')
        self.label_win.config (text = "YOU LOSE!")
        self.dealer_win()
        root.after(2000, self.reset)
      if sum(self.dealer_points) < 17: # a new card is dealt to the dealer only if current sum is less than 17 (rules of how the dealer plays)
        self.hidden_card()

    def dealer_win(self): # player loses bet
      self.total_sum -= self.bet_amt
      return str(self.total_sum) # player wins bet
    def player_win(self): # player loses bet
      self.total_sum += self.bet_amt
      return str(self.total_sum)
    def player_blackjack(self): # player wins bet with blackjack. wins 1.5x the betting amt
      self.total_sum += (1.5 * self.bet_amt)
    def dealer_blackjack(self): # player loses bet to dealer blackjack. owes 1.5x the betting amt
      self.total_sum -= (1.5 * self.bet_amt)
      
    
    def dealer_hit(self): # the rules of blackjack to determine the winner 
      if sum(self.dealer_points) == 21: 
         self.label_win.config (text = "Dealer Wins - BLACKJACK!")
         self.dealer_blackjack()
         root.after(2500, self.reset)     
      elif sum(self.dealer_points) > sum(self.player_points) and sum(self.dealer_points) < 21:
         self.label_win.config (text = "Dealer Wins!")
         self.dealer_win()
         root.after(2500, self.reset)
      elif sum(self.dealer_points) > 21 :
         self.label_win.config(text = "Player Wins!")
         self.player_win()
         root.after(2500, self.reset)
      elif sum(self.player_points) == sum(self.dealer_points):
         self.label_win.config (text = "Tie!")
         root.after(2500, self.reset)
      elif sum(self.dealer_points) < sum(self.player_points) and sum(self.dealer_points) > 17:
         self.label_win.config (text = "Player Wins!")
         self.player_win()
         root.after(2500, self.reset)    
      elif sum(self.dealer_points) < sum(self.player_points) and sum(self.dealer_points) < 17 and len(self.dealer_points)<len(self.player_points):
         self.new_card_dealer()
         root.after(2000, self.dealer_hit)
      else:
        self.label_win.config (text = "Player Wins!")
        self.player_win()
        root.after(2500, self.reset)

  
    def stand(self): # dealer's cards and total is revealed and outcome is assessed by calling self.dealer_hit()
      self.deal_button.config(state='disabled')
      self.hit_button.config(state='disabled')
      self.stand_button.config(state='disabled')
      self.reveal_card()
      self.sum_label_dealer.config(text="Dealer's Total: %d" % sum(self.dealer_points))
      self.dealer_hit()

    def new_game(self): # game resets to intial values and layout after round is over
     
      self.hit_button.config(state='disabled')
      self.stand_button.config(state='disabled')
      self.deal_button.config(state='disabled')
      
      self.player_points = []
      self.dealer_points = []
      self.playerhand = []
      self.dealerhand = []
      self.deck = []
 
      self.cards_frame_player.destroy()
      self.cards_frame_player = Frame(self.cards_frame, bg= 'white')
      self.cards_frame_player.grid(row=0, column=1)
      self.sum_label_player = Label(self.cards_frame_player,text="", bg='white')
      self.sum_label_player.grid(row=1, column= 0) 
      
      self.cards_frame_dealer.destroy()
      self.cards_frame_dealer = Frame(self.cards_frame, bg = "white")
      self.cards_frame_dealer.grid(row=2, column=1)
      self.sum_label_dealer = Label(self.cards_frame_dealer,text="", bg = 'white')
      self.sum_label_dealer.grid(row=3, column= 0)

      self.restart_button.destroy()

      for letter in ["C","D","S","H"]:
          for number in range(1,14): # 1 is ace 11 is jack 12 is Q 13 is K
            filename = "cards//%s%s.png" % (number,letter)
            value = number
            self.deck.append(card(filename,value))
      random.shuffle(self.deck)

      self.photo_label.config(image=self.bg)
      self.label_win.config(text="") 
      self.deal_button.place(x=40,y=235)
      self.hit_button.place(x=100,y=235)
      self.stand_button.place(x=150,y=235)

      self.label_win.place(x=382,y=275)

      self.current_total_label.config(text = f"Current Total is ${self.total_sum}", font = ("Times",10,"bold"),fg='white', bg = '#963836')
      self.bet_amt_label.config(text = "Enter bet amount", font = ("Times",11,"bold italic"),fg='white', bg = "#963836")
      self.bet_amt_label.place(x=47,y=105)
      self.bet_amt_entry = Entry()
      self.bet_amt_entry.place(x=42,y=135)
      self.bet_amt_button = Button(self.master, text = "Enter",bg = "white", command=self.bet)
      self.bet_amt_button.place(x=90,y=165)
     

    def restart(self): # new game with inital amount
       self.total_sum = 100
       self.new_game()
  
    def reset(self): 
     if self.total_sum > 0: # this is for a new round of the same game
       self.new_game()
     else: # if current amount <= 0 then the player must start a new game
       self.label_win.config (text = "No More Money To Bet!")
       self.label_win.place(x=342,y=275)

  
root = Tk()
my_gui = BlackJack(root) #creates the BabyBlackJack instance
root.mainloop()
