from pathlib import Path

import polars as pl

from utils import load_all_cards, FOOD_TYPES, HABITATS, common_name_to_enum_name

bird_impl_file_path = (
    Path(__file__).parent.parent / "src" / "bird_card" / "bird_card_impl.rs"
)

bird_action_impl_file_path = (
    Path(__file__).parent.parent / "src" / "bird_card" / "bird_card_action_impl.rs"
)
bird_action_test_file_path = (
    Path(__file__).parent.parent / "src" / "bird_card" / "test_bird_card_action_impl.rs"
)


def main():
    birds, bonuses, goals = load_all_cards()

    with open(bird_impl_file_path, mode="w") as f:
        # Imports
        f.writelines(
            [
                "// This code is generated automatically via a script in code_gen/ folder\n",
                "use strum_macros::EnumIter;\n\n",
                "use super::BirdCardColor;\n",
                "use crate::{{bonus_card::BonusCard, habitat::Habitat, expansion::Expansion, food::{{BirdCardCost, CostAlternative}}, nest::NestType}};\n",
            ]
        )

        # Start with enum
        f.writelines(
            [
                "\n#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, EnumIter)]",
                "\npub enum BirdCard {\n",
            ]
        )

        for bird in birds.iter_rows(named=True):
            enum_name = bird["enum_name"]
            f.write(f"  {enum_name},\n")
        f.write("}\n")

        # Impl block
        f.writelines(
            [
                "\n",
                "impl BirdCard {\n",
            ]
        )

        # Index function
        f.writelines(
            [
                "  pub fn index(&self) -> u16 {\n",
                "    match self {\n",
            ]
        )
        f.writelines(
            [
                f"      Self::{row['enum_name']} => {row['index']},\n"
                for row in birds.iter_rows(named=True)
            ]
        )
        f.writelines(["    }\n", "  }\n"])

        # Name function
        f.writelines(
            [
                "\n",
                "  pub fn name(&self) -> &'static str {\n",
                "    match self {\n",
            ]
        )
        f.writelines(
            [
                f'      Self::{row["enum_name"]} => "{row["Common name"]}",\n'
                for row in birds.iter_rows(named=True)
            ]
        )
        f.writelines(["    }\n", "  }\n"])

        # Cost function
        f.writelines(
            [
                "\n",
                "  pub fn cost(&self) -> &'static BirdCardCost {\n",
                "    match self {\n",
            ]
        )
        cost_lines = []
        for row in birds.iter_rows(named=True):
            cost_line = f"      Self::{row['enum_name']} => &(["
            for food_type in FOOD_TYPES:
                rust_food_type = (
                    "None" if row[food_type] is None else f"Some({row[food_type]})"
                )
                cost_line += f"{rust_food_type}, "
            cost_line = cost_line[:-2]
            cost_line += f"], {row['Total']}, CostAlternative::"
            cost_line += "Yes" if row["food_cost_alt"] else "No"
            cost_line += "),\n"
            cost_lines.append(cost_line)
        f.writelines(cost_lines)
        f.writelines(["    }\n", "  }\n"])

        # Color function
        f.writelines(
            [
                "\n",
                "  pub fn color(&self) -> &BirdCardColor {\n",
                "    match self {\n",
            ]
        )
        f.writelines(
            [
                f"      Self::{row['enum_name']} => &BirdCardColor::{row['Color'].capitalize()},\n"
                for row in birds.iter_rows(named=True)
            ]
        )
        f.writelines(["    }\n", "  }\n"])

        # Victory points function
        f.writelines(
            [
                "\n",
                "  pub fn points(&self) -> u8 {\n",
                "    match self {\n",
            ]
        )
        f.writelines(
            [
                f"      Self::{row['enum_name']} => {row['Victory points']},\n"
                for row in birds.iter_rows(named=True)
            ]
        )
        f.writelines(["    }\n", "  }\n"])

        # Habitats function
        f.writelines(
            [
                "\n",
                "  pub fn habitats(&self) -> &'static [Habitat] {\n",
                "    match self {\n",
            ]
        )
        habitat_lines = []
        for row in birds.iter_rows(named=True):
            habitat_line = f"      Self::{row['enum_name']} => &["
            for habitat in HABITATS:
                if row[habitat]:
                    habitat_line += f"Habitat::{habitat}, "
            habitat_line = habitat_line[:-2]
            habitat_line += "],\n"
            habitat_lines.append(habitat_line)
        f.writelines(habitat_lines)
        f.writelines(["    }\n", "  }\n"])

        # Wingspan function
        f.writelines(
            [
                "\n",
                "  pub fn wingspan(&self) -> Option<u16> {\n",
                "    match self {\n",
            ]
        )
        wingspan_lines = []
        for row in birds.iter_rows(named=True):
            # NOTE: Flightless birds are "*"
            wingspan_val = (
                "None"
                if row["Wingspan"] is None or row["Wingspan"] == "*"
                else f"Some({row['Wingspan']})"
            )
            wingspan_lines.append(
                f"      Self::{row['enum_name']} => {wingspan_val},\n"
            )
        f.writelines(wingspan_lines)
        f.writelines(["    }\n", "  }\n"])

        # Egg Capacity function
        f.writelines(
            [
                "\n",
                "  pub fn egg_capacity(&self) -> u8 {\n",
                "    match self {\n",
            ]
        )
        wingspan_lines = []
        f.writelines(
            [
                f"      Self::{row['enum_name']} => {row['Egg limit']},\n"
                for row in birds.iter_rows(named=True)
            ]
        )
        f.writelines(["    }\n", "  }\n"])

        # Nest Type function
        f.writelines(
            [
                "\n",
                "  pub fn nest_type(&self) -> &NestType {\n",
                "    match self {\n",
            ]
        )
        f.writelines(
            [
                f"      Self::{row['enum_name']} => &NestType::{row['Nest type'].capitalize()},\n"
                for row in birds.iter_rows(named=True)
            ]
        )
        f.writelines(["    }\n", "  }\n"])

        # is_predator
        f.writelines(
            [
                "\n",
                "  pub fn is_predator(&self) -> bool {\n",
                "    match self {\n",
            ]
        )
        f.writelines(
            [
                f"      Self::{row['enum_name']} => {str(row['is_predator']).lower()},\n"
                for row in birds.iter_rows(named=True)
            ]
        )
        f.writelines(["    }\n", "  }\n"])

        # Expansions
        f.writelines(
            [
                "\n",
                "  pub fn expansion(&self) -> Expansion {\n",
                "    match self {\n",
            ]
        )
        expansion_lines = []
        for row in birds.iter_rows(named=True):
            exp_val = f"Expansion::{row['expansion'].capitalize()}"
            expansion_lines.append(f"      Self::{row['enum_name']} => {exp_val},\n")
        f.writelines([*expansion_lines, "    }\n", "  }\n"])

        # Bonus card membership
        f.writelines(
            [
                "\n",
                "  pub fn bonus_card_membership(&self) -> Vec<BonusCard> {\n",
                "    match self {\n",
            ]
        )
        expansion_lines = []
        column_names = set(birds.columns) & set(bonuses["Bonus card"])
        for row in birds.iter_rows(named=True):
            card_membership = []
            for column in column_names:
                if row[column] == "X":
                    card_membership.append(
                        f"BonusCard::{common_name_to_enum_name(column)}"
                    )

            expansion_lines.append(
                f"      Self::{row['enum_name']} => vec![{', '.join(card_membership)}],\n"
            )
        f.writelines([*expansion_lines, "    }\n", "  }\n"])

        # Close impl block
        f.write("}\n")

    # # Return early to not overwrite actual work

    power_birds = (
        birds.with_columns(pl.col("Power text").str.to_lowercase().alias("power_text"))
        .group_by("power_text")
        .agg(pl.col("enum_name"))
    )

    # Setup of manual impl of bird cards
    if bird_action_impl_file_path.exists():
        with open(bird_action_impl_file_path, mode="w") as f:
            # Impl block
            f.writelines(
                [
                    "use super::BirdCard;\n",
                    "use crate::wingspan_env::WingspanEnv;\n",
                    "\nimpl BirdCard {\n",
                ]
            )

            # Activate function
            f.writelines(
                [
                    "  pub fn activate(&self, env: &mut WingspanEnv) {\n",
                    "    match self {\n",
                ]
            )

            activate_lines = []
            for row in power_birds.iter_rows(named=True):
                birds_line = "\n        | ".join(
                    [f"Self::{em}" for em in row["enum_name"]]
                )

                bird_line = f"      {birds_line} => {{\n"
                bird_line += f"        // {row['power_text']}\n"
                bird_line += "        todo!()\n"
                bird_line += "      },\n"
                activate_lines.append(bird_line)

            f.writelines([*activate_lines, "    }\n", "  }\n"])
            # Close impl block
            f.write("}\n")


#     with open(bird_action_test_file_path, mode="w") as f:
#         f.writelines([
#             "use super::BirdCard;\n",
#             "use crate::wingspan_env::WingspanEnv;\n"
#             "\n",
#         ])

#         f.writelines([
#             "#[cfg(test)]\n",
#             "mod test {\n",
#             "  use crate::{bird_card::BirdCard, habitat::Habitat, wingspan_env::{WingspanEnv, WingspanEnvConfigBuilder}};\n",
#             "\n",
#   """
#   macro_rules! test_bird_card {
#       ($test_name:ident, $bird_name:ident, $habitat:expr) => {
#           #[test]
#           fn $test_name() {
#               let config_builder = WingspanEnvConfigBuilder::default();
#               let mut env = WingspanEnv::try_new(config_builder.build().unwrap());

#               let bird_card = BirdCard::$bird_name;
#               let habitat = $habitat;

#               env.current_player_mut().get_mat_mut().get_row_mut(&habitat).play_a_bird(bird_card);

#               let _ = bird_card.activate(&mut env, &habitat, 0);
#           }
#       };
#   }
#   """,
#             "\n",
#         ])


#         f.writelines(["}\n",])


if __name__ == "__main__":
    main()
