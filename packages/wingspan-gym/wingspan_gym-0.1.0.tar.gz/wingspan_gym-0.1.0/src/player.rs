use crate::{
    action::Action,
    bird_card::{is_enough_food_to_play_a_card, BirdCard},
    bonus_card::BonusCard,
    error::{WingError, WingResult},
    food::{FoodIndex, Foods},
    habitat::{Habitat, HABITATS},
    player_mat::PlayerMat,
};
use pyo3::prelude::*;

#[derive(Debug, Clone)]
#[pyclass]
pub struct Player {
    #[pyo3(get)]
    foods: Foods,
    #[pyo3(get)]
    bird_cards: Vec<BirdCard>,
    #[pyo3(get)]
    bonus_cards: Vec<BonusCard>,

    #[pyo3(get)]
    pub(crate) turns_left: u8,

    mat: PlayerMat,

    #[pyo3(get)]
    end_of_round_points: u8,

    // Optimization that uses a fact, that before every bird play we check for resources etc.
    _playable_card_hab_combos: Vec<(BirdCard, Habitat, usize)>,
}

impl Default for Player {
    fn default() -> Self {
        Self {
            foods: [1, 1, 1, 1, 1],
            bird_cards: vec![],
            bonus_cards: vec![],
            turns_left: 8,
            mat: Default::default(),
            end_of_round_points: 0,
            _playable_card_hab_combos: vec![],
        }
    }
}

impl Player {
    pub fn new(bird_cards: Vec<BirdCard>, bonus_cards: Vec<BonusCard>) -> Self {
        Self {
            bird_cards,
            bonus_cards,
            ..Default::default()
        }
    }

    pub fn set_turns_left(&mut self, turns_left: u8) {
        self.turns_left = turns_left;
    }

    pub fn discard_bird_card(&mut self, index: usize) -> WingResult<()> {
        if index >= self.bird_cards.len() {
            return Err(WingError::InvalidAction);
        }

        self.bird_cards.remove(index);
        Ok(())
    }

    pub fn discard_bonus_card(&mut self, index: usize) -> WingResult<()> {
        if index >= self.bonus_cards.len() {
            return Err(WingError::InvalidAction);
        }

        self.bonus_cards.remove(index);
        Ok(())
    }

    pub fn discard_food(&mut self, index: FoodIndex, num_food: u8) -> WingResult<()> {
        let index = index as usize;
        if index >= self.get_foods().len() {
            return Err(WingError::InvalidAction);
        }
        if self.foods[index] == 0 {
            return Err(WingError::InvalidAction);
        }

        self.foods[index] -= num_food;
        Ok(())
    }

    pub fn discard_food_or_bird_card(&mut self, index: usize) -> WingResult<()> {
        if index < 5 {
            self.discard_food(index.into(), 1)
        } else {
            self.discard_bird_card(index - 5)
        }
    }

    pub fn can_play_a_bird_card(&mut self, habitats: Vec<Habitat>) -> bool {
        let mut playable_cards = vec![];
        for (idx, card) in self.bird_cards.iter().enumerate() {
            if is_enough_food_to_play_a_card(card, &self.foods) {
                let mut cur_card_habitat_combos: Vec<_> = self
                    .mat
                    .playable_habitats(card)
                    .into_iter()
                    .filter(|habitat| habitats.contains(habitat))
                    .map(|habitat| (*card, habitat, idx))
                    .collect();
                playable_cards.append(&mut cur_card_habitat_combos)
            }
        }
        self._playable_card_hab_combos = playable_cards;

        !self._playable_card_hab_combos.is_empty()
    }

    pub fn play_a_bird_card(
        &mut self,
        bird_card_idx: u8,
    ) -> WingResult<(BirdCard, Habitat, usize, Vec<Action>)> {
        let bird_card_idx = bird_card_idx as usize;
        if bird_card_idx >= self._playable_card_hab_combos.len() {
            return Err(WingError::InvalidAction);
        }

        let (bird_card, hab, orig_card_idx) = self._playable_card_hab_combos[bird_card_idx];

        let mut food_actions = self.pay_bird_cost(&bird_card)?;
        let mut egg_actions = self.mat.put_bird_card(bird_card, &hab)?;
        self.bird_cards.remove(orig_card_idx);

        food_actions.append(&mut egg_actions);
        Ok((
            bird_card,
            hab,
            self.mat.get_row(&hab).get_birds().len() - 1,
            food_actions,
        ))
    }

    fn pay_bird_cost(&mut self, bird_card: &BirdCard) -> WingResult<Vec<Action>> {
        let (costs, total, is_alt) = bird_card.cost();

        if !is_enough_food_to_play_a_card(bird_card, &self.foods) {
            return Err(WingError::InvalidAction);
        }

        let result = match is_alt {
            crate::food::CostAlternative::Yes => {
                // Note: No need to keep track of total cost since it does not appear in "/" (or CostAlternative::Yes) cards

                // First determine what are the discard options
                let mut discard_options = vec![];
                for (food_idx, food_cost) in costs.iter().enumerate() {
                    if let Some(food_cost) = food_cost {
                        if self.foods[food_idx] >= *food_cost {
                            discard_options.push((food_idx.into(), *food_cost));
                        }
                    }
                }

                // If there is only one option, just do it
                if discard_options.len() == 1 {
                    let (food_idx, food_cost) = discard_options.pop().unwrap();

                    self.foods[food_idx as usize] -= food_cost;
                    vec![]
                } else {
                    vec![Action::DiscardFoodChoice(
                        discard_options.into_boxed_slice(),
                    )]
                }
            }
            crate::food::CostAlternative::No => {
                // No Cost Alternative, so no choices needed
                let mut total_defined_cost = 0;
                for (food_idx, food_cost) in costs.iter().enumerate() {
                    if let Some(food_cost) = food_cost {
                        self.foods[food_idx] -= *food_cost;
                        total_defined_cost += *food_cost;
                    }
                }

                // For all of the arbitrary costs, return actions needed
                (0..total - total_defined_cost)
                    .map(|_| Action::DiscardFood)
                    .collect()
            }
        };

        Ok(result)
    }

    pub fn can_discard_food(&self) -> bool {
        self.get_foods().iter().sum::<u8>() > 0
    }

    pub fn can_discard_bird_card(&self) -> bool {
        !self.bird_cards.is_empty()
    }

    pub fn calculate_points(&self) -> u8 {
        // Get points from birds
        let bird_points: u8 = self
            .mat
            .rows()
            .iter()
            .map(|mat_row| mat_row.get_birds().iter().map(|b| b.points()).sum::<u8>())
            .sum();

        // Get points from eggs
        let egg_points = self.mat.egg_count();

        // Points from tucked cards
        let tucked_cards: u8 = self
            .mat
            .rows()
            .iter()
            .map(|mat_row| mat_row.get_tucked_cards().iter().sum::<u8>())
            .sum();

        // Points from cached cards
        let cached_food: u8 = self
            .mat
            .rows()
            .iter()
            .map(|mat_row| mat_row.get_cached_food().iter().flatten().sum::<u8>())
            .sum();

        let bonus_points: u8 = self
            .bonus_cards
            .iter()
            .map(|bc| {
                let count = bc.get_count_of_matching(self) as u8;
                match bc.scoring_rule() {
                    crate::bonus_card::ScoringRule::Each(points_per_each) => {
                        points_per_each * count
                    }
                    crate::bonus_card::ScoringRule::Ladder(steps) => {
                        let mut points = 0;
                        let mut idx = 0;
                        while idx < steps.len() && count >= steps[idx].0 {
                            points = steps[idx].1;
                            idx += 1;
                        }
                        points
                    }
                }
            })
            .sum();

        self.end_of_round_points
            + bird_points
            + bonus_points
            + egg_points
            + tucked_cards
            + cached_food
            + (self.foods.iter().sum::<u8>() / 4)
    }

    pub fn add_bird_card(&mut self, bird_card: BirdCard) {
        self.bird_cards.push(bird_card);
    }

    pub fn append_bird_cards(&mut self, bird_card: &mut Vec<BirdCard>) {
        self.bird_cards.append(bird_card);
    }

    pub fn add_bonus_cards(&mut self, bonus_cards: &mut Vec<BonusCard>) {
        self.bonus_cards.append(bonus_cards);
    }

    pub fn add_food(&mut self, food_idx: FoodIndex, food_count: u8) {
        self.foods[food_idx as usize] += food_count;
    }

    pub fn get_bird_cards(&self) -> &Vec<BirdCard> {
        &self.bird_cards
    }

    pub fn get_birds_on_mat(&self) -> [&Vec<BirdCard>; 3] {
        self.mat.rows().map(|mr| mr.get_birds())
    }

    pub fn get_bonus_cards(&self) -> &Vec<BonusCard> {
        &self.bonus_cards
    }

    pub fn get_foods(&self) -> &Foods {
        &self.foods
    }

    pub fn add_end_of_round_points(&mut self, pts: u8) {
        self.end_of_round_points += pts;
    }

    pub fn get_mat(&self) -> &PlayerMat {
        &self.mat
    }

    pub fn get_mat_mut(&mut self) -> &mut PlayerMat {
        &mut self.mat
    }

    pub fn get_playable_card_hab_combos(&self) -> &Vec<(BirdCard, Habitat, usize)> {
        &self._playable_card_hab_combos
    }
}

#[pymethods]
impl Player {
    pub fn birds_on_mat(&self) -> [Vec<BirdCard>; 3] {
        HABITATS.map(
            |hab| self.mat.get_row(&hab).get_birds().to_vec()
        )
    }
}

#[cfg(test)]
impl Player {
    pub fn new_test(
        foods: Foods,
        bird_cards: Vec<BirdCard>,
        bonus_cards: Vec<BonusCard>,
        turns_left: u8,
        mat: PlayerMat,
        end_of_round_points: u8,
        _playable_card_hab_combos: Vec<(BirdCard, Habitat, usize)>,
    ) -> Self {
        Self {
            foods,
            bird_cards,
            bonus_cards,
            turns_left,
            mat,
            end_of_round_points,
            _playable_card_hab_combos,
        }
    }
}
