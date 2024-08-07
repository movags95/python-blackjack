# # Project outline
# We have a the computer as the dealer and a human player at the keyboard and a Deck of 52 x Cards
# Human player places a bet from their bankroll

# Game then starts and player draws 2 cards face up and computer draws 2 cards one face up and the other face down.
# Player goes first and can either Hit (recieve another card) or Stay (stop receiving cards)


# # Scenarios
# If player keeps hitting and sum of cards > 21 then they have bust and lost the bet regardless of what the computer does. Dealer collects the money
# if player ends their turn with a sum lower than 21 and the computer acheives a sum lower than or eq 21 then and higher than the player sum then computer has won and takes all the money
# Computer can bust and then human gets double their bet money back into their bank roll

# Special rules
# Face cards all have a value of 10
# Aces can have a value of 1 or 11 depending on whats favorable for player


from random import shuffle

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
rank_values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card():
    
    def __init__(self, rank: str, suit: str):
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()
        self.value = rank_values[self.rank]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
    
class Deck():

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(rank, suit)
                self.deck.append(created_card)

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + str(card)
        return 'The deck contains: ' + deck_comp
        

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        return self.deck.pop()
    
class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card: Card):
        self.cards.append(card)
        self.value += card.value

        # Track any aces
        if card.rank == 'Ace':
            self.aces += 1


    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value += -10
            self.aces += -1

class Chips():

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:

        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except:
            print('Sorry please provide an integer')
        else:
            if chips.bet > chips.total:
                print(f'You do not have enough. You have ${chips.total}.')
            else: 
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Hit (H) or Stand (S)? ")

        if x[0].upper() == 'H':
            hit(deck, hand)
        elif x[0].upper() == 'S':
            print("Player stands! Dealers turn.")
            playing = False
        else:
            print('Sorry, I did not understand that. Please enter H or S.')
            continue

        break

def show_some(player, dealer):
    # Show only one of the dealers card
    print("\n Dealers Hand:")
    print("First card hidden!")
    print(dealer.cards[1])

    # Show all of the players card
    print(f"\n Players Hand (total: {player.value}):", *player.cards, sep='\n')

def show_all(player, dealer):
    # Show all dealers cards
    # Calculate and display total value for dealer
    print(f"\n Dealers Hand (total: {dealer.value}):", *dealer.cards, sep='\n')

    # Show all players cards
    # Calculate and display total card value for the players hand
    print(f"\n Players Hand (total: {player.value}):", *player.cards, sep='\n')

def player_busts(player, dealer, chips):
    print("BUST Player")
    chips.lose_bet()
def player_wins(player, dealer, chips):
    print("WIN Player")
    chips.win_bet()
def dealer_busts(player, dealer, chips):
    print("BUST Dealer. WIN Player")
    chips.win_bet()
def dealer_wins(player, dealer, chips):
    print("WIN Dealer")
    chips.lose_bet()
def push(player, dealer):
    print("PUSH! Dealer and player tie.")



if __name__ == '__main__':
    playing = True

    while True:
        print("Welcome to Blackjack!")

        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Set up the player chips
        player_chips = Chips()

        # Prompt the player for their bet
        take_bet(player_chips)

        # Show cards but keep dealers 1 hidden
        show_some(player_hand, dealer_hand)

        while playing:
            # Prompt user for hit or stand
            hit_or_stand(deck, player_hand)

            # Then show cards while keeping dealers hidden
            show_some(player_hand, dealer_hand)

            # If player hand exceeds 21 run bust and break out of loop
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                break

        # if the player hasnt busted, we are going to play the dealers hand until the dealer reaches 17
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            # Show all cards
            show_all(player_hand, dealer_hand)

            # Run the different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)

        # Display players total chips
        print (f"\nPlayer total chips: ${player_chips.total}")

        new_game = input("Would you like to play again? (y/n) ")

        if new_game[0].upper() == 'Y':
            playing = True
            continue
        else:
            print("Thank you for playing!")
            break
