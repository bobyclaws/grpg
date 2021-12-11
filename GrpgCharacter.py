import logging

from .clock import clock

from .reactions import Reactor

from .compute import E
from .formulae import FormulaeStore

from .weapon import Weapon
from .stats import StatsManager
from .event import Event

from .GrpgCharacterBase import GrpgCharacterBase
from .talent_impl import auto, charge, skill, burst, plunge


class GrpgCharacter(GrpgCharacterBase):

    def __init__(self, inherent):
        super().__init__()
        
        # character's state in the game.
        self.weapon: Weapon = None
        self.domain = None
        self.player_name = None
        self.current_hp = None
        self.current_stamina = 225
        self.alive = True
        self.name = self.name or "??"

        self.sm = StatsManager(self, inherent)
        self.fs = FormulaeStore(self)
        self.reactor = Reactor(self)

        
        # player talents' action data.
        self.talent_data = {
            'auto': {},
            'charge': {},
            'skill': {},
            'burst': {},
            'plunge': {}
        } 


    def set_player(self, party_name: str):
        """set which party the character belongs to"""
        self.player_name = party_name

    def set_domain(self, domain):
        """set the domain the character is in."""
        self.domain = domain

    def set_weapon(self, weapon: dict):
        """Set's the character's weapon"""
        self.weapon = weapon

    def __str__(self):
        """provides a meaningful name for logging."""
        return f'({self.party_pos}{self.player_name} {self.name})' 



    def prepare(self):
        """prepare before entering the domain"""
        logging.info(f"{self}: preparing")
        self.sm.prepare()
        self.reset_hp()

        # inject all tickers.
        self.tick.inject(self)
        



   

    def reset_hp(self):
        """restore character's full hp"""
        logging.info(f"{self}: resetting hp to {self.sm.stats['Max HP']}")
        self.current_hp = self.sm.stats['Max HP'].val


 


    
     

    @property
    def party_pos(self):
        """gives the character's position in party. (int)"""
        for pos, chara in enumerate(self.domain.players[self.player_name]['party']):
            if chara is self:
                return pos
        return '?'

    def take_field(self):
        "do stuff where chara takes the field here"
        logging.info(f'{self}: taking field')



    def leave_field(self):
        "do stuff when chara leaves field here"
        logging.info(f'{self}: leaving field')
        pass


    def get_hp(self):
        """
        get's the current hp
        NOTE: why's this even a function
        """
        return self.current_hp




    def take_hit(self, bonk):
        """get hit by a bonk """



        elem = bonk['element']
        em = bonk['em']
        dmg_in = bonk['dmg']

        
        # update incoming dmg
        self.fs.dmg_in.set(dmg_in)

        # update attacker level ( helps calculating defense)
        self.fs.attacker_level.set(90)

        # update final res
        self.fs.effective_res.equals(self.sm.get_effective_res(elem))

        #TODO: do elemental reaction stuff
        self.reactor.react(elem, em)


        # damage taken is above hp, so character dies. also emit event.
        if self.fs.final_dmg.val >= self.current_hp:
            self.alive = False
            self.domain.game.events.append(Event(Event.CHARA_FALL, self.party_pos))
            self.current_hp = 0

            # see if all party members died and emit game over event
            game_over = True
            for chara in self.domain.players[self.player_name]['party']:
                if chara.alive:
                    game_over = False
                    break
            if game_over:
                self.domain.game.events.append(Event(Event.GAME_OVER, self.player_name))
        
        else:
            # reduce hp with final dmg
            self.current_hp = self.current_hp -  self.fs.final_dmg.val
            logging.info(f"dmg taken: {self.fs.final_dmg.val}, hp: {self.current_hp}/{self.sm.stats['Max HP']} eq: {self.fs.final_dmg.eq()}")



    def equip_weapon(self, name, level):
        """equips a weapon of given name and level"""
        self.weapon = Weapon(name, level)

        # inherit its buffs
        self.sm.apply_pbuffs(self.weapon.pbuffs)


    def is_onfield(self):
        """checks whether player is on field"""
        player = self.domain.players[self.player_name]
        if self.party_pos == player['on_chara']:
            return True
        return False

    @clock.ticker(interval=2, times=5)
    def tick(self):
        """update character state every turn here"""
        logging.info(f"{self}: ticking")
        self.current_stamina += 10


    def get_stats(self):
        """returns all the necessary character's state for debugging"""
        return f"""{self}>> hp: {self.get_hp()}/{self.sm.stats['Max HP']}, stamina: {self.current_stamina}/ {self.sm.stats['Max Stamina']} """
        


    def get_talent(self, talent_name: str):
        
        if talent_name not in ['auto', 'charge', 'skill', 'burst']:
            raise Exception('Invalid talent_name')

        level = self.sm.inherent['Talents'][talent_name]['Level']
        talent = self.sm.inherent['Talents'][talent_name]

        data = dict()
        for k, v in talent.items():
            if isinstance(v, dict):
                data[k] = v[level]
            elif isinstance(v, (int, float, str)):
                data[k] = v

        return data
        
    
    #SECTION: ABILITIES

    @auto
    def invoke_auto(self):
        pass
        
    @charge
    def invoke_charge(self):
      pass

    @skill
    def invoke_skill(self):
        pass

    @burst
    def invoke_burst(self):
        pass
    
    @plunge
    def invoke_plunge(self):
        pass
  
